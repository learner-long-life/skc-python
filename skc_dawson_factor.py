import math
import numpy
from skc_unitary_decompose import *
from skc_aram_factor import *
from skc_utils import *

##############################################################################
# This is plagiarized from Chris Dawson's su2.cpp: su2::mat_to_cart3
def matrix_to_unitary4d(matrix_U):

	print "matrix_to_unitary4d of " + str(matrix_U)
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
	return Unitary4D(ni=si, nx=sx, ny=sy, nz=sz)

##############################################################################
# The similarity matrix is the rotation to get from A to B?
def find_similarity_matrix(matrix_A, matrix_B):

	unitary_A = matrix_to_unitary4d(matrix_A)
	unitary_B = matrix_to_unitary4d(matrix_B)
	
	[axis_a, angle_a] = unitary_A.to_rotation()
	[axis_b, angle_b] = unitary_B.to_rotation()
	print "Rotation A: " + str(axis_a) + " " + str(angle_a)
	print "Rotation B: " + str(axis_b) + " " + str(angle_b)

	# angle_a and angle_b should be the same
	assert_approx_equals(angle_a, angle_b)

	vector_a = axis_a.to_array()
	vector_b = axis_b.to_array()
	
	norm_a = vector_norm(vector_a)
	norm_b = vector_norm(vector_b)
	
	# Rotation axes should be unit vectors
	assert_approx_equals(norm_a, 1)
	assert_approx_equals(norm_b, 1)

	# ab = a . b (vector dot product)
	ab_dot_product = numpy.dot(vector_a, vector_b)

	# s = b x a (vector cross product), perpendicular to both a & b
	vector_s = numpy.cross(vector_b, vector_a)
	print "vector_s = " + str(vector_s)

	# what is the interpretation of the cross product here? did we need to
	# normalize this? oops
	norm_s = vector_norm(vector_s)
	if (abs(norm_s) < TOLERANCE):
		# The vectors are parallel or anti parallel 
		# i am just pretending they are parallel so fix this.
		return I2.matrix;

	#angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	# Occasionally the lengths of these vectors will drift, so renormalize here
	angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	for i in range(len(vector_s)):
		vector_s[i] /= norm_s

	# compose angle and axis of rotation into a matrix
	axis_s = Cart3DCoords(vector_s[0], vector_s[1], vector_s[2])
	print "axis_s = " + str(axis_s)
	unitary_S = axis_s.to_unitary_rotation(angle_s)
	unitary_S.print_string()
	return unitary_S.to_matrix()

#############################################################################
def dawson_x_group_factor(matrix_U):
	unitary_U = matrix_to_unitary4d(matrix_U)
	unitary_U.print_string()
	
	print "angle_u= " + str(unitary_U.angle)
	
	# st = pow(0.5 - 0.5*sqrt(1 - a[1]*a[1]),0.25);
	# a[0] = cos(phi/2), from the I component above
	# st = sin(theta/2) = 4th root of (1/2 - 1/2 * cos(phi/2))
	ni = math.cos(unitary_U.angle/2)
	st = math.pow(0.5 - 0.5*ni, 0.25);
	# ct = cos(theta/2), from cos^2 + sin^2 = 1
	ct = math.sqrt(1-(st**2));
	# This converts to spherical coordinations, theta = pitch, alpha = yaw
	theta = 2*math.asin(st);
	alpha = math.atan(st);
	
	print "st= " + str(st)
	print "ct= " + str(ct)
	print "theta= " + str(theta)
	print "alpha= " + str(alpha)

	ax = st*math.cos(alpha); # x component
	bx = ax
	ay = st*math.sin(alpha); # y component
	by = ay
	az = ct; # z components
	bz = -az; # a and b have opposite z components
	
	vector_a = Cart3DCoords(ax, ay, az)
	vector_b = Cart3DCoords(bx, by, bz)
	print "vector_a= " + str(vector_a)
	print "vector_b= " + str(vector_b)
	
	matrix_A = vector_a.to_unitary_rotation(theta).to_matrix()
	matrix_B = vector_b.to_unitary_rotation(theta).to_matrix()
	
	op_A = Operator(name="A", matrix=matrix_A)
	op_B = Operator(name="B", matrix=matrix_B)
	op_B_dag = op_B.dagger()

	matrix_C = find_similarity_matrix(op_A.matrix,op_B_dag.matrix)

	return [matrix_B, matrix_C]

#############################################################################
def dawson_group_factor(matrix_U):
	# U is a rotation about some axis, find out by how much, then make
	# that a rotation about the X-axis.
	print "matrix_U= " + str(matrix_U)
	unitary_U = matrix_to_unitary4d(matrix_U)
	
	[axis_u, angle_u] = unitary_U.to_rotation()

	# do the same rotation about the x axis (n is an angle)
	unitary_XU = x_axis.to_unitary_rotation(angle_u)	
	matrix_XU = unitary_XU.to_matrix()
	
	print "matrix_XU= " + str(matrix_XU)

	# oh!! the similarity matrix is what S stands for!
	# and it is the rotation to get from U to XU
	matrix_S = find_similarity_matrix(matrix_U, matrix_XU);
	matrix_S_dag = numpy.conjugate(numpy.transpose(matrix_S))

	print "matrix_S= " + str(matrix_S)
	
	# now then wtf is this?! the real bgc-decompose
	[matrix_A, matrix_B] = dawson_x_group_factor(matrix_XU);
	
	print "matrix_A= " + str(matrix_A)
	print "matrix_B= " + str(matrix_B)

	V = matrix_S * matrix_A * matrix_S_dag	
	W = matrix_S * matrix_B * matrix_S_dag	
	
	return [ V,W ]
