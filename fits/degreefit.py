import math
import networkx as nx
import numpy as np
import scipy as sp
from scipy import special


def read_degree_list(filename):
    G = nx.read_edgelist(filename, delimiter=' ', nodetype=int)
    degree = G.degree().values()
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
    return (1.0 / lambdas * np.exp(-((degree_list - 1) / lambdas)))


def generic_likelihood(
        lambda_estimator, likelihood_term_calculator, degree_list):

    lambda_estimate = lambda_estimator(degree_list)
    likelihood_terms = likelihood_term_calculator(lambda_estimate, degree_list)
    return likelihood_terms


def poisson(degree_list):
    return generic_likelihood(
        poisson_lambda_estimation, poisson_likelihood_term, degree_list)


def geometric(degree_list):
    return generic_likelihood(
        geometric_lambda_estimation, geometric_likelihood_term, degree_list)


def akaike_criterion(likelihood_terms):
    """ Given a numpy array of likelihood terms, compute the AIC. """
    l_theta = 2.0 * np.log(likelihood_terms).sum()
    return 2.0 - l_theta + 4.0/(len(likelihood_terms) - 2.0)


def calculate_akaike_weights(degree_fit_result):
    min_aic = min([v['AIC'] for v in degree_fit_result.values()])

    for distribution, fit in degree_fit_result.items():
        aic = fit['AIC']
        d = -(aic - min_aic)/2.0
        degree_fit_result[distribution]['weight'] = math.exp(d)

    sum_deltas = sum([v['weight'] for v in degree_fit_result.values()])

    for distribution in degree_fit_result:
        degree_fit_result[distribution]['weight'] /= sum_deltas

    return degree_fit_result


def degree_list_fitter(likelihood_calculators, degree_list):

    """ Given a degree distribution, and a list of likelihood calculators,
    calculate the AIC for fitting the data, and the Akaike weights.

    'likelihood_calculators' is an dictionary keyed on distribution names of
    likelihood calculator functions.
    """

    degree_list = np.array(degree_list, dtype=np.float)

    results = {}

    for distribution, likelihood_calculator in likelihood_calculators.items():
        likelihood_terms = likelihood_calculator(degree_list)
        aic = akaike_criterion(likelihood_terms)
        results[distribution] = {'AIC': aic}

    results = calculate_akaike_weights(results)
    return results
