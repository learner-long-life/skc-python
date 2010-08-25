from skc.kdtree import *
from skc.basic_approx.file import *
from skc.compose import *
from skc.decompose import *
from skc.basis import *

import math

# Really, we should save the basis to a file with the instruction set, maybe
basis = get_hermitian_basis(d=2)

filenames = []
for i in range(1,15):
	filenames.append("pickles/su2/gen-g"+str(i)+"-1.pickle")

# This is the data that we load from a file
sequences = []
for filename in filenames:
	new_sequences = read_from_file(filename)
	sequences.extend(new_sequences)

def components_to_kdpoint(components, basis, angle):
	point = basis.sort_canonical_order(components)
	point.append(angle) # add the angle as the last component
	return point

def unitary_to_kdpoint(matrix_U):
	(components, K, matrix_H) = unitary_to_axis(matrix_U, basis)
	return components_to_kdpoint(components, basis, K/2.0)

data = []
# Process this to produce the format the kdtree expects, namely a list of components in each dimension
for operator in sequences:
	#print "op= " + str(operator)
	#print "matrix= " + str(operator.matrix)
	#operator.dimensions = unitary_to_kdpoint(operator.matrix)
	#print "dimensions= " + str(operator.dimensions)
	# Now dimensions is in R^{d^2}
	data.append(operator)
	

# This is the random matrix that we are looking for
(search_U, components, angle) = get_random_unitary(basis)
search_op = Operator(name="Search", matrix=search_U)
# Re-center angles from 0 to 2pi, instead of -pi to pi
if (angle < 0):
	angle += 2*math.pi
search_op.dimensions = components_to_kdpoint(components, basis, angle)
print "search.dimensions= " + str(search_op.dimensions)

# Build it! Kablooey
tree = KDTree.construct_from_data(data)
nearest = tree.query(search_op, t=2) # find nearest 4 points

for op in nearest:
	print "op= " + str(op)
	print "op.dims= " + str(op.dimensions)
	print "fowler_dist(op,U)= " + str(fowler_distance(op.matrix, search_U))
	print "trace_dist(op,U)= " + str(trace_distance(op.matrix, search_U))
