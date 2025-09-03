#MKLEIN MASTERS THESIS
import os
from gt4py.eve import NodeTranslator, PreserveLocationVisitor
from gt4py.next.iterator import ir
from gt4py.next.ffront.experimental import concat_where
from gt4py.next import Dimension
from gt4py.next.iterator.ir_utils import ir_makers as im
from gt4py.next.iterator import ir as itir
from gt4py.next import common

import pdb
from gt4py.next.iterator.ir_utils.common_pattern_matcher import is_applied_as_fieldop

lookup_e_se = {
    "E2C[0]C2E[0]": "E2C2E[0]", "E2C[0]C2E[1]": "self", "E2C[0]C2E[2]": "E2C2E[1]",
    "E2C[1]C2E[0]": "E2C2E[2]", "E2C[1]C2E[1]": "self", "E2C[1]C2E[2]": "E2C2E[3]",
    
    "E2C[0]C2V[0]": "E2C2V[0]",  "E2C[0]C2V[1]": "E2C2V[2]", "E2C[0]C2V[2]": "E2C2V[1]",
    "E2C[1]C2V[0]": "E2C2V[0]",  "E2C[1]C2V[1]": "E2C2V[3]", "E2C[1]C2V[2]": "E2C2V[1]",
    
    "E2V[0]V2C[0]": "E2V2C[2]",  "E2V[0]V2C[1]": "E2V2C[3]", "E2V[0]V2C[2]": "E2V2C[4]",
    "E2V[0]V2C[3]": "E2V2C[0]",  "E2V[0]V2C[4]": "E2V2C[1]", "E2V[0]V2C[5]": "E2V2C[5]",
    "E2V[1]V2C[0]": "E2V2C[1]",  "E2V[1]V2C[1]": "E2V2C[0]", "E2V[1]V2C[2]": "E2V2C[6]",
    "E2V[1]V2C[3]": "E2V2C[7]",  "E2V[1]V2C[4]": "E2V2C[8]", "E2V[1]V2C[5]": "E2V2C[9]",
    
    "E2V[0]V2E[0]": "E2V2E[0]",  "E2V[0]V2E[1]": "E2V2E[1]", "E2V[0]V2E[2]": "E2V2E[2]",
    "E2V[0]V2E[3]": "self",      "E2V[0]V2E[4]": "E2V2E[3]", "E2V[0]V2E[5]": "E2V2E[4]",
    "E2V[1]V2E[0]": "self",      "E2V[1]V2E[1]": "E2V2E[5]", "E2V[1]V2E[2]": "E2V2E[6]",
    "E2V[1]V2E[3]": "E2V2E[7]",  "E2V[1]V2E[4]": "E2V2E[8]", "E2V[1]V2E[5]": "E2V2E[9]",
}

lookup_e_e = {
    "E2C[0]C2E[0]": "E2C2E[0]", "E2C[0]C2E[1]": "E2C2E[1]", "E2C[0]C2E[2]": "self",
    "E2C[1]C2E[0]": "self",     "E2C[1]C2E[1]": "E2C2E[2]", "E2C[1]C2E[2]": "E2C2E[3]",
    
    "E2C[0]C2V[0]": "E2C2V[2]", "E2C[0]C2V[1]": "E2C2V[0]",  "E2C[0]C2V[2]": "E2C2V[1]",
    "E2C[1]C2V[0]": "E2C2V[0]", "E2C[1]C2V[1]": "E2C2V[1]",  "E2C[1]C2V[2]": "E2C2V[3]",
    
    "E2V[0]V2C[0]": "E2V2C[2]", "E2V[0]V2C[1]": "E2V2C[3]",  "E2V[0]V2C[2]": "E2V2C[4]",
    "E2V[0]V2C[3]": "E2V2C[5]", "E2V[0]V2C[4]": "E2V2C[0]",  "E2V[0]V2C[5]": "E2V2C[1]",
    "E2V[1]V2C[0]": "E2V2C[6]", "E2V[1]V2C[1]": "E2V2C[1]",  "E2V[1]V2C[2]": "E2V2C[0]",
    "E2V[1]V2C[3]": "E2V2C[7]", "E2V[1]V2C[4]": "E2V2C[8]",  "E2V[1]V2C[5]": "E2V2C[9]",
    
    "E2V[0]V2E[0]": "E2V2E[0]",  "E2V[0]V2E[1]": "E2V2E[1]", "E2V[0]V2E[2]": "E2V2E[2]",
    "E2V[0]V2E[3]": "E2V2E[3]",  "E2V[0]V2E[4]": "self",     "E2V[0]V2E[5]": "E2V2E[4]",
    "E2V[1]V2E[0]": "E2V2E[5]",  "E2V[1]V2E[1]": "self",     "E2V[1]V2E[2]": "E2V2E[6]",
    "E2V[1]V2E[3]": "E2V2E[7]",  "E2V[1]V2E[4]": "E2V2E[8]", "E2V[1]V2E[5]": "E2V2E[9]",
}

