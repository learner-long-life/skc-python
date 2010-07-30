import math

#from skc_operator import *
from skc_utils import *

#############################################################################
# Tuple representing unitary operator as vectors in the basis of
# Generalized Pauli dxd matrices
class UnitaryD:

	# n_vector - a dictionary of vector components keyed by basis index (j,k)
	# basis - a dictionary of basis matrices, keyed by same index (j,k)
	def __init__(self, n_vector, basis):
		self.n_vector = n_vector
		self.basis = basis
		norm = scipy.linalg.norm(self.n_vector)
		assert_approx_equals(norm, 1)
		if (abs(norm - 1) > TOLERANCE):
			raise RuntimeError("Matrix is not normalized: " + str(norm))
	
	# Return tuple of axis of rotation and angle
	def to_rotation(self):
		raise RuntimeError("Not yet implemented for SU(d)!")
		
	def to_matrix(self):
		raise RuntimeError("Not yet implemented for SU(d)!")
		
	def print_string(self):
		string = ""
		for key, value in self.n_vector.items():
			string += str(key) + "=" + str(value) + ","
		return "[" + string + "]"
		
##############################################################################
# Cartesian coordinates in R^d
class CartDCoords:

	def __init__(self, coords):
		self.norm = scipy.linalg.norm(self.coords)
		if (abs(norm - 1) > TOLERANCE):
			raise RuntimeError("Cart3D coords not normalized: " + str(norm))
		self.coords = coords
				
	def normalize(self):
		for i in range(len(self.coords)):
			self.coords[i] /= self.norm
		
	# To generalized (d-1)-spherical coordinates
	def to_spherical_coords(self):
		raise RuntimeError("Not yet implemented for SU(d)!")
		
	def to_array(self):
		return self.coords
		
	def to_unitary_rotation(self, rotation_angle):
		raise RuntimeError("Not yet implemented for SU(d)!")
		
	def __str__(self):
		string = "";
		for coord in self.coords:
			string += coord + ","
		return "[" + string + "]"
	
##############################################################################
# Spherical coordinates on surface of unit (d-1)-sphere
class SphericalDCoords:

	def __init__(self, theta, alpha):
		raise RuntimeError("Not yet implemented for SU(d)!")
		
	def to_cart3d_coords(self):
		raise RuntimeError("Not yet implemented for SU(d)!")
