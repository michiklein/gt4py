from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir as itir

class StripDegenerateIfs(PreserveLocationVisitor, NodeTranslator):
    """Remove `if_(cond, X, X)` expressions where both branches are identical.

    We consider a guard degenerate only when the two branches are
    syntactically equal *and* do not themselves contain an `if_`.
    This ensures we do not accidentally rewrite complex conditional
    structures.
    """

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    def _contains_if(self, n: itir.Expr):
        return (
            isinstance(n, itir.FunCall)
            and (
                (isinstance(n.fun, itir.SymRef) and n.fun.id == "if_")
                or any(self._contains_if(a) for a in n.args)
            )
        )

    # ------------------------------------------------------------------
    # Visitor
    # ------------------------------------------------------------------
    def visit_FunCall(self, node: itir.FunCall):  # type: ignore[override]
        node = self.generic_visit(node)

        if (
            isinstance(node.fun, itir.SymRef)
            and node.fun.id == "if_"
            and node.args[1] == node.args[2]
            and not self._contains_if(node.args[1])
        ):
            return node.args[1]
        return node
