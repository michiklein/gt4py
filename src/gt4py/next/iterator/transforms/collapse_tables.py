# GT4Py - GridTools Framework
#
# Copyright (c) 2014-2024, ETH Zurich
# All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause


from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir

lookup_e_se = {
    # E2C2E
    "E2C[0]C2E[0]": "E2C2E[0]",
    "E2C[0]C2E[1]": "E2C2E[1]",
    "E2C[0]C2E[2]": "self",
    "E2C[1]C2E[0]": "self",
    "E2C[1]C2E[1]": "E2C2E[2]",
    "E2C[1]C2E[2]": "E2C2E[3]",
    # E2C2V
    "E2C[0]C2V[0]": "E2C2V[0]",
    "E2C[0]C2V[1]": "E2C2V[2]",
    "E2C[0]C2V[2]": "E2C2V[1]",
    "E2C[1]C2V[0]": "E2C2V[0]",
    "E2C[1]C2V[1]": "E2C2V[1]",
    "E2C[1]C2V[2]": "E2C2V[3]",
    # E2V2C
    "E2V[0]V2C[0]": "E2V2C[0]",
    "E2V[0]V2C[1]": "E2V2C[2]",
    "E2V[0]V2C[2]": "E2V2C[3]",
    "E2V[0]V2C[3]": "E2V2C[4]",
    "E2V[0]V2C[4]": "E2V2C[1]",
    "E2V[0]V2C[5]": "E2V2C[5]",
    "E2V[1]V2C[0]": "E2V2C[0]",
    "E2V[1]V2C[1]": "E2V2C[6]",
    "E2V[1]V2C[2]": "E2V2C[7]",
    "E2V[1]V2C[3]": "E2V2C[8]",
    "E2V[1]V2C[4]": "E2V2C[1]",
    "E2V[1]V2C[5]": "E2V2C[9]",
    # E2V2E
    "E2V[0]V2E[0]": "E2V2E[0]",
    "E2V[0]V2E[1]": "E2V2E[1]",
    "E2V[0]V2E[2]": "self",
    "E2V[0]V2E[3]": "E2V2E[2]",
    "E2V[0]V2E[4]": "E2V2E[3]",
    "E2V[0]V2E[5]": "E2V2E[4]",
    "E2V[1]V2E[0]": "E2V2E[5]",
    "E2V[1]V2E[1]": "E2V2E[6]",
    "E2V[1]V2E[2]": "self",
    "E2V[1]V2E[3]": "E2V2E[7]",
    "E2V[1]V2E[4]": "E2V2E[8]",
    "E2V[1]V2E[5]": "E2V2E[9]",
}

lookup_e_e = {
    # E2C2E
    "E2C[0]C2E[0]": "E2C2E[0]",
    "E2C[0]C2E[1]": "E2C2E[1]",
    "E2C[0]C2E[2]": "self",
    "E2C[1]C2E[0]": "E2C2E[2]",
    "E2C[1]C2E[1]": "self",
    "E2C[1]C2E[2]": "E2C2E[3]",
    # E2C2V
    "E2C[0]C2V[0]": "E2C2V[0]",
    "E2C[0]C2V[1]": "E2C2V[2]",
    "E2C[0]C2V[2]": "E2C2V[1]",
    "E2C[1]C2V[0]": "E2C2V[3]",
    "E2C[1]C2V[1]": "E2C2V[0]",
    "E2C[1]C2V[2]": "E2C2V[1]",
    # E2V2C
    "E2V[0]V2C[0]": "E2V2C[0]",
    "E2V[0]V2C[1]": "E2V2C[2]",
    "E2V[0]V2C[2]": "E2V2C[3]",
    "E2V[0]V2C[3]": "E2V2C[4]",
    "E2V[0]V2C[4]": "E2V2C[5]",
    "E2V[0]V2C[5]": "E2V2C[1]",
    "E2V[1]V2C[0]": "E2V2C[0]",
    "E2V[1]V2C[1]": "E2V2C[6]",
    "E2V[1]V2C[2]": "E2V2C[7]",
    "E2V[1]V2C[3]": "E2V2C[8]",
    "E2V[1]V2C[4]": "E2V2C[1]",
    "E2V[1]V2C[5]": "E2V2C[9]",
    # E2V2E
    "E2V[0]V2E[0]": "self",
    "E2V[0]V2E[1]": "E2V2E[0]",
    "E2V[0]V2E[2]": "E2V2E[1]",
    "E2V[0]V2E[3]": "E2V2E[2]",
    "E2V[0]V2E[4]": "E2V2E[3]",
    "E2V[0]V2E[5]": "E2V2E[4]",
    "E2V[1]V2E[0]": "self",
    "E2V[1]V2E[1]": "E2V2E[5]",
    "E2V[1]V2E[2]": "E2V2E[6]",
    "E2V[1]V2E[3]": "E2V2E[7]",
    "E2V[1]V2E[4]": "E2V2E[8]",
    "E2V[1]V2E[5]": "E2V2E[9]",
}

