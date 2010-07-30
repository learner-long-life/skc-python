# Test matrix direct sum
from skc_utils import *

import numpy

A = matrix_direct_sum(numpy.matrix(1), numpy.matrix(2))

print str(A)