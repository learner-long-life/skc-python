from skc_operator import *

import math
import unittest

class TestOperator(unittest.TestCase):

	# Test that hash value implies equality
	def test_hash(self):
		hash1 = I2.__hash__()
		hash2 = H.__hash__()
		hash3 = T.__hash__()
		msg = "hash(I2)= " + str(hash1) + " hash(H)= " + str(hash2)
		self.assertNotEquals(hash1, hash2, msg)
		msg = "hash(H)= " + str(hash2) + " hash(T)= " + str(hash3)
		self.assertNotEquals(hash2, hash3, msg)
		msg = "hash(I2)= " + str(hash1) + " hash(T)= " + str(hash3)
		self.assertNotEquals(hash1, hash3, msg)

##############################################################################
def get_suite():
	suite = unittest.TestSuite()
	loader = unittest.TestLoader()
	suite1 = loader.loadTestsFromTestCase(TestOperator)
	suite.addTest(suite1)
	return suite

##############################################################################
if (__name__ == '__main__'):
	suite = get_suite()
	unittest.TextTestRunner(verbosity=3).run(suite)
