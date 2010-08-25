from skc.basic_approx.file import *
from skc.decompose import *
from skc.kdtree import *

def components_to_kdpoint(components, basis, angle):
	point = basis.sort_canonical_order(components)
	point.append(angle) # add the angle as the last component
	return point

def unitary_to_kdpoint(matrix_U):
	(components, K, matrix_H) = unitary_to_axis(matrix_U, basis)
	return components_to_kdpoint(components, basis, K)
	
def build_kdtree(filename_prefix, filename_upper, filename_suffix, basis):
	filenames = []
	for i in range(1,filename_upper):
		filenames.append(filename_prefix+str(i)+filename_suffix)
	
	# This is the data that we load from a file
	sequences = []
	for filename in filenames:
		new_sequences = read_from_file(filename)
		sequences.extend(new_sequences)
	
	data = []
	# Process this to produce the format the kdtree expects, namely a list of components in each dimension
	for operator in sequences:
		#print "op= " + str(operator)
		#print "matrix= " + str(operator.matrix)
		#operator.dimensions = unitary_to_kdpoint(operator.matrix)
		#print "dimensions= " + str(operator.dimensions)
		# Now dimensions is in R^{d^2}
		data.append(operator)
		
	
	# Build it! Kablooey
	tree = KDTree.construct_from_data(data)
	return tree

##############################################################################
# Find the closest basic approximation in approxes to arbitrary unitary u
# Based on operator norm distance
def find_basic_approx(approxes, u, distance):
    min_dist = numpy.finfo(numpy.float32).max # set to max float value at first
    closest_approx = None
    found = False
    for approx in approxes:
        #print "approx= " + str(approx)
        #print "u= " + str(u)
        current_dist = distance(approx.matrix,u.matrix)
        #print "current_dist= " + str(current_dist)
        #print "min_dist= " + str(min_dist)
        if (current_dist < min_dist):
            found = True
            min_dist = current_dist
            closest_approx = approx
            
    if (not found):
        raise RuntimeError("No closest approximation found.")
    
    return (closest_approx, min_dist)