lookup_e_n = {
    # E2C2E
    "E2C[0]C2E[0]": "self",
    "E2C[0]C2E[1]": "E2C2E[0]",
    "E2C[0]C2E[2]": "E2C2E[1]",
    "E2C[1]C2E[0]": "E2C2E[2]",
    "E2C[1]C2E[1]": "self",
    "E2C[1]C2E[2]": "E2C2E[3]",
    # E2C2V
    "E2C[0]C2V[0]": "E2C2V[0]",
    "E2C[0]C2V[1]": "E2C2V[1]",
    "E2C[0]C2V[2]": "E2C2V[2]",
    "E2C[1]C2V[0]": "E2C2V[3]",
    "E2C[1]C2V[1]": "E2C2V[1]",
    "E2C[1]C2V[2]": "E2C2V[0]",
    # E2V2C
    "E2V[0]V2C[0]": "E2V2C[0]",
    "E2V[0]V2C[1]": "E2V2C[2]",
    "E2V[0]V2C[2]": "E2V2C[3]",
    "E2V[0]V2C[3]": "E2V2C[1]",
    "E2V[0]V2C[4]": "E2V2C[4]",
    "E2V[0]V2C[5]": "E2V2C[5]",
    "E2V[1]V2C[0]": "E2V2C[0]",
    "E2V[1]V2C[1]": "E2V2C[6]",
    "E2V[1]V2C[2]": "E2V2C[7]",
    "E2V[1]V2C[3]": "E2V2C[1]",
    "E2V[1]V2C[4]": "E2V2C[8]",
    "E2V[1]V2C[5]": "E2V2C[9]",
    # E2V2E
    "E2V[0]V2E[0]": "E2V2E[0]",
    "E2V[0]V2E[1]": "E2V2E[1]",
    "E2V[0]V2E[2]": "E2V2E[2]",
    "E2V[0]V2E[3]": "E2V2E[3]",
    "E2V[0]V2E[4]": "self",
    "E2V[0]V2E[5]": "E2V2E[4]",
    "E2V[1]V2E[0]": "E2V2E[5]",
    "E2V[1]V2E[1]": "E2V2E[6]",
    "E2V[1]V2E[2]": "E2V2E[7]",
    "E2V[1]V2E[3]": "E2V2E[8]",
    "E2V[1]V2E[4]": "self",
    "E2V[1]V2E[5]": "E2V2E[9]",
}

