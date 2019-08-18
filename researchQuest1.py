
from collections import defaultdict 

file = open('wiki-topcats-reduced.txt')

'''
Function that returns all the nodes that compose the "reduced graph" without
duplicates (a set).
'''
def get_set_of_nodes():
	file = open('wiki-topcats-reduced.txt')
	l = []
	s = []
	for line in file:
		p = line.split()
		l.append(int(p[0]))
		s.append(int(p[1]))
	l = set(l).union(set(s))
	nod = set(l)
	return nod

'''
Function that returns the number of nodes of the "reduced graph"
'''
def get_nodes():
	a = len(get_set_of_nodes())
	print('The total number of nodes is {}'.format(a))
	return a

'''
Function that returns a dictionary {node : [nodes]}.
This dictionary rapresents all the connected edges of the "reduced graph"
'''
def get_edges_dict():
	file = open('wiki-topcats-reduced.txt')
	d = defaultdict(list)
	for line in file:
		(key, val) = line.split()
		d[int(key)].append(val)
	d = dict(d)
	return d

'''
Function that returns a dictionary in the form {node : degree} that 
will be used to compute the average degreee of the graph. The degree
is calculated by simply taking the lenght of the list of nodes that
reach the node itself.
'''
def get_degree_nodes(dictionary_to_get):
	# @param: dictionary_to_get, dict = {node : [list_of_nodes]}
	d2 = {}
	for key,value in dictionary_to_get.items():
		d2[key] = len(value)
	return(d2)

'''
Function that returns the total number of edges of the "reduced graph".
'''
def get_edges():
	file = open('wiki-topcats-reduced.txt')
	ed = []
	for line in file:
		ed.append(line.strip())
	edges = len(ed)
	print('The total number of edges is {}'.format(edges))
	return edges
	
'''
Function used to compute the average degree for a directed graph
'''
def avg_deg(e, n):
	av = int(round(((e * 2)) / n, 0))
	print('The average degree of the graph in {}'.format(av))

'''
Function that returns the maximal number of nodes of a directed graph
and the density value of a directed graph to check whether the
two values are far or not between each other
'''
def check_density(e, n):
	max_nodes = n * (n-1)
	density = float((e)/((n) * (n-1)))

	print('The maximum number of edge is {}'.format(max_nodes) + ', the density value is {}'.format(density))

