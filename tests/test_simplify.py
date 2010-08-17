from skc_simplify import *

import math
import unittest

##############################################################################
class TestSimplifyEngine(unittest.TestCase):

	def setUp(self):
		rules = [AdjointRule(), DoubleIdentityRule('I')]
		self.engine = SimplifyEngine(rules)
		
	def test_min_arg_count(self):
		self.assertEquals(self.engine.min_arg_count, 2)

	def test_simplest(self):
		# This should simplify to I
		sequence = ['I', 'I']
		(global_obtains, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['I'])
		self.assertEqual(global_obtains, True)

	def test_repeated_identity(self):
		# This should simplify to I
		sequence = ['I', 'I', 'I', 'I', 'I']
		(global_obtains, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['I'])
		self.assertEqual(global_obtains, True)

	def test_none_obtains(self):
		# This should simplify to I
		sequence = ['X', 'I', 'Y', 'I', 'Z']
		(global_obtains, new_sequence) = self.engine.simplify(sequence)
		self.assertEqual(new_sequence, ['X', 'I', 'Y', 'I', 'Z'])
		self.assertEqual(global_obtains, False)

##############################################################################
class TestDoubleIdentityRule(unittest.TestCase):

	def setUp(self):
		self.rule = DoubleIdentityRule('I')

	def test_simplest(self):
		# This should simplify to I
		sequence = ['I', 'I']
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])

	def test_simplest_not(self):
		# This should simplify to I
		sequence = ['X', 'Z']
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['X', 'Z'])

##############################################################################
class TestAdjointRule(unittest.TestCase):

	def setUp(self):
		self.rule = AdjointRule()

	# Test that adjoint rule obtains for simplest case
	def test_simplest(self):
		# This should simplify to I
		sequence = ['Q', 'Qd']
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])

	def test_simplest_reverse(self):
		# This should also simplify to I
		sequence = ['Qd', 'Q']
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])
		
	def test_different_prefixes(self):
		sequence = ['X', 'Zd']
		# This should not simplify
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['X', 'Zd'])

	def test_equal_length(self):
		# This should not simplify
		sequence = ['Ydd', 'Xdd']
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, False)
		self.assertEqual(sequence, ['Ydd', 'Xdd'])

	def test_repeated_d(self):
		sequence = ['Qddd', 'Qdd']
		# This should simplify to I
		obtains = self.rule.simplify(sequence)
		self.assertEqual(obtains, True)
		self.assertEqual(sequence, ['I'])
		
##############################################################################		
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestAdjointRule)
	suite2 = loader.loadTestsFromTestCase(TestDoubleIdentityRule)
	suite3 = loader.loadTestsFromTestCase(TestSimplifyEngine)
	suite.addTest(suite1)
	suite.addTest(suite2)
	suite.addTest(suite3)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
