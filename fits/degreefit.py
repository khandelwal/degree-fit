import networkx as nx 
import numpy as np
import scipy as sp
from scipy import special


def read_degree_list(filename):
    G = nx.read_edgelist(filename, delimiter=' ', nodetype=int)
    degree=G.degree().values()
    return degree


def poisson_lambda_estimation(degree_list):
    """ This estimates the parameter lambda for the Poisson distribution 
    given a list of numbers. """
    return degree_list.mean()


def geometric_lambda_estimation(degree_list):
    """ Estimate the parameter lambda for the Geometric (Exponential)
    distribution"""
    inverse_theta = np.log(
        [degree_list.sum() / (degree_list.sum() - len(degree_list))])[0]
    return 1.0/inverse_theta


def poisson_likelihood_term(lambda_estimate, degree_list):

    lambdas = np.empty(len(degree_list))
    lambdas.fill(lambda_estimate)

    theta_ds = np.power(degree_list, lambdas)

    exponents = np.empty(len(degree_list))
    exponents.fill(-lambda_estimate)

    numerator = theta_ds * np.exp(exponents)
    denominator = special.gamma(degree_list + 1.0)

    return numerator / denominator

def geometric_likelihood_term(lambda_estimate, degree_list):
    degree_list = np.array(degree_list)

    lambdas = np.empty(len(degree_list))
    lambdas.fill(lambda_estimate)
    return (1.0/lambdas * np.exp(-((degree_list - 1)/ lambdas)))

def generic_likelihood(degree_list, lambda_estimator):
    lambda_estimate = lambda_estimator(degree_list)
    likelihood_terms = likelihood_term_calculator(lambda_estimate, degree_list)
    return likelihood_terms


def akaike_criterion(likelihood_terms):
    """ Given a numpy array of likelihood terms, compute the AIC. """
    l_theta = 2.0 * numpy.log(likelihood_terms).sum()
    return 2 - l_theta + 4.0/(len(likelihood_terms) - 2.0)


def degree_list_fitter(degree_list, likelihood_calculators):
    degree_list = np.array(degree_list, dtype=np.float)

    results = {}

    for calculator_type, calculator in likelihood_calculators.items():
        likelihood_terms = calculator(degree_list)
        aic = akaike_criterion(likelihood_tersm)
        results[calcuator_type] = aic
    return result
