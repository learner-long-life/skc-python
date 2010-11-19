from skc.utils import *
from skc.trig import *

import math
import unittest
import random

class TestTrig(unittest.TestCase):

	# Test case 1 for recovering angle between 0 and pi/2
	def test_recover_angle_1(self):
		angle = (random.random() * PI_HALF)
		cos_phi = math.cos(angle)
		sin_phi = math.sin(angle)
		angle2 = recover_angle(cos_phi, sin_phi)
		assert_approx_equals(angle, angle2)

	# Test case 2 for recovering angle between pi/2 and pi
	def test_recover_angle_2(self):
		angle = (random.random() * PI_HALF) + PI_HALF
		cos_phi = math.cos(angle)
		sin_phi = math.sin(angle)
		angle2 = recover_angle(cos_phi, sin_phi)
		assert_approx_equals(angle, angle2)

	# Test case 3 for recovering angle between pi and 3pi/2
	def test_recover_angle_3(self):
		angle = (random.random() * PI_HALF) + PI
		cos_phi = math.cos(angle)
		sin_phi = math.sin(angle)
		angle2 = recover_angle(cos_phi, sin_phi)
		assert_approx_equals(angle, angle2)

	# Test case 4 for recovering angle between 3pi/2 and 2pi
	def test_recover_angle_4(self):
		angle = (random.random() * PI_HALF) + THREE_PI_HALF
		cos_phi = math.cos(angle)
		sin_phi = math.sin(angle)
		angle2 = recover_angle(cos_phi, sin_phi)
		assert_approx_equals(angle, angle2)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestTrig)
	suite.addTest(suite1)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
