from skc_utils import *

##############################################################################
def get_group_commutator(matrix_V, matrix_W):
	return matrix_V * matrix_W * matrix_V.H * matrix_W.H

##############################################################################
def conjugate(matrix_A, matrix_B):
	return matrix_B * matrix_A * matrix_B.H

##############################################################################
def create_diagonal_submatrices(matrix_D, d):
	# Divide up matrix_D into 2x2 SU(2) unitaries, U_i
	submatrices_D = []
	for i in range(d/2):
		i2 = i*2
		i21 = (2*i)+1
		a11 = matrix_D[(i2,i2)]
		a12 = 0.0 #matrix_D[(i,i+1)]
		a21 = 0.0 #matrix_D[(i+1,i)]
		a22 = matrix_D[(i21,i21)]
		submatrix_D = matrixify([[a11,a12],[a21,a22]])
		print "D_"+str(i)+ "= " + str(submatrix_D)
		submatrices_D.append(submatrix_D)
		assert_matrix_unitary(submatrix_D)
	return submatrices_D

##############################################################################
def reconstruct_diagonal_matrix(submatrices, d):
	matrix_D = matrixify(numpy.eye(d))
	
	for i in range(d/2):
		i2 = i*2
		i21 = (2*i)+1
		submatrix_D = submatrices[i]
		#print "U_"+str(i)+ "= " + str(submatrix_U)
		matrix_D[(i2,i2)] = submatrix_D[(0,0)]
		matrix_D[(i21,i21)] = submatrix_D[(1,1)]
		
	return matrix_D