lookup_e_n = {
    "E2C[0]C2E[0]": "E2C2E[0]", "E2C[0]C2E[1]": "E2C2E[1]", "E2C[0]C2E[2]": "self",
    "E2C[1]C2E[0]": "self",     "E2C[1]C2E[1]": "E2C2E[2]", "E2C[1]C2E[2]": "E2C2E[3]",
    
    "E2C[0]C2V[0]": "E2C2V[2]",  "E2C[0]C2V[1]": "E2C2V[0]",  "E2C[0]C2V[2]": "E2C2V[1]",
    "E2C[1]C2V[0]": "E2C2V[0]",  "E2C[1]C2V[1]": "E2C2V[1]",  "E2C[1]C2V[2]": "E2C2V[2]",
    
    "E2V[0]V2C[0]": "E2V2C[2]",  "E2V[0]V2C[1]": "E2V2C[3]",  "E2V[0]V2C[2]": "E2V2C[0]",
    "E2V[0]V2C[3]": "E2V2C[1]",  "E2V[0]V2C[4]": "E2V2C[4]",  "E2V[0]V2C[5]": "E2V2C[5]",
    "E2V[1]V2C[0]": "E2V2C[0]",  "E2V[1]V2C[1]": "E2V2C[6]",  "E2V[1]V2C[2]": "E2V2C[7]",
    "E2V[1]V2C[3]": "E2V2C[8]",  "E2V[1]V2C[4]": "E2V2C[9]",  "E2V[1]V2C[5]": "E2V2C[1]",
    
    "E2V[0]V2E[0]": "E2V2E[0]",  "E2V[0]V2E[1]": "E2V2E[1]",  "E2V[0]V2E[2]": "self",
    "E2V[0]V2E[3]": "E2V2E[3]",  "E2V[0]V2E[4]": "E2V2E[4]",  "E2V[0]V2E[5]": "E2V2E[5]",
    "E2V[1]V2E[0]": "E2V2E[5]",  "E2V[1]V2E[1]": "E2V2E[6]",  "E2V[1]V2E[2]": "E2V2E[7]",
    "E2V[1]V2E[3]": "E2V2E[8]",  "E2V[1]V2E[4]": "E2V2E[9]",  "E2V[1]V2E[5]": "self",
}

