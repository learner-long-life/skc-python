# Testing that we can compose a unitary by exponentiating a hermitian

from skc_operator import *
from skc_utils import *
from skc_basis import *
from skc_compose import *
from skc_decompose import *

import random
import unittest

# Maximum dimension (2**D) to test
D = 4

##############################################################################
def test_pauli_unitary():
	# Pauli matrices are unitary
	assert_matrix_unitary(SX.matrix)
	assert_matrix_unitary(SY.matrix)
	assert_matrix_unitary(SZ.matrix)
	assert_matrix_unitary(I2.matrix)

##############################################################################
def test_pauli_hermitian():
	# Test for Hermiticity just for good measure
	assert_matrix_hermitian(SX.matrix)
	assert_matrix_hermitian(SY.matrix)
	assert_matrix_hermitian(SZ.matrix)
	assert_matrix_hermitian(I2.matrix)

##############################################################################
def create_test_case(d):

	class TestComposeCase(unittest.TestCase):
	
		def setUp(self):
			self.basis = get_hermitian_basis(d=2)

		def test_compose(self):
			# Get a random Hermitian
			(H, components) = get_random_hermitian(self.basis)
			
			#U = exp_hermitian_to_unitary(H, math.pi/2, self.basis)
			#print "U(pi/2)= " + str(U)
			#assert_matrix_unitary(U)
			angle = random.random() * math.pi
			U = exp_hermitian_to_unitary(H, angle, self.basis)
			#print "U("+str(angle)+")= " + str(U)
			assert_matrix_unitary(U)
			
		def test_axis_roundtrip(self):
			(matrix_U, components, angle) = get_random_unitary(self.basis)
			(components2, K, matrix_H) = unitary_to_axis(matrix_U, self.basis)
			matrix_U2 = axis_to_unitary(components2, K/2.0, self.basis)
			fowler_dist = fowler_distance(matrix_U, matrix_U2)
			assert_approx_equals_tolerance(fowler_dist, 0, TOLERANCE10)
			trace_dist = trace_distance(matrix_U, matrix_U2)
			assert_approx_equals(trace_dist, 0)

	return TestComposeCase

##############################################################################	
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()

	# Create one test case for every SU(d)
	for i in range(1,D+1):
		d = 2**i
		test_case = create_test_case(d)
		suite1 = loader.loadTestsFromTestCase(test_case)
		suite.addTest(suite1)
	
	# Add single function tests from above
	suite.addTest(unittest.FunctionTestCase(test_pauli_unitary))
	suite.addTest(unittest.FunctionTestCase(test_pauli_hermitian))
	return suite
	
##############################################################################	
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)