import math
import numpy

from skc.utils import *

##############################################################################
# Recover an angle given the cosine and sine values, taken e.g. from a
# complex value.
# This is tricky because acos usually goes from [0,pi] while
# asin usually goes from [-pi/2,+pi/2], whereas angles in general go from
# [0,2pi]. Using the signs of the cosine and sine value, we can figure out
# the correct original angle
def recover_angle(cos_phi, sin_phi):
	# Recover two versions of the angle from the cosine and sine
	phi_acos = math.acos(cos_phi)
	phi_asin = math.asin(sin_phi)
	
	sign_cos = numpy.sign(cos_phi)
	sign_sin = numpy.sign(sin_phi)
	
	# phi \in [0, pi/2]
	if ((sign_cos > 0) and (sign_sin > 0)):
		assert_approx_equals(phi_acos, phi_asin)
		assert(phi_acos > 0)
		assert(phi_acos < PI_HALF)
		return phi_acos
	# phi \in [pi/2, pi]
	elif ((sign_cos < 0) and (sign_sin > 0)):
		# sine is symmetric about pi/2
		# phi_asin will be in [0,pi/2], so reflect it into [pi/2,pi]
		phi_asin = PI - phi_asin
		assert_approx_equals(phi_acos, phi_asin)
		assert(phi_acos > PI_HALF)
		assert(phi_acos < PI)
		return phi_acos
	# phi \in [pi,3pi/2]
	elif ((sign_cos < 0) and (sign_sin < 0)):
		# cosine is symmetric about pi
		# phi_acos will be in [pi/2,pi], so reflect it into [pi,3pi/2]
		phi_acos = TWO_PI - phi_acos
		# phi_asin will be in [-pi/2,0], so reflect it into [pi,3pi/2]
		phi_asin = PI - phi_asin
		assert_approx_equals(phi_acos, phi_asin)
		assert(phi_acos > PI)
		assert(phi_acos < THREE_PI_HALF)
		return phi_acos
	# phi \in [3pi/2,2pi]
	elif ((sign_cos > 0) and (sign_sin < 0)):
		# phi_acos will be in [0,pi/2], so reflect it into [3pi/2,2pi]
		phi_acos = TWO_PI - phi_acos
		# phi_asin will be in [-pi/2,0] so shift it into [3pi/2,2pi]
		phi_asin = phi_asin + TWO_PI
		assert_approx_equals(phi_acos, phi_asin)
		assert(phi_acos > THREE_PI_HALF)
		assert(phi_acos < TWO_PI)
		return phi_acos
	else:
		# We shouldn't even be here, Mr. Frodo
		assert(false)