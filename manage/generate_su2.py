from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basic_approx import *
from skc.basis import *

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

H2 = get_hermitian_basis(d=2)

print "BASIS H2"
for (k,v) in H2.items_minus_identity():
	print str(k) + " => " + str(v.matrix)

set_filename_prefix("pickles/su2/gen")

settings = BasicApproxSettings()
settings.set_iset(iset2)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(I2)
settings.basis = H2

generate_approxes(16, settings)
