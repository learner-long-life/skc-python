import numpy
import scipy.linalg

from skc.utils import *
from skc.compose import *

##############################################################################
# Find non-collinear point (relative to the origin) to an axis and return an
# orthogonal vector to the axis going through (in R^3), using trigonometry
# Everything is a 3-vector [x,y,z]
def find_orthogonal_axis_trig(axis_P):
	axis_P = numpy.array(axis_P) # Convert to a numpy.array so we can scale it
	axis_X = (1,0,0) # arbitrarily choose point on x-axis
	# Calculate the dot product between P and X to get cos(theta)
	dot_X_P = numpy.dot(axis_P, axis_X)
	# Scale axis_P by cos(theta) to project axis_X onto axis_P
	axis_R = axis_P * dot_X_P
	print "axis_R= " + str(axis_R)
	# The orthogonal axis goes from the projection onto axis_P to axis_X
	axis_Q = axis_X - axis_R
	# Renormalize the vector
	norm_Q = scipy.linalg.norm(axis_Q)
	axis_Q = axis_Q / norm_Q
	assert_approx_equals(scipy.linalg.norm(axis_Q), 1)

	# Verify orthogonality (inner product is zero)
	inner_Q_P = numpy.inner(axis_Q, axis_P)
	assert_approx_equals(inner_Q_P, 0)
	return axis_Q

##############################################################################
# Given two axes in R^3, return the matrix which is SU(2) operator corresponding
# to a rotation of axis1 to axis2
def get_rotation_matrix(axis_1, axis_2, basis, angle_sign=-1):
	axis_1_array = basis.sort_canonical_order(axis_1)
	axis_2_array = basis.sort_canonical_order(axis_2)
	axis_T_array = numpy.cross(axis_1_array, axis_2_array)
	print "axis_1= " + str(axis_1_array)
	print "axis_2= " + str(axis_2_array)
	print "axis_T= " + str(axis_T_array)
	norm_T = scipy.linalg.norm(axis_T_array)
	axis_T_array = numpy.array(axis_T_array) / norm_T
	print "axis_T= " + str(axis_T_array)
	
	axis_T = basis.unsort_canonical_order(axis_T_array)
	
	dot_1_2 = numpy.inner(axis_1_array, axis_2_array)
	
	angle_1_2 = math.acos(dot_1_2)
	assert(angle_1_2 > 0.0)
	
	# Make the angle negative because... why?
	angle = angle_sign * (angle_1_2/2.0); # divide by 2 for double covering
	print "angle= " + str(angle)
	matrix_T = axis_to_unitary(axis_T, angle, basis)
	return matrix_T
