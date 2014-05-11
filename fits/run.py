import degreefit

if __name__ == '__main__':

    likelihood_calculators = {
        'poisson': degreefit.poisson,
        'geometric': degreefit.geometric
    }

    degree_list = degreefit.read_degree_list('/opt/data/fit/edge_air_traffic.txt')
    results = degreefit.degree_list_fitter(likelihood_calculators, degree_list)
    print results
