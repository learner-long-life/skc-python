# Test whether we can roundtrip from unitary to axis and back

from skc_diagonalize import *
from skc_basis import *
from skc_utils import *
from skc_compose import *
from skc_decompose import *

import numpy
import math

B = get_hermitian_basis(d=4)
	
(matrix_U, components, angle) = get_random_unitary(B)

print "U= " + str(matrix_U)

(components2, K, matrix_H) = unitary_to_axis(matrix_U, B)

matrix_U2 = axis_to_unitary(components2, K/2.0, B)

print "U2= " + str(matrix_U2)

fowler_dist = fowler_distance(matrix_U, matrix_U2)

print "fowler_dist(U,U2)= " + str(fowler_dist)

trace_dist = trace_distance(matrix_U, matrix_U2)

print "trace_dist(U,U2)= " + str(trace_dist)

assert_approx_equals_tolerance(fowler_dist, 0, TOLERANCE10)
