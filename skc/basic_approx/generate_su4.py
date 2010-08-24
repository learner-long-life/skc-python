from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basis import *
from skc.basic_approx import *

import numpy

H1_matrix = numpy.kron(H.matrix, I2.matrix)
H2_matrix = numpy.kron(I2.matrix, H.matrix)
H1 = Operator(name="H1", matrix=H1_matrix)
H2 = Operator(name="H2", matrix=H2_matrix)

T1_matrix = numpy.kron(T.matrix, I2.matrix)
T2_matrix = numpy.kron(I2.matrix, T.matrix)
T1 = Operator(name="T1", matrix=T1_matrix)
T2 = Operator(name="T2", matrix=T2_matrix)

Tinv1_matrix = numpy.kron(T_inv.matrix, I2.matrix)
Tinv2_matrix = numpy.kron(I2.matrix, T_inv.matrix)
Tinv1 = Operator(name="T1d", matrix=Tinv1_matrix)
Tinv2 = Operator(name="T2d", matrix=Tinv2_matrix)

CNot_matrix = matrixify([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CNot = Operator(name="CN", matrix=CNot_matrix)
CNotd = Operator(name="CNd", matrix=CNot_matrix.H)

iset4 = [H1, H2, T1, T2, Tinv1, Tinv2, CNot, CNotd]

for insn in iset4:
	print str(insn)
#iset = [H, T, T_inv]

# Simplifying rules
identity_rule = IdentityRule()
double_H1_rule = DoubleIdentityRule('H1')
double_H2_rule = DoubleIdentityRule('H2')
double_CN_rule = DoubleIdentityRule('CN')
adjoint_rule = AdjointRule()

simplify_rules = [
	identity_rule,
	double_H1_rule,
	double_H2_rule,
	double_CN_rule,
	adjoint_rule
	]
#simplify_rules = []

H4 = get_hermitian_basis(d=4)

set_filename_prefix("pickles/su4/basic_approxes")

settings = BasicApproxSettings()
settings.set_iset(iset4)
settings.init_simplify_engine(simplify_rules)
settings.identity = H4.identity

generate_approxes(6, settings)