from collections import defaultdict
from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir
from gt4py.next.iterator.ir_utils import ir_makers as im


class CollapseIfs(PreserveLocationVisitor, NodeTranslator):
    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)
        if not self._is_plus(node) or not any(self._contains_if(a) for a in node.args):
            return node
        # try to collapse `if_` branches sharing the same condition
        node = self._collapse_same_conditions(node)

        # `node` might no longer be a `plus` expression after collapsing. In that case we are
        # done, but we still need to make sure that any *new* sub-expressions created by the
        # collapsing step are visited as well (so that nested plus-chains are processed).

        if not self._is_plus(node):
            # Just traverse its children once more to allow deeper collapsing.
            return self.generic_visit(node)

        # Flatten nested `plus` nodes that may have been introduced by the collapsing step.
        args: list[ir.Expr] = []
        # Child expressions have already been processed by the initial
        # `self.generic_visit(node)` at the top of this function, so we do **not**
        # need to visit them again here. We can safely flatten nested `plus`
        # nodes without an extra recursive traversal, which avoids building up
        # deep call stacks on very long chains.

        for a in node.args:
            if self._is_plus(a):
                # `a` is already fully processed, so we simply splice its
                # arguments into the current list.
                args.extend(a.args)
            else:
                args.append(a)

        new_node = args[0] if len(args) == 1 else self._make_plus_chain(args)

        # We return the rebuilt node directly. The surrounding pass-manager
        # infrastructure will re-run the transform on the whole IR until it
        # reaches a fixed point, so an additional traversal *inside* this call
        # is unnecessary and can lead to extremely deep recursion.
        return new_node

    def _make_plus_chain(self, items):
        items = [i for i in items if i is not None]
        res = items[0]
        for itm in items[1:]:
            res = im.plus(res, itm)
        return res

    def _collapse_same_conditions(self, node):
        groups, others = defaultdict(list), []
        for a in node.args:
            c = self._extract_condition(a)
            if c is None:
                others.append(a)
            else:
                groups[self._condition_key(c)].append((c, a))
        new_terms = others
        for g in groups.values():
            if len(g) <= 1:
                new_terms.append(g[0][1])
                continue
            then_terms, else_terms = [], []
            for _, t in g:
                tp, ep = self._split_if_statement(t)
                then_terms.append(tp)
                else_terms.append(ep)

            # Heuristic safety check: avoid collapsing if a branch mixes plain symbols (likely
            # iterator parameters) with expressions. Such mixing can later confuse type
            # inference (e.g., iterator + field value). If we detect heterogeneity, keep the
            # original terms untouched.

            def _branch_mixes_syms(branch_terms):
                has_sym = any(isinstance(bt, ir.SymRef) for bt in branch_terms)
                has_other = any(not isinstance(bt, ir.SymRef) for bt in branch_terms)
                return has_sym and has_other

            if _branch_mixes_syms(then_terms) or _branch_mixes_syms(else_terms):
                new_terms.extend(t for _, t in g)
                continue
            t_comb = self._make_plus_chain(then_terms) if len(then_terms) > 1 else then_terms[0]
            e_comb = self._make_plus_chain(else_terms) if len(else_terms) > 1 else else_terms[0]
            new_terms.append(im.if_(g[0][0], t_comb, e_comb))
        return new_terms[0] if len(new_terms) == 1 else self._make_plus_chain(new_terms)

    def _contains_if(self, n):
        return isinstance(n, ir.FunCall) and (
            (isinstance(n.fun, ir.SymRef) and n.fun.id == "if_") or any(self._contains_if(a) for a in n.args)
        )

    def _extract_condition(self, n):
        if isinstance(n, ir.FunCall):
            if isinstance(n.fun, ir.SymRef) and n.fun.id == "if_":
                return n.args[0]
            if len(n.args) == 1:
                return self._extract_condition(n.args[0])
        return None

    def _split_if_statement(self, n):
        # If this is a direct `if_` call we simply return its `then` and `else` branches.
        if isinstance(n, ir.FunCall) and isinstance(n.fun, ir.SymRef) and n.fun.id == "if_":
            # Structure: if_(cond, then_branch, else_branch)
            # We assume the IR always provides exactly three arguments here.
            return n.args[1], n.args[2]

        # Handle common unary wrappers (e.g. `deref(x)` or single-argument `shift(x)`).
        # We only treat wrappers with a *single* argument here to avoid accidentally
        # mis-handling multi-argument calls. For more complex wrappers, collapsing is
        # skipped and the original expression is preserved (returning the same node for
        # both branches).
        if isinstance(n, ir.FunCall) and len(n.args) == 1:
            inner_then, inner_else = self._split_if_statement(n.args[0])
            # If no `if_` was found inside, keep the original node untouched.
            if inner_then is n.args[0] and inner_else is n.args[0]:
                return n, n

            def _rebuild(arg):
                new_call = ir.FunCall(fun=n.fun, args=[arg])
                # Preserve source location metadata if available to aid in
                # debugging and subsequent passes.
                if getattr(n, "location", None) is not None:
                    new_call.location = n.location  # type: ignore[attr-defined]
                return new_call

            return _rebuild(inner_then), _rebuild(inner_else)

        # Fallback: not an `if_` and not a recognised wrapper.
        return n, n

    def _condition_key(self, c):
        if isinstance(c, ir.SymRef):
            return ("SymRef", c.id)
        if isinstance(c, ir.Literal):
            return ("Literal", type(c.value).__name__, c.value)
        if isinstance(c, ir.FunCall) and isinstance(c.fun, ir.SymRef):
            return ("FunCall", c.fun.id, tuple(self._condition_key(a) for a in c.args))
        return str(c)

    def _is_plus(self, n):
        return isinstance(n, ir.FunCall) and isinstance(n.fun, ir.SymRef) and n.fun.id == "plus"