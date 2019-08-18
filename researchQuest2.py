import researchQuest1 as rq1
import statistics as st
import operator as op
import heapq as heap
from collections import defaultdict
from tqdm import tqdm, trange

'''
Nullary funtion that returns a dictionary {category : list_of_nodes} 
'''
def get_categories_dict():
	categories = {}
	file = open('wiki-topcats-categories.txt')
	for line in file:
		element = line.split()
		categories[element[0][9:-1]] = list(map(int,element[1:]))
	return categories


'''
Nullary function that returns a dictionary which contains the categories
that have more than 3500 nodes. We obtained only the nodes that are present
in the reduced graph.
'''
def get_only_big_categories():
	categ = get_categories_dict()
	nod = rq1.get_set_of_nodes()
	yy = []
	for key, val in categ.items():
		if len(val) < 3500:
			yy.append(key)
	for y in yy:
		categ.pop(y, None)
	r = {}
	for key, val in categ.items():
		r[key] = set(val).intersection(nod)
	return r


'''
Function that is used to display the cardinality of each category.
'''
def print_cardinality(dictio):
	# @param dictio, dict = {category : list_of_nodes}
	for k in sorted(dictio, key=lambda k: len(dictio[k]), reverse=True):
		print(k, ": ", str(len(dictio[k])))

'''
Given a node index 'source', this algorithm (Dijkstra) finds
for every other node the length of the shortest path to that
node. Distance for each node is stored in the array 'distances'.
The heapq library is used to save the paths. This data structure is
very efficient for our purpose and most of all for our big amount of data.
'''
infinity = 10000
def Dijkstra(graph, source, target):
	# @param: graph, list of lists
	# @param: source, set of int
	# @param: target, set of int
     
    if source in target:
    	return 0

    distances = [infinity] * len(graph)
    distances[source] = 0

    queue = [(0, source)]
    heap.heapify(queue)

    while len(queue) != 0:
        node = heap.heappop(queue)[1]
        
        dist = distances[node]

        for neighbor in graph[node]:
            if neighbor in target:
                return dist + 1

            if dist + 1 < distances[neighbor]:
                distances[neighbor] = dist + 1
                heap.heappush(queue, (distances[neighbor], neighbor))

    return infinity


'''
This function creates the full graph. The graph is rapresented as a list of lists.
Each index of the list rapresents a node and the inner lists are all the nodes reached
by the 'index-node'
'''
def load_graph(filename = 'wiki-topcats-reduced.txt'):
	edges = []
	max_index = -1
	with open(filename) as file:
		for line in file:
			edge = line.strip().split('\t')
			a = int(edge[0])
			b = int(edge[1])
			max_index = max(max_index, a)
			max_index = max(max_index, b)
			edges.append((a, b))
	
	graph = [[] for i in range(max_index + 1)]

	for edge in edges:
		graph[edge[0]].append(edge[1])

	return graph


'''
Function that computes all the shortest paths (with Dijkstra's algorithm) 
from the nodes of one category to another and then computes the median of 
all these paths. The information is stored in a dictionary {'category' : median_value}
'''
def get_medians_shortest_paths(graph, my_category, categories):
  # @param my_category, set(int)
  # @param categories, dict = {str: set(int)}
  total_distances = defaultdict(list)
  
  for source in tqdm(my_category):
    for name, other_category in categories.items():
        total_distances[name].append(Dijkstra(graph, source, other_category))

  result = {}
  for name, other_category in categories.items():
    if len(total_distances[name]) == 0:
      result[name] = -1
    else:
      result[name] = st.median(total_distances[name])

  return result


'''
Function that sorts the category rank by the value of the median of the shortest paths
from C0. 
'''
def rank_it(dictionary_rank):
	# @param dictionary_rank, dict = {'category' : median_value}
	sorted_x = sorted(rank_list.items(), key=op.itemgetter(1), reverse=False)
	return sorted_x


'''
Function that sorts the list of nodes by their indgree value.
'''
def sort_nodes(list_of_tuples):
    list_of_tuples.sort(key=op.itemgetter(1), reverse=True)
    return list_of_tuples


'''
Function that returns a sorted list of tuples that rapresents the rank of the nodes.
As inputs we have to give two categories since we want to rank the nodes based on the indegree of
the edges coming from the previous ranked category and the category itself.
'''
def rank_nodes(graph, category_a, category_b):
	# @param: graph, list of lists that rapresents the full graph
	# @param: category_a, list of int
	# @param: category_b, list of int
    in_degrees = [0] * len(graph)
    for a in category_a:
        for b in graph[a]:
            in_degrees[b] += 1
    result = []
    for n in category_b:
        result.append((n, in_degrees[n]))
    return sort_nodes(result)


'''
This function actually computes the full rank of all the nodes of our graph. Given
the block rank (where we rank the categories by the median of the shortest paths), the full graph
and the dictionary of the categories it gives the rank as a list of tuples (node, indegree value).
'''
def compute_rank_nodes(ranklist, graph, dictionary):
	# @param: ranklist, list of tuple [(category_name, median_of_shortest_path)]
	# @param: graph, list of lists that rapresents the full graph
	# @param: dictionary, 
    l = []
    for e in trange(0, len(ranklist)-1):
        if e == 0:
            first_category = []
            for i in dictionary[ranklist[e][0]]:
                first_category.append(i)
            r = rank_nodes(graph, first_category, first_category)
            l.append(ranklist[e][0])
            l = l + r
        first_category = []
        second_category = []
        for i in dictionary[ranklist[e][0]]:
            first_category.append(i)
        for j in dictionary[ranklist[e+1][0]]:
            second_category.append(j)
        l.append(ranklist[e+1][0])
        l += rank_nodes(graph, first_category, second_category)
    return l


'''
Nullary function that returns a dictionary {node : name of article}
'''
def get_dictionary_article_names():
    names = {}
    filename = "wiki-topcats-page-names.txt"
    with open(filename) as file:
        for line in file:
            element = line.strip().split(" ", 1)
            if len(element) != 2:
                continue
            names[int(element[0])] = element[1]
    return names


'''
Function that takes as input the dictionary that maps the article's name to each node and
the full list of ranked nodes (@nr). As result it prints the top-three-ranked article for each
category.
'''
def get_top_three_of_each_category(dictionames, nr):
	# @param dictionames, dict = {node:name of the article}
	# @param nr, list of tuples = [(node, indegee)]
    for el in range(0, len(nr)):
        if isinstance(nr[el], str):
            print(nr[el].replace('_', ' ').replace('-', ' ') + ": ")
            print("1st ranked article: ", get_article_name(dictionames, nr[el+1][0]))
            print("2nd ranked article: ", get_article_name(dictionames, nr[el+2][0]))
            print("3rd ranked article: ", get_article_name(dictionames, nr[el+3][0]))
            print()


'''
Function that 'reads' the dictionary which contains the names of the articles so that,
given the number of the node (@articode), returns the string that rapresents the real 
name of the Wikipedia article.
'''
def get_article_name(dictionames, arti_code):
	# @param dictionames, dict = {node : name_of_article}
	# @param arti_code, int = node 
	return dictionames[arti_code]


