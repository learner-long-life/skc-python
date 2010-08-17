from skc_simplify import *

import math
import unittest

##############################################################################
class TestAdjointRule(unittest.TestCase):

	def setUp(self):
		self.rule = AdjointRule()

	# Test that adjoint rule obtains for simplest case
	def test_simplest(self):
		# This should simplify to I
		(obtains, C) = self.rule.simplify(['Q', 'Qd'])
		self.assertEqual(obtains, True)
		self.assertEqual(C, 'I')

	def test_simplest_reverse(self):
		# This should also simplify to I
		(obtains, C) = self.rule.simplify(['Qd', 'Q'])
		self.assertEqual(obtains, True)
		self.assertEqual(C, 'I')
		
	def test_different_prefixes(self):
		# This should not simplify
		(obtains, C) = self.rule.simplify(['X', 'Zd'])
		self.assertEqual(obtains, False)

	def test_equal_length(self):
		# This should not simplify
		(obtains, C) = self.rule.simplify(['Ydd', 'Xdd'])
		self.assertEqual(obtains, False)

	def test_repeated_d(self):
		# This should simplify to I
		(obtains, C) = self.rule.simplify(['Qddd', 'Qdd'])
		self.assertEqual(obtains, True)
		self.assertEqual(C, 'I')
		
##############################################################################		
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestAdjointRule)
	suite.addTest(suite1)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