lookup_c_u = {
    "C2E[0]E2C[0]": "C2E2C[0]", "C2E[0]E2C[1]": "self", "C2E[1]E2C[0]": "self", 
    "C2E[1]E2C[1]": "C2E2C[1]", "C2E[2]E2C[0]": "self", "C2E[2]E2C[1]": "C2E2C[2]",

    "C2E[0]E2V[0]": "C2V[0]", "C2E[0]E2V[1]": "C2V[1]", "C2E[1]E2V[0]": "C2V[0]", 
    "C2E[1]E2V[1]": "C2V[2]", "C2E[2]E2V[0]": "C2V[1]", "C2E[2]E2V[1]": "C2V[2]",

    "C2V[0]V2C[0]": "C2V2C[3]", "C2V[0]V2C[1]": "C2V2C[4]", "C2V[0]V2C[2]": "C2V2C[0]", 
    "C2V[0]V2C[3]": "self",     "C2V[0]V2C[4]": "C2V2C[1]", "C2V[0]V2C[5]": "C2V2C[5]",
    "C2V[1]V2C[0]": "C2V2C[0]", "C2V[1]V2C[1]": "C2V2C[6]", "C2V[1]V2C[2]": "C2V2C[7]", 
    "C2V[1]V2C[3]": "C2V2C[8]", "C2V[1]V2C[4]": "C2V2C[2]", "C2V[1]V2C[5]": "self",
    "C2V[2]V2C[0]": "C2V2C[1]", "C2V[2]V2C[1]": "self",     "C2V[2]V2C[2]": "C2V2C[2]", 
    "C2V[2]V2C[3]": "C2V2C[9]", "C2V[2]V2C[4]": "C2V2C[10]", "C2V[2]V2C[5]": "C2V2C[11]",

    "C2V[0]V2E[0]": "C2V2E[3]", "C2V[0]V2E[1]": "C2V2E[4]", "C2V[0]V2E[2]": "C2V2E[0]",
    "C2V[0]V2E[3]": "C2V2E[1]", "C2V[0]V2E[4]": "C2V2E[5]", "C2V[0]V2E[5]": "C2V2E[6]",
    "C2V[1]V2E[0]": "C2V2E[7]", "C2V[1]V2E[1]": "C2V2E[8]", "C2V[1]V2E[2]": "C2V2E[9]", 
    "C2V[1]V2E[3]": "C2V2E[10]", "C2V[1]V2E[4]": "C2V2E[2]", "C2V[1]V2E[5]": "C2V2E[0]",
    "C2V[2]V2E[0]": "C2V2E[1]", "C2V[2]V2E[1]": "C2V2E[2]", "C2V[2]V2E[2]": "C2V2E[11]", 
    "C2V[2]V2E[3]": "C2V2E[12]", "C2V[2]V2E[4]": "C2V2E[13]", "C2V[2]V2E[5]": "C2V2E[14]",

    "C2E2C[0]C2E2C[0]": "C2E2C2E2C[0]", "C2E2C[0]C2E2C[1]": "C2E2C2E2C[1]", "C2E2C[0]C2E2C[2]": "self",
    "C2E2C[1]C2E2C[0]": "C2E2C2E2C[2]", "C2E2C[1]C2E2C[1]": "self", "C2E2C[1]C2E2C[2]": "C2E2C2E2C[3]",
    "C2E2C[2]C2E2C[0]": "self", "C2E2C[2]C2E2C[1]": "C2E2C2E2C[4]", "C2E2C[2]C2E2C[2]": "C2E2C2E2C[5]",

    "C2E2CO[0]C2E2CO[0]": "self",         "C2E2CO[0]C2E2CO[1]": "C2E2C[0]", "C2E2CO[0]C2E2CO[2]": "C2E2C[1]",
    "C2E2CO[1]C2E2CO[0]": "C2E2C[2]", "C2E2CO[1]C2E2CO[1]": "C2E2C[0]", "C2E2CO[1]C2E2CO[2]": "C2E2C2E2C[0]",
    "C2E2CO[2]C2E2CO[0]": "C2E2C2E2C[1]", "C2E2CO[2]C2E2CO[1]": "self",         "C2E2CO[2]C2E2CO[2]": "C2E2C[1]",
    "C2E2CO[0]C2E2CO[3]": "C2E2C2E2C[2]", "C2E2CO[3]C2E2CO[0]": "self",         "C2E2CO[1]C2E2CO[3]": "C2E2C2E2C[3]", 
    "C2E2CO[3]C2E2CO[1]": "C2E2C[2]", "C2E2CO[2]C2E2CO[3]": "self",         "C2E2CO[3]C2E2CO[2]": "C2E2C2E2C[4]", 
    "C2E2CO[3]C2E2CO[3]": "C2E2C2E2C[5]",
}

