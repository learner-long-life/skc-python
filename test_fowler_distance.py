from skc_operator import *

import math

dist = fowler_distance(H.matrix, H.matrix)
print "dist(H,H)= " + str(dist)

H2 = numpy.exp(1.0j*math.pi / 2) * H.matrix

dist = fowler_distance(H2, H.matrix)
print "dist(H,H2)= " + str(dist)