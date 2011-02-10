from skc.utils import *
import math

c_approx = 4*math.sqrt(2)
eps_0 = 1.0 / 64

print "c_approx= " + str(c_approx)
print "eps_0= " + str(eps_0)

for i in range(1,100):
	eps = 1.0 / (2**i)
	n =n_from_eps(eps, eps_0, c_approx)
	print "n= " + str(n)
	print "eps= " + str(eps)

