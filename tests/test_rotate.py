from skc.utils import *
from skc.rotate import *
from skc.operator import *

import math
import unittest
import random

class TestRotate(unittest.TestCase):

	def test_rotate_z(self):
		matrix_Z = rotate_Z(PI)
		#print "matrix_Z= " + str(matrix_Z)
		assert_matrices_approx_equal(matrix_Z, SZ.matrix, distance=fowler_distance)

	def test_rotate_y(self):
		matrix_Y = rotate_Y(PI)
		#print "matrix_Y= " + str(matrix_Y)
		assert_matrices_approx_equal(matrix_Y, SY.matrix, distance=fowler_distance)
		
	def test_rotate_x(self):
		matrix_X = rotate_X(PI)
		#print "matrix_X= " + str(matrix_X)
		assert_matrices_approx_equal(matrix_X, SX.matrix, distance=fowler_distance)
		
##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestRotate)
	suite.addTest(suite1)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
