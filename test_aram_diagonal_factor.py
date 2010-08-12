from skc_diagonalize import *
from skc_basis import *
from skc_compose import *
from skc_dawson_factor import *
from skc_group_factor import *

import numpy

d=4
H4 = get_hermitian_basis(d=d)
H2 = get_hermitian_basis(d=2)
X_AXIS = cart3d_to_h2(x=1, y=0, z=0)


(matrix_U, components, angle) = get_random_unitary(H4)
print "matrix_U= " + str(matrix_U)

# Get the SU(d) unitary matrix_U in diagonal form (matrix_D)
(matrix_P, matrix_D) = diagonalize(matrix_U, H4)

print "matrix_D= " + str(matrix_D)

range_d2 = range(d/2)

submatrices_U = create_diagonal_submatrices(matrix_U, d)

# Reconstruct the matrices from scratch just so we can round-trip this.
matrix_U2 = reconstruct_diagonal_matrix(submatrices_U, d)
#matrixify(numpy.eye(d))
	
trace_dist = trace_distance(matrix_D, matrix_U2)
assert_approx_equals(trace_dist, 0)

# Find balanced group commutator for each submatrix
submatrices_V = []
submatrices_W = []

for submatrix_U in submatrices_U:
	print "U_i= " + str(submatrix_U)
	(submatrix_V, submatrix_W) = dawson_group_factor(submatrix_U, H2, X_AXIS)
	print "V_i= " + str(submatrix_V)
	print "W_i= " + str(submatrix_W)
	delta = get_group_commutator(submatrix_V, submatrix_W)
	print "delta= " + str(delta)
	dist = trace_distance(submatrix_U, delta)
	print "dist(U_i, delta)= " + str(dist)
	assert_approx_equals_tolerance(dist, 0, 1)
	#assert_matrices_approx_equal(submatrix_U, delta, trace_distance)
	# Write an assert_group_factor method here from skc_group_factor
	submatrices_V.append(submatrix_V)
	submatrices_W.append(submatrix_W)
	
# Construct the big group commutator from the subcommutators
matrix_V = reconstruct_diagonal_matrix(submatrices_V, d)
matrix_W = reconstruct_diagonal_matrix(submatrices_V, d)

# Verify that we can multiply it all back again
matrix_U3 = get_group_commutator(matrix_V, matrix_W)
trace_dist = trace_distance(matrix_D, matrix_U3)
print "dist(D,U3)= " + str(trace_dist)
#assert_approx_equals(trace_dist, 0)

matrix_U4 = conjugate(matrix_U3, matrix_P)
trace_dist = trace_distance(matrix_U, matrix_U4)
print "dist(U,U4)= " + str(trace_dist)