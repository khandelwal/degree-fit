import unittest
import degreefit
import numpy as np

class PoissonTest(unittest.TestCase):
    """ Test all the Poisson distribution related functions. """ 
    def test_poisson_lambda_estimation(self):
        degree_list = np.array([5, 5, 5])
        self.assertEqual(5.0, degreefit.poisson_lambda_estimation(degree_list))
        self.assertAlmostEqual(
            2.80,
            degreefit.poisson_lambda_estimation(
                np.array([1, 2.4, 5])), places=3)

    def test_likelihood(self):
        lambda_estimate = degreefit.poisson_lambda_estimation(
            np.array([5, 5, 5]))

        result = degreefit.poisson_likelihood_term(
            lambda_estimate, np.array([5, 5, 5]))
        self.assertEqual(len(result), 3)
        for r in result:
            self.assertAlmostEqual(0.1754, r, places=3)

class GeometricTest(unittest.TestCase):
    def test_geometric_lambda_estimation(self):
        degree_list = np.array([5, 5, 5, 5], dtype=np.float)
        self.assertAlmostEqual(
            4.48, degreefit.geometric_lambda_estimation(degree_list), places=2)

    def test_likelihood(self):
        degree_list = np.array([5, 5, 5, 5], dtype=np.float)
        lambda_estimate = degreefit.geometric_lambda_estimation(degree_list)
        result = degreefit.geometric_likelihood_term(
            lambda_estimate, degree_list)
        self.assertEqual(len(degree_list), len(result))
        for r in result:
            self.assertAlmostEqual(0.0913, r, places=3)

class AICTest(unittest.TestCase):
    def test_akaike_criterion(self):
        degree_list = np.array([5, 5, 5])
        lambda_estimate = degreefit.poisson_lambda_estimation(degree_list)
        likelihoods= degreefit.poisson_likelihood_term(
            lambda_estimate, degree_list)
        result = degreefit.akaike_criterion(likelihoods)
        self.assertAlmostEqual(16.44, result, places=2)
