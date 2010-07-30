# Test file to try and find an orthonormal,traceless basis for SU(D)

import numpy
from skc_utils import *
from skc_operator import *
from skc_basis import *

def test_unitary_identity(basis_dict):

	# Extract the dimension of the matrices, based on (0,0) identity element
	element00 = basis_dict[(0,0)]
	d = element00.matrix.shape[0]

def test_orthogonality(basis):

	# Extract the dimension of the matrices, based on (0,0) identity element
	identity_element = basis.identity
	d = basis.d
	print "TESTING BASIS FOR " + str(d) + "x" + str(d) + " MATRICES"
	
	basis_dict = basis.basis_dict

	print "TESTING IDENTITY MATRIX"
	# identity element should be equal to eye(d)
	identity = numpy.matrix(numpy.eye(d), dtype=numpy.complex)
	id_distance = trace_distance(identity, identity_element.matrix)
	assert_approx_equals(id_distance, 0)

	print "TESTING SELF TRACELESS"
	# Assert that all basis elements are traceless
	for gate in basis_dict.values():
		if (gate == identity_element):
			# Skip the identity, it is not traceless
			continue
		#print "Testing \n" + str(gate)
		assert_approx_equals(numpy.trace(gate.matrix), 0)
	
	# I think this property only holds for Pauli matrices and SU(2)
	#print "TESTING SELF-PRODUCT TRACE"
	# Assert that all basis elements have a trace self-product of d
	#for gate in basis_dict.values():
	#	print "Testing " + str(gate) +"\n" + str(gate.matrix)
	#	abs_trace = numpy.abs(numpy.trace(gate.matrix*gate.matrix))
	#	assert_approx_equals(abs_trace, d)
	
	print "TESTING ORTHOGONALITY"
	for gate in basis_dict.values():
		# Remove the gate from the second list copy to avoid self-multiplication
		basis2 = list(basis_dict.values())
		#print "Removing \n" + str(gate)
		#print "From \n" + str(basis2)
		basis2.remove(gate)
		for gate2 in basis2:
			#print "Testing \n" + str(gate) + "\n " + str(gate.matrix)
			#print "  vs. \n" + str(gate2) + "\n " + str(gate2.matrix)
			inner_product = hs_inner_product(gate.matrix, gate2.matrix)
			assert_approx_equals(inner_product, 0)


#########################################################################
# Unitary bases

S2 = get_unitary_basis(d=2) # SU(2), single qubit, same as Pauli matrices

test_orthogonality(S2)

S2.print_string()
S2.map(assert_matrix_unitary)

S4 = get_unitary_basis(d=4) # SU(4), two-qubit

test_orthogonality(S4)

S4.print_string()
S4.map(assert_matrix_unitary)
	
S8 = get_unitary_basis(d=8) # SU(4), two-qubit

test_orthogonality(S8)

S8.print_string()
S8.map(assert_matrix_unitary)

##########################################################################
# Hermitian bases
S2 = get_hermitian_basis(d=2) # SU(2), single qubit, same as Pauli matrices

test_orthogonality(S2)

S2.print_string()
S2.map(assert_matrix_hermitian)

S4 = get_hermitian_basis(d=4) # SU(4), two-qubit

test_orthogonality(S4)

S4.print_string()
S4.map(assert_matrix_hermitian)

S8 = get_hermitian_basis(d=8) # SU(4), two-qubit

test_orthogonality(S8)

S8.print_string()
S8.map(assert_matrix_hermitian)
