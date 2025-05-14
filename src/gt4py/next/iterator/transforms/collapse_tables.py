# #MKLEIN MASTERS THESIS
# from gt4py.eve import NodeTranslator, PreserveLocationVisitor
# from gt4py.next.iterator import ir
# from gt4py.next.ffront.experimental import concat_where
# from gt4py.next import Dimension
# from gt4py.next.iterator.ir_utils import ir_makers as im
# from gt4py.next.iterator import ir as itir
# from gt4py.next import common

# # # Define the conditionals for use in tables
# # edge_cond1 = im.less(Dimension("Edge"), im.divides_(im.ref("num_edges"), 3))
# # edge_cond2 = im.less(Dimension("Edge"), im.multiplies_(2, im.divides_(im.ref("num_edges"), 3)))
# # cell_cond = im.less(Dimension("Cell"), im.divides_(im.ref("num_cells"), 2))
# # lookup_e = {
# #     # E2C2E
# #     "E2C[0]C2E[0]": im.if_(edge_cond1, "E2C2E[0]", im.if_(edge_cond2, "self", "E2C2E[0]")),
# #     "E2C[0]C2E[1]": im.if_(edge_cond1, "E2C2E[1]", im.if_(edge_cond2, "E2C2E[0]", "E2C2E[1]")),
# #     "E2C[0]C2E[2]": im.if_(edge_cond1, "self", im.if_(edge_cond2, "E2C2E[1]", "self")),
# #     "E2C[1]C2E[0]": im.if_(edge_cond1, "self", im.if_(edge_cond2, "E2C2E[2]", "E2C2E[2]")),
# #     "E2C[1]C2E[1]": im.if_(edge_cond1, "E2C2E[2]", im.if_(edge_cond2, "self", "self")),
# #     "E2C[1]C2E[2]": im.if_(edge_cond1, "E2C2E[3]", im.if_(edge_cond2, "E2C2E[3]", "E2C2E[3]")),
# #     # E2C2V
# #     "E2C[0]C2V[0]": im.if_(edge_cond1, "E2C2V[0]", im.if_(edge_cond2, "E2C2V[0]", "E2C2V[0]")),
# #     "E2C[0]C2V[1]": im.if_(edge_cond1, "E2C2V[2]", im.if_(edge_cond2, "E2C2V[1]", "E2C2V[2]")),
# #     "E2C[0]C2V[2]": im.if_(edge_cond1, "E2C2V[1]", im.if_(edge_cond2, "E2C2V[2]", "E2C2V[1]")),
# #     "E2C[1]C2V[0]": im.if_(edge_cond1, "E2C2V[0]", im.if_(edge_cond2, "E2C2V[3]", "E2C2V[3]")),
# #     "E2C[1]C2V[1]": im.if_(edge_cond1, "E2C2V[1]", im.if_(edge_cond2, "E2C2V[1]", "E2C2V[0]")),
# #     "E2C[1]C2V[2]": im.if_(edge_cond1, "E2C2V[3]", im.if_(edge_cond2, "E2C2V[0]", "E2C2V[1]")),
# #     # E2V2C
# #     "E2V[0]V2C[0]": im.if_(edge_cond1, "E2V2C[0]", im.if_(edge_cond2, "E2V2C[0]", "E2V2C[0]")),
# #     "E2V[0]V2C[1]": im.if_(edge_cond1, "E2V2C[2]", im.if_(edge_cond2, "E2V2C[2]", "E2V2C[2]")),
# #     "E2V[0]V2C[2]": im.if_(edge_cond1, "E2V2C[3]", im.if_(edge_cond2, "E2V2C[3]", "E2V2C[3]")),
# #     "E2V[0]V2C[3]": im.if_(edge_cond1, "E2V2C[4]", im.if_(edge_cond2, "E2V2C[1]", "E2V2C[4]")),
# #     "E2V[0]V2C[4]": im.if_(edge_cond1, "E2V2C[1]", im.if_(edge_cond2, "E2V2C[4]", "E2V2C[5]")),
# #     "E2V[0]V2C[5]": im.if_(edge_cond1, "E2V2C[5]", im.if_(edge_cond2, "E2V2C[5]", "E2V2C[1]")),
# #     "E2V[1]V2C[0]": im.if_(edge_cond1, "E2V2C[0]", im.if_(edge_cond2, "E2V2C[0]", "E2V2C[0]")),
# #     "E2V[1]V2C[1]": im.if_(edge_cond1, "E2V2C[6]", im.if_(edge_cond2, "E2V2C[6]", "E2V2C[6]")),
# #     "E2V[1]V2C[2]": im.if_(edge_cond1, "E2V2C[7]", im.if_(edge_cond2, "E2V2C[7]", "E2V2C[7]")),
# #     "E2V[1]V2C[3]": im.if_(edge_cond1, "E2V2C[8]", im.if_(edge_cond2, "E2V2C[1]", "E2V2C[8]")),
# #     "E2V[1]V2C[4]": im.if_(edge_cond1, "E2V2C[1]", im.if_(edge_cond2, "E2V2C[8]", "E2V2C[1]")),
# #     "E2V[1]V2C[5]": im.if_(edge_cond1, "E2V2C[9]", im.if_(edge_cond2, "E2V2C[9]", "E2V2C[9]")),
# #     # E2V2E
# #     "E2V[0]V2E[0]": im.if_(edge_cond1, "E2V2E[0]", im.if_(edge_cond2, "E2V2E[0]", "self")),
# #     "E2V[0]V2E[1]": im.if_(edge_cond1, "E2V2E[1]", im.if_(edge_cond2, "E2V2E[1]", "E2V2E[0]")),
# #     "E2V[0]V2E[2]": im.if_(edge_cond1, "self", im.if_(edge_cond2, "E2V2E[2]", "E2V2E[1]")),
# #     "E2V[0]V2E[3]": im.if_(edge_cond1, "E2V2E[2]", im.if_(edge_cond2, "E2V2E[3]", "E2V2E[2]")),
# #     "E2V[0]V2E[4]": im.if_(edge_cond1, "E2V2E[3]", im.if_(edge_cond2, "self", "E2V2E[3]")),
# #     "E2V[0]V2E[5]": im.if_(edge_cond1, "E2V2E[4]", im.if_(edge_cond2, "E2V2E[4]", "E2V2E[4]")),
# #     "E2V[1]V2E[0]": im.if_(edge_cond1, "E2V2E[5]", im.if_(edge_cond2, "E2V2E[5]", "self")),
# #     "E2V[1]V2E[1]": im.if_(edge_cond1, "E2V2E[6]", im.if_(edge_cond2, "E2V2E[6]", "E2V2E[5]")),
# #     "E2V[1]V2E[2]": im.if_(edge_cond1, "self", im.if_(edge_cond2, "E2V2E[7]", "E2V2E[6]")),
# #     "E2V[1]V2E[3]": im.if_(edge_cond1, "E2V2E[7]", im.if_(edge_cond2, "E2V2E[8]", "E2V2E[7]")),
# #     "E2V[1]V2E[4]": im.if_(edge_cond1, "E2V2E[8]", im.if_(edge_cond2, "self", "E2V2E[8]")),
# #     "E2V[1]V2E[5]": im.if_(edge_cond1, "E2V2E[9]", im.if_(edge_cond2, "E2V2E[9]", "E2V2E[9]")),
# # }

