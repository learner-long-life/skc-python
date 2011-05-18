# Generate the two-qubit operator group for Fowler enumeration

from skc.basic_approx.generate import *

import numpy
from skc.operator import *
from skc.simplify import *
from skc.simplify import *
from skc.basis import *
from skc.basic_approx import *

# S matrix
S_matrix = matrixify([[1, 0], [0, 1.0j]])
S = Operator("S", S_matrix)
Sd_matrix = matrixify([[1, 0], [0, -1.0j]])
Sd = Operator("Sd", Sd_matrix)

X1_matrix = numpy.kron(SX.matrix, I2.matrix)
X2_matrix = numpy.kron(I2.matrix, SX.matrix)
X1 = Operator(name="X1", matrix=X1_matrix)
X2 = Operator(name="X2", matrix=X2_matrix)

Z1_matrix = numpy.kron(SZ.matrix, I2.matrix)
Z2_matrix = numpy.kron(I2.matrix, SZ.matrix)
Z1 = Operator(name="Z1", matrix=Z1_matrix)
Z2 = Operator(name="Z2", matrix=Z2_matrix)

H1_matrix = numpy.kron(H.matrix, I2.matrix)
H2_matrix = numpy.kron(I2.matrix, H.matrix)
H1 = Operator(name="H1", matrix=H1_matrix)
H2 = Operator(name="H2", matrix=H2_matrix)

S1_matrix = numpy.kron(S.matrix, I2.matrix)
S2_matrix = numpy.kron(I2.matrix, S.matrix)
S1 = Operator(name="S1", matrix=S1_matrix)
S2 = Operator(name="S2", matrix=S2_matrix)

Sd1_matrix = numpy.kron(Sd.matrix, I2.matrix)
Sd2_matrix = numpy.kron(I2.matrix, Sd.matrix)
Sd1 = Operator(name="Sd1", matrix=Sd1_matrix)
Sd2 = Operator(name="Sd2", matrix=Sd2_matrix)

T1_matrix = numpy.kron(T.matrix, I2.matrix)
T2_matrix = numpy.kron(I2.matrix, T.matrix)
T1 = Operator(name="T1", matrix=T1_matrix)
T2 = Operator(name="T2", matrix=T2_matrix)

CNot12_matrix = matrixify([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CNot12 = Operator(name="CNOT12", matrix=CNot12_matrix)

CNot21_matrix = matrixify([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
CNot21 = Operator(name="CNOT21", matrix=CNot21_matrix)

gset = [X1, X2, Z1, Z2, H1, H2, S1, S2, Sd1, Sd2, CNot12, CNot21]

##############################################################################
# Hermitian basis

H4 = get_hermitian_basis(d=4)

print "BASIS H2"
for (k,v) in H4.items_minus_identity():
	print str(k) + " => " + str(v.matrix)

##############################################################################
# Simplifying rules
identity_rule = IdentityRule(H4.identity.name)

double_rules = []

for gate in gset:
	new_double_rule = DoubleIdentityRule(symbol=gate.name, id_sym=H4.identity.name)
	double_rules.append(new_double_rule)

# H1 and H2 commute with each other
H_rules = []
h1h2h1_rule = GeneralRule(['H1', 'H2', 'H1'], 'H2')
h2h1h2_rule = GeneralRule(['H2', 'H1', 'H2'], 'H1')

H_rules.append(h1h2h1_rule)
H_rules.append(h2h1h2_rule)

# Leave out T rules for now, since T is not in our group
		
adjoint_rule = AdjointRule(id_sym=H4.identity.name)

simplify_rules = [
	identity_rule,
	adjoint_rule
	]
simplify_rules.extend(H_rules)
simplify_rules.extend(double_rules)

##############################################################################
# Custom enumeration rules
def custom_enumeration_rules(operator):
	# Reorder operators which commute
	if (len(operator.ancestors) == 2):
		ancestor1 = operator.ancestors[0]
		ancestor2 = operator.ancestors[1]
		len_ancestor1 = len(ancestor1)
		len_ancestor2 = len(ancestor2)
		
		# Don't do this commutation check for CNOT gates
		if ((len_ancestor1 > 4) or (len_ancestor2 > 4)):
			return False
		
		if ((ancestor1[len_ancestor1-1] == '2') and
			(ancestor2[len_ancestor2-1] == '1')):
			new_op = Operator('', operator.matrix);
			# Swap the ancestors
			new_op.ancestors = [ancestor2, ancestor1]
			# Verify that the canonical order is already in the list
			# assert(new_op in new_sequences)
			print "Eliminating the commuted sequence: " + str(operator)
			return True
	return False

##############################################################################
# Prepare settings
set_filename_prefix("pickles/fowler_su4/gen")

settings = BasicApproxSettings()
settings.set_iset(gset)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(H4.identity)
settings.basis = H4
settings.custom_rules_func = custom_enumeration_rules
