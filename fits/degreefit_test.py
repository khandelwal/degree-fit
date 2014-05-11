import unittest
import degreefit

class PoissonTest(unittest.TestCase):
    """ Test all the Poisson distribution related functions. """ 
    def test_poisson_lambda_estimation(self):
        self.assertEqual(5.0, degreefit.poisson_lambda_estimation([5, 5, 5]))
        self.assertAlmostEqual(
            2.80, degreefit.poisson_lambda_estimation([1, 2.4, 5]), places=3)

    def test_likelihood(self):
        lambda_estimate = degreefit.poisson_lambda_estimation([5, 5, 5])
        result = degreefit.poisson_likelihood_term(lambda_estimate, [5, 5, 5])
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertAlmostEqual(0.1754, r, places=3)
            
class GeometricTest(unittest.TestCase):
    def test_geometric_lambda_estimation(self):
        self.assertAlmostEqual(
            4.48, degreefit.geometric_lambda_estimation([5, 5, 5, 5]), places=2)

    def test_likelihood(self):
        degree_list = [5, 5, 5, 5]
        lambda_estimate = degreefit.geometric_lambda_estimation(degree_list)
        result = degreefit.geometric_likelihood_term(
            lambda_estimate, degree_list)
        self.assertEqual(len(degree_list), len(result))
        for r in result:
            self.assertAlmostEqual(0.0913, r, places=3)
