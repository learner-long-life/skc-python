# Scratch file to determine whether two rotations commute or not, and if not,
# why not

from skc.operator import *
from skc.utils import *
from skc.compose import *
from skc.basis import *

RXY = SX.matrix * SY.matrix
RYX = SY.matrix * SX.matrix
dist = fowler_distance(RXY, RYX)
# Equal to a phase factor! This is very telling...
assert_approx_equals(dist, 0)

# As usual, get a hermitian basis first
B2 = get_hermitian_basis(d=2)

# Generate a random unitary for us to decompose
# Randomness is the spice of life
(matrix_U, axis_U, angle) = get_random_unitary(B2)
(matrix_U2, axis_U2, angle2) = get_random_unitary(B2)

R12 = matrix_U * matrix_U2
R21 = matrix_U2 * matrix_U
dist = fowler_distance(R12, R21)
# Not equal, even up to a phase factor
assert_approx_not_equals(dist, 0)
