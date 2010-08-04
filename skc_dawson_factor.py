import math
import numpy
from skc_utils import *
#from skc_compose import *
from skc_decompose import *

##############################################################################
# The similarity matrix is the rotation to get from A to B?
def find_similarity_matrix(matrix_A, matrix_B, basis):

	(components_A, scale_A, hermitian_A) = unitary_to_axis(matrix_A, basis)
	(components_B, scale_B, hermitian_B) = unitary_to_axis(matrix_B, basis)
	
	angle_a = scale_A / 2.0
	angle_b = scale_B / 2.0

	# angle_a and angle_b should be the same
	assert_approx_equals(angle_a, angle_b)

	vector_a = basis.sort_canonical_order(components_A)
	vector_b = basis.sort_canonical_order(components_B)
	
	norm_a = scipy.linalg.norm(vector_a)
	norm_b = scipy.linalg.norm(vector_b)
	
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
	norm_s = scipy.linalg.norm(vector_s)
	if (abs(norm_s) < TOLERANCE):
		# The vectors are parallel or anti parallel 
		# i am just pretending they are parallel so fix this.
		return basis.identity.matrix;

	#angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	# Occasionally the lengths of these vectors will drift, so renormalize here
	angle_s = math.acos(ab_dot_product / (norm_a * norm_b))
	
	assert((angle_s > -PI_HALF) and (angle_s < PI_HALF))
	for i in range(len(vector_s)):
		vector_s[i] /= norm_s

	# compose angle and axis of rotation into a matrix
	components_S = basis.unsort_canonical_order(vector_s)
	print "components_S = " + str(components_S)
	matrix_U = axis_to_unitary(components_S, angle_s/2.0, basis)
	print "matrix_U= " + str(matrix_U)

	return matrix_U

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
