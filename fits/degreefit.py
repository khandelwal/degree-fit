import networkx as nx 
import numpy as np

def read_degree_list(filename):
    G = nx.read_edgelist(filename, delimiter=' ', nodetype=int)
    degree=G.degree().values()
    return degree


def poisson_lambda_estimation(num_list):
    """ This estimates the parameter lambda for the Poisson distribution 
    given a list of numbers. """
    x = np.array(num_list)
    return x.mean()


def geometric_lambda_estimation(num_list):
    """ Estimate the parameter lambda for the Geometric (Exponential)
    distribution"""

    x = np.array([float(i) for i in num_list])
    inverse_theta = np.log([x.sum() / (x.sum() - len(x))])[0]
    return 1.0/inverse_theta
