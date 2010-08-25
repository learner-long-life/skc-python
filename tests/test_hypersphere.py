from skc.basis import *
from skc.decompose import *
from skc.hypersphere import *

import math
import unittest

##############################################################################
# Tests 1.5xround-tripping, axis_to_unitary to unitary_to_hspherical to
# hspherical_to_unitary
def test_hsphere_coords_axis(angle, axis, basis):
	matrix_U = axis_to_unitary(axis, angle/2.0, basis)
	#print "U=" + str(matrix_U)
	hsphere_coords = unitary_to_hspherical(matrix_U, basis)
	
	#print str(hsphere_coords)
	
	matrix_U2 = hspherical_to_unitary(hsphere_coords, basis)
	#print "U2=" + str(matrix_U2)
	
	assert_matrices_approx_equal(matrix_U, matrix_U2, trace_distance)

def create_hsphere_test_case(basis, axis, angle):
	##############################################################################
	# Class for testing matrix logarithms for various SU(d)
	class TestHSphereCoords(unittest.TestCase):
		
		def setUp(self):
			self.basis = basis
			self.axis = axis
			self.angle = angle
	
		#---------------------------------------------------------------------
		def test_hsphere_coords_roundtrip(self):
		
			(matrix_U, components, angle) = get_random_unitary(self.basis)
			
			axis = self.basis.sort_canonical_order(components)
			#print "axis= " + str(axis)
			#print "U=" + str(matrix_U)
			hsphere_coords = unitary_to_hspherical(matrix_U, self.basis)
			
			#print str(hsphere_coords)
			
			matrix_U2 = hspherical_to_unitary(hsphere_coords, self.basis)
			#print "U2=" + str(matrix_U2)
			
			assert_matrices_approx_equal(matrix_U, matrix_U2, trace_distance)
		
		#---------------------------------------------------------------------
		# Force negative angle to test that edge case
		def test_hsphere_coords_random_negative(self):
		
			(matrix_U, components, angle) = \
				get_random_unitary(self.basis, angle_lower = -PI_HALF, angle_upper = 0)
			axis = self.basis.sort_canonical_order(components)
			#print "axis= " + str(axis)
			#print "U=" + str(matrix_U)
			hsphere_coords = unitary_to_hspherical(matrix_U, self.basis)
			
			#print str(hsphere_coords)
			
			matrix_U2 = hspherical_to_unitary(hsphere_coords, self.basis)
			#print "U2=" + str(matrix_U2)
			
			assert_matrices_approx_equal(matrix_U, matrix_U2, trace_distance)
		
		#---------------------------------------------------------------------
		# Test round-tripping of cartesian to hspherical coords and back
		# about a random axis and fixed angle
		def test_hsphere_coords_random_axis(self):
			theta = math.pi / 12
		
			axis = pick_random_axis(self.basis)
			test_hsphere_coords_axis(theta, axis, self.basis)
			
		#---------------------------------------------------------------------
		# Test round-tripping of cartesian to hspherical coords and back
		# about both a fixed axis and fixed angle
		def test_hsphere_coords_axis(self):
			test_hsphere_coords_axis(self.angle, self.axis, self.basis)
			
	TestHSphereCoords.__name__ += "SU" + str(basis.d) 
	
	return TestHSphereCoords

H2 = get_hermitian_basis(d=2)
axis2 = cart3d_to_h2(x=1, y=1, z=1)
angle = math.pi/12
su2_tests = create_hsphere_test_case(H2, axis2, angle)

H4 = get_hermitian_basis(d=4)
axis4 = pick_random_axis(H4)
su4_tests = create_hsphere_test_case(H4, axis4, angle)

H8 = get_hermitian_basis(d=8)
axis8 = pick_random_axis(H8)
su8_tests = create_hsphere_test_case(H8, axis8, angle)

#test_hsphere_coords_axis(angle=math.pi/12, axis=axis2, basis=H2)
#test_hsphere_coords_random_axis(basis=H2)
#test_hsphere_coords_random(basis=H2)
#test_hsphere_coords_random_negative(basis=H2)
#test_hsphere_coords_roundtrip(basis=H2)
#test_hsphere_coords_random_axis(basis=H4)
#test_hsphere_coords_random(basis=H4)

##############################################################################
# Class for testing matrix logarithms for various SU(d)
class TestHSphereLastCoord(unittest.TestCase):

	# Degenerate case where phi_1 = phi_2 = 0, then phi_3 should = 0 too
	def test_fix_last_hsphere_coord_degen_1(self):
		c_n1 = 0
		c_n = c_n1
		product = 0
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals(phi_n1, 0)

	def test_fix_last_hsphere_coord_case_1(self):
		c_n1 = math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals_tolerance(phi_n1, 0.785398163397, 1e-12)

	# These hard-coded examples are taken from an SU(2) rotation of math.pi / 12
	# about an axis(1,1,1) normalized
	# This should return a phi_ni in the range [0, PI_HALF]
	def test_fix_last_hsphere_coord_case_1(self):
		c_n1 = math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals_tolerance(phi_n1, 0.785398163397, 1e-12)

	# This should return a phi_ni in the range [PI_HALF, PI]
	# by just flipping the sign of the phi_1 
	def test_fix_last_hsphere_coord_case_2(self):
		c_n1 = -math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = -c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		correct_phi_n1 = 0.785398163397 + PI_HALF
		#correct_phi_n1 = THREE_PI_HALF - 0.785398163397
		assert_approx_equals_tolerance(phi_n1, correct_phi_n1, 1e-12)

	# This should return a phi_ni in the range [PI, THREE_PI_HALF]
	# by just flipping the sign of the phi_1 
	def test_fix_last_hsphere_coord_case_3(self):
		c_n1 = math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = c_n1
		phi_1 = -math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		assert_approx_equals_tolerance(phi_n1, 0.785398163397 + PI, 1e-12)

	# This should return a phi_ni in the range [THREE_PI_HALF, TWO_PI]
	# by just flipping the sign of the phi_1 
	def test_fix_last_hsphere_coord_case_4(self):
		c_n1 = -math.sin(math.pi/24)*(1.0/math.sqrt(3))
		c_n = -c_n1
		phi_1 = math.pi / 24
		phi_2 = math.acos(c_n / math.sin(phi_1))
		product = -math.sin(phi_1) * math.sin(phi_2)
		phi_n1 = fix_last_hsphere_coord(product=product, c_n=c_n, c_n1=c_n1)
		#correct_phi_n1 = 0.785398163397 + PI
		correct_phi_n1 = TWO_PI - 0.785398163397
		assert_approx_equals_tolerance(phi_n1, correct_phi_n1, 1e-12)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestHSphereLastCoord)
	suite.addTest(suite1)

	suite2 = loader.loadTestsFromTestCase(su2_tests)
	suite.addTest(suite2)
	suite3 = loader.loadTestsFromTestCase(su4_tests)
	suite.addTest(suite3)
	suite4 = loader.loadTestsFromTestCase(su8_tests)
	suite.addTest(suite4)
	return suite

if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)