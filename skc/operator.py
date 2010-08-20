# Operator/gate, including annotation and ancestry
# The most basic kind of operator is a basic instruction from a universal gate set

import numpy;
import math;
import scipy.linalg;

from skc.utils import *

class Operator:

	def __init__(self, name, matrix, ancestors=[]):
		self.name = name
		self.matrix = matrix
		if (len(ancestors) == 0):
			ancestors = [name]
		self.ancestors = ancestors
		
	def __str__(self):
		return "Operator: " + str(self.name) + "\n" \
			"  Ancestors: " + str(self.ancestors)
			
	def __hash__(self):
		hash = self.name.__hash__()
		for ancestor in self.ancestors:
			hash *= ancestor.__hash__()
		return hash
			
	def print_matrix(self):
			print "  Matrix: " + str(self.matrix)
			
	def add_ancestors(self, other, new_name=""):
		# Append new ancestors to the end of self
		new_ancestors = self.ancestors + other.ancestors
		new_op = Operator(new_name, None, new_ancestors)
		return new_op
		
	def ancestors_as_string(self):
		return list_as_string(self.ancestors)

	def multiply(self, other, new_name=""):
		new_matrix = self.matrix * other.matrix
		new_ancestors = self.ancestors + other.ancestors
		new_op = Operator(new_name, new_matrix, new_ancestors)
		return new_op
		
	def dagger(self):
		new_matrix = self.matrix.H
		reversed_ancestors = list(self.ancestors)
		reversed_ancestors.reverse()
		new_ancestors = []
		for ancestor in reversed_ancestors:
			new_ancestors.append(ancestor+"d")
		new_name = self.name + "d"
		return Operator(new_name, new_matrix, new_ancestors)
		
	def scale(self, scalar, new_name=""):
		new_matrix = self.matrix * scalar
		new_ancestors = self.ancestors + [scalar]
		return Operator(new_name, new_matrix, new_ancestors)
		
	def __eq__(self, other):
		return (self.name == other.name) and (self.ancestors == other.ancestors)

def get_identity(d):
	return Operator("I", matrixify(numpy.eye(d)))

##############################################################################
# SU(2) constants
# 2x2 identity matrix
I2 = get_identity(2)

# Pauli X matrix
SX_matrix = matrixify([[0, 1], [1, 0]])
SX = Operator("SX", SX_matrix)

# Pauli Y matrix
SY_matrix = matrixify([[0, -1j], [1j, 0]])
SY = Operator("SY", SY_matrix)

# Pauli Z matrix
SZ_matrix = matrixify([[1, 0], [0, -1]])
SZ = Operator("SZ", SZ_matrix)

# Hadamard gate
H_matrix = (1/math.sqrt(2)) * matrixify([[1, 1], [1, -1]])
H = Operator("H", H_matrix)

# pi/8 gate
T_matrix = matrixify([[1, 0], [0, numpy.exp(1j * math.pi / 4)]])
T = Operator("T", T_matrix)

# Inverse pi/8 gate
T_inv = Operator("T_inv", T.matrix.I)
