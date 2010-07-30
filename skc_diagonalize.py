# Functions for diagonalizing matrices

import scipy.linalg
import numpy

from skc_utils import *

##############################################################################
# Diagonalize the given unitary in the given basis, returning the
# diagonal matrix W, and the unitary matrix V such that
# V^{-1} * U * V = W
def diagonalize(matrix_U, basis):
	d = basis.d
	print "U= " + str(matrix_U)
	
	(eig_vals, eig_vecs) = scipy.linalg.eig(matrix_U)
	
	print "eig_vals= " + str(eig_vals)
	print "eig_vecs= " + str(eig_vecs)
	
	# Create rows of the matrix from elements of the eigenvectors, to
	# fake creating a matrix from column vectors
	eig_length = len(eig_vecs)
	assert(len(eig_vals) == eig_length)
	
	## Verify eigenvalues and eigenvectors, via Av = \lambdav (eigenvalue eqn)
	#for i in range(eig_length):
	#	col_vec = numpy.matrix(eig_vecs[:,i]).transpose()
	#	scaled_vec1 = matrix_U * col_vec
	#	#print "scaled_vec1= " + str(scaled_vec1)
	#	scaled_vec2 = col_vec * eig_vals[i]
	#	#print "scaled_vec2= " + str(scaled_vec2)
	#	dist = vector_distance(scaled_vec1, scaled_vec2)
	#	assert_approx_equals(dist, 0)
		
	# Create the diagonalization matrix V
	matrix_V = numpy.matrix(eig_vecs) #numpy.matrix(rows)
	
	print "V= " + str(matrix_V)
	
	# Get adjoint
	matrix_V_dag = numpy.transpose(numpy.conjugate(matrix_V))
	
	# Eigenvector matrix should be unitary if we are to have
	# V be its own inverse
	assert_matrix_unitary(matrix_V)
	
	# Multiply V^{-1} * U * V to diagonalize
	matrix_W = matrix_V.I * matrix_U * matrix_V
	
	print "W= " + str(matrix_W)
	
	# Construct the diagonalized matrix that we want
	matrix_diag = numpy.matrix(numpy.eye(d), dtype=numpy.complex)
	for i in range(eig_length):
		matrix_diag[(i,i)] = eig_vals[i]
	
	# Verify that off-diagonal elements are close to zero
	for i in range(eig_length):
		for j in range(eig_length):
			if (i != j):
				assert_approx_equals(matrix_W[(i,j)], 0)
				
	for i in range(eig_length):
		assert_approx_equals(matrix_W[(i,i)], eig_vals[i])

	return (matrix_V, matrix_W)

##############################################################################
# Return a diagonal matrix whose diagonal elements are natural logarithms
# of the corresponding diagonal elements in the input matrix
def get_matrix_logarithm(matrix_diag):
	d = matrix_diag.shape[0]
	# Copy the matrix
	matrix_ln = numpy.matrix(numpy.zeros([d,d], dtype=numpy.complex))
	
	# Substitute diagonal elements for their natural logarithm
	for i in range(d):
		matrix_ln[(i,i)] = numpy.log(matrix_diag[(i,i)])
		
	return matrix_ln
	
##############################################################################
# Given a Hermitian matrix H which is the logarithm of the unitary U
# and a basis, return the different components of H in that basis
# Also return the global constant factor K
def get_basis_components(matrix_H, basis):
	d = basis.d

	# Create a dictionary with the same keys as basis_dict
	component_dict = {}	
	
	# Iterate over basis elements to pick out components in H
	# Don't include the identity element here, we will recalculate it
	# higher up
	for key,gate in basis.items_minus_identity():
		kc_alpha = numpy.trace(matrix_H * gate.matrix)
		component_dict[key] = kc_alpha
		print str(key) + "=> " + str(kc_alpha)
		# Components should be real, with negligible imaginary parts
		#assert_approx_equals(kc_alpha.imag, 0)
	
	# Extract the identity component as a special case.
	# Maybe there's a better way to do this?
	#id_component = numpy.trace(matrix_H).real / d
	#component_dict[basis.identity_key] = id_component
	# Normalization factor
	#scale = 1 / sum
	
	#for key,value in component_dict.items():
	#	component_dict[key] = value * scale
		
	# Check that we really normalized the values
	#assert_approx_equals(scipy.linalg.norm(component_dict.values()), 1)
	
	# Check that we really have the norm of the component vector
	norm = scipy.linalg.norm(component_dict.values())
	print "norm= " + str(norm)
		
	return (component_dict, norm)