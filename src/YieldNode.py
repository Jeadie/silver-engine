class YieldNode(object):

    def __init__(self, time, p, y, prev_nodes = None, next_nodes = None):
        """
        :param time: Discrete time value for node from root
        :param p: Decimal probability of shifting to upper next node.
        :param y: Forward Yield rate at time increment
        :param prev_nodes: tuple reference to previous two nodes
        :param next_nodes: tuple reference to next two nodes
        """
        self.time = time
        self._p = p
        self.y = y
        # temp price variable to calculate spot and forward rates
        self._price = 1;

        # If kwargs passed in check for validity and set, else None
        if((prev_nodes is None) | (next_nodes is None)):
            self.prev_up, self.prev_down, self.next_up, self.next_down = (None, None, None, None)
            return

        if(len(prev_nodes) ==2):
            self.prev_up = prev_nodes[0]
            self.prev_down = prev_nodes[1]
        if(len(next_nodes) ==2):
            self.next_up = next_nodes[0]
            self.next_down = next_nodes[1]


    # Domain checking setter and getters
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
