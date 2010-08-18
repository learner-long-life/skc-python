from skc_basis import *
from skc_decompose import *
from skc.hypersphere import *

import math


axis = cart3d_to_h2(x=1, y=1, z=1)

def test_hsphere_coords(d):
	theta = math.pi / 12

	basis = get_hermitian_basis(d=d)
	axis = pick_random_axis(basis)
	
	matrix_U = axis_to_unitary(axis, theta/2.0, basis)
	print "U=" + str(matrix_U)
	hsphere_coords = unitary_to_hspherical(matrix_U, basis)
	
	print str(hsphere_coords)

test_hsphere_coords(d=2)