lookup_c_u = {
    # C2E2C
    "C2E[0]E2C[0]": "self",
    "C2E[0]E2C[1]": "C2E2C[0]",
    "C2E[1]E2C[0]": "C2E2C[1]",
    "C2E[1]E2C[1]": "self",
    "C2E[2]E2C[0]": "self",
    "C2E[2]E2C[1]": "C2E2C[2]",
    # C2E2V
    "C2E[0]E2V[0]": "C2V[0]",
    "C2E[0]E2V[1]": "C2V[1]",
    "C2E[1]E2V[0]": "C2V[1]",
    "C2E[1]E2V[1]": "C2V[2]",
    "C2E[2]E2V[0]": "C2V[0]",
    "C2E[2]E2V[1]": "C2V[2]",
    # C2V2C
    "C2V[0]V2C[0]": "C2V2C[0]",
    "C2V[0]V2C[1]": "C2V2C[1]",
    "C2V[0]V2C[2]": "C2V2C[3]",
    "C2V[0]V2C[3]": "self",
    "C2V[0]V2C[4]": "C2V2C[4]",
    "C2V[0]V2C[5]": "C2V2C[5]",
    "C2V[1]V2C[0]": "C2V2C[0]",
    "C2V[1]V2C[1]": "C2V2C[2]",
    "C2V[1]V2C[2]": "C2V2C[6]",
    "C2V[1]V2C[3]": "self",
    "C2V[1]V2C[4]": "C2V2C[7]",
    "C2V[1]V2C[5]": "C2V2C[8]",
    "C2V[2]V2C[0]": "C2V2C[1]",
    "C2V[2]V2C[1]": "C2V2C[2]",
    "C2V[2]V2C[2]": "C2V2C[9]",
    "C2V[2]V2C[3]": "self",
    "C2V[2]V2C[4]": "C2V2C[10]",
    "C2V[2]V2C[5]": "C2V2C[11]",
    # C2V2E
    "C2V[0]V2E[0]": "C2V2E[3]",
    "C2V[0]V2E[1]": "C2V2E[4]",
    "C2V[0]V2E[2]": "C2V2E[0]",
    "C2V[0]V2E[3]": "C2V2E[5]",
    "C2V[0]V2E[4]": "C2V2E[1]",
    "C2V[0]V2E[5]": "C2V2E[6]",
    "C2V[1]V2E[0]": "C2V2E[2]",
    "C2V[1]V2E[1]": "C2V2E[7]",
    "C2V[1]V2E[2]": "C2V2E[8]",
    "C2V[1]V2E[3]": "C2V2E[9]",
    "C2V[1]V2E[4]": "C2V2E[1]",
    "C2V[1]V2E[5]": "C2V2E[10]",
    "C2V[2]V2E[0]": "C2V2E[2]",
    "C2V[2]V2E[1]": "C2V2E[11]",
    "C2V[2]V2E[2]": "C2V2E[0]",
    "C2V[2]V2E[3]": "C2V2E[12]",
    "C2V[2]V2E[4]": "C2V2E[13]",
    "C2V[2]V2E[5]": "C2V2E[14]",
}

