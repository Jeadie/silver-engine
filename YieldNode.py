class YieldNode(object):

	def __init__(self, time, p, y): 
		self.prev_up = None
		self.prev_down = None
		self.next_up = None
		self.next_down = None
		self.time = time
		self.p = p
		self.y = y

	def __init__(self, time, p, y, prev_nodes, next_nodes): 
		__init__(self, time, p, y)
		if(length(prev_nodes) ==2): 
			self.prev_up = prev_nodes[0]
			self.prev_down = prev_nodes[1]
		if(length(next_nodes) ==2): 
			self.next_up = next_nodes[0]
			self.next_down = next_nodes[1]

	@property
	def p(self): 
		return self.p

	@p.setter
	def p(self, value): 
		if value >=0 & value <=1: 
			self.p = value
	

	def __str__(self): 
		return "YieldNode: time={0}, yield={1}.".format(self.time, self.y)

class ForwardYieldLattice(object): 
	
	def __init__(self, periods, p_up, y0, dy): 
		self.NodeLayers = [[] for i in range(periods)]
		self.duration = periods
		# Probability of yield going up at next time interval given time, yield and probability at being at given YieldNode
		self.p = lambda t, y, p: p_up
		# yield of upper node at next time for a given node with time, yield and probability of going up
		self.y_u = lambda t, y, p_up: y+dy
		# yield of upper node at next time for a given node with time, yield and probability of going up
		self.y_d = lambda t, y, p_down: y-dy
		self.y0 = y0
		self.init_nodes()

	def init_nodes(self): 
		#construct root node manually
		root_node = YieldNode(0, 1, self.y0)

		# for each layer create new nodes and link back to prior nodes
		for	layer, time in zip(self.NodeLayers[1:], range(1, self.durations)): 
			for i in range(2, time +1): 
				prev_node_down = self.get_node(time -1, i)
				prev_node_up =  self.get_node(time -1, i-1)
				node = None
				# configure all nodes but final node
				if prev_node_down is not None: 
					y = prev_node_down.y
					p = prev_node_down.p
					node = YieldNode(i, time, self.p(time-1, y, p), self.y_u(time-1, y, p), [prev_node_up, prev_node_down], [None, None])

				# if node is final node in layer
				else: 
					y = prev_node_up.y
					p = prev_node_up.p
					node = YieldNode(i, time, self.p(time-1,y,p), self.y_d(time-1, y, p), [prev_node_up, prev_node_down], [None, None])
				self.NodeLayers[time].append(node)

	def get_node(self, t, i): 
		"""
		t, int: discrete time period
		i, int: index into list of nodes (starting from 0, in decreasing order of yield i = 0 is greatest yield)
		return, YieldNode: Node at particular point in lattice or None if node does not exist
		"""

		# check if node exists at given time and index
		if(t < 0 | (i < 0 | i > t)): 
			return None
		return self.NodeLayers()[t][i]

	def __str__(self): 
		return "\n".join([str(i) for i in layer for layer in self.NodeLayers])

if '__name__' == '__main__': 
	a = ForwardYieldLattice(5, 0.5, 0.03, 0.01); 
	print(a)
