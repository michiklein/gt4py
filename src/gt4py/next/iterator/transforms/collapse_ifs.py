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

    # Wrapper calls that merely forward their first argument (no side-effects)
    # and therefore can be skipped when looking for nested ``if_`` nodes.
    _SAFE_WRAPPERS: set[str] = {"cast_", "deref"}

    def _unwrap(self, n: ir.Expr) -> ir.Expr:
        """Peel off benign wrapper calls so that helper routines can
        recognise an underlying ``if_``.

        A wrapper is considered *benign* when it:
        1. Is a plain ``ir.FunCall`` whose ``fun`` is an ``ir.SymRef``;
        2. Its ``id`` is listed in ``_SAFE_WRAPPERS``;
        3. The value being wrapped is the **first** positional argument.
        The loop stops on the first non-wrapper expression and returns it.
        """
        while (
            isinstance(n, ir.FunCall)
            and isinstance(n.fun, ir.SymRef)
            and n.fun.id in self._SAFE_WRAPPERS
            and n.args
        ):
            n = n.args[0]
        return n

    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)
        
        # First, handle degenerate if statements (same then/else branches)
        if self._is_if(node):
            simplified = self._simplify_degenerate_if(node)
            if simplified is not None:
                return simplified
        
        # Handle collapsing if statements with same conditions for commutative operations
        if self._should_collapse(node) and any(self._contains_if(a) for a in node.args):
            node = self._collapse_same_conditions(node)

        # If this is a plus operation, also flatten nested plus operations
        if self._is_plus(node):
            args: list[ir.Expr] = []
            for a in node.args:
                if self._is_plus(a):
                    args.extend(a.args)
                else:
                    args.append(a)

            new_node = args[0] if len(args) == 1 else self._make_plus_chain(args)
            return new_node

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

            def _branch_mixes_syms(branch_terms):
                has_sym = any(isinstance(bt, ir.SymRef) for bt in branch_terms)
                has_other = any(not isinstance(bt, ir.SymRef) for bt in branch_terms)
                return has_sym and has_other

            if _branch_mixes_syms(then_terms) or _branch_mixes_syms(else_terms):
                new_terms.extend(t for _, t in g)
                continue
            
            op_id = node.fun.id if isinstance(node.fun, ir.SymRef) else None
            builder = self._COMMUTATIVE_OPS_MAPPING.get(op_id)
            if builder is not None:
                t_comb = self._make_operation_chain(then_terms, builder) if len(then_terms) > 1 else then_terms[0]
                e_comb = self._make_operation_chain(else_terms, builder) if len(else_terms) > 1 else else_terms[0]
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
        n_un = self._unwrap(n)
        if isinstance(n_un, ir.FunCall):
            if isinstance(n_un.fun, ir.SymRef) and n_un.fun.id == "if_":
                return n_un.args[0]
            if len(n_un.args) == 1:
                return self._extract_condition(n_un.args[0])
        return None

    def _split_if_statement(self, n):
        """Return the *then* and *else* parts of an ``if_`` expression wrapped in
        arbitrary safe wrappers.  If *n* is not (or does not contain) an
        ``if_`` the pair *(n, n)* is returned so that callers can detect the
        fallback easily.
        """
        n_un = self._unwrap(n)

        # Base case – actual if_ node
        if (
            isinstance(n_un, ir.FunCall)
            and isinstance(n_un.fun, ir.SymRef)
            and n_un.fun.id == "if_"
        ):
            return n_un.args[1], n_un.args[2]

        # If still a FunCall, try recurring through its first argument when it
        # looks like a unary decorator (not in _SAFE_WRAPPERS)
        if isinstance(n_un, ir.FunCall) and len(n_un.args) == 1:
            inner_then, inner_else = self._split_if_statement(n_un.args[0])
            if inner_then is n_un.args[0] and inner_else is n_un.args[0]:
                return n_un, n_un

            def _rebuild(arg):
                new_call = ir.FunCall(fun=n_un.fun, args=[arg] + n_un.args[1:])
                if getattr(n_un, "location", None) is not None:
                    new_call.location = n_un.location  # type: ignore[attr-defined]
                return new_call

            return _rebuild(inner_then), _rebuild(inner_else)

        # Anything else – give up
        return n_un, n_un

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