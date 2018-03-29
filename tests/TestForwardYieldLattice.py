from unittest import TestCase
from src.ForwardYieldLattice import ForwardYieldLattice

class TestForwardYieldLattice(TestCase):
    def setUp(self):
        self.yield_up = lambda t, y: y + 0.01
        self.yield_down = lambda t, y: y - 0.01
        self.p_func = lambda t,y,p: 0.7
        self.lattice = ForwardYieldLattice(5, 0.03, yield_up_func=self.yield_up, yield_down_func=self.yield_down, prob_func=self.p_func)

    def test_calculate_forward_yields(self):
        # General cases
        self.assertAlmostEqual(self.lattice.calculate_forward_yields(2,3), 0.041508, places=5, msg='Forward yield not correct for a single period')

        # multi-year forward yields
        self.assertAlmostEqual(self.lattice.calculate_forward_yields(1,3), 0.05711395, places=5, msg='Forward yield not correct for multiple periods')
        #Spot and forward yield should corroborate
        self.assertAlmostEqual(self.lattice.calculate_forward_yields(0,3), self.lattice.get_spot_rate(3), places=5, msg='Forward yield not same as spot yield for same periods.')

    def test_get_spot_rate(self):
        self.assertAlmostEqual(self.lattice.get_spot_rate(1), self.lattice.y0, places= 5, msg = "Initial spot rate isn't what is from initial parameter")

        self.assertAlmostEqual(self.lattice.get_spot_rate(3), 0.0479975767, places=5, msg = "General spot rate miscalculated")


    def test_get_forward_rate(self):
        self.assertAlmostEqual(self.lattice.get_spot_rate(3), self.lattice.get_forward_rate(0, 3), places = 5, msg = 'forward and spot functionality not consistent')

        self.assertAlmostEqual(self.lattice.get_forward_rate(2, 3), 0.0415086735187, places = 5,  msg = 'Forward rate incorrect for single time period')
        self.assertAlmostEqual(self.lattice.get_forward_rate(1, 3), 0.05711395, places =5, msg = 'Forward rate incorrect for multiple time periods')


    def test_get_node(self):
        self.assertEqual(self.lattice.get_node(0, 0).y, self.lattice.y0, msg= 'Initial node incorrect')
