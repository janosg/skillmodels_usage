import numpy as np
import pandas as pd
from skillmodels.model_functions.transition_functions import \
    no_squares_translog, linear
from bld.project_paths import project_paths_join as ppj


def generate_test_data(nobs, factors, periods, included_positions, meas_names,
                       initial_mean, initial_cov, intercepts, loadings,
                       meas_sd, gammas, trans_sd):

    np.random.seed(12345)
    nfac = len(factors)
    initial_factors = np.random.multivariate_normal(
        mean=initial_mean, cov=initial_cov, size=(nobs))
    factor_data = []
    meas_data = []
    m_to_factor = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    counter = 0
    for t in periods:

        if t == 0:
            new_facs = initial_factors
        else:
            new_facs = np.zeros((nobs, nfac))
            new_facs[:, :nfac - 1] += np.random.normal(
                loc=np.zeros(nfac - 1), scale=trans_sd[t - 1],
                size=(nobs, nfac - 1))
            for f, factor in enumerate(factors):
                if f == 0:
                    new_facs[:, f] += no_squares_translog(
                        factor_data[t - 1], gammas[f][t - 1],
                        included_positions[f])
                elif f == 1:
                    new_facs[:, f] += linear(
                        factor_data[t - 1], gammas[f][t - 1],
                        included_positions[f])
                else:
                    new_facs[:, f] = factor_data[t - 1][:, f]
        factor_data.append(new_facs)
        nmeas = 9 if t == 0 else 6
        # noise part of measurements
        measurements = np.random.normal(
            loc=np.zeros(nmeas), scale=meas_sd[counter: counter + nmeas],
            size=(nobs, nmeas))
        # add structural part of measurements
        for m in range(nmeas):
            factor_pos = m_to_factor[m]
            measurements[:, m] += (new_facs[:, factor_pos] * loadings[counter])
            measurements[:, m] += intercepts[counter]
            counter += 1
        df = pd.DataFrame(data=measurements, columns=meas_names[:nmeas])
        df['period'] = t
        df['id'] = np.arange(nobs)
        meas_data.append(df)
    large_df = pd.concat(meas_data)
    large_df.sort_values(by=['id', 'period'], inplace=True)
    return large_df


if __name__ == '__main__':
    factor_names = ['fac1', 'fac2', 'fac3']
    nfac = len(factor_names)
    nperiods = 4
    periods = list(range(nperiods))
    included_positions = [np.arange(3), np.array([1, 2]), []]

    meas_names = ['y{}'.format(i + 1) for i in range(9)]

    true_gammas = [
        [[0.750, 0.03, 0.03, 0.0003, 0.0020, 0.0024, 0.6],
         [0.750, 0.03, 0.03, 0.0003, 0.0020, 0.0024, 0.6],
         [0.750, 0.03, 0.03, 0.0003, 0.0020, 0.0024, 0.6]],

        [[.925, 0.04, 0.75],
         [.925, 0.04, 0.75],
         [.925, 0.04, 0.75]],

        np.zeros((3, 0))]

    true_loadings = np.arange(start=0.5, stop=1.85, step=0.05)
    true_intercepts = np.arange(start=-0.665, stop=0.665, step=0.05)
    true_X_zero = np.array([10, 15, 30])
    true_cov_matrix = np.array([[2.0, 0.05, 0.1],
                                [0.05, 4.0, 0.0],
                                [0.1, 0.0, 9.0]])

    nobs = 8000
    base_meas_sd = 0.7
    base_trans_sd = 1.0

    true_meas_sd = true_loadings * base_meas_sd
    true_trans_sd = [[0.4, 0.5], [0.4, 0.5], [0.4, 0.5]]

    large_df = generate_test_data(
        nobs=nobs, factors=factor_names, periods=periods,
        included_positions=included_positions,
        meas_names=meas_names,
        initial_mean=true_X_zero, initial_cov=true_cov_matrix,
        intercepts=true_intercepts, loadings=true_loadings,
        meas_sd=true_meas_sd, gammas=true_gammas,
        trans_sd=true_trans_sd)

    out_path = ppj('OUT_DATA', 'ns_translog_data.dta')
    large_df.to_stata(out_path)
