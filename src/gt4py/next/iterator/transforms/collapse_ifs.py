from collections import defaultdict
from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir
from gt4py.next.iterator.ir_utils import ir_makers as im


class CollapseIfs(PreserveLocationVisitor, NodeTranslator):
    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)
        if not self._is_plus(node) or not any(self._contains_if(a) for a in node.args):
            return node
        node = self._collapse_same_conditions(node)

        if not self._is_plus(node):
            return self.generic_visit(node)

        args: list[ir.Expr] = []
        for a in node.args:
            if self._is_plus(a):
                args.extend(a.args)
            else:
                args.append(a)

        new_node = args[0] if len(args) == 1 else self._make_plus_chain(args)
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