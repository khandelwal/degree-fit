import unittest
import degreefit

class PoissonTest(unittest.TestCase):
    """ Test all the Poisson distribution related functions. """ 
    def test_poisson_lambda_estimation(self):
        self.assertEqual(5.0, degreefit.poisson_lambda_estimation([5, 5, 5]))
        self.assertAlmostEqual(
            2.80, degreefit.poisson_lambda_estimation([1, 2.4, 5]), places=3)

class GeometricTest(unittest.TestCase):
    def test_geometric_lambda_estimation(self):
        self.assertAlmostEqual(
            4.48, degreefit.geometric_lambda_estimation([5, 5, 5, 5]), places=2)
