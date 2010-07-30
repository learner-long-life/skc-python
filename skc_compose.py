# Module for composing / constructing matrices from a given basis
# Either random or non-random, unitary or hermitian

import random
import scipy.linalg
import numpy

from skc_utils import *
from skc_diagonalize import *

##############################################################################
def get_random_hermitian(basis):
	# Vector of elements corresponding to components from basis
	components = {}
	for k,v in basis.items_minus_identity():
		components[k] = random.random()
		
	norm = scipy.linalg.norm(components.values())

	for k in components:
		components[k] /= norm
		
	# Check that we have actually normalized this vector
	assert_approx_equals(scipy.linalg.norm(components.values()), 1)
	
	d = basis.d
	sum = matrixify(numpy.zeros([d,d]))
	
	for k,v in basis.items_minus_identity():
		sum += components[k] * basis.get(k).matrix
		
	assert_matrix_hermitian(sum)
	
	return (sum, components)

##############################################################################
def exp_hermitian_to_unitary(matrix_H, basis):
	(matrix_V, matrix_W) = diagonalize(matrix_H, basis)
	Udiag = matrix_exp_diag(-1j*(math.pi/2)*matrix_W)
	assert_matrix_unitary(Udiag)
	# Now translate it back to its non-diagonal form
	U = matrix_V * Udiag * matrix_V.I
	assert_matrix_unitary(U)
	return U
	
##############################################################################
# Compose a random unitary by first creating a random Hermitian
# from the given Hermitian basis, and exponentiating it.
# Return the unitary matrix and its original Hermitian components
# This works for general SU(d), where d is given by the hermitian basis.
def get_random_unitary(basis_H):
	(matrix_H, components_H) = get_random_hermitian(basis_H)
	
	matrix_U = exp_hermitian_to_unitary(matrix_H, basis_H)
	return (matrix_U, components_H)
