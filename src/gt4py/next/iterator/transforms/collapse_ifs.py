from collections import defaultdict
from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir
from gt4py.next.iterator.ir_utils import ir_makers as im
from typing import Optional


class CollapseIfs(PreserveLocationVisitor, NodeTranslator):
    # Commutative & associative ops that we can safely collapse across
    _COMMUTATIVE_OPS_MAPPING: dict[str, callable] = {
        "plus": im.plus,
        "multiplies": im.multiplies_,
        "maximum": im.maximum,
        "minimum": im.minimum,
    }

    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)
        
        # Handle collapsing if statements with same conditions for commutative operations
        if self._should_collapse(node) and any(self._contains_if(a) for a in node.args):
            node = self._collapse_same_conditions(node)

        # If this is a plus operation, also flatten nested plus operations
        if self._is_plus(node):
            args: list[ir.Expr] = []
            for a in node.args:
                # Only flatten a nested plus if doing so does *not* cross a guard.
                if self._is_plus(a) and not self._contains_if(a):
                    args.extend(a.args)
                else:
                    args.append(a)

            new_node = args[0] if len(args) == 1 else self._make_plus_chain(args)
            node = self.generic_visit(new_node)

        # Do not remove degenerate guards here; a dedicated post-pass handles that.

        # Return the processed node as-is (no additional traversal)
        return node

    def _simplify_degenerate_if(self, node: ir.FunCall) -> Optional[ir.Expr]:
        """Simplify if statements where then and else branches are identical."""
        if self._is_if(node) and node.args[1] == node.args[2]:
            return node.args[1]
        return None

    def _make_plus_chain(self, items):
        items = [i for i in items if i is not None]
        res = items[0]
        for itm in items[1:]:
            res = im.plus(res, itm)
        return res

    def _make_operation_chain(self, items, operation):
        """Make a chain of operations with the given operation function."""
        items = [i for i in items if i is not None]
        res = items[0]
        for itm in items[1:]:
            res = operation(res, itm)
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

            op_id = node.fun.id if isinstance(node.fun, ir.SymRef) else None
            builder = self._COMMUTATIVE_OPS_MAPPING.get(op_id)
            if builder is not None:
                t_comb_raw = self._make_operation_chain(then_terms, builder) if len(then_terms) > 1 else then_terms[0]
                e_comb_raw = self._make_operation_chain(else_terms, builder) if len(else_terms) > 1 else else_terms[0]

                # Recursively process the combined branches so further collapses inside them happen
                t_comb = self.visit(t_comb_raw)
                e_comb = self.visit(e_comb_raw)
            else:
                # Fallback: cannot collapse
                new_terms.extend(t for _, t in g)
                continue
            
            new_terms.append(im.if_(g[0][0], t_comb, e_comb))
        
        if len(new_terms) == 1:
            return new_terms[0]
        op_id = node.fun.id if isinstance(node.fun, ir.SymRef) else None
        builder = self._COMMUTATIVE_OPS_MAPPING.get(op_id)
        if builder is not None:
            return self._make_operation_chain(new_terms, builder)
        else:
            # Cannot safely combine – return original node with possibly simplified sub-terms
            return node

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
        if isinstance(n, ir.FunCall) and isinstance(n.fun, ir.SymRef) and n.fun.id == "if_":
            return n.args[1], n.args[2]

        if isinstance(n, ir.FunCall) and len(n.args) == 1:
            inner_then, inner_else = self._split_if_statement(n.args[0])
            if inner_then is n.args[0] and inner_else is n.args[0]:
                return n, n

            def _rebuild(arg):
                new_call = ir.FunCall(fun=n.fun, args=[arg])
                if getattr(n, "location", None) is not None:
                    new_call.location = n.location  # type: ignore[attr-defined]
                return new_call

            return _rebuild(inner_then), _rebuild(inner_else)

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

    def _is_if(self, n):
        return isinstance(n, ir.FunCall) and isinstance(n.fun, ir.SymRef) and n.fun.id == "if_"

    def _should_collapse(self, n):
        return isinstance(n, ir.FunCall) and isinstance(n.fun, ir.SymRef) and n.fun.id in self._COMMUTATIVE_OPS_MAPPING

    def _is_multiplies(self, n):
        return isinstance(n, ir.FunCall) and isinstance(n.fun, ir.SymRef) and n.fun.id == "multiplies"