# # lookup_c = {
# #     # C2E2C
# #     "C2E[0]E2C[0]": im.if_(cell_cond, "self", "C2E2C[0]"),
# #     "C2E[0]E2C[1]": im.if_(cell_cond, "C2E2C[0]", "self"),
# #     "C2E[1]E2C[0]": im.if_(cell_cond, "C2E2C[1]", "C2E2C[1]"),
# #     "C2E[1]E2C[1]": im.if_(cell_cond, "self", "self"),
# #     "C2E[2]E2C[0]": im.if_(cell_cond, "self", "self"),
# #     "C2E[2]E2C[1]": im.if_(cell_cond, "C2E2C[2]", "C2E2C[2]"),
# #     # C2E2V
# #     "C2E[0]E2V[0]": im.if_(cell_cond, "C2V[0]", "C2V[0]"),
# #     "C2E[0]E2V[1]": im.if_(cell_cond, "C2V[1]", "C2V[1]"),
# #     "C2E[1]E2V[0]": im.if_(cell_cond, "C2V[1]", "C2V[1]"),
# #     "C2E[1]E2V[1]": im.if_(cell_cond, "C2V[2]", "C2V[2]"),
# #     "C2E[2]E2V[0]": im.if_(cell_cond, "C2V[0]", "C2V[0]"),
# #     "C2E[2]E2V[1]": im.if_(cell_cond, "C2V[2]", "C2V[2]"),
# #     # C2V2C
# #     "C2V[0]V2C[0]": im.if_(cell_cond, "C2V2C[0]", "self"),
# #     "C2V[0]V2C[1]": im.if_(cell_cond, "C2V2C[1]", "C2V2C[3]"),
# #     "C2V[0]V2C[2]": im.if_(cell_cond, "C2V2C[3]", "C2V2C[4]"),
# #     "C2V[0]V2C[3]": im.if_(cell_cond, "self", "C2V2C[5]"),
# #     "C2V[0]V2C[4]": im.if_(cell_cond, "C2V2C[4]", "C2V2C[0]"),
# #     "C2V[0]V2C[5]": im.if_(cell_cond, "C2V2C[5]", "C2V2C[1]"),
# #     "C2V[1]V2C[0]": im.if_(cell_cond, "C2V2C[0]", "self"),
# #     "C2V[1]V2C[1]": im.if_(cell_cond, "C2V2C[2]", "C2V2C[6]"),
# #     "C2V[1]V2C[2]": im.if_(cell_cond, "C2V2C[6]", "C2V2C[7]"),
# #     "C2V[1]V2C[3]": im.if_(cell_cond, "self", "C2V2C[2]"),
# #     "C2V[1]V2C[4]": im.if_(cell_cond, "C2V2C[7]", "C2V2C[0]"),
# #     "C2V[1]V2C[5]": im.if_(cell_cond, "C2V2C[8]", "C2V2C[8]"),
# #     "C2V[2]V2C[0]": im.if_(cell_cond, "C2V2C[1]", "self"),
# #     "C2V[2]V2C[1]": im.if_(cell_cond, "C2V2C[2]", "C2V2C[9]"),
# #     "C2V[2]V2C[2]": im.if_(cell_cond, "C2V2C[9]", "C2V2C[10]"),
# #     "C2V[2]V2C[3]": im.if_(cell_cond, "self", "C2V2C[2]"),
# #     "C2V[2]V2C[4]": im.if_(cell_cond, "C2V2C[10]", "C2V2C[1]"),
# #     "C2V[2]V2C[5]": im.if_(cell_cond, "C2V2C[11]", "C2V2C[11]"),
# #     # C2V2E
# #     "C2V[0]V2E[0]": im.if_(cell_cond, "C2V2E[3]", "C2V2E[0]"),
# #     "C2V[0]V2E[1]": im.if_(cell_cond, "C2V2E[4]", "C2V2E[3]"),
# #     "C2V[0]V2E[2]": im.if_(cell_cond, "C2V2E[0]", "C2V2E[1]"),
# #     "C2V[0]V2E[3]": im.if_(cell_cond, "C2V2E[5]", "C2V2E[4]"),
# #     "C2V[0]V2E[4]": im.if_(cell_cond, "C2V2E[1]", "C2V2E[5]"),
# #     "C2V[0]V2E[5]": im.if_(cell_cond, "C2V2E[6]", "C2V2E[6]"),
# #     "C2V[1]V2E[0]": im.if_(cell_cond, "C2V2E[2]", "C2V2E[7]"),
# #     "C2V[1]V2E[1]": im.if_(cell_cond, "C2V2E[7]", "C2V2E[8]"),
# #     "C2V[1]V2E[2]": im.if_(cell_cond, "C2V2E[8]", "C2V2E[1]"),
# #     "C2V[1]V2E[3]": im.if_(cell_cond, "C2V2E[9]", "C2V2E[9]"),
# #     "C2V[1]V2E[4]": im.if_(cell_cond, "C2V2E[1]", "C2V2E[2]"),
# #     "C2V[1]V2E[5]": im.if_(cell_cond, "C2V2E[10]", "C2V2E[10]"),
# #     "C2V[2]V2E[0]": im.if_(cell_cond, "C2V2E[2]", "C2V2E[0]"),
# #     "C2V[2]V2E[1]": im.if_(cell_cond, "C2V2E[11]", "C2V2E[11]"),
# #     "C2V[2]V2E[2]": im.if_(cell_cond, "C2V2E[0]", "C2V2E[12]"),
# #     "C2V[2]V2E[3]": im.if_(cell_cond, "C2V2E[12]", "C2V2E[13]"),
# #     "C2V[2]V2E[4]": im.if_(cell_cond, "C2V2E[13]", "C2V2E[2]"),
# #     "C2V[2]V2E[5]": im.if_(cell_cond, "C2V2E[14]", "C2V2E[14]"),
# # }

