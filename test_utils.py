from skc_operator import *
from skc_utils import *

import math
import unittest

class TestUtils(unittest.TestCase):

	# Test that fowler_distance is independent of a global phase
	def test_fowler_distance(self):
		dist = fowler_distance(H.matrix, H.matrix)
		assert_approx_equals_tolerance(dist, 0, TOLERANCE9)

		# Shift by a global phase
		H2 = numpy.exp(1.0j*math.pi / 2) * H.matrix
		
		dist = fowler_distance(H2, H.matrix)
		assert_approx_equals_tolerance(dist, 0, TOLERANCE9)
		
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestUtils)
	suite.addTest(suite1)
	return suite

if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
