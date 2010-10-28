# Scratch file to test finding an arbitrary orthogonal axis from a point

import math
import scipy.linalg
import numpy

from skc.utils import *
from skc.compose import *
from skc.basis import *

# Find non-collinear point (relative to the origin) to an axis and return an
# orthogonal vector to the axis going through (in R^3)
# Everything is a 3-vector [x,y,z]
def find_orthogonal_axis(axis_P):
	axis_P = numpy.array(axis_P) # Convert to a numpy.array so we can scale it
	axis_X = (1,0,0) # arbitrarily choose point on x-axis
	# Calculate the dot product between P and X to get cos(theta)
	dot_X_P = numpy.dot(axis_P, axis_X)
	# Scale axis_P by cos(theta) to project axis_X onto axis_P
	axis_R = axis_P * dot_X_P
	print "axis_R= " + str(axis_R)
	# The orthogonal axis goes from the projection onto axis_P to axis_X
	axis_Q = axis_X - axis_R
	# Verify orthogonality (inner product is zero)
	inner_Q_P = numpy.inner(axis_Q, axis_P)
	assert_approx_equals(inner_Q_P, 0)
	return axis_Q

# As usual, get a hermitian basis first
B2 = get_hermitian_basis(d=2)

# Generate a random unitary for us to decompose to get an axis
# This is a bit heavyweight, but I don't want to write a function get generate
# a random normalized axis
(matrix_U, axis_U, angle) = get_random_unitary(B2)
print "U= " + str(matrix_U)
print "axis_U= " + str(axis_U)
print "angle= " + str(angle)

# Convert the axis \hat{u} to an array so we can do vector operations on it
axis_U_array = B2.sort_canonical_order(axis_U)
print "axis_U_array= " + str(axis_U_array)

axis_Q_array = find_orthogonal_axis(axis_U_array)
print "axis_Q_array= " + str(axis_Q_array)