# # Define the conditionals for use in tables
# edge_cond1 = im.less(
#     im.index(itir.AxisLiteral(value="Edge", kind=common.DimensionKind.HORIZONTAL)), 
#     im.divides_(im.ref("num_edges"), 3)
# )
# edge_cond2 = im.less(
#     im.index(itir.AxisLiteral(value="Edge", kind=common.DimensionKind.HORIZONTAL)), 
#     im.multiplies_(2, im.divides_(im.ref("num_edges"), 3))
# )
# cell_cond = im.less(
#     im.index(itir.AxisLiteral(value="Cell", kind=common.DimensionKind.HORIZONTAL)), 
#     im.divides_(im.ref("num_cells"), 2)
# )
# lookup_e = {
#     # E2C2E
#     "E2C[0]C2E[0]": im.if_(edge_cond1, "E2C2E[0]", im.if_(edge_cond2, "self", "E2C2E[0]")),
#     "E2C[0]C2E[1]": im.if_(edge_cond2, "E2C2E[0]", "E2C2E[1]"),
#     "E2C[0]C2E[2]": im.if_(edge_cond2, "E2C2E[1]", "self"),
#     "E2C[1]C2E[0]": im.if_(edge_cond1, "self", "E2C2E[2]"),
#     "E2C[1]C2E[1]": im.if_(edge_cond1, "E2C2E[2]", "self"),
#     "E2C[1]C2E[2]": "E2C2E[3]",
#     # E2C2V
#     "E2C[0]C2V[0]": "E2C2V[0]",
#     "E2C[0]C2V[1]": im.if_(edge_cond2, "E2C2V[1]", "E2C2V[2]"),
#     "E2C[0]C2V[2]": im.if_(edge_cond2, "E2C2V[2]", "E2C2V[1]"),
#     "E2C[1]C2V[0]": im.if_(edge_cond1, "E2C2V[0]", "E2C2V[3]"),
#     "E2C[1]C2V[1]": im.if_(edge_cond1, "E2C2V[1]", im.if_(edge_cond2, "E2C2V[1]", "E2C2V[0]")),
#     "E2C[1]C2V[2]": im.if_(edge_cond1, "E2C2V[3]", im.if_(edge_cond2, "E2C2V[0]", "E2C2V[1]")),
#     # E2V2C
#     "E2V[0]V2C[0]": "E2V2C[0]",
#     "E2V[0]V2C[1]": "E2V2C[2]",
#     "E2V[0]V2C[2]": "E2V2C[3]",
#     "E2V[0]V2C[3]": im.if_(edge_cond2, "E2V2C[1]", "E2V2C[4]"),
#     "E2V[0]V2C[4]": im.if_(edge_cond1, "E2V2C[1]", im.if_(edge_cond2, "E2V2C[4]", "E2V2C[5]")),
#     "E2V[0]V2C[5]": im.if_(edge_cond2, "E2V2C[5]", "E2V2C[1]"),
#     "E2V[1]V2C[0]": "E2V2C[0]",
#     "E2V[1]V2C[1]": "E2V2C[6]",
#     "E2V[1]V2C[2]": "E2V2C[7]",
#     "E2V[1]V2C[3]": im.if_(edge_cond2, "E2V2C[1]", "E2V2C[8]"),
#     "E2V[1]V2C[4]": im.if_(edge_cond2, "E2V2C[8]", "E2V2C[1]"),
#     "E2V[1]V2C[5]": "E2V2C[9]",
#     # E2V2E
#     "E2V[0]V2E[0]": im.if_(edge_cond2, im.if_(edge_cond1, "E2V2E[0]", "E2V2E[0]"), "self"),
#     "E2V[0]V2E[1]": im.if_(edge_cond2, "E2V2E[1]", "E2V2E[0]"),
#     "E2V[0]V2E[2]": im.if_(edge_cond1, "self", im.if_(edge_cond2, "E2V2E[2]", "E2V2E[1]")),
#     "E2V[0]V2E[3]": im.if_(edge_cond1, "E2V2E[2]", im.if_(edge_cond2, "E2V2E[3]", "E2V2E[2]")),
#     "E2V[0]V2E[4]": im.if_(edge_cond1, "E2V2E[3]", im.if_(edge_cond2, "self", "E2V2E[3]")),
#     "E2V[0]V2E[5]": "E2V2E[4]",
#     "E2V[1]V2E[0]": im.if_(edge_cond2, "E2V2E[5]", "self"),
#     "E2V[1]V2E[1]": im.if_(edge_cond2, "E2V2E[6]", "E2V2E[5]"),
#     "E2V[1]V2E[2]": im.if_(edge_cond1, "self", im.if_(edge_cond2, "E2V2E[7]", "E2V2E[6]")),
#     "E2V[1]V2E[3]": im.if_(edge_cond1, "E2V2E[7]", im.if_(edge_cond2, "E2V2E[8]", "E2V2E[7]")),
#     "E2V[1]V2E[4]": im.if_(edge_cond1, "E2V2E[8]", im.if_(edge_cond2, "self", "E2V2E[8]")),
#     "E2V[1]V2E[5]": "E2V2E[9]",
# }