lookup_c_d = {
    # C2E2C
    "C2E[0]E2C[0]": "C2E2C[0]",
    "C2E[0]E2C[1]": "self",
    "C2E[1]E2C[0]": "C2E2C[1]",
    "C2E[1]E2C[1]": "self",
    "C2E[2]E2C[0]": "self",
    "C2E[2]E2C[1]": "C2E2C[2]",
    # C2E2V
    "C2E[0]E2V[0]": "C2V[0]",
    "C2E[0]E2V[1]": "C2V[1]",
    "C2E[1]E2V[0]": "C2V[1]",
    "C2E[1]E2V[1]": "C2V[2]",
    "C2E[2]E2V[0]": "C2V[0]",
    "C2E[2]E2V[1]": "C2V[2]",
    # C2V2C
    "C2V[0]V2C[0]": "self",
    "C2V[0]V2C[1]": "C2V2C[3]",
    "C2V[0]V2C[2]": "C2V2C[4]",
    "C2V[0]V2C[3]": "C2V2C[5]",
    "C2V[0]V2C[4]": "C2V2C[0]",
    "C2V[0]V2C[5]": "C2V2C[1]",
    "C2V[1]V2C[0]": "self",
    "C2V[1]V2C[1]": "C2V2C[6]",
    "C2V[1]V2C[2]": "C2V2C[7]",
    "C2V[1]V2C[3]": "C2V2C[2]",
    "C2V[1]V2C[4]": "C2V2C[0]",
    "C2V[1]V2C[5]": "C2V2C[8]",
    "C2V[2]V2C[0]": "self",
    "C2V[2]V2C[1]": "C2V2C[9]",
    "C2V[2]V2C[2]": "C2V2C[10]",
    "C2V[2]V2C[3]": "C2V2C[2]",
    "C2V[2]V2C[4]": "C2V2C[1]",
    "C2V[2]V2C[5]": "C2V2C[11]",
    # C2V2E
    "C2V[0]V2E[0]": "C2V2E[0]",
    "C2V[0]V2E[1]": "C2V2E[3]",
    "C2V[0]V2E[2]": "C2V2E[1]",
    "C2V[0]V2E[3]": "C2V2E[4]",
    "C2V[0]V2E[4]": "C2V2E[5]",
    "C2V[0]V2E[5]": "C2V2E[6]",
    "C2V[1]V2E[0]": "C2V2E[7]",
    "C2V[1]V2E[1]": "C2V2E[8]",
    "C2V[1]V2E[2]": "C2V2E[1]",
    "C2V[1]V2E[3]": "C2V2E[9]",
    "C2V[1]V2E[4]": "C2V2E[2]",
    "C2V[1]V2E[5]": "C2V2E[10]",
    "C2V[2]V2E[0]": "C2V2E[0]",
    "C2V[2]V2E[1]": "C2V2E[11]",
    "C2V[2]V2E[2]": "C2V2E[12]",
    "C2V[2]V2E[3]": "C2V2E[13]",
    "C2V[2]V2E[4]": "C2V2E[2]",
    "C2V[2]V2E[5]": "C2V2E[14]",
}

