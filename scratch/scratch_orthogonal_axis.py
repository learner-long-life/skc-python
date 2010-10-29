# Scratch file to test finding an arbitrary orthogonal axis from a point

import math
import scipy.linalg
import numpy

from skc.utils import *
from skc.compose import *
from skc.basis import *
from skc.hypersphere import *
from super.precompile import *

##############################################################################
# Same as above function, but much more roundabout using spherical coordinates
# Also, it is kinda awkward that I don't have an cart3d_to_hspherical, so
# I just take a matrix argument and ignore the rotation angle argument
def find_orthogonal_axis_spher(matrix_U, axis_U, basis_B2):
	# Convert to spherical coordinates so we can find an orthogonal axis
	# This is a slow and stupid method, I just include it here for my amusement
	hsphere_coords = unitary_to_hspherical(matrix_U, basis_B2)
	axis_U_theta = hsphere_coords[1]
	axis_U_phi = hsphere_coords[2]
	print "hsphere= " + str(hsphere_coords)
	
	# Convert the axis \hat{u} to an array so we can do vector operations on it
	axis_U_array = basis_B2.sort_canonical_order(axis_U)
	print "axis_U_array= " + str(axis_U_array)
	
	# Just verify that we understand how trigonometry works here
	axis_U_z = numpy.cos(axis_U_theta)
	axis_U_y = numpy.sin(axis_U_theta) * numpy.cos(axis_U_phi)
	axis_U_x = numpy.sin(axis_U_theta) * numpy.sin(axis_U_phi)
	axis_U_array2 = [axis_U_x, axis_U_y, axis_U_z]
	print "axis_U_array2= " + str(axis_U_array2)
	
	# And assert that they are equal
	axis_U = [axis_U_x, axis_U_y, axis_U_z]
	assert_vectors_approx_equal(axis_U_array, axis_U)
	
	# Add PI/2 to get an orthogonal axis (along theta coordinate)
	axis_W_theta = (axis_U_theta + PI_HALF) % PI
	axis_W_phi = axis_U_phi
	
	# Reconstruct axis for \hat{w}, which is orthogonal to \hat{a} and \hat{u}
	axis_W_z = numpy.cos(axis_W_theta)
	axis_W_y = numpy.sin(axis_W_theta) * numpy.cos(axis_W_phi)
	axis_W_x = numpy.sin(axis_W_theta) * numpy.sin(axis_W_phi)
	axis_W_array = [axis_W_x, axis_W_y, axis_W_z]
	
	print "axis_W_array= " + str(axis_W_array)
	
	# Take inner product to verify axis_W and axis_U are orthogonal
	inner_W_U = numpy.inner(axis_U_array2, axis_W_array)
	assert_approx_equals(0, inner_W_U)
	return axis_W_array

# As usual, get a hermitian basis first
B2 = get_hermitian_basis(d=2)

# Generate a random unitary for us to decompose to get an axis
# This is a bit heavyweight, but I don't want to write a function get generate
# a random normalized axis
(the_matrix_U, the_axis_U, the_angle) = get_random_unitary(B2)
print "U= " + str(the_matrix_U)
print "axis_U= " + str(the_axis_U)
print "angle= " + str(the_angle)

# Convert the axis \hat{u} to an array so we can do vector operations on it
the_axis_U_array = B2.sort_canonical_order(the_axis_U)
print "axis_U_array= " + str(the_axis_U_array)

# Test the trigonometric method
the_axis_Q_array = find_orthogonal_axis_trig(the_axis_U_array)
print "axis_Q_array= " + str(the_axis_Q_array)

# This doesn't work for now, probably some special cases of converting back
# from spherical to cartesian coordinates. Commented out for now.
# You can comment back in later if you are motivated to fix this.
## Test the spherical coord method
#the_axis_Q2_array = find_orthogonal_axis_spher(the_matrix_U, the_axis_U, B2)
#print "axis_Q2_array= " + str(the_axis_Q2_array)