# lookup_c = {
#     # C2E2C
#     "C2E[0]E2C[0]": im.if_(cell_cond, "self", "C2E2C[0]"),
#     "C2E[0]E2C[1]": im.if_(cell_cond, "C2E2C[0]", "self"),
#     "C2E[1]E2C[0]": "C2E2C[1]",
#     "C2E[1]E2C[1]": "self",
#     "C2E[2]E2C[0]": "self",
#     "C2E[2]E2C[1]": "C2E2C[2]",
#     # C2E2V
#     "C2E[0]E2V[0]": "C2V[0]",
#     "C2E[0]E2V[1]": "C2V[1]",
#     "C2E[1]E2V[0]": "C2V[1]",
#     "C2E[1]E2V[1]": "C2V[2]",
#     "C2E[2]E2V[0]": "C2V[0]",
#     "C2E[2]E2V[1]": "C2V[2]",
#     # C2V2C
#     "C2V[0]V2C[0]": im.if_(cell_cond, "C2V2C[0]", "self"),
#     "C2V[0]V2C[1]": im.if_(cell_cond, "C2V2C[1]", "C2V2C[3]"),
#     "C2V[0]V2C[2]": im.if_(cell_cond, "C2V2C[3]", "C2V2C[4]"),
#     "C2V[0]V2C[3]": im.if_(cell_cond, "self", "C2V2C[5]"),
#     "C2V[0]V2C[4]": im.if_(cell_cond, "C2V2C[4]", "C2V2C[0]"),
#     "C2V[0]V2C[5]": im.if_(cell_cond, "C2V2C[5]", "C2V2C[1]"),
#     "C2V[1]V2C[0]": im.if_(cell_cond, "C2V2C[0]", "self"),
#     "C2V[1]V2C[1]": im.if_(cell_cond, "C2V2C[2]", "C2V2C[6]"),
#     "C2V[1]V2C[2]": im.if_(cell_cond, "C2V2C[6]", "C2V2C[7]"),
#     "C2V[1]V2C[3]": im.if_(cell_cond, "self", "C2V2C[2]"),
#     "C2V[1]V2C[4]": im.if_(cell_cond, "C2V2C[7]", "C2V2C[0]"),
#     "C2V[1]V2C[5]": "C2V2C[8]",
#     "C2V[2]V2C[0]": im.if_(cell_cond, "C2V2C[1]", "self"),
#     "C2V[2]V2C[1]": im.if_(cell_cond, "C2V2C[2]", "C2V2C[9]"),
#     "C2V[2]V2C[2]": im.if_(cell_cond, "C2V2C[9]", "C2V2C[10]"),
#     "C2V[2]V2C[3]": im.if_(cell_cond, "self", "C2V2C[2]"),
#     "C2V[2]V2C[4]": im.if_(cell_cond, "C2V2C[10]", "C2V2C[1]"),
#     "C2V[2]V2C[5]": "C2V2C[11]",
#     # C2V2E
#     "C2V[0]V2E[0]": im.if_(cell_cond, "C2V2E[3]", "C2V2E[0]"),
#     "C2V[0]V2E[1]": im.if_(cell_cond, "C2V2E[4]", "C2V2E[3]"),
#     "C2V[0]V2E[2]": im.if_(cell_cond, "C2V2E[0]", "C2V2E[1]"),
#     "C2V[0]V2E[3]": im.if_(cell_cond, "C2V2E[5]", "C2V2E[4]"),
#     "C2V[0]V2E[4]": im.if_(cell_cond, "C2V2E[1]", "C2V2E[5]"),
#     "C2V[0]V2E[5]": "C2V2E[6]",
#     "C2V[1]V2E[0]": im.if_(cell_cond, "C2V2E[2]", "C2V2E[7]"),
#     "C2V[1]V2E[1]": im.if_(cell_cond, "C2V2E[7]", "C2V2E[8]"),
#     "C2V[1]V2E[2]": im.if_(cell_cond, "C2V2E[8]", "C2V2E[1]"),
#     "C2V[1]V2E[3]": "C2V2E[9]",
#     "C2V[1]V2E[4]": im.if_(cell_cond, "C2V2E[1]", "C2V2E[2]"),
#     "C2V[1]V2E[5]": "C2V2E[10]",
#     "C2V[2]V2E[0]": im.if_(cell_cond, "C2V2E[2]", "C2V2E[0]"),
#     "C2V[2]V2E[1]": "C2V2E[11]",
#     "C2V[2]V2E[2]": im.if_(cell_cond, "C2V2E[0]", "C2V2E[12]"),
#     "C2V[2]V2E[3]": im.if_(cell_cond, "C2V2E[12]", "C2V2E[13]"),
#     "C2V[2]V2E[4]": im.if_(cell_cond, "C2V2E[13]", "C2V2E[2]"),
#     "C2V[2]V2E[5]": "C2V2E[14]",
# }

