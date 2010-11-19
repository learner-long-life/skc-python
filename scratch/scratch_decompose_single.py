from skc.basis import *
from skc.compose import *
from skc.trig import *

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