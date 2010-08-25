from skc.kdtree import *
from skc.basic_approx.file import *
from skc.compose import *
from skc.decompose import *
from skc.basis import *
from skc.basic_approx.search import *

import math

# Really, we should save the basis to a file with the instruction set, maybe
basis = get_hermitian_basis(d=2)

tree = build_kdtree("pickles/su2/gen-g", 16, "-1.pickle", basis)

# This is the random matrix that we are looking for
(search_U, components, angle) = get_random_unitary(basis)
search_op = Operator(name="Search", matrix=search_U)
angle *= 2.0
# Re-center angles from 0 to 2pi, instead of -pi to pi
if (angle < 0):
	for (k,v) in components.items():
		components[k] = v * -1
	angle *= -1
search_op.dimensions = components_to_kdpoint(components, basis, angle)
print "search.dimensions= " + str(search_op.dimensions)

nearest = tree.query(search_op, t=2) # find nearest 4 points

for op in nearest:
	print "op= " + str(op)
	print "op.dims= " + str(op.dimensions)
	print "fowler_dist(op,U)= " + str(fowler_distance(op.matrix, search_U))
	print "trace_dist(op,U)= " + str(trace_distance(op.matrix, search_U))
