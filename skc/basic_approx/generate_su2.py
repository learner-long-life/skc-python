from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basic_approx import *

import skc.basic_approx

import numpy

iset2 = [H, T, T_inv]

for insn in iset2:
	print str(insn)

# Simplifying rules
identity_rule = IdentityRule()
double_H_rule = DoubleIdentityRule('H')
adjoint_rule = AdjointRule()
# We should also add a rule for 8T gates -> I

simplify_rules = [
	identity_rule,
	double_H_rule,
	adjoint_rule
	]
#simplify_rules = []

set_filename_prefix("pickles/basic_approxes_su2")

settings = BasicApproxSettings()
settings.set_iset(iset2)
settings.init_simplify_engine(simplify_rules)
settings.identity = I2

generate_approxes(10, settings)
