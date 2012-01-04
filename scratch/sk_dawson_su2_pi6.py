from skc.operator import *
from skc.dawson.factor import *
from skc.dawson import *
from skc.compose import *
from skc.basis import *
from skc.simplify import *
import skc.utils
import math
import numpy

# We want to compile pi/6 phase gate
matrix_U = matrixify([[1,0],[0,numpy.exp(1.0j*math.pi/6.0)]])
op_U = Operator(name="U", matrix=matrix_U)

n = 9
print "U= " + str(matrix_U)

##############################################################################
# Prepare the simplify engine
# Simplifying rules
identity_rule = IdentityRule(id_sym=H2.identity.name)
double_H_rule = DoubleIdentityRule('H', id_sym=H2.identity.name)
double_I_rule = DoubleIdentityRule(H2.identity.name, id_sym=H2.identity.name)
adjoint_rule = AdjointRule()
T8_rule = GeneralRule(['T','T','T','T','T','T','T','T'], H2.identity.name)
Td8_rule = GeneralRule(['Td','Td','Td','Td','Td','Td','Td','Td'], H2.identity.name)
# We should also add a rule for 8T gates -> I

simplify_rules = [
	identity_rule,
	double_H_rule,
	double_I_rule,
	adjoint_rule,
	T8_rule,
	Td8_rule
	]

simplify_engine = SimplifyEngine(simplify_rules)

skc.utils.self_adjoint_operators = ['H', H2.identity.name]

# Prepare the compiler
sk_set_factor_method(dawson_group_factor)
sk_set_basis(H2)
sk_set_axis(X_AXIS)
sk_set_simplify_engine(simplify_engine)
sk_build_tree("su2", 15)

Un = solovay_kitaev(op_U, n)
print "Approximated U: " + str(Un)

print "Un= " + str(Un.matrix)

print "trace_dist(U,Un)= " + str(trace_distance(Un.matrix, op_U.matrix))
print "fowler_dist(U,Un)= " + str(fowler_distance(Un.matrix, op_U.matrix))
print "sequence length= " + str(len(Un.ancestors))
print "n= " + str(n)
