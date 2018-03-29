from unittest import TestCase
from src.YieldNode import YieldNode

class TestYieldNode(TestCase):
    def setUp(self):
        self.Node = YieldNode(0, 0.5, 0.03)

    def test_price(self):
        self.Node.price = 1
        self.assertTrue(self.Node.price == 1, msg = 'Custom price setter failed. ')
        self.Node.price = -1
        self.assertTrue(self.Node.price == 1, msg = 'Price cannot be changed to negative value')

    def test_p(self):
        self.Node.p = 0.5
        self.assertTrue(self.Node.p == 0.5, msg='Custom probability setter failed. ')
        self.Node.p = -0.00001
        self.assertTrue(self.Node.p == 0.5, msg='Probability cannot be negative value')
        self.Node.p = 1.00001
        self.assertTrue(self.Node.p <= 1, msg= 'Probability cannot be above 1')
