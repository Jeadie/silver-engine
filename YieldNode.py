import math

class YieldNode(object):

    def __init__(self, time, p, y, prev_nodes = None, next_nodes = None):
        """

        :param time: Discrete time value for node from root
        :param p: Decimal probability of shifting to upper next node.
        :param y: Forward Yield rate at time increment
        :param prev_nodes: tuple reference to previous two nodes
        :param next_nodes: tuple reference to next two nodes
        """
        self.prev_up = None
        self.prev_down = None
        self.next_up = None
        self.next_down = None
        self.time = time
        self._p = p
        self.y = y
        # temp price variable to calculate spot and forward rates
        self._price = 1;

        # If kwargs passed in check for validity and set, else None
        if((prev_nodes is None) | (next_nodes is None)):
            return

        if(len(prev_nodes) ==2):
            self.prev_up = prev_nodes[0]
            self.prev_down = prev_nodes[1]
        if(len(next_nodes) ==2):
            self.next_up = next_nodes[0]
            self.next_down = next_nodes[1]

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if (value >= 0.0):
            self._price = value

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        if (value >=0) & (value <=1):
            self._p = value


    def __str__(self):
        return "[YieldNode: time={0}, yield={1}, prob={2}, price={3}]".format(self.time, self.y, self.p, self.price)

class ForwardYieldLattice(object): 

    def __init__(self, periods, y0, yield_up_func = None, yield_down_func = None, prob_func = None):
        self.NodeLayers = [[] for i in range(periods)]

        # n choose 2 combinations for forward rates and n spot rates
        # rates is array of length, periods and at each time, time-1 rates.
        self.rates = [[None for i in range(time)] for time in range(0, periods)]
        self.duration = periods


        # Probability of yield going up at next time interval given time, yield and probability at being at given YieldNode
        self.p = lambda t, y, p: 0.5 if (prob_func is None) else prob_func

        # yield of upper node at next time for a given node with time, yield and probability of going up
        self.y_u = lambda t, y: y + 0.01 if (yield_up_func is None) else yield_up_func
        # yield of upper node at next time for a given node with time, yield and probability of going up
        self.y_d = lambda t, y: y - 0.01 if (yield_down_func is None) else yield_down_func
        self.y0 = y0
        self.p0 = 0.5
        self.init_nodes()
        self.back_prop()


    def back_prop(self):
        """
        Calculates the arbitrage-based spot and forward yields based on a binomial
        based lattice approach. Using n sized lattices to compute the spot rate
        for 0,n. Then using these spot rates to calculate forward rates.
        """
        self.set_spot_rate(1, self.y0)
        # create lattices of size n to find spot rate of 0,n
        for end_time in range(self.duration -1, 1, -1):
            for node in self.NodeLayers[end_time]:
                node.price = 1 / (1 + node.y)

            # back-propagate final prices to time 0
            for time_layer in self.NodeLayers[end_time-1::-1]:
                for node in time_layer:
                    node_up = node.next_up
                    node_down = node.next_down
                    node.price = 1 / (1 + node.y) * (node.p * node_up.price + (1 - node.p) * node_down.price)

            # Use time 0 to calculate spot yield
            root = self.get_node(0,0)
            spot_0_end_time_yield = math.pow(root.price, (-1.0/end_time)) - 1
            self.set_spot_rate(end_time, spot_0_end_time_yield)

        # Use spot yields to calculate forward yields
        for time_end in range(2, self.duration):
            for time_start in range(1, time_end):
                forward_yield = self.calculate_forward_yields(time_start, time_end)
                self.set_forward_rate(time_start, time_end, forward_yield)

    def calculate_forward_yields(self, t1, t2):
        """
        :param t1, t2: Discrete time periods
        :return: Returns the arbitrage-based forward rate between t1 and t2 where t2 > t1
        """
        spot_to_t1 = self.get_spot_rate(t1)
        spot_to_t2 = self.get_spot_rate(t2)
        return  math.pow(math.pow(1 + spot_to_t2, t2) / math.pow(1 + spot_to_t1, t1), 1/(t2-t1)) -1

    def init_nodes(self):
        """
        Construct the forwards lattice with Yield Nodes with the given probability and yield functions
        """
        #construct root node manually
        root_node = YieldNode(0, self.p(0, self.y0, self.p0), self.y0)
        self.NodeLayers[0].append(root_node)
        # for each layer create new nodes and link back to prior nodes
        for	layer, time in zip(self.NodeLayers[1:], range(1, self.duration)):
            for i in range(0, time +1):
                prev_node_down = self.get_node(time -1, i)
                prev_node_up =  self.get_node(time -1, i-1)

                # configure all nodes from the previous time's node below
                if prev_node_down is not None:
                    y = prev_node_down.y
                    p = prev_node_down.p
                    node = YieldNode(time, self.p(time-1, y, p), self.y_u(time-1, y), prev_nodes = [prev_node_up, prev_node_down], next_nodes = [None, None])

                # if node is final node in layer (i.e. if node only has down predecessors)
                else:
                    y = prev_node_up.y
                    p = prev_node_up.p
                    node = YieldNode(time, self.p(time-1,y,p), self.y_d(time-1, y), [prev_node_up, prev_node_down], [None, None])
                self.NodeLayers[time].append(node)

        # Connect lattice nodes to next time period
        for t in range(0, self.duration):
            for i in range(t+1):
                node = self.get_node(t, i)
                if node is not None:
                    node.next_up = self.get_node(t+1, i)
                    node.next_down = self.get_node(t+1, i+1)


    # Setter Getters for rates #
    def set_forward_rate(self, t1, t2, y):
        self.rates[t2][t1] = y

    def get_spot_rate(self, t):
        return self.rates[t][0] if (self.rates[t][0] is not None) else None

    def set_spot_rate(self, t, y):
        self.rates[t][0] = y

    def get_forward_rate(self, t1, t2, y):
        return self.rates[t2][t1] if (self.rates[t2][t1] is not None) else None

    def get_node(self, t, i):
        """
        t, int: discrete time period
        i, int: index into list of nodes (starting from 0, in decreasing order of yield i = 0 is greatest yield)
        return, YieldNode: Node at particular point in lattice or None if node does not exist
        """

        # check if node exists at given time and index
        if(t < 0 | (i < 0 | i > t)):
            return None
        try:
            return self.NodeLayers[t][i]
        except:
            return None

    def __str__(self):
        layers = [" ".join([str(i) for i in layer]) for layer in self.NodeLayers]
        return "\n".join(layers)


if __name__ == '__main__': 
    a = ForwardYieldLattice(5, 0.7, 0.03, 0.01);
    print(a)
