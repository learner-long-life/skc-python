from skc_basic_approx import *
from skc_operator import *
import math
import numpy
import cPickle
import time

from iset4 import *

#iset = [H1, H2, T1, T2, Tinv1, Tinv2]
iset = [H, T, T_inv]

f = open('basic_approxes.pickle', 'wb')

# Write the basic instruction set to a file
cPickle.dump(iset, f, cPickle.HIGHEST_PROTOCOL)

# Do it!
basic_approxes = []

begin_time = time.time()

# Collect all basic approxes for sequences of length 1 up to length l_0
for i in range(7):
	i_approxes = gen_basic_approx(iset, i+1)
	basic_approxes.extend(i_approxes)
	print "Number of basic approximations so far: " + str(len(basic_approxes))

gen_time = time.time() - begin_time
print "Generation time: " + str(gen_time)

print "Writing basic approximations to file: basic_approxes.pickle"

begin_time = time.time()

# Write the approximations
cPickle.dump(basic_approxes, f, cPickle.HIGHEST_PROTOCOL)

write_time = time.time() - begin_time
print "Writing time: " + str(write_time)

print "Writing done, closing file."

f.close()