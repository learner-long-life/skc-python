# Methods for decomposing unitaries

from skc_diagonalize import *
from skc_compose import *

##############################################################################
# Given a Hermitian matrix H which is the logarithm of the unitary U
# and a basis, return the different components of H in that basis
# Also return the global constant factor K
def get_basis_components(matrix_H, basis):
	d = basis.d

	# Create a dictionary with the same keys as basis_dict
	component_dict = {}	
	
	# Iterate over basis elements to pick out components in H
	# Don't include the identity element here, we will recalculate it
	# higher up
	for key,gate in basis.items_minus_identity():
		kc_alpha = numpy.trace(matrix_H * gate.matrix)
		component_dict[key] = kc_alpha
		print str(key) + "=> " + str(kc_alpha)
		# Components should be real, with negligible imaginary parts
		#assert_approx_equals(kc_alpha.imag, 0)
	
	# Extract the identity component as a special case.
	# Maybe there's a better way to do this?
	#id_component = numpy.trace(matrix_H).real / d
	#component_dict[basis.identity_key] = id_component
	# Normalization factor
	#scale = 1 / sum
	
	# Check that we really have the norm of the component vector
	norm = scipy.linalg.norm(component_dict.values())
	print "norm= " + str(norm)
	
	sign = None

	for key,value in component_dict.items():
		if (sign == None):
			if (value > 0):
				sign = +1
			elif (value < 0):
				sign = -1
		else:
			if (value > 0):
				assert(sign != -1)
				#print "assert sign != -1"
			elif (value < 0):
				assert(sign != +1)
				#print "assert sign != +1"
		component_dict[key] = value / norm
		
	# Fix sign of components so that they are all positive
	for k,v in component_dict.items():
		component_dict[k] = numpy.abs(v)
		assert(component_dict[k] >= 0)

	# Check that we really normalized the values
	assert_approx_equals(scipy.linalg.norm(component_dict.values()), 1)
	
	# Verify that we can compose the matrix again from these components
	M = matrix_from_components(component_dict, basis)
	dist = fowler_distance(M, matrix_H)
	if (dist > TOLERANCE3):
		print "dist= " + str(dist)
		print "M= " + str(M)
	#assert_approx_equals(dist, 0)
	
	# Fix the scale factor to have the right sign
	K = sign*norm
	print "sign= " + str(sign)

	return (component_dict, K)

##########################################################################
def unitary_to_axis(matrix_U, basis):
	(matrix_V, matrix_W) = diagonalize(matrix_U, basis)
	
	print "V= " + str(matrix_V)
	print "W= " + str(matrix_W)
	
	matrix_ln = get_matrix_logarithm(matrix_W)
	
	print "matrix_ln= " + str(matrix_ln)
	
	# Reconjugate to transform into iH
	matrix_iH = matrix_V * matrix_ln * matrix_V.I
	
	# Factor out -i (since we used -i in exp_hermitian_to_unitary)
	matrix_H = (-1.0/1j) * matrix_iH
	
	print "matrix_H= " + str(matrix_H)
	trace_norm = numpy.trace(matrix_H * matrix_H.H)
	print "trace_norm(H)= " + str(trace_norm)
	
	# Compare the calculated components with our original
	(components2, K) = get_basis_components(matrix_H, basis)
	angle = K/2.0
	# Scale matrix by our calculated angle
	matrix_H = matrix_H / angle
	return (components2, K, matrix_H)