import unittest

import test_recompose
import test_find_basis

loader = unittest.TestLoader()

suite = unittest.TestSuite()
suite.addTest(test_recompose.get_suite())
suite.addTest(test_find_basis.get_suite())
unittest.TextTestRunner(verbosity=2).run(suite)