# GT4Py - GridTools Framework
#
# Copyright (c) 2014-2024, ETH Zurich
# All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause


from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir

class CollapseTables(PreserveLocationVisitor, NodeTranslator):
    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)
        if ( isinstance(node.fun, ir.FunCall)
            and node.args.value[0] == "C2E"
            and node.args.value[1] == "E2V"
               
        ):
            return ir.FunCall(
                fun=ir.SymRef(value="C2E2V"),
            )