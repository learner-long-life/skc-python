from skc_diagonalize import *
from skc_basis import *
from skc_utils import *
from skc_compose import *
from skc_decompose import *

import numpy
import math

def test_decomposing_unitary(d):
	print "*******************************************************************"
	print "TESTING DECOMPOSITION OF UNITARY IN SU("+str(d)+")"
	B = get_hermitian_basis(d)
	
	(matrix_U, components, angle) = get_random_unitary(B)
	
	print "U= " + str(matrix_U)
		
	(matrix_V, matrix_W) = diagonalize(matrix_U, B)
	
	print "V= " + str(matrix_V)
	print "W= " + str(matrix_W)
	
	matrix_ln = get_matrix_logarithm(matrix_W)
	
	print "matrix_ln= " + str(matrix_ln)
	
	# Reconjugate to transform into iH
	matrix_iH = matrix_V * matrix_ln * matrix_V.I
	
	# Factor out -i (since we used -i in exp_hermitian_to_unitary)
	matrix_H = (-1.0/1j) * matrix_iH
	
	print "matrix_H= " + str(matrix_H)
	
	# Compare the calculated components with our original
	(components2, K) = get_basis_components(matrix_H, B)
	
	print "K= " + str(K)
	print "angle= " + str(angle)
	assert_approx_equals_tolerance(numpy.abs(K), numpy.abs(2*angle), TOLERANCE4)
	
	#print "Renormalizing... "
	# Renormalize components
	#for key,value in components2.items():
	#	components2[key] = value / K
	#	print "("+str(key)+")= " + str(components2[key])
	
	# Assert that the components are now normalized
	norm = scipy.linalg.norm(components.values())
	norm2= scipy.linalg.norm(components2.values())
	print "norm= " + str(norm)
	print "norm2= " + str(norm2)
	assert_approx_equals(norm2, 1)
		
	for key in components2.keys():
		print str(key)
		print "  actual= " + str(components[key])
		print "  comput= " + str(components2[key])
		ratio = abs(components[key]) / abs(components2[key])
		#print "  ratio= " + str(ratio)
		assert_approx_equals_tolerance(ratio, 1, TOLERANCE6)

test_decomposing_unitary(d=2)
test_decomposing_unitary(d=4)
test_decomposing_unitary(d=8)
