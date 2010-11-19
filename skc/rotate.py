# Module for single-qubit rotations

from skc.utils import *

import numpy
import math

# Create the SU(2) matrix for rotating about the x-axis by theta radians
def rotate_X(theta):
	a = math.cos(theta/2.0)
	b = -1j*math.sin(theta/2.0)
	c = -1j*math.sin(theta/2.0)
	d = math.cos(theta/2.0)
	return matrixify([[a,b],[c,d]])
	
# Create the SU(2) matrix for rotating about the y-axis by theta radians
def rotate_Y(theta):
	a = math.cos(theta/2.0)
	b = -math.sin(theta/2.0)
	c = math.sin(theta/2.0)
	d = math.cos(theta/2.0)
	return matrixify([[a,b],[c,d]])

# Create the SU(2) matrix for rotating about the z-axis by theta radians
def rotate_Z(theta):
	a = math.cos(theta/2.0) - 1j*math.sin(theta/2.0)
	b = 0
	c = 0
	d = math.cos(theta/2.0) + 1j*math.sin(theta/2.0)
	return matrixify([[a,b],[c,d]])