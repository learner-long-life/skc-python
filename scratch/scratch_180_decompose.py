# Scratch file to test Kitaev's decomposition of an arbitrary unitary into
# two 180 degree rotations (see Figure S8.2b in his book)

from skc.decompose import *
from skc.compose import *
from skc.basis import *
from skc.hypersphere import *
from skc.utils import *

import numpy
import scipy.linalg

B2 = get_hermitian_basis(d=2)

(matrix_U, axis_U, angle) = get_random_unitary(B2)
print "U= " + str(matrix_U)
print "axis_U= " + str(axis_U)
print "angle= " + str(angle)

axis_U_array = B2.sort_canonical_order(axis_U)
print "axis_U_array= " + str(axis_U_array)

hsphere_coords = unitary_to_hspherical(matrix_U, B2)
axis_U_theta = hsphere_coords[1]
axis_U_phi = hsphere_coords[2]

axis_U_z = numpy.cos(axis_U_theta)
axis_U_y = numpy.sin(axis_U_theta) * numpy.cos(axis_U_phi)
axis_U_x = numpy.sin(axis_U_theta) * numpy.sin(axis_U_phi)
axis_U_array2 = [axis_U_x, axis_U_y, axis_U_z]

print "axis_U_array2= " + str(axis_U_array2)

axis_A_theta = (axis_U_theta + PI_HALF) % PI
axis_A_phi = axis_U_phi

print "hsphere= " + str(hsphere_coords)

axis_A_z = numpy.cos(axis_A_theta)
axis_A_y = numpy.sin(axis_A_theta) * numpy.cos(axis_A_phi)
axis_A_x = numpy.sin(axis_A_theta) * numpy.sin(axis_A_phi)
axis_A_array = [axis_A_x, axis_A_y, axis_A_z]

print "axis_A_array= " + str(axis_A_array)

# Take inner product to verify axis_A and axis_U are orthogonal
inner_A_U = numpy.inner(axis_U_array2, axis_A_array)

print "inner(axis_A, axis_U)= " + str(inner_A_U)

# Axis to rotate about to get from \hat{u} to \hat{a} (cross product)
axis_A1_array = numpy.cross(axis_U_array, axis_A_array)

print "axis_A1_array= " + str(axis_A1_array)

# Take more inner products to verify orthogonality
inner_A_A1 = numpy.inner(axis_A_array, axis_A1_array)
inner_U_A1 = numpy.inner(axis_U_array, axis_A1_array)
print "inner(axis_A, axis_A1)= " + str(inner_A_A1)
print "inner(axis_U, axis_A1)= " + str(inner_U_A1)

norm_A1 = scipy.linalg.norm(axis_A1_array)
axis_A1_array = axis_A1_array / norm_A1
axis_A1 = B2.unsort_canonical_order(axis_A1_array)

# Matrix A is the rotation of 90 degrees from \hat{u} about \hat{a1}
matrix_A1 = axis_to_unitary(axis_A1, PI/2.0, B2)

# Conjugate about a Pauli X rotation
matrix_A = matrix_A1 * SX.matrix * matrix_A1.H

# Add PI_HALF to the last hsphere coordinates to get orthogonal axis
# Also, we want the first coord (the unitary rotation angle) to be 180 degrees
# when we convert back below
#hsphere_A = [PI, hsphere_coords[1], (hsphere_coords[2] + PI_HALF) % PI]
#matrix_A = hspherical_to_unitary(hsphere_A, B2)
#print "A= " + str(matrix_A)

matrix_X = SX.matrix

# Construct the rotation of 90 degrees about the x-axis (arbitrary choice)
# For some reason Kitaev just uses the Pauli X matrix.
#axis_A = B2.unsort_canonical_order(axis_A_array)
#matrix_A1 = axis_to_unitary(axis_A, PI/4.0, B2)
#matrix_A = matrix_A1 * matrix_X * matrix_A1.H
#print "A= " + str(matrix_A)
#print "Adag= " + str(matrix_A.H)

#(axis_A, K_A, hermitian_A) = unitary_to_axis(matrix_A, B2)
#print "axis_A= " + str(axis_A)
#print "angle_A= " + str(K_A/2.0)

#matrix_B1 = axis_to_unitary(axis_U, angle/2.0, B2)
#matrix_B = matrix_B1 * matrix_B * matrix_B1

#matrix_B = axis_to_unitary(axis_U, angle/2.0, B2)
#print "B= " + str
# Add PI_HALF to the last hsphere coordinates to get orthogonal axis
# Also, we want the first coord (the unitary rotation angle) to be 180 degrees
# when we convert back below
#hsphere_A = [PI, hsphere_coords[1], (hsphere_coords[2] + PI_HALF) % PI]

# Here we go
#matrix_A = axis_to_unitary(X_AXIS, hspherical_to_unitary(hsphere_A, B2)
#print "A= " + str(matrix_A)

# And now rotate this rotation by conjugating it with angle/2 about the
# original unitary axis
matrix_B2 = axis_to_unitary(axis_U, angle/2.0, B2)
matrix_B1 = matrix_B2 * matrix_A1 * matrix_B2.H
matrix_B = matrix_B2 * matrix_A * matrix_B2.H

(axis_B, K_B, hermitian_B) = unitary_to_axis(matrix_B, B2)
print "axis_B= " + str(axis_B)

axis_B_array = B2.sort_canonical_order(axis_B)

inner_U_B = numpy.inner(axis_U_array, axis_B_array)
print "inner(axis_U, axis_B)= " + str(inner_U_B)

overlap_A_B = numpy.dot(axis_B_array, axis_A_array)
angle_A_B = math.acos(overlap_A_B)
print "angle_A_B= " + str(angle_A_B)

matrix_U2 = matrix_A * matrix_B

print "U2= " + str(matrix_U2)

dist = fowler_distance(matrix_U, matrix_U2)
print "dist(U,U2)= " + str(dist)

matrix_I = matrix_A * matrix_A.H * matrix_B * matrix_B.H
dist = fowler_distance(I2.matrix, matrix_I)
print "dist(I,I2)= " + str(dist)


#matrix_B = matrix_C * matrix_A * matrix_C.H
#print "B= " + str(matrix_B)

# Now compose the two 180 degree rotations, and hopefully we get back U!
#matrix_U2 = matrix_A