lookup_c_d = {
    "C2E[0]E2C[0]": "C2E2C[0]", "C2E[0]E2C[1]": "self", "C2E[1]E2C[0]": "C2E2C[1]", 
    "C2E[1]E2C[1]": "self",     "C2E[2]E2C[0]": "self", "C2E[2]E2C[1]": "C2E2C[0]",

    "C2E[0]E2V[0]": "C2V[0]", "C2E[0]E2V[1]": "C2V[1]", "C2E[1]E2V[0]": "C2V[0]", 
    "C2E[1]E2V[1]": "C2V[2]", "C2E[2]E2V[0]": "C2V[1]", "C2E[2]E2V[1]": "C2V[2]",

    "C2V[0]V2C[0]": "C2V2C[3]", "C2V[0]V2C[1]": "C2V2C[4]", "C2V[0]V2C[2]": "C2V2C[5]", 
    "C2V[0]V2C[3]": "C2V2C[0]", "C2V[0]V2C[4]": "self",     "C2V[0]V2C[5]": "C2V2C[1]",
    "C2V[1]V2C[0]": "C2V2C[6]", "C2V[1]V2C[1]": "C2V2C[1]", "C2V[1]V2C[2]": "self", 
    "C2V[1]V2C[3]": "C2V2C[2]", "C2V[1]V2C[4]": "C2V2C[7]", "C2V[1]V2C[5]": "C2V2C[8]",
    "C2V[2]V2C[0]": "self",     "C2V[2]V2C[1]": "C2V2C[0]", "C2V[2]V2C[2]": "C2V2C[9]", 
    "C2V[2]V2C[3]": "C2V2C[10]","C2V[2]V2C[4]": "C2V2C[11]","C2V[2]V2C[5]": "C2V2C[2]",

    "C2V[0]V2E[0]": "C2V2E[3]", "C2V[0]V2E[1]": "C2V2E[4]", "C2V[0]V2E[2]": "C2V2E[5]", 
    "C2V[0]V2E[3]": "C2V2E[0]", "C2V[0]V2E[4]": "C2V2E[1]", "C2V[0]V2E[5]": "C2V2E[6]",
    "C2V[1]V2E[0]": "C2V2E[7]", "C2V[1]V2E[1]": "C2V2E[1]", "C2V[1]V2E[2]": "C2V2E[2]", 
    "C2V[1]V2E[3]": "C2V2E[8]", "C2V[1]V2E[4]": "C2V2E[9]", "C2V[1]V2E[5]": "C2V2E[10]",
    "C2V[2]V2E[0]": "C2V2E[0]", "C2V[2]V2E[1]": "C2V2E[11]", "C2V[2]V2E[2]": "C2V2E[12]", 
    "C2V[2]V2E[3]": "C2V2E[13]", "C2V[2]V2E[4]": "C2V2E[14]", "C2V[2]V2E[5]": "C2V2E[2]",

    "C2E2C[0]C2E2C[0]": "C2E2C2E2C[0]", "C2E2C[0]C2E2C[1]": "C2E2C2E2C[1]", "C2E2C[0]C2E2C[2]": "self",
    "C2E2C[1]C2E2C[0]": "C2E2C2E2C[2]", "C2E2C[1]C2E2C[1]": "self", "C2E2C[1]C2E2C[2]": "C2E2C2E2C[3]",
    "C2E2C[2]C2E2C[0]": "self", "C2E2C[2]C2E2C[1]": "C2E2C2E2C[4]", "C2E2C[2]C2E2C[2]": "C2E2C2E2C[5]",

    "C2E2CO[0]C2E2CO[0]": "self",         "C2E2CO[0]C2E2CO[1]": "C2E2C[0]", "C2E2CO[0]C2E2CO[2]": "C2E2C[1]",
    "C2E2CO[1]C2E2CO[0]": "C2E2C[2]", "C2E2CO[1]C2E2CO[1]": "C2E2C[0]", "C2E2CO[1]C2E2CO[2]": "C2E2C2E2C[0]",
    "C2E2CO[2]C2E2CO[0]": "C2E2C2E2C[1]", "C2E2CO[2]C2E2CO[1]": "self",         "C2E2CO[2]C2E2CO[2]": "C2E2C[1]",
    "C2E2CO[0]C2E2CO[3]": "C2E2C2E2C[2]", "C2E2CO[3]C2E2CO[0]": "self",         "C2E2CO[1]C2E2CO[3]": "C2E2C2E2C[3]", 
    "C2E2CO[3]C2E2CO[1]": "C2E2C[2]", "C2E2CO[2]C2E2CO[3]": "self",         "C2E2CO[3]C2E2CO[2]": "C2E2C2E2C[4]", 
    "C2E2CO[3]C2E2CO[3]": "C2E2C2E2C[5]",
}

