# Scratch file to test Kitaev's decomposition of an arbitrary unitary into
# two 180 degree rotations (see Figure S8.2b in his book)

from skc.operator import *
from skc.utils import *

import numpy
import scipy.linalg

pi8_matrix = matrixify([[1, 0], [0, numpy.exp(numpy.pi*(1.0j/8.0))]])

pi8_op = Operator("pi8", pi8_matrix)
pi8d_op = pi8_op.dagger()

A_matrix = tensor_chain([pi8_op.matrix, I2.matrix])
C_matrix = tensor_chain([pi8d_op.matrix, pi8_op.matrix])

A_op = Operator("A", A_matrix)
C_op = Operator("C", C_matrix)

print "A_op= " + str(A_op.matrix)
print "C_op= " + str(C_op.matrix)

CNot12_matrix = matrixify([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
CNot12 = Operator(name="CNOT12", matrix=CNot12_matrix)

D_op = A_op.multiply(CNot12)
E_op = D_op.multiply(C_op)
F_op = E_op.multiply(CNot12)

print "D_op= " + str(D_op.matrix)
print "E_op= " + str(E_op.matrix)
print "F_op= " + str(F_op.matrix)