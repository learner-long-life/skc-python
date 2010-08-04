from skc_basis import *
from skc_decompose import *
from skc_compose import *
from skc_utils import *

import unittest

##############################################################################
# Method for constructing a matrix from basis components
def test_recompose(d):
	B = get_hermitian_basis(d=d)
	(H, components) = get_random_hermitian(B)
	
	#print "H= " + str(H)
	
	(components2, norm) = get_basis_components(H, B)
	
	H3 = matrix_from_components(components2, B)
	
	#print "H3= " + str(H3)
	
	dist = trace_distance(H, H3)
	assert_approx_equals(dist, 0)

##############################################################################
# Class for testing recompose for various SU(d)
class TestRecompose(unittest.TestCase):

	def test_recompose(self):
		for i in range(1,5):
			d = 2**i
			test_recompose(d=d)

def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestRecompose)
	suite.addTest(suite1)
	return suite

if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
