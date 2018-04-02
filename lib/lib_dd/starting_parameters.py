import os

import numpy as np
from scipy import stats

import lib_dd.base_class as base_class


class starting_parameters(object):

    def estimate_starting_parameters_3(self, re, mim):
        estimator = base_class.starting_pars_3(
            re, mim, self.frequencies, self.tau
        )
        parameters = estimator.estimate(self)
        return parameters

    def estimate_starting_parameters_2(self, re, mim):
        """
        Try to find good starting parameters using a Gaussian m-distribution.

        This should only work well if we have only one peak in the data
        (imaginary/phase)
        """
        rho0 = np.sqrt(re[0] ** 2 + mim[0] ** 2)

        # start playing with gaussians distributions
        pol_maximum = np.argmax(mim)

        f_max = self.frequencies[pol_maximum]
        tau_max = 1 / (2 * np.pi * f_max)
        s_max = np.log10(tau_max)

        m = stats.norm.pdf(self.s, s_max, 1)
        # normalize
        m /= np.sum(m)

        pars_linear = np.hstack((rho0, m))
        parameters = self.convert_parameters(pars_linear)
        return parameters

    def estimate_starting_parameters_1(self, re, mim):
        """
        Heuristic 1 to generate a suitable starting distribution for a fit

        TODO: Florsch et al. 2014 has a name for this kind of heuristic...
        """
        parameters = np.zeros((self.s.shape[0] + 1))
        pars = np.zeros(parameters.shape)

        # rho0
        parameters[0] = np.sqrt(re[0] ** 2 + mim[0] ** 2)

        # generate test chargeabilities m_i
        test_m = np.logspace(-12, 0, 20)

        best = 0
        best_diff = None
        for nr, i in enumerate(test_m):
            pars[0] = parameters[0]
            pars[1:] = i
            pars = self.convert_parameters(pars)
            tre_tmim = self.forward(pars)
            tre = tre_tmim[:, 0]
            tmim = tre_tmim[:, 1]

            diff_im = np.sum(np.abs(tmim - mim))
            if(best_diff is None or best_diff > diff_im):
                best_diff = diff_im
                best = nr
            if('DD_DEBUG_STARTING_PARS' in os.environ and
               os.environ['DD_DEBUG_STARTING_PARS'] == '1'):
                # enable debug plots
                fig, axes = plt.subplots(2, 1, figsize=(5, 4))
                fig.suptitle('test m: {0} - diff\_im: {1}'.format(
                    i, diff_im))
                ax = axes[0]
                ax.semilogx(self.frequencies, re, '.-', color='k')
                ax.semilogx(self.frequencies, tre, '.-', color='gray')
                ax.set_ylabel(r'part1')
                ax.set_xlabel('f (Hz)')
                ax = axes[1]
                ax.semilogx(self.frequencies, mim, '.-', color='k')
                ax.semilogx(self.frequencies, tmim, '.-', color='gray')
                ax.set_ylabel(r'part2')
                ax.set_xlabel('f (Hz)')
                filename = 'starting_model_{0}.png'.format(nr)
                fig.savefig(filename, dpi=150)

        parameters[1:] = test_m[best]

        parameters = self.convert_parameters(parameters)
        return parameters

    def estimate_starting_parameters(self, spectrum):
        re = spectrum[:, 0]
        mim = spectrum[:, 1]

        # the starting model can be set via the environment variable
        starting_model = int(os.environ.get('DD_STARTING_MODEL', 3))

        if(starting_model == 1):
            # find good flat starting paramaters
            parameters = self.estimate_starting_parameters_1(re, mim)
        elif(starting_model == 2):
            # find normally distributed starting parameters
            parameters = self.estimate_starting_parameters_2(re, mim)
        elif(starting_model == 3):
            # frequency bin wise
            parameters = self.estimate_starting_parameters_3(re, mim)
        else:
            raise Exception(
                'starting model heuristic number {} not known!'.format(
                    starting_model)
            )

        return parameters
