# Testing that we can tell whether a matrix is unitary or not

from skc_operator import *
from skc_utils import *
from skc_basis import *
from skc_compose import *

# Pauli matrices are unitary
assert_matrix_unitary(SX.matrix)
assert_matrix_unitary(SY.matrix)
assert_matrix_unitary(SZ.matrix)
assert_matrix_unitary(I2.matrix)

# Test for Hermiticity just for good measure
assert_matrix_hermitian(SX.matrix)
assert_matrix_hermitian(SY.matrix)
assert_matrix_hermitian(SZ.matrix)
assert_matrix_hermitian(I2.matrix)

# SU(2)
B2 = get_hermitian_basis(d=2)

# Get a random Hermitian
(H, components) = get_random_hermitian(B2)

U = exp_hermitian_to_unitary(H, B2)

print "U= " + str(U)

assert_matrix_unitary(U)

B4 = get_hermitian_basis(d=4)
(H4, components4) = get_random_hermitian(B4)

U4 = exp_hermitian_to_unitary(H4, B4)

print "U4= " + str(U4)

assert_matrix_unitary(U4)
