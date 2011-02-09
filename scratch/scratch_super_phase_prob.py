# Scratch test to generate probabilities from a random eigenvalue

from random import random
from skc.trig import recover_angle
import math

# Set the value of n here, the resolution for performing phase simulation
# phi = k / 2^n
n = 8

n_exp = 2**n;

# Get a random k within the range 0 to 2^n
k = int(random()*n_exp)

print "k= " + str(k)

phi_k = (k * 1.0) / n_exp

print "phi_k= " + str(phi_k)

cos_k = math.cos(2*math.pi*phi_k)
sin_k = math.sin(2*math.pi*phi_k)

print "cos_k= " + str(cos_k)
print "sin_k= " + str(sin_k)

# Divide the uniform distribution over [0,1] into intervals to
# return non-uniform distributions
cos_partition = (1 - cos_k)/2.0
sin_partition = (1 + sin_k)/2.0

print "cos_partition= " + str(cos_partition)
print "sin_partition= " + str(sin_partition)

# Number of Bernoulli trials to recover a value of cos(phi_k) or sin(phi_k)
s = 1000000;

# Initialize counting ones for both the cosine and sine series
cos_count = 0
sin_count = 0

for i in range(s):
	# get a random number from uniform distrib over [0,1] and convert
	r = random()
	if (r < cos_partition):
		cos_count += 1
	if (r < sin_partition):
		sin_count += 1

print "cos_count= " + str(cos_count)
print "sin_count= " + str(sin_count)

cos_prob = (cos_count * 1.0) / s
sin_prob = (sin_count * 1.0) / s

print "cos_prob= " + str(cos_prob)
print "sin_prob= " + str(sin_prob)

cos_phi_k_2 = 1-(cos_prob*2)
sin_phi_k_2 = (sin_prob*2) - 1

print "cos_phi_k_2= " + str(cos_phi_k_2)
print "sin_phi_k_2= " + str(sin_phi_k_2)

# Recover phi_k from the outcomes of the Bernoulli trials, treating the count
# of ones as an approximation of the probability
phi_k_cos_2 = math.acos(cos_phi_k_2) / (2*math.pi)
phi_k_sin_2 = math.asin(sin_phi_k_2) / (2*math.pi)

print "phi_k_cos_2= " + str(phi_k_cos_2)
print "phi_k_sin_2= " + str(phi_k_sin_2)

k_cos_2 = round(phi_k_cos_2 * n_exp)
k_sin_2 = round(phi_k_sin_2 * n_exp)

print "k_cos_2= " + str(k_cos_2)
print "k_sin_2= " + str(k_sin_2)

two_pi_phi_k_2 = recover_angle(cos_phi=cos_phi_k_2, sin_phi=sin_phi_k_2,
	tolerance=1e-2)

phi_k_2 = two_pi_phi_k_2 / (2*math.pi)

print "phi_k_2= " + str(phi_k_2)

k_2 = round(phi_k_2 * n_exp)

print "k_2= " + str(k_2)