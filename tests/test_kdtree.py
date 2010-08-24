from skc.kdtree import *

data = <load data> # iterable of points (which are also iterable, same length)
point = <the point of which neighbours we're looking for>

tree = KDTree.construct_from_data(data)
nearest = tree.query(point, t=4) # find nearest 4 points
