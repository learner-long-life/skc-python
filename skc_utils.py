# Utilities for Solovay-Kitaev compiler

#from skc_operator import *
from skc_types import *

import math
import numpy
import random
import scipy.linalg

TOLERANCE = 1e-15
TOLERANCE2 = 1e-14
TOLERANCE3 = 1e-13

##############################################################################
def matrixify(array):
	return numpy.matrix(array, dtype=numpy.complex)
	
##############################################################################
# Given an axis and a rotation angle, return the associated rotation matrix
# axis - a vector of 3 elements indicating the x, y, and z components of axis
# angle - floating point number, rotation angle in radians
def compose(axis, angle):
	raise RuntimeError("Not implemented for SU(D) yet!")
	
def vector_norm(array):
	raise RuntimeError("Not implemented for SU(D) yet!")

##############################################################################
# The following functions (get_eigenvalues and trace_distance) are plagiarized from
# Chris Dawson's su2.cpp
# matrix_M is currently assumed to be a 2x2 matrix
def get_eigenvalues(M):
	raise RuntimeError("Not implemented for SU(D) yet!")
	
##############################################################################
def trace_norm(M):
	op_M = Operator(name="M", matrix=M)
	op_M_dag = op_M.dagger()
	ops_M_M_dag = op_M.multiply(op_M_dag)
	trace = numpy.trace(ops_M_M_dag.matrix)
	return math.sqrt(trace)
	
##############################################################################
def trace_distance(matrix_A, matrix_B):
	matrix_diff = matrix_A - matrix_B
	matrix_diff_dag = numpy.transpose(numpy.conjugate(matrix_diff))
	product = matrix_diff * matrix_diff_dag
	#print "prod= " + str(product)	
	trace_vals = scipy.linalg.eigvals(product);
	return scipy.linalg.norm(trace_vals)
	
##############################################################################
def fowler_distance(matrix_A, matrix_B):
	d = matrix_A.shape[0]
	assert(matrix_A.shape == matrix_B.shape)
	matrix_adjoint = numpy.transpose(numpy.conjugate(matrix_A))
	prod = matrix_adjoint * matrix_B
	trace = numpy.trace(prod)
	frac = (d - abs(trace)) / d
	return math.sqrt(frac)

##############################################################################
def assert_approx_equals_tolerance(value1, value2, tolerance):
	diff = abs(value1 - value2)
	if (diff >= tolerance):
		print "Diff: " + str(diff)
	assert(diff < tolerance)
	
##############################################################################
def assert_approx_equals(value1, value2):
	assert_approx_equals_tolerance(value1, value2, TOLERANCE2)
	
##############################################################################
def approx_equals(value1, value2):
	return (abs(value1 - value2) < TOLERANCE)

##############################################################################
# Convert a unitary rotation to hyperspherical coordinates
# \psi, \theta, \phi on surface of a 3-sphere
def unitary_to_hspherical(U):
	raise RuntimeError("Not implemented for SU(D) yet!")
	
##############################################################################
# This is plagiarized from Chris Dawson's su2.cpp: su2::mat_to_cart3
def matrix_to_unitary4d(matrix_U):

	#print "matrix_to_unitary4d of " + str(matrix_U)
	# The below are negative, and contain an extra factor of i, b/c of the
	# term -i sin(theta/2) (sx*X + sy*Y + sz*Z)
	sx = -1 * matrix_U[(0,1)].imag;
	# x component, imag(U(1,0)) should be identical
	assert_approx_equals(matrix_U[(0,1)].imag, matrix_U[(1,0)].imag)
	sy = matrix_U[(1,0)].real;
	# y component, real(U(0,1)) should be identical
	assert_approx_equals(matrix_U[(1,0)].real, -matrix_U[(0,1)].real)
	sz = (matrix_U[(1,1)].imag - matrix_U[(0,0)].imag)/2.0;
	# z component
	assert_approx_equals(matrix_U[(1,1)].imag, -matrix_U[(0,0)].imag)
	# identity component
	si = (matrix_U[(0,0)].real + matrix_U[(1,1)].real)/2.0;
	assert_approx_equals(matrix_U[(0,0)].real, matrix_U[(1,1)].real)
	theta = 2 * math.acos(si)
	sin_theta_half = math.sin(theta / 2)
	# I think the components into Unitary are supposed to still contain
	# sin(theta/2) factor, after all si does above
	#sx /= sin_theta_half
	#sy /= sin_theta_half
	#sz /= sin_theta_half
	#print "ni=" + str(si)
	#print "nx=" + str(sx)
	#print "ny=" + str(sy)
	#print "nz=" + str(sz)
	return Unitary4D(ni=si, nx=sx, ny=sy, nz=sz)

##############################################################################
# Indented printing based on depth
def print_indented(message, depth):
	print (" " * (depth * 2)) + message

# Chain the tensor product of multiple operators
def tensor_chain(op_vector):
	if (len(op_vector) == 0):
		raise RuntimeError("Cannot chain empty list of operators")
	product = None
	for op in op_vector:
		#print "op= " + str(op)
		#print "product= " + str(product)
		if (product == None):
			product = op
		else:
			product = numpy.kron(product, op)
	return product

##############################################################################
def vector_distance(vector_A, vector_B):
	vector_diff = vector_A - vector_B
	return scipy.linalg.norm(vector_diff)

##############################################################################	
def matrix_direct_sum(matrix_A, matrix_B):
  direct_sum = numpy.zeros( numpy.add(matrix_A.shape, matrix_B.shape) )
  direct_sum = matrixify(direct_sum)
  direct_sum[:matrix_A.shape[0],:matrix_A.shape[1]] = matrix_A
  direct_sum[matrix_A.shape[0]:,matrix_A.shape[1]:] = matrix_B
  return direct_sum
  
##############################################################################
def assert_matrices_approx_equal(matrix1, matrix2, distance):
	dist = distance(matrix1, matrix2)
	if (dist > TOLERANCE3):
		print "matrices not-equal"
		print str(matrix1)
		print str(matrix2)
	assert_approx_equals(dist, 0)
	
##############################################################################
def assert_matrix_hermitian(matrix):
	adjoint = numpy.transpose(numpy.conjugate(matrix))
	assert_matrices_approx_equal(matrix, adjoint, trace_distance)
	
##############################################################################
def assert_matrix_unitary(matrix):
	d = matrix.shape[0]
	identity = matrixify(numpy.eye(d))
	adjoint = numpy.transpose(numpy.conjugate(matrix))
	product = matrix * adjoint	
	assert_matrices_approx_equal(product, identity, trace_distance)

##############################################################################
def assert_matrix_nonempty(matrix):	
	abs_trace = numpy.abs(numpy.trace(matrix*matrix.H))
	if (abs_trace < TOLERANCE3):
		print "abs_trace= " + str(abs_trace)
		print "Matrix is empty \n" + str(matrix)
	assert(abs_trace > TOLERANCE3)
	
##############################################################################
def matrix_exp_diag(matrix):
	d = matrix.shape[0]
	matrix_exp = matrixify(numpy.eye(d))
	for i in range(d):
		matrix_exp[(i,i)] = numpy.exp(matrix[(i,i)])
	return matrix_exp
	
##############################################################################
# Taylor series approximation
def matrix_exp(matrix, steps):
	d = matrix.shape[0]
	identity = matrixify(numpy.eye(d))
	sum = identity
	product = identity
	denom = 1
	for i in range(steps):
		product = product * matrix
		denom = denom * (i+1)
		#print "prod/denom= " + str(product / denom)
		sum = sum + (product / denom)
		#print "sum= " + str(product / denom)
	return sum