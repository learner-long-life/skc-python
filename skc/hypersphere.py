from skc.decompose import *

##############################################################################
# Convert hyperspherical coordinates in a certain basis to a unitary
def hspherical_to_unitary(hsphere_coords, basis):
	(components, K, matrix_H) = unitary_to_axis(matrix_U, basis)
	angle = K/2.0
	
	print "angle= " + str(angle)
	ni = numpy.trace(matrix_U * basis.identity.matrix) / basis.d
	print "ni= " + str(ni)
	
	cartesian_coords = basis.sort_canonical_order(components)
	
	for i in range(len(cartesian_coords)):
		cartesian_coords[i] *= math.sin(angle)
	
	# For SU(d), we require (d^2) - 1 hyperspherical coordinates
	d21 = (basis.d**2) - 1
	
	# Initialize hsphere_coords to contain initial angle
	hsphere_coords = [angle]
	print "hsphere_coords[0]= " + str(hsphere_coords[0])
	
	for i in range(1,d21):
		# If the current hsphere coord is zero, then all other
		# hsphere coords degenerate to zero, and we're done
		if (approx_equals(hsphere_coords[i-1], 0)):
			print "hsphere_coords["+str(i)+"] is zero, all others degenerate"
			for j in range(i,d21):
				hsphere_coords.append(0)
			break
		
		# Otherwise, proceed with taking succesive sines and cosines
		
		# Take sin of previous hsphere coord
		sin_i1 = math.sin(hsphere_coords[i-1])
		# Find product of all previous sines of hsphere coords
		product = 1
		for j in range(0,i):
			print "sin(hsphere_coords["+str(j)+"])= " + \
				str(math.sin(hsphere_coords[j]))
			product *= math.sin(hsphere_coords[j])
		print "product of sines from 0 to " + str(i) + "= " + str(product)
		print "cartesian_coord["+str(i)+"]= " + str(cartesian_coords[i-1])
		print "ratio= " + str(cartesian_coords[i-1] / product)
		angle_i = math.acos(cartesian_coords[i-1] / product)
		print "hsphere_coord[" + str(i) + "]= " + str(angle_i)
		hsphere_coords.append(angle_i)
		
		# If this is the next to last hsphere_coord, take the last sine
		if (i == (d21-1)):
			hsphere_coords[d21-1] = math.asin(cartesian_coords[d21-1] / product)
	return hsphere_coords

##############################################################################
# Convert a unitary rotation to hyperspherical coordinates
def unitary_to_hspherical(matrix_U, basis):
	(components, K, matrix_H) = unitary_to_axis(matrix_U, basis)
	angle = K/2.0
	
	print "angle= " + str(angle)
	ni = numpy.trace(matrix_U * basis.identity.matrix) / basis.d
	print "ni= " + str(ni)
	
	cartesian_coords = basis.sort_canonical_order(components)
	
	for i in range(len(cartesian_coords)):
		cartesian_coords[i] *= math.sin(angle)
	
	# For SU(d), we require (d^2) - 1 hyperspherical coordinates
	d21 = (basis.d**2) - 1
	
	# Initialize hsphere_coords to contain initial angle
	hsphere_coords = [angle]
	print "hsphere_coords[0]= " + str(hsphere_coords[0])
	
	for i in range(1,d21):
		# If the current hsphere coord is zero, then all other
		# hsphere coords degenerate to zero, and we're done
		if (approx_equals(hsphere_coords[i-1], 0)):
			print "hsphere_coords["+str(i)+"] is zero, all others degenerate"
			for j in range(i,d21):
				hsphere_coords.append(0)
			break
		
		# Otherwise, proceed with taking succesive sines and cosines
		
		# Take sin of previous hsphere coord
		sin_i1 = math.sin(hsphere_coords[i-1])
		# Find product of all previous sines of hsphere coords
		product = 1
		for j in range(0,i):
			print "sin(hsphere_coords["+str(j)+"])= " + \
				str(math.sin(hsphere_coords[j]))
			product *= math.sin(hsphere_coords[j])
		print "product of sines from 0 to " + str(i) + "= " + str(product)
		print "cartesian_coord["+str(i)+"]= " + str(cartesian_coords[i-1])
		print "ratio= " + str(cartesian_coords[i-1] / product)
		angle_i = math.acos(cartesian_coords[i-1] / product)
		print "hsphere_coord[" + str(i) + "]= " + str(angle_i)
		hsphere_coords.append(angle_i)
		
		# If this is the next to last hsphere_coord, take the last sine
		if (i == (d21-1)):
			hsphere_coords[d21-1] = math.asin(cartesian_coords[d21-1] / product)
	return hsphere_coords
