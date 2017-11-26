# -*- coding: utf-8 -*-

__author__ = "Marcos Rangel"

import argparse

class Graph(object):

    def __init__(self, graph_dict=None,maxPath=0):
        """ initializes a graph object 
            If no dictionary or None is given, an empty dictionary will be used
        """
        self.maxPath = maxPath
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict


    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_all_paths(self, start_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.__graph_dict 
        path = path + [start_vertex]
        if len(path) == self.maxPath:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, path)
                for p in extended_paths: 
                    paths.append(p)
        return paths

def getNeighbors(line,col,sizeMatrix):
	""" return all neighbors from a point"""
	neighbors = []
	if line-1>=0:
		neighbors.append((line-1,col))
	if col+1<sizeMatrix:
		neighbors.append((line,col+1))
	if line+1<sizeMatrix:
		neighbors.append((line+1,col))
	if col-1>=0:
		neighbors.append((line,col-1))
	return neighbors
	
def buildMatrixInGraph(sizeMatrix):
	"""Build a Graph based in matrix's length """
	graph = {}

	for line in range(0,sizeMatrix):
		for col in range(0,sizeMatrix):
			graph[(line,col)] = getNeighbors(line,col,sizeMatrix)

	return graph

def calculatePaths(inputMatrix,paths):
	"""Return in dict all paths that keys are your value in matrix"""

	dictPaths = {}

	for path in paths:
		value = 0
		for vertice in path:
			line, col = vertice
			value = value + inputMatrix[line][col]
		if value not in dictPaths.keys():
			dictPaths[value] = []
		dictPaths[value] = dictPaths[value] + [path]

	return dictPaths

def intersection(prev,actual):
	"""Verify if exists any intersection between snakes' candidates"""
	arrayIntersection = set(prev).intersection(actual)

	if len(arrayIntersection)>0:
		return True
	return False

def findSnakes(sizePaths):
	"""After grouped keys, it's verify all snakes' candidadates""" 

	snakes = []
	for key in sizePaths.keys():
			if len(sizePaths[key])>1:
				for prevIndex in range(0,len(sizePaths[key])-1):
					for actualIndex in range(prevIndex+1,len(sizePaths[key])):
						lose = intersection(sizePaths[key][prevIndex],sizePaths[key][actualIndex])
						if not lose:
							snakes.append(sizePaths[key][prevIndex])
							snakes.append(sizePaths[key][actualIndex])
							return (key, snakes)
	return snakes

def readMatrixfromFile(file):
	"""Read Matrix inside csv file """
	pointer = open(file,"r")
	matrix = []
	for line in pointer.readlines():
		matrix = matrix + [[ int(''.join(c for c in number if c in '0123456789')) for number in line.split(';') ]]
	pointer.close()
	return matrix

def main():

	matrixFile = ''

	lengthSnake = ''

	parser = argparse.ArgumentParser(description='This is a Snake Search Script')
	parser.add_argument('-i','--inputMatrix', help='Input a matrix file (csv)',required=True)
	parser.add_argument('-l','--lengthSnake',help='Input a length of snake to search', required=True)
	args = parser.parse_args()
 
	inputMatrix = readMatrixfromFile(args.inputMatrix)

	lengthSnake = int(args.lengthSnake)

	sizeMatrix = len(inputMatrix)

	adjGraph = buildMatrixInGraph(sizeMatrix)

	graph = Graph(adjGraph,lengthSnake)

	paths = []

	for line in range(0,sizeMatrix):
		for col in range(0,sizeMatrix):
			paths = paths + graph.find_all_paths((line,col))

	sizePaths = {}

	if (len(paths)):

		sizePaths = calculatePaths(inputMatrix,paths)

		resultSnakes = findSnakes(sizePaths)

		if len(resultSnakes)>0:
			print 'You Win !!!!'
			val , snakes = resultSnakes
			print 'Value', val
			print 'Snakes', snakes
		else:
			print 'FAIL'
	else:			
		print 'FAIL'

if __name__ == '__main__':
	main()




