# Scratch file to determine whether two rotations commute or not, and if not,
# why not

from skc.operator import *
from skc.utils import *
from skc.compose import *
from skc.decompose import *
from skc.basis import *

B2 = get_hermitian_basis(d=2)

axis_X_array = [1,0,0]
axis_Y_array = [0,1,0]
axis_Z_array = [0,0,1]

axis_X = B2.unsort_canonical_order(axis_X_array)
axis_Y = B2.unsort_canonical_order(axis_Y_array)

print "x_axis= " + str(axis_X)
print "y_axis= " + str(axis_Y)
print "pi/4= " + str(PI/4.0)

RX = axis_to_unitary(axis_X, PI/4.0, B2)
# Note that the conjugating rotation angle shouldn't effect the composed
# rotation angle
RY = axis_to_unitary(axis_Y, PI/6.0, B2)
RXY = RY.H * RX * RY
(axis_xy, K_xy, matrix_H_xy) = unitary_to_axis(RXY, B2)

angle_xy = K_xy/2.0
assert_approx_equals(angle_xy, PI/4.0)

print "axis_xy= " + str(axis_xy)
print "angle_xy= " + str(angle_xy)
print "matrix_H_xy= " + str(matrix_H_xy)

axis_xy_array = B2.sort_canonical_order(axis_xy)
dot_x_xy = numpy.dot(axis_xy_array, axis_X_array)
dot_y_xy = numpy.dot(axis_xy_array, axis_Y_array)
dot_z_xy = numpy.dot(axis_xy_array, axis_Z_array)
assert_approx_equals(math.sin(PI/6.0), dot_x_xy)
assert_approx_equals(math.cos(PI/6.0), dot_z_xy)
assert_approx_equals(0, dot_y_xy)

##############################################################################
# Let's use the axis_XY above as a fixed, non-random, non-orthogonal axis
RXXY = RXY.H * RX * RXY
(axis_XXY, K_XXY, matrix_H_XXY) = unitary_to_axis(RXXY, B2)

angle_XXY = K_XXY/2.0
assert_approx_equals(angle_XXY, PI/4.0)

print "axis_XXY= " + str(axis_XXY)
print "angle_XXY= " + str(angle_XXY)
print "matrix_H_XXY= " + str(matrix_H_XXY)

(matrix_U, axis_U, angle) = get_random_unitary(B2)
axis_U = {
	('f', (2, 1)): 0.26839308905806225,
	('f', (1, 2)): 0.82690780394690444,
	('h', (2, 2)): 0.49415446321730094
	}

print "axis_U= " + str(axis_U)
axis_U_array = B2.sort_canonical_order(axis_U)
axis_T_array = numpy.cross(axis_X_array, axis_U_array)
norm_T = scipy.linalg.norm(axis_T_array)
axis_T_array = axis_T_array / norm_T

axis_T = B2.unsort_canonical_order(axis_T_array)

print "axis_U_array= " + str(axis_U_array)
print "axis_X_array= " + str(axis_X_array)

dot_U_X = numpy.inner(axis_U_array, axis_X_array)

print "dot_U_X= " + str(dot_U_X)

angle_U_X = math.acos(dot_U_X)

print "axis_T= " + str(axis_T)
print "angle_T= " + str(angle_U_X)

angle = -(angle_U_X/2.0); #-math.pi/10;
print "angle= " + str(angle)

matrix_T = axis_to_unitary(axis_T, angle, B2)
RTX = matrix_T.H * RX * matrix_T
(axis_TX, K_TX, matrix_H_TX) = unitary_to_axis(RTX, B2)
print "axis_TX= " + str(axis_TX)
axis_TX_array = B2.sort_canonical_order(axis_TX)
assert_vectors_approx_equal(axis_TX_array, axis_U_array)