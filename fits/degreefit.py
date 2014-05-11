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
    return np.array(degree_list).mean()


def geometric_lambda_estimation(degree_list):
    """ Estimate the parameter lambda for the Geometric (Exponential)
    distribution"""

    x = np.array([float(k) for k in degree_list])
    inverse_theta = np.log([x.sum() / (x.sum() - len(x))])[0]
    return 1.0/inverse_theta


def poisson_likelihood_term(lambda_estimate, degree_list):

    degree_list = np.array(degree_list)

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