# lookup_v = {
#     # V2E2C
#     "V2E[0]E2C[0]": "V2C[1]",
#     "V2E[0]E2C[1]": "V2C[0]",
#     "V2E[1]E2C[0]": "V2C[2]",
#     "V2E[1]E2C[1]": "V2C[1]",
#     "V2E[2]E2C[0]": "V2C[3]",
#     "V2E[2]E2C[1]": "V2C[2]",
#     "V2E[3]E2C[0]": "V2C[3]",
#     "V2E[3]E2C[1]": "V2C[4]",
#     "V2E[4]E2C[0]": "V2C[4]",
#     "V2E[4]E2C[1]": "V2C[5]",
#     "V2E[5]E2C[0]": "V2C[5]",
#     "V2E[5]E2C[1]": "V2C[0]",
#     # V2E2V
#     "V2E[0]E2V[0]": "V2E2V[0]",
#     "V2E[0]E2V[1]": "self",
#     "V2E[1]E2V[0]": "V2E2V[1]",
#     "V2E[1]E2V[1]": "self",
#     "V2E[2]E2V[0]": "V2E2V[2]",
#     "V2E[2]E2V[1]": "self",
#     "V2E[3]E2V[0]": "self",
#     "V2E[3]E2V[1]": "V2E2V[3]",
#     "V2E[4]E2V[0]": "self",
#     "V2E[4]E2V[1]": "V2E2V[4]",
#     "V2E[5]E2V[0]": "self",
#     "V2E[5]E2V[1]": "V2E2V[5]",
#     # V2C2V
#     "V2C[0]C2V[0]": "V2E2V[0]",
#     "V2C[0]C2V[1]": "self",
#     "V2C[0]C2V[2]": "V2E2V[5]",
#     "V2C[1]C2V[0]": "V2E2V[0]",
#     "V2C[1]C2V[1]": "V2E2V[1]",
#     "V2C[1]C2V[2]": "self",
#     "V2C[2]C2V[0]": "V2E2V[1]",
#     "V2C[2]C2V[1]": "V2E2V[2]",
#     "V2C[2]C2V[2]": "self",
#     "V2C[3]C2V[0]": "self",
#     "V2C[3]C2V[1]": "V2E2V[2]",
#     "V2C[3]C2V[2]": "V2E2V[3]",
#     "V2C[4]C2V[0]": "self",
#     "V2C[4]C2V[1]": "V2E2V[3]",
#     "V2C[4]C2V[2]": "V2E2V[4]",
#     "V2C[5]C2V[0]": "V2E2V[5]",
#     "V2C[5]C2V[1]": "self",
#     "V2C[5]C2V[2]": "V2E2V[4]",
#     # V2C2E
#     "V2C[0]C2E[0]": "V2C2E[6]",
#     "V2C[0]C2E[1]": "V2C2E[0]",
#     "V2C[0]C2E[2]": "V2C2E[1]",
#     "V2C[1]C2E[0]": "V2C2E[7]",
#     "V2C[1]C2E[1]": "V2C2E[0]",
#     "V2C[1]C2E[2]": "V2C2E[2]",
#     "V2C[2]C2E[0]": "V2C2E[2]",
#     "V2C[2]C2E[1]": "V2C2E[8]",
#     "V2C[2]C2E[2]": "V2C2E[3]",
#     "V2C[3]C2E[0]": "V2C2E[3]",
#     "V2C[3]C2E[1]": "V2C2E[4]",
#     "V2C[3]C2E[2]": "V2C2E[9]",
#     "V2C[4]C2E[0]": "V2C2E[5]",
#     "V2C[4]C2E[1]": "V2C2E[4]",
#     "V2C[4]C2E[2]": "V2C2E[10]",
#     "V2C[5]C2E[0]": "V2C2E[1]",
#     "V2C[5]C2E[1]": "V2C2E[11]",
#     "V2C[5]C2E[2]": "V2C2E[5]",
#     # V2E2C2V
#     "V2E[0]E2C2V[0]": "V2E2C2V[0]",
#     "V2E[0]E2C2V[1]": "self",
#     "V2E[0]E2C2V[2]": "V2E2C2V[1]",
#     "V2E[0]E2C2V[3]": "V2E2C2V[2]",
#     "V2E[1]E2C2V[0]": "V2E2C2V[1]",
#     "V2E[1]E2C2V[1]": "self",
#     "V2E[1]E2C2V[2]": "V2E2C2V[3]",
#     "V2E[1]E2C2V[3]": "V2E2C2V[0]",
#     "V2E[2]E2C2V[0]": "self",
#     "V2E[2]E2C2V[1]": "V2E2C2V[3]",
#     "V2E[2]E2C2V[2]": "V2E2C2V[4]",
#     "V2E[2]E2C2V[3]": "V2E2C2V[1]",
#     "V2E[3]E2C2V[0]": "self",
#     "V2E[3]E2C2V[1]": "V2E2C2V[4]",
#     "V2E[3]E2C2V[2]": "V2E2C2V[3]",
#     "V2E[3]E2C2V[3]": "V2E2C2V[5]",
#     "V2E[4]E2C2V[0]": "self",
#     "V2E[4]E2C2V[1]": "V2E2C2V[5]",
#     "V2E[4]E2C2V[2]": "V2E2C2V[4]",
#     "V2E[4]E2C2V[3]": "V2E2C2V[2]",
#     "V2E[5]E2C2V[0]": "V2E2C2V[2]",
#     "V2E[5]E2C2V[1]": "self",
#     "V2E[5]E2C2V[2]": "V2E2C2V[5]",
#     "V2E[5]E2C2V[3]": "V2E2C2V[0]",
# }

