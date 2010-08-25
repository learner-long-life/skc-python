#############################################################################
# 4-tuple representing unitary rotation as components of Identity and
# R_x, R_y, R_z rotation matrices
class Unitary4D:

	def __init__(self, ni, nx, ny, nz):
		self.ni = ni
		self.nx = nx
		self.ny = ny
		self.nz = nz
		norm = self.norm()
		if (abs(norm - 1) > TOLERANCE):
			raise RuntimeError("Matrix is not normalized: " + str(norm))
		x_sqr = self.nx ** 2
		y_sqr = self.ny ** 2
		z_sqr = self.nz ** 2
		self.w = math.sqrt(x_sqr + y_sqr + z_sqr)
		self.angle = 2 * math.atan2(self.w, self.ni)
		self.cos_theta_half = math.cos(self.angle/2)
		self.sin_theta_half = math.sin(self.angle/2)

		if (abs(self.cos_theta_half - self.ni) > TOLERANCE):
			raise RuntimeError("Identity component ["+str(self.ni)+"] "\
				"not consistent with cos_theta_half ["+str(cos_theta_half)+"]")

	
	# Return tuple of axis of rotation and angle
	def to_rotation(self):
		vx = self.nx / self.sin_theta_half
		vy = self.ny / self.sin_theta_half
		vz = self.nz / self.sin_theta_half
		axis = Cart3DCoords(vx, vy, vz)
		return [axis, self.angle]
		
	def to_matrix(self):
		# ni already contains cos(theta/2) factor, i guess we could just use that instead
		Im = I2.matrix *self.cos_theta_half
		#print "Im = " + str(Im)
		# nx, ny, nz already contain sin(theta/2) factor
		Xm = -1j * SX.matrix * self.nx
		#print "Xm = " + str(Xm)
		Ym = -1j * SY.matrix * self.ny
		#print "Ym = " + str(Ym)
		Zm = -1j * SZ.matrix * self.nz
		#print "Zm = " + str(Zm)
		return Im + Xm + Ym + Zm
		
	def norm(self):
		isqr = self.ni**2
		xsqr = self.nx**2
		ysqr = self.ny**2
		zsqr = self.nz**2
		return math.sqrt(isqr + xsqr + ysqr + zsqr)
		
	def print_string(self):
		print "["
		print "  I = " + str(self.ni)
		print "  X = " + str(self.nx)
		print "  Y = " + str(self.ny)
		print "  Z = " + str(self.nz)
		print "]"
		print "Angle (radians) = " + str(self.angle)

##############################################################################
# This is plagiarized from Chris Dawson's su2.cpp: su2::mat_to_cart3
def matrix_to_unitary4d(matrix_U):

	#print "matrix_to_unitary4d of " + str(matrix_U)
	# The below are negative, and contain an extra factor of i, b/c of the
	# term -i sin(theta/2) (sx*X + sy*Y + sz*Z)
	sx = -1 * matrix_U[(0,1)].imag;
	# x component, imag(U(1,0)) should be identical
	assert_approx_equals(matrix_U[(0,1)].imag, matrix_U[(1,0)].imag)
	sy = matrix_U[(1,0)].real;
	# y component, real(U(0,1)) should be identical
	assert_approx_equals(matrix_U[(1,0)].real, -matrix_U[(0,1)].real)
	sz = (matrix_U[(1,1)].imag - matrix_U[(0,0)].imag)/2.0;
	# z component
	assert_approx_equals(matrix_U[(1,1)].imag, -matrix_U[(0,0)].imag)
	# identity component
	si = (matrix_U[(0,0)].real + matrix_U[(1,1)].real)/2.0;
	assert_approx_equals(matrix_U[(0,0)].real, matrix_U[(1,1)].real)
	theta = 2 * math.acos(si)
	sin_theta_half = math.sin(theta / 2)
	# I think the components into Unitary are supposed to still contain
	# sin(theta/2) factor, after all si does above
	#sx /= sin_theta_half
	#sy /= sin_theta_half
	#sz /= sin_theta_half
	#print "ni=" + str(si)
	#print "nx=" + str(sx)
	#print "ny=" + str(sy)
	#print "nz=" + str(sz)
	return Unitary4D(ni=si, nx=sx, ny=sy, nz=sz)

# Convert a unitary rotation to hyperspherical coordinates
# \psi, \theta, \phi on surface of a 3-sphere
def unitary_to_hspherical(U):
	#U.print_string()
	psi = math.acos(U.ni)
	#print "psi= " + str(psi)
	if (approx_equals(psi, 0)):
		# Check for division by zero
		# If psi is zero, then we degenerate to a 3-sphere pole, theta and phi don't matter
		theta = 0
		phi = 0
	else:
		sin_psi = math.sin(psi)
		theta = math.acos(U.nz / sin_psi)
		#print "theta= " + str(theta)
		if (approx_equals(theta, 0)):
			# Check again for division by zero
			# If theta is zero, then we degenerate to a 2-sphere pole, phi doesn't matter
			phi = 0
		else:
			sin_theta = math.sin(theta)
			cos_theta = math.cos(theta)
			phi = math.asin(U.ny / (sin_psi * sin_theta))
			phi2 = math.acos(U.nx / (sin_psi * sin_theta))
			#print "phi= " + str(phi)
			#print "phi2= " + str(phi2)
			# For some reason the tolerance on this is pretty terrible
			assert_approx_equals_tolerance(phi, phi2, TOLERANCE3)
	#print "phi= " + str(phi)
	return [psi, theta, phi]
