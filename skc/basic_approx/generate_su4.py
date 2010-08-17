from skc.basic_approx.generate import *

from skc_operator import *
from skc_simplify import *

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
Tinv1 = Operator(name="Tinv1", matrix=Tinv1_matrix)
Tinv2 = Operator(name="Tinv2", matrix=Tinv2_matrix)

iset4 = [H1, H2, T1, T2, Tinv1, Tinv2]
#iset = [H, T, T_inv]

# Simplifying rules
double_identity_rule = DoubleIdentityRule('I')

simplify_rules = [double_identity_rule]

generate_approxes("basic_approxes_su4.pickle", iset4, 7, simplify_rules)