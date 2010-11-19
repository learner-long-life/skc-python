from skc.basis import *
from skc.compose import *
from skc.decompose import *
from skc.trig import *
from skc.rotate import *
from skc.operator import *

import math

B2 = get_hermitian_basis(d=2)

(matrix_U, axis_U, angle_U) = get_random_unitary(B2, angle_lower=0, angle_upper=PI_HALF)
print "U= " + str(matrix_U)
print "axis_U= " + str(axis_U)
print "angle_U= " + str(angle_U)

a = matrix_U[(0,0)]
b = matrix_U[(0,1)]
c = matrix_U[(1,0)]
d = matrix_U[(1,1)]

mag_A = numpy.abs(a)
mag_B = numpy.abs(b)
mag_C = numpy.abs(c)
mag_D = numpy.abs(d)

# We recover angles alpha, beta, and gamma using Kitaev's terminology from
# KSV p. 205 and p. 97 of my own notes

# Verify that all the beta's 
beta_A = math.acos(mag_A)*2
beta_B = math.asin(mag_B)*2
beta_C = math.asin(mag_C)*2
beta_D = math.acos(mag_D)*2

# Make sure that these recovered angles are consistent
assert_approx_equals(beta_A, beta_B)
assert_approx_equals(beta_B, beta_C)
assert_approx_equals(beta_C, beta_D)
beta = beta_A
print "beta= " + str(beta)

phase_A = a / mag_A
phase_B = b / mag_B
phase_C = c / mag_C
phase_D = d / mag_D

angle_A = recover_angle(phase_A.real, phase_A.imag)
angle_D = recover_angle(phase_D.real, phase_D.imag)
angle_C = recover_angle(phase_C.real, phase_C.imag)
angle_B = recover_angle(phase_B.real, phase_B.imag)

alpha = angle_B - angle_A - THREE_PI_HALF
delta = angle_C - angle_A - THREE_PI_HALF
print "alpha= " + str(alpha)
print "delta= " + str(delta)

phi_A = angle_A + (alpha/2) + (delta/2)
phi_B = angle_D - (alpha/2) - (delta/2)

print "phi_A= " + str(phi_A)
print "phi_B= " + str(phi_B)
assert_approx_equals(phi_A, 0)
assert_approx_equals(phi_B, TWO_PI)
phi = 0

# Reconstruct the matrix manually
def reconstruct_from_angle_mag(angle, mag):
	phase = numpy.exp(1j*angle)
	return mag * phase
	
a = reconstruct_from_angle_mag(-alpha/2.0 - delta/2.0 + phi, math.cos(beta/2.0))
b = reconstruct_from_angle_mag(alpha/2.0 - delta/2.0 + THREE_PI_HALF + phi, math.sin(beta/2.0))
c = reconstruct_from_angle_mag(-alpha/2.0 + delta/2.0 + THREE_PI_HALF + phi, math.sin(beta/2.0))
d = reconstruct_from_angle_mag(alpha/2.0 + delta/2.0 + phi, math.cos(beta/2.0))

matrix_U3 = matrixify([[a,b],[c,d]])
print "matrix_U3= " + str(matrix_U3)
dist = fowler_distance(matrix_U3, matrix_U)
print "dist(U,U2)= " + str(dist)
assert_approx_equals(0, dist)

# Now let's recompose the matrix from Euler angle decomposition
matrix_Z1 = rotate_Z(delta)
print "Rot_Z(delta)= " + str(matrix_Z1)
matrix_X = rotate_X(beta)
print "Rot_X(beta)= " + str(matrix_X)
matrix_Z2 = rotate_Z(alpha)
print "Rot_Z(alpha)= " + str(matrix_Z2)

matrix_U2 = matrix_Z1 * matrix_X * matrix_Z2
print "matrix_U2= " + str(matrix_U2)
dist = fowler_distance(matrix_U2, matrix_U)
print "dist(U,U2)= " + str(dist)

(axis_U2, K2, matrix_H2) = unitary_to_axis(matrix_U2, B2)
angle_U2 = K2/2.0
print "axis_U2= " + str(axis_U2)
print "angle_U2= " + str(angle_U2)

assert_approx_equals(0, dist)