# class CollapseTables(PreserveLocationVisitor, NodeTranslator):

#     def visit_FunCall(self, node: ir.FunCall):
#         node = self.generic_visit(node)

#         if (
#             isinstance(node.fun, ir.FunCall)
#             and isinstance(node.fun.fun, ir.SymRef)
#             and node.fun.fun.id == "shift"
#             and node.fun.args
#             and node.args
#         ):
#             flat_args = node.fun.args
#             if len(flat_args) % 2 != 0:
#                 return node

#             key_parts = []
#             for i in range(0, len(flat_args), 2):
#                 symbol_arg = flat_args[i]
#                 offset_arg = flat_args[i + 1]

#                 if (
#                     isinstance(symbol_arg, ir.OffsetLiteral)
#                     and isinstance(symbol_arg.value, ir.SymbolRef)
#                     and isinstance(offset_arg, ir.OffsetLiteral)
#                     and isinstance(offset_arg.value, int)
#                 ):
#                     part = f"{symbol_arg.value}[{offset_arg.value}]"
#                     key_parts.append(part)
#                 else:
#                     return node

#             key = "".join(key_parts)

#             for table in [lookup_v, lookup_c, lookup_e]:
#                 if key in table:
#                     replacement = table[key]
#                     if isinstance(replacement, str):
#                         # For string replacements (mainly in lookup_v)
#                         if replacement == "self":
#                             return node.args[0]
#                         else:
#                             sym_name, index_str = replacement.split("[")
#                             index = int(index_str.rstrip("]"))
#                             return ir.FunCall(
#                                 fun=ir.FunCall(
#                                     fun=ir.SymRef(id="shift"),
#                                     args=[
#                                         ir.OffsetLiteral(value=ir.SymbolRef(sym_name)),
#                                         ir.OffsetLiteral(value=index),
#                                     ],
#                                 ),
#                                 args=node.args,
#                             )
#                     elif isinstance(replacement, ir.FunCall):
#                         # For conditional expressions (in lookup_e and lookup_c)
#                         # Helper function to process values in the expression
#                         def process_value(val):
#                             if val == "self":
#                                 return node.args[0]
#                             elif isinstance(val, str):
#                                 sym_name, index_str = val.split("[")
#                                 index = int(index_str.rstrip("]"))
#                                 return ir.FunCall(
#                                     fun=ir.FunCall(
#                                         fun=ir.SymRef(id="shift"),
#                                         args=[
#                                             ir.OffsetLiteral(value=ir.SymbolRef(sym_name)),
#                                             ir.OffsetLiteral(value=index),
#                                         ],
#                                     ),
#                                     args=node.args,
#                                 )
#                             elif isinstance(val, ir.FunCall):
#                                 # For nested conditionals 
#                                 if val.fun.id == "if_":
#                                     cond = val.args[0]
#                                     true_branch = process_value(val.args[1])
#                                     false_branch = process_value(val.args[2])
#                                     return im.if_(cond, true_branch, false_branch)
#                                 return val
#                             return val
                        
#                         # Process the main conditional
#                         condition = replacement.args[0]
#                         true_branch = process_value(replacement.args[1])
#                         false_branch = process_value(replacement.args[2])
                        
#                         return im.if_(condition, true_branch, false_branch)
                    
#                     break  # Exit after finding in any table
            
#         return node




#MKLEIN MASTERS THESIS
from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir
from gt4py.next.ffront.experimental import concat_where
from gt4py.next import Dimension
from gt4py.next.iterator.ir_utils import ir_makers as im

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
    # V2E2C2V
    "V2E[0]E2C2V[0]": "V2E2C2V[0]",
    "V2E[0]E2C2V[1]": "self",
    "V2E[0]E2C2V[2]": "V2E2C2V[1]",
    "V2E[0]E2C2V[3]": "V2E2C2V[2]",
    "V2E[1]E2C2V[0]": "V2E2C2V[1]",
    "V2E[1]E2C2V[1]": "self",
    "V2E[1]E2C2V[2]": "V2E2C2V[3]",
    "V2E[1]E2C2V[3]": "V2E2C2V[0]",
    "V2E[2]E2C2V[0]": "self",
    "V2E[2]E2C2V[1]": "V2E2C2V[3]",
    "V2E[2]E2C2V[2]": "V2E2C2V[4]",
    "V2E[2]E2C2V[3]": "V2E2C2V[1]",
    "V2E[3]E2C2V[0]": "self",
    "V2E[3]E2C2V[1]": "V2E2C2V[4]",
    "V2E[3]E2C2V[2]": "V2E2C2V[3]",
    "V2E[3]E2C2V[3]": "V2E2C2V[5]",
    "V2E[4]E2C2V[0]": "self",
    "V2E[4]E2C2V[1]": "V2E2C2V[5]",
    "V2E[4]E2C2V[2]": "V2E2C2V[4]",
    "V2E[4]E2C2V[3]": "V2E2C2V[2]",
    "V2E[5]E2C2V[0]": "V2E2C2V[2]",
    "V2E[5]E2C2V[1]": "self",
    "V2E[5]E2C2V[2]": "V2E2C2V[5]",
    "V2E[5]E2C2V[3]": "V2E2C2V[0]",
}

class CollapseTables(PreserveLocationVisitor, NodeTranslator):

    def visit_FunCall(self, node: ir.FunCall):
        node = self.generic_visit(node)

        if (
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
                    part = f"{symbol_arg.value}[{offset_arg.value}]"
                    key_parts.append(part)
                else:
                    return node

            key = "".join(key_parts)

            # if Dimension("Edge") < (im.divides_(im.ref("num_edges"), 3)):
            #     lookup_e = lookup_e_se
            # elif Dimension("Edge") < (2 * im.divides_(im.ref("num_edges"), 3)):
            #     lookup_e = lookup_e_n
            # else:
            #     lookup_e = lookup_e_e

            # if Dimension("Cell") < (im.divides_(im.ref("num_cells"), 2)):
            #     lookup_c = lookup_c_u
            # else:
            #     lookup_c = lookup_c_d
                

            if Dimension("Edge") < (9216 // 3):
                lookup_e = lookup_e_se
            elif Dimension("Edge") < (2 * 9216 // 3):
                lookup_e = lookup_e_n
            else:
                lookup_e = lookup_e_e

            if Dimension("Cell") < (9216 // 2):
                lookup_c = lookup_c_u
            else:
                lookup_c = lookup_c_d

            for table in [lookup_v, lookup_c, lookup_e]:
                if key in table:
                    replacement = table[key]
                    if replacement == "self":
                        return node.args[0]
                    else:
                        sym_name, index_str = replacement.split("[")
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
