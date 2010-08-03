from skc_basis import *
from skc_decompose import *
from skc_compose import *
from skc_utils import *

def test_recompose(d):
	B = get_hermitian_basis(d=d)
	(H, components) = get_random_hermitian(B)
	
	print "H= " + str(H)
	
	(components2, norm) = get_basis_components(H, B)
	
	for k,v in components2.items():
		print str(k) + " => " + str(v)
		components2[k] /= norm
		
	H3 = matrix_from_components(components2, B)
	
	print "H3= " + str(H3)
	
	dist = trace_distance(H, H3)
	assert_approx_equals(dist, 0)
	
test_recompose(d=2)
test_recompose(d=4)
test_recompose(d=8)