lookup_v = {
    # V2E2C
    "V2E[0]E2C[0]": "V2C[1]",
    "V2E[0]E2C[1]": "V2C[0]",
    "V2E[1]E2C[0]": "V2C[2]",
    "V2E[1]E2C[1]": "V2C[1]",
    "V2E[2]E2C[0]": "V2C[3]",
    "V2E[2]E2C[1]": "V2C[2]",
    "V2E[3]E2C[0]": "V2C[3]",
    "V2E[3]E2C[1]": "V2C[4]",
    "V2E[4]E2C[0]": "V2C[4]",
    "V2E[4]E2C[1]": "V2C[5]",
    "V2E[5]E2C[0]": "V2C[5]",
    "V2E[5]E2C[1]": "V2C[0]",
    # V2E2V
    "V2E[0]E2V[0]": "V2E2V[0]",
    "V2E[0]E2V[1]": "self",
    "V2E[1]E2V[0]": "V2E2V[1]",
    "V2E[1]E2V[1]": "self",
    "V2E[2]E2V[0]": "V2E2V[2]",
    "V2E[2]E2V[1]": "self",
    "V2E[3]E2V[0]": "self",
    "V2E[3]E2V[1]": "V2E2V[3]",
    "V2E[4]E2V[0]": "self",
    "V2E[4]E2V[1]": "V2E2V[4]",
    "V2E[5]E2V[0]": "self",
    "V2E[5]E2V[1]": "V2E2V[5]",
    # V2C2V
    "V2C[0]C2V[0]": "V2E2V[0]",
    "V2C[0]C2V[1]": "self",
    "V2C[0]C2V[2]": "V2E2V[5]",
    "V2C[1]C2V[0]": "V2E2V[0]",
    "V2C[1]C2V[1]": "V2E2V[1]",
    "V2C[1]C2V[2]": "self",
    "V2C[2]C2V[0]": "V2E2V[1]",
    "V2C[2]C2V[1]": "V2E2V[2]",
    "V2C[2]C2V[2]": "self",
    "V2C[3]C2V[0]": "self",
    "V2C[3]C2V[1]": "V2E2V[2]",
    "V2C[3]C2V[2]": "V2E2V[3]",
    "V2C[4]C2V[0]": "self",
    "V2C[4]C2V[1]": "V2E2V[3]",
    "V2C[4]C2V[2]": "V2E2V[4]",
    "V2C[5]C2V[0]": "V2E2V[5]",
    "V2C[5]C2V[1]": "self",
    "V2C[5]C2V[2]": "V2E2V[4]",
    # V2C2E
    "V2C[0]C2E[0]": "V2C2E[6]",
    "V2C[0]C2E[1]": "V2C2E[0]",
    "V2C[0]C2E[2]": "V2C2E[1]",
    "V2C[1]C2E[0]": "V2C2E[7]",
    "V2C[1]C2E[1]": "V2C2E[0]",
    "V2C[1]C2E[2]": "V2C2E[2]",
    "V2C[2]C2E[0]": "V2C2E[2]",
    "V2C[2]C2E[1]": "V2C2E[8]",
    "V2C[2]C2E[2]": "V2C2E[3]",
    "V2C[3]C2E[0]": "V2C2E[3]",
    "V2C[3]C2E[1]": "V2C2E[4]",
    "V2C[3]C2E[2]": "V2C2E[9]",
    "V2C[4]C2E[0]": "V2C2E[5]",
    "V2C[4]C2E[1]": "V2C2E[4]",
    "V2C[4]C2E[2]": "V2C2E[10]",
    "V2C[5]C2E[0]": "V2C2E[1]",
    "V2C[5]C2E[1]": "V2C2E[11]",
    "V2C[5]C2E[2]": "V2C2E[5]",
}


class CollapseTables(PreserveLocationVisitor, NodeTranslator):
    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)

        if ( #check if we have a shift
            isinstance(node.fun, ir.FunCall)
            and isinstance(node.fun.fun, ir.SymRef)
            and node.fun.fun.id == "shift"
            and node.fun.args
            and node.args
        ):
            flat_args = node.fun.args

            if len(flat_args) % 2 != 0:
                return node

            key_parts = []
            for i in range(0, len(flat_args), 2):
                symbol_arg = flat_args[i]
                offset_arg = flat_args[i + 1]

                if (
                    isinstance(symbol_arg, ir.OffsetLiteral)
                    and isinstance(symbol_arg.value, ir.SymbolRef)
                    and isinstance(offset_arg, ir.OffsetLiteral)
                    and isinstance(offset_arg.value, int)
                ):
                    part = f"{symbol_arg.value}[{offset_arg.value}]" #translate into form that we have in the lookup tables
                    key_parts.append(part)
                else:
                    return node #not the type of shift we are looking for

            key = "".join(key_parts)

            if True: #TODO
                lookup_e = lookup_e_se
            elif False:
                lookup_e = lookup_e_e
            else:
                lookup_e = lookup_e_n

            if True: #TODO
                lookup_c = lookup_c_u
            else:
                lookup_c = lookup_c_d

            for table in [lookup_v, lookup_c, lookup_e]: #find our replacement
                if key in table:
                    replacement = table[key]
                    if replacement == "self":
                        return node.args[0]
                    else:
                        sym_name, index_str = replacement.split("[") #fix my stupid format
                        index = int(index_str.rstrip("]"))
                        return ir.FunCall(
                            fun=ir.FunCall(
                                fun=ir.SymRef(id="shift"),
                                args=[
                                    ir.OffsetLiteral(value=ir.SymbolRef(sym_name)),
                                    ir.OffsetLiteral(value=index),
                                ],
                            ),
                            args=node.args,
                        )

        return node


