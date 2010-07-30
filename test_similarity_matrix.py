from skc_dawson_factor import *
from skc_unitary_decompose import *
from skc_operator import *
from skc_utils import *

import math

def test_similarity(unitary_U1, unitary_U2):
	
	print "U1="
	unitary_U1.print_string()
	
	matrix_U1 = unitary_U1.to_matrix()
	print str(matrix_U1)
	
	op_U1 = Operator(name="U", matrix=matrix_U1)
	
	print "U2="
	unitary_U2.print_string()
	
	matrix_U2 = unitary_U2.to_matrix()
	print str(matrix_U2)
	
	op_U2 = Operator(name="U", matrix=matrix_U2)

	# Test finding similarity matrix
	matrix_S = find_similarity_matrix(matrix_U1, matrix_U2)
	
	print "S="
	print str(matrix_S)
	
	unitary_S = matrix_to_unitary4d(matrix_S)
	unitary_S.print_string()
	
	[axis_S, angle_S] = unitary_S.to_rotation()
	print "axis_S: " + str(axis_S)
	print "angle_S: " + str(angle_S)
	
	op_U1 = Operator(name="U2", matrix=matrix_U1)
	op_S = Operator("S", matrix_S)
	op_S_dag = op_S.dagger()
	conjugated_U2 = op_S.multiply(op_U2).multiply(op_S_dag)
	
	# Now let's conjugate this bitch
	print "Conjugated U2="
	print str(conjugated_U2.matrix)
	
	distance = trace_distance(matrix_U1, conjugated_U2.matrix)
	print "Distance from U= " + str(distance)
	assert(distance < TOLERANCE)
	
	# Test that swapping U1 and U2 gives adjoint S
	matrix_S2 = find_similarity_matrix(matrix_U2, matrix_U1)
	matrix_S2_dag = numpy.transpose(numpy.conjugate(matrix_S2))
	dist2 = trace_distance(matrix_S, matrix_S2_dag)
	print "Distance(S,S2_dag)= " + str(dist2)
	assert(dist2 < TOLERANCE)

#############################################################################
# Some definitions common to all the tests below
x_axis = Cart3DCoords(1,0,0)
y_axis = Cart3DCoords(0,1,0)
z_axis = Cart3DCoords(0,0,1)

#############################################################################
# Start with something easy, which we've verified with Chris's C++ compiler
# x-axis to z-axis
theta = math.pi

unitary_U1 = x_axis.to_unitary_rotation(theta)
unitary_U2 = z_axis.to_unitary_rotation(theta)

print "======================"
print "SIMILARITY(X pi, Z pi)"
test_similarity(unitary_U1, unitary_U2)

#############################################################################
# Start with something easy, which we've verified with Chris's C++ compiler
# x-axis to y-axis
theta = math.pi

unitary_U1 = x_axis.to_unitary_rotation(theta)
unitary_U2 = y_axis.to_unitary_rotation(theta)

print "======================"
print "SIMILARITY(X pi, Y pi)"
test_similarity(unitary_U1, unitary_U2)

#############################################################################
# Test something more complicated
theta = math.pi / 12

# First rotation is about axis (1,0,0)
unitary_U = x_axis.to_unitary_rotation(theta)

# Second rotation is about axis(0,1,0) of same angle
unitary_U2 = y_axis.to_unitary_rotation(theta)

print "====="
print "SIMILARITY(X pi/12, Y pi/12)"
test_similarity(unitary_U, unitary_U2)