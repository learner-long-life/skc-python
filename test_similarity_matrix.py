from skc_dawson_factor import *
from skc_basis import *
from skc_operator import *
from skc_utils import *

import math

def test_similarity(matrix_U1, matrix_U2, basis):
	
	print "U1= " + str(matrix_U1)
	
	print "U2= " + str(matrix_U2)

	# Test finding similarity matrix
	matrix_S = find_similarity_matrix(matrix_U1, matrix_U2, basis)
	
	print "S= "
	print str(matrix_S)
	
	(axis_S, K, matrix_H) = unitary_to_axis(matrix_S, basis)
	angle_S = K/2.0
	
	print "axis_S: " + str(axis_S)
	print "angle_S: " + str(angle_S)
	
	# S * U2 * S^\dagger
	matrix_U = matrix_S * matrix_U2 * matrix_S.H
	
	# Now let's conjugate this bitch
	print "Conjugated U="
	print str(matrix_U)
	
	distance = fowler_distance(matrix_U1, matrix_U)
	print "Distance from U= " + str(distance)
	assert_approx_equals(distance, 0)
	
	# Test that swapping U1 and U2 gives adjoint S
	matrix_S2 = find_similarity_matrix(matrix_U2, matrix_U1, basis)
	dist2 = fowler_distance(matrix_S, matrix_S2.H)
	print "Distance(S,S2_dag)= " + str(dist2)
	assert_approx_equals(dist2, 0)

#############################################################################
# Some definitions common to all the tests below
B2 = get_hermitian_basis(d=2)
x_axis = {('f',(1,2)): 1, ('f',(2,1)): 0, ('h',(2,2)): 0}
y_axis = {('f',(1,2)): 0, ('f',(2,1)): 1, ('h',(2,2)): 0}
z_axis = {('f',(1,2)): 0, ('f',(2,1)): 0, ('h',(2,2)): 1}

#############################################################################
# Start with something easy, which we've verified with Chris's C++ compiler
# x-axis to z-axis
theta = math.pi

unitary_U1 = axis_to_unitary(x_axis, theta/2.0, B2)
assert_matrices_approx_equal(SX.matrix, unitary_U1, fowler_distance)
unitary_U2 = axis_to_unitary(z_axis, theta/2.0, B2)
assert_matrices_approx_equal(SZ.matrix, unitary_U2, fowler_distance)

print "======================"
print "SIMILARITY(X pi, Z pi)"
test_similarity(unitary_U1, unitary_U2, B2)

#############################################################################
# Start with something easy, which we've verified with Chris's C++ compiler
# x-axis to y-axis
theta = math.pi

unitary_U1 = axis_to_unitary(x_axis, theta/2.0, B2)
assert_matrices_approx_equal(SX.matrix, unitary_U1, fowler_distance)
unitary_U2 = axis_to_unitary(y_axis, theta/2.0, B2)
assert_matrices_approx_equal(SY.matrix, unitary_U2, fowler_distance)

print "======================"
print "SIMILARITY(X pi, Y pi)"
test_similarity(unitary_U1, unitary_U2, B2)

#############################################################################
# Test something more complicated
theta = math.pi / 12

# First rotation is about axis (1,0,0)
unitary_U = axis_to_unitary(x_axis, theta, B2)

# Second rotation is about axis(0,1,0) of same angle
unitary_U2 = axis_to_unitary(y_axis, theta, B2)

print "====="
print "SIMILARITY(X pi/12, Y pi/12)"
test_similarity(unitary_U, unitary_U2, B2)