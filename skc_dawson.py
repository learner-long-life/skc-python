# Solovay-Kitaev compiler using Dawson's group factor

from skc_dawson_factor import *
from skc_basic_approx import *
from skc_operator import *
from skc_utils import *

import cPickle
import time

##############################################################################
# Global variables
the_basis = None
# Not currently used with aram_diagonal_factor method
the_axis = None
the_factor_method = None
basic_approxes = None

##############################################################################
def load_basic_approxes(filename):
	global basic_approxes
	f = open(filename, 'rb')
	
	begin_time = time.time()
	
	iset = cPickle.load(f)
	
	iset_time = time.time() - begin_time
	print "Loaded instruction set in: " + str(iset_time)
	print "Iset = " + str(iset)
	
	begin_time = time.time()
	
	basic_approxes = cPickle.load(f)
	#basic_approxes = [I2]
	
	approx_time = time.time() - begin_time
	
	print "Loaded basic approximations in: " + str(approx_time)
	print "Number of BA: " + str(len(basic_approxes))

##############################################################################
# Dawson's code uses trace distance (although the paper uses operator norm)
def distance(matrix_U1,matrix_U2):
	return trace_distance(matrix_U1, matrix_U2)

##############################################################################
def set_axis(axis):
	global the_axis
	the_axis = axis
	print "the_axis= " + str(the_axis)

##############################################################################
# Not currently used with aram_diagonal_factor method
def set_basis(basis):
	global the_basis
	the_basis = basis
	print "the_basis= " + str(the_basis)

##############################################################################
def set_factor_method(factor_method):
	global the_factor_method
	the_factor_method = factor_method
	print "the_factor_method= " + str(the_factor_method.__name__)

##############################################################################
def solovay_kitaev(U, n, id, ancestry):
	print "*******************************************************************"
	print str(id)+"_"+str(n)
	print ancestry
	print "-------------------------------------------------------------------"
	
	if (n == 0):
		basic_approx, min_dist = find_basic_approx(basic_approxes, U, distance)
		# discard min_dist for now. but just you wait...
		print "Returning basic approx: " + str(basic_approx)
		return basic_approx
	else:
		print "Beginning level " + str(n)
		U_n1 = solovay_kitaev(U, n-1, 'U', ancestry+id) # U_{n-1}
		print "U_"+str(n-1)+": " + str(U_n1)
		U_n1_dagger = U_n1.dagger()
		U_U_n1_dagger = U.multiply(U_n1_dagger).matrix
		V_matrix,W_matrix = the_factor_method(U_U_n1_dagger, the_basis)
		print "V: " + str(V_matrix)
		print "W: " + str(W_matrix)
		V = Operator(name="V", matrix=V_matrix)
		W = Operator(name="W", matrix=W_matrix)
		V_n1 = solovay_kitaev(V, n-1, 'V', ancestry+id) # V_{n-1}
		print "V_"+str(n-1)+": " + str(V_n1)
		V_n1_dagger = V_n1.dagger()
		W_n1 = solovay_kitaev(W, n-1, 'W', ancestry+id) # W_{n-1}
		print "W_"+str(n-1)+": " + str(W_n1)
		W_n1_dagger = W_n1.dagger()
		V_n1_dagger_W_n1_dagger = V_n1_dagger.multiply(W_n1_dagger)
		V_n1_W_n1 = V_n1.multiply(W_n1)
		delta = V_n1_W_n1.multiply(V_n1_dagger_W_n1_dagger)
		U_n = delta.multiply(U_n1)
		print "delta_"+str(n)+": " + str(U_n)
		print "Ending level " + str(n)
		return U_n
