##############################################################################
# Find the closest basic approximation in approxes to arbitrary unitary u
# Based on operator norm distance
def find_basic_approx(approxes, u, distance):
    min_dist = numpy.finfo(numpy.float32).max # set to max float value at first
    closest_approx = None
    found = False
    for approx in approxes:
        #print "approx= " + str(approx)
        #print "u= " + str(u)
        current_dist = distance(approx.matrix,u.matrix)
        #print "current_dist= " + str(current_dist)
        #print "min_dist= " + str(min_dist)
        if (current_dist < min_dist):
            found = True
            min_dist = current_dist
            closest_approx = approx
            
    if (not found):
        raise RuntimeError("No closest approximation found.")
    
    return (closest_approx, min_dist)
