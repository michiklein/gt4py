from gt4py import next as gtx
from gt4py.next import neighbor_sum
from gt4py.next.iterator.transforms import (
    unroll_reduce,
    fuse_as_fieldop,
    inline_lifts,
    normalize_shifts,
    inline_lambdas,
    collapse_list_get,
    pass_manager,
    collapse_tables,
)
from gt4py.next.common import NeighborConnectivityType
from gt4py._core import definitions as core_defs

Vertex = gtx.Dimension("Vertex")
Edge = gtx.Dimension("Edge")
Cell = gtx.Dimension("Cell")
C2EDim = gtx.Dimension("C2E", kind=gtx.DimensionKind.LOCAL)
E2VDim = gtx.Dimension("E2V", kind=gtx.DimensionKind.LOCAL)
E2V = gtx.FieldOffset("E2V", source=Vertex, target=(Edge, E2VDim))
C2E = gtx.FieldOffset("C2E", source=Edge, target=(Cell, C2EDim))


@gtx.field_operator
def shift_twice_concrete(
    inp: gtx.Field[gtx.Dims[Vertex], gtx.float64],
) -> gtx.Field[gtx.Dims[Cell], gtx.float64]:
    foo = inp(E2V[0])
    return foo(C2E[0])


ir = shift_twice_concrete.__gt_gtir__()
print(ir)
print(repr(ir))
ir = fuse_as_fieldop.FuseAsFieldOp.apply(ir, offset_provider_type={})
print(ir)
print(repr(ir))
ir = normalize_shifts.NormalizeShifts().visit(ir)
print(ir)
print(repr(ir))
ir = collapse_tables.CollapseTables().visit(ir)
print(ir)
print(repr(ir))
exit(1)

@gtx.field_operator
def shift_twice(
    inp: gtx.Field[gtx.Dims[Vertex], gtx.float64],
) -> gtx.Field[gtx.Dims[Cell], gtx.float64]:
    return neighbor_sum(neighbor_sum(inp(E2V), axis=E2VDim)(C2E), axis=C2EDim)


@gtx.program
def shift_twice_program(
    inp: gtx.Field[gtx.Dims[Vertex], gtx.float64],
    result: gtx.Field[gtx.Dims[Cell], gtx.float64],
):
    shift_twice(inp, out=result)


E2VType = NeighborConnectivityType(
    domain=(Edge, E2VDim),
    codomain=Vertex,
    skip_value=None,
    dtype=core_defs.Int32DType,
    max_neighbors=2,
)
C2EType = NeighborConnectivityType(
    domain=(Cell, C2EDim),
    codomain=Edge,
    skip_value=None,
    dtype=core_defs.Int32DType,
    max_neighbors=3,
)
offset_provider_type = {"E2V": E2VType, "C2E": C2EType}


ir = shift_twice_program.gtir
print(ir)
# ir = pass_manager.apply_common_transforms(ir, offset_provider=offset_provider_type)
# print(ir)
# ir = fuse_as_fieldop.FuseAsFieldOp.apply(ir, offset_provider_type=offset_provider_type)
# print(ir)
# ir = unroll_reduce.UnrollReduce.apply(ir, offset_provider_type=offset_provider_type)
# print(ir)
# # ir = normalize_shifts.NormalizeShifts().visit(ir)
# ir = collapse_list_get.CollapseListGet().visit(ir)
# print(ir)
# # ir = normalize_shifts.NormalizeShifts().visit(ir)
# ir = inline_lambdas.InlineLambdas.apply(ir, opcount_preserving=False)
# ir = inline_lifts.InlineLifts().visit(ir)
# ir = inline_lambdas.InlineLambdas.apply(ir, opcount_preserving=False)
# ir = inline_lifts.InlineLifts().visit(ir)
# ir = normalize_shifts.NormalizeShifts().visit(ir)
# print(ir)
