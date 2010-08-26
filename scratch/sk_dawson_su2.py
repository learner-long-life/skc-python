from skc.operator import *
from skc.dawson.factor import *
from skc.dawson import *
from skc.compose import *
from skc.basis import *
import math

H2 = get_hermitian_basis(d=2)
theta = math.pi / 4 # 45 degrees
axis = cart3d_to_h2(x=1, y=1, z=1)

# Compose a unitary to compile
matrix_U = axis_to_unitary(axis, theta, H2)
op_U = Operator(name="U", matrix=matrix_U)

n = 2
print "U= " + str(matrix_U)
print "n= " + str(n)

# Prepare the compiler
sk_set_factor_method(dawson_group_factor)
sk_set_basis(H2)
sk_set_axis(X_AXIS)
sk_build_tree("su2", 15)

Un = solovay_kitaev(op_U, n)
print "Approximated U: " + str(Un)

print "Un= " + str(Un.matrix)

print "trace_dist(U,Un)= " + str(trace_distance(Un.matrix, op_U.matrix))
print "fowler_dist(U,Un)= " + str(fowler_distance(Un.matrix, op_U.matrix))