lookup_v = {
    "V2E[0]E2C[0]": "V2C[1]", "V2E[0]E2C[1]": "V2C[0]", "V2E[1]E2C[0]": "V2C[1]", 
    "V2E[1]E2C[1]": "V2C[2]", "V2E[2]E2C[0]": "V2C[2]", "V2E[2]E2C[1]": "V2C[3]", 
    "V2E[3]E2C[0]": "V2C[3]", "V2E[3]E2C[1]": "V2C[4]", "V2E[4]E2C[0]": "V2C[5]", 
    "V2E[4]E2C[1]": "V2C[4]", "V2E[5]E2C[0]": "V2C[0]", "V2E[5]E2C[1]": "V2C[5]",

    "V2E[0]E2V[0]": "V2E2V[0]", "V2E[0]E2V[1]": "self", "V2E[1]E2V[0]": "V2E2V[1]", 
    "V2E[1]E2V[1]": "self", "V2E[2]E2V[0]": "self", "V2E[2]E2V[1]": "V2E2V[2]", 
    "V2E[3]E2V[0]": "self", "V2E[3]E2V[1]": "V2E2V[3]", "V2E[4]E2V[0]": "self", 
    "V2E[4]E2V[1]": "V2E2V[4]", "V2E[5]E2V[0]": "V2E2V[5]", "V2E[5]E2V[1]": "self",

    "V2C[0]C2V[0]": "V2E2V[0]", "V2C[0]C2V[1]": "V2E2V[5]", "V2C[0]C2V[2]": "self", 
    "V2C[1]C2V[0]": "V2E2V[0]", "V2C[1]C2V[1]": "V2E2V[1]", "V2C[1]C2V[2]": "self", 
    "V2C[2]C2V[0]": "V2E2V[1]", "V2C[2]C2V[1]": "self", "V2C[2]C2V[2]": "V2E2V[2]", 
    "V2C[3]C2V[0]": "self", "V2C[3]C2V[1]": "V2E2V[2]", "V2C[3]C2V[2]": "V2E2V[3]", 
    "V2C[4]C2V[0]": "self", "V2C[4]C2V[1]": "V2E2V[4]", "V2C[4]C2V[2]": "V2E2V[3]", 
    "V2C[5]C2V[0]": "V2E2V[5]", "V2C[5]C2V[1]": "self", "V2C[5]C2V[2]": "V2E2V[4]",

    "V2C[0]C2E[0]": "V2C2E[6]", "V2C[0]C2E[1]": "V2C2E[0]", "V2C[0]C2E[2]": "V2C2E[1]", 
    "V2C[1]C2E[0]": "V2C2E[7]", "V2C[1]C2E[1]": "V2C2E[0]", "V2C[1]C2E[2]": "V2C2E[2]", 
    "V2C[2]C2E[0]": "V2C2E[2]", "V2C[2]C2E[1]": "V2C2E[8]", "V2C[2]C2E[2]": "V2C2E[3]", 
    "V2C[3]C2E[0]": "V2C2E[3]", "V2C[3]C2E[1]": "V2C2E[4]", "V2C[3]C2E[2]": "V2C2E[9]", 
    "V2C[4]C2E[0]": "V2C2E[5]", "V2C[4]C2E[1]": "V2C2E[4]", "V2C[4]C2E[2]": "V2C2E[10]", 
    "V2C[5]C2E[0]": "V2C2E[1]", "V2C[5]C2E[1]": "V2C2E[11]", "V2C[5]C2E[2]": "V2C2E[5]",

    "V2E[0]E2C2V[0]": "V2E2C2V[0]", "V2E[0]E2C2V[1]": "self", "V2E[0]E2C2V[2]": "V2E2C2V[1]", 
    "V2E[0]E2C2V[3]": "V2E2C2V[2]", "V2E[1]E2C2V[0]": "V2E2C2V[1]", "V2E[1]E2C2V[1]": "self", 
    "V2E[1]E2C2V[2]": "V2E2C2V[0]", "V2E[1]E2C2V[3]": "V2E2C2V[3]", "V2E[2]E2C2V[0]": "self", 
    "V2E[2]E2C2V[1]": "V2E2C2V[3]", "V2E[2]E2C2V[2]": "V2E2C2V[1]", "V2E[2]E2C2V[3]": "V2E2C2V[4]", 
    "V2E[3]E2C2V[0]": "self", "V2E[3]E2C2V[1]": "V2E2C2V[4]", "V2E[3]E2C2V[2]": "V2E2C2V[3]", 
    "V2E[3]E2C2V[3]": "V2E2C2V[5]", "V2E[4]E2C2V[0]": "self", "V2E[4]E2C2V[1]": "V2E2C2V[5]", 
    "V2E[4]E2C2V[2]": "V2E2C2V[2]", "V2E[4]E2C2V[3]": "V2E2C2V[4]", "V2E[5]E2C2V[0]": "V2E2C2V[2]", 
    "V2E[5]E2C2V[1]": "self", "V2E[5]E2C2V[2]": "V2E2C2V[0]", "V2E[5]E2C2V[3]": "V2E2C2V[5]",
}

class CollapseTables(PreserveLocationVisitor, NodeTranslator):

    def __init__(self):
        super().__init__()
        self.state = None

    def visit_FunCall(self, node: ir.FunCall):
        if is_applied_as_fieldop(node):
            self.state = {
                "needs_index": False, 
                "index_type": None,
                "needs_grid_params": False,
                "grid_params": {}
            }
            index_param = ir.Sym(id="edge_idx")
            self.state["index_param"] = index_param
            
            visited_node = self.generic_visit(node)
            
            additional_params = []
            additional_args = []

            if self.state["needs_index"]:
                additional_params.append(self.state["index_param"])
                index_expr = im.index(itir.AxisLiteral(
                    value=self.state["index_type"], 
                    kind=common.DimensionKind.HORIZONTAL
                ))
                additional_args.append(index_expr)

            if self.state["needs_grid_params"]:
                for param_name, param_sym in self.state["grid_params"].items():
                    additional_params.append(param_sym)
                    additional_args.append(ir.SymRef(id=param_name))

            if additional_params:
                if isinstance(visited_node.fun, ir.FunCall) and len(visited_node.fun.args) > 0:
                    stencil = visited_node.fun.args[0]
                    if isinstance(stencil, ir.Lambda):
                        new_stencil = ir.Lambda(
                            params=stencil.params + additional_params,
                            expr=stencil.expr
                        )
                        visited_node = ir.FunCall(
                            fun=ir.FunCall(
                                fun=visited_node.fun.fun,
                                args=[new_stencil] + visited_node.fun.args[1:]
                            ),
                            args=visited_node.args + additional_args
                        )
            
            self.state = None
            return visited_node
        
        node = self.generic_visit(node)
        if (
            isinstance(node.fun, ir.FunCall)
            and isinstance(node.fun.fun, ir.SymRef)
            and node.fun.fun.id == "shift"
            and node.fun.args
            and node.args
            and len(node.fun.args) % 2 == 0
        ):
            flat_args = node.fun.args
            parts = []
            for i in range(0, len(flat_args), 2):
                sa, oa = flat_args[i], flat_args[i+1]
                if (
                    isinstance(sa, ir.OffsetLiteral)
                    and isinstance(oa, ir.OffsetLiteral)
                    and isinstance(oa.value, int)
                ):
                    # Accept both plain string and SymbolRef in OffsetLiteral
                    name = sa.value.id if isinstance(sa.value, ir.SymRef) else sa.value
                    if not isinstance(name, str):
                        return node
                    parts.append(f"{name}[{oa.value}]")
                else:
                    return node
            key = "".join(parts)
            if key not in lookup_e_se and key not in lookup_e_e and key not in lookup_e_n \
               and key not in lookup_c_u  and key not in lookup_c_d  and key not in lookup_v:
                return node
            if key.startswith("E2"):
                if self.state is not None:
                    self.state["needs_index"] = True
                    self.state["index_type"] = "Edge"
                    self.state["needs_grid_params"] = True
                    self.state["grid_params"]["num_edges"] = ir.Sym(id="num_edges")
                return self._process_edge_lookup(key, node.args, flat_args)
            elif key.startswith("C2"):
                if self.state is not None:
                    self.state["needs_index"] = True
                    self.state["index_type"] = "Cell"
                    self.state["index_param"] = ir.Sym(id="cell_idx")
                    self.state["needs_grid_params"] = True
                    self.state["grid_params"]["num_cells"] = ir.Sym(id="num_cells")
                return self._process_cell_lookup(key, node.args, flat_args)
            elif key.startswith("V2"):
                return self._process_vertex_lookup(key, node.args, flat_args)
        return node
    
    def _process_edge_lookup(self, key, args, flat_args):
        east      = self._lookup_from_table(key, lookup_e_e, args, flat_args)
        north     = self._lookup_from_table(key, lookup_e_n, args, flat_args)
        southeast = self._lookup_from_table(key, lookup_e_se, args, flat_args)
        
        if self.state and "index_param" in self.state:
            edge_idx = ir.SymRef(id=self.state["index_param"].id)
        else:
            edge_idx = im.deref(im.index(itir.AxisLiteral(value="Edge", kind=common.DimensionKind.HORIZONTAL)))

        # Check environment variable directly
        block_32_flag = os.environ.get("GT4PY_COLLAPSE_TABLES_BLOCK_32", "").lower() in ["1", "true", "True", "TRUE"]
        
        if block_32_flag:
            # Each lookup is in its own block of 32, repeating every 96
            block_size = im.literal("32", "int32")
            block_idx = im.divides_(im.deref(edge_idx), block_size)
            mod3 = im.call("mod")(block_idx, im.literal("3", "int32"))
            cond1 = im.eq(mod3, im.literal("0", "int32"))  # east
            cond2 = im.eq(mod3, im.literal("1", "int32"))  # north
        else:
            # Original logic with blocks of 3
            num_edges     = im.deref(ir.SymRef(id="num_edges"))
            div3          = im.divides_(num_edges, im.literal("3", "int32"))
            two3          = im.multiplies_(im.literal("2", "int32"), div3)
            cond1         = im.less(im.deref(edge_idx), div3)  
            cond2         = im.less(im.deref(edge_idx), two3)  
        
        return im.if_(
            cond1,
            east,
            im.if_(cond2, north, southeast)
        )

    def _process_cell_lookup(self, key, args, flat_args):
        up           = self._lookup_from_table(key, lookup_c_u, args, flat_args)
        down         = self._lookup_from_table(key, lookup_c_d, args, flat_args)
        
        if self.state and "index_param" in self.state:
            cell_idx = ir.SymRef(id=self.state["index_param"].id)  
        else:
            cell_idx = im.deref(im.index(itir.AxisLiteral(value="Cell", kind=common.DimensionKind.HORIZONTAL)))

        # Check environment variable directly
        block_32_flag = os.environ.get("GT4PY_COLLAPSE_TABLES_BLOCK_32", "").lower() in ["1", "true", "True", "TRUE"]
        
        if block_32_flag:
            # Each lookup is in its own block of 32, alternating up/down
            block_size = im.literal("32", "int32")
            block_idx = im.divides_(im.deref(cell_idx), block_size)
            mod2 = im.call("mod")(block_idx, im.literal("2", "int32"))
            cond = im.eq(mod2, im.literal("0", "int32"))  # up if even, down if odd
        else:
            # Original logic with half
            num_cells    = im.deref(ir.SymRef(id="num_cells"))
            half         = im.divides_(num_cells, im.literal("2", "int32"))
            cond         = im.less(im.deref(cell_idx), half) 
        return im.if_(cond, up, down)

    def _process_vertex_lookup(self, key, args, flat_args):
        return self._lookup_from_table(key, lookup_v, args, flat_args)

    def _lookup_from_table(self, key, table, args, flat_args):
        sym = table[key]
        if sym == "self":
            return args[0]
        if "[" in sym and sym.endswith("]"):
            name, rest = sym.split("[", 1)
            idx = int(rest[:-1])
        else:
            name, idx = sym, 0
        return self._make_shift(name, idx, args)
    
    def _make_shift(self, symref, index, args):
        if isinstance(symref, ir.SymbolRef):
            sym_lit = symref
        else:
            sym_lit = ir.SymbolRef(symref)
        return ir.FunCall(
            fun=ir.FunCall(
                fun=ir.SymRef(id="shift"),
                args=[
                    ir.OffsetLiteral(value=sym_lit),
                    ir.OffsetLiteral(value=index),
                ],
            ),
            args=args,
        )