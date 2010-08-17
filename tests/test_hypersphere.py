from skc_dawson_factor import *
from skc_decompose import *
from skc_operator import *
from skc_utils import *
from skc_basis import *

import math

theta = math.pi / 12

H2 = get_hermitian_basis(d=2)

axis = cart3d_to_h2(x=1, y=1, z=1)

matrix_U = axis_to_unitary(axis, theta, H2)

print "U=" + str(matrix_U)

[psi, theta, phi] = unitary_to_hspherical(matrix_U, H2)

print "psi= " + str(psi)
print "theta= " + str(theta)
print "phi= " + str(phi)
