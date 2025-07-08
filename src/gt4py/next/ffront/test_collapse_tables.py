from gt4py import next as gtx
from gt4py.next.iterator.transforms import (
    fuse_as_fieldop,
    normalize_shifts,
    collapse_tables,
    inline_fundefs,
    pass_manager,
)
from gt4py.next.common import NeighborConnectivityType
from gt4py._core import definitions as core_defs
from gt4py.next.iterator.transforms.inline_lambdas import InlineLambdas


Vertex = gtx.Dimension("Vertex")
Edge = gtx.Dimension("Edge")
Cell = gtx.Dimension("Cell")
C2EDim = gtx.Dimension("C2E", kind=gtx.DimensionKind.LOCAL)
E2VDim = gtx.Dimension("E2V", kind=gtx.DimensionKind.LOCAL)
V2EDim = gtx.Dimension("V2E", kind=gtx.DimensionKind.LOCAL)
E2V = gtx.FieldOffset("E2V", source=Vertex, target=(Edge, E2VDim))
C2E = gtx.FieldOffset("C2E", source=Edge, target=(Cell, C2EDim))
V2E = gtx.FieldOffset("V2E", source=Edge, target=(Vertex, E2VDim))

@gtx.field_operator
def shift_twice_concrete(
    inp: gtx.Field[gtx.Dims[Vertex], gtx.float64],
) -> gtx.Field[gtx.Dims[Vertex], gtx.float64]:
    foo = inp(E2V[0])
    return foo(V2E[2])

@gtx.field_operator
def shift_once(
    inp: gtx.Field[gtx.Dims[Vertex], gtx.float64],
) -> gtx.Field[gtx.Dims[Edge], gtx.float64]:
    return inp(E2V[0])

@gtx.field_operator
def shift_again(
    inp: gtx.Field[gtx.Dims[Edge], gtx.float64],
) -> gtx.Field[gtx.Dims[Vertex], gtx.float64]:
    return inp(V2E[2])

@gtx.field_operator
def shift_twice_split(
    inp: gtx.Field[gtx.Dims[Vertex], gtx.float64],
) -> gtx.Field[gtx.Dims[Vertex], gtx.float64]:
    return shift_again(shift_once(inp))


E2VType = NeighborConnectivityType(
    domain=(Edge, E2VDim),
    codomain=Vertex,
    skip_value=None,
    dtype=core_defs.Int32DType,
    max_neighbors=2,
)
V2EType = NeighborConnectivityType(
    domain=(Vertex, V2EDim),
    codomain=Edge,
    skip_value=None,
    dtype=core_defs.Int32DType,
    max_neighbors=3,
)

offset_provider_type = {"E2V": E2VType, "V2E": V2EType}

def optimize_and_print(ir):
    ir = InlineLambdas().visit(ir)
    ir = pass_manager.apply_common_transforms(ir, offset_provider={})
    ir = fuse_as_fieldop.FuseAsFieldOp.apply(ir, offset_provider_type={})
    ir = normalize_shifts.NormalizeShifts().visit(ir)
    ir = collapse_tables.CollapseTables().visit(ir)
    print(ir)
    print(repr(ir))

ir_combined = shift_twice_concrete.__gt_gtir__()

optimize_and_print(ir_combined)

ir_split = shift_twice_split.__gt_gtir__()
optimize_and_print(ir_split)
