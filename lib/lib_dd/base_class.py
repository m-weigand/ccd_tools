# -*- coding: utf-8 -*-
""" Copyright 2014-2017 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import logging

import numpy as np

import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()
import lib_dd.int_pars as int_pars

logger = logging.getLogger('lib_dd.main')


def determine_tau_range(settings):
    """Return the tau values depending on the settings 'Nd', 'tau_values'
    and 'tau_sel' in the dict 'settings'

    Tau values can be set by using one of the following strings in
        self.settings['tausel']:

            data
            data_ext
            factor_left,factor_right
            ,factor_right
            factor_left,

    Missing values are replaced by one (i.e. the data frequency limits are
                                        used).
    """
    # check which selection strategy to use
    if('tau_values' in settings):
        # we got custom tau values
        tau = settings['tau_values']
        s = np.log10(tau)
        tau_f_values = 1 / (2 * np.pi * tau)
    else:
        # determine range
        if(settings['tausel'] == 'data'):
                factor_left = 1
                factor_right = 1
        elif(settings['tausel'] == 'data_ext'):
                factor_left = 10
                factor_right = 10
        else:
            # try to parse
            items = settings['tausel'].split(',')
            if(len(items) != 2):
                raise Exception('Wrong format for tausel')

            if(not items[0]):
                factor_left = 1
            else:
                factor_left = int(items[0])

            if(not items[1]):
                factor_right = 1
            else:
                factor_right = int(items[1])

        # determine tau values for one data set
        tau, s, tau_f_values = get_tau_values_for_data(
            settings['frequencies'],
            settings['Nd'],
            factor_left=factor_left,
            factor_right=factor_right)
    return tau, s, tau_f_values


def get_tau_values_for_data(frequencies, Nd, factor_left=1,
                            factor_right=1):
    r"""
    Return the :math:`\tau` values corresponding to the frequency range of
    the data set.

    Parameters
    ----------
    Nd : number of :math:`\tau` values per decade
    factor_left : factor to divide to the lower limit by
    factor_right : factor to multiply to the upper limit

    Returns
    -------
    tau,s with :math:`s = log_{10}(\tau)`

    """
    minf = np.min(frequencies)
    maxf = np.max(frequencies)

    # check min/max frequencies
    # if(minf < 1e-4):
    #    logger.warn('Minimum frequency below global minimum')

    # if(maxf > 1e-4):
    #    logger.warn('Maximum frequency above global minimum')

    # global min/max values for tau, corresponding to the frequency range
    # [1e-4 Hz,1e6 Hz]
    min_tau_f = 1e-15
    max_tau_f = 1e16
    nr_decades = np.log10(max_tau_f) - np.log10(min_tau_f)
    g_tau_fmin = 1.0 / (2 * np.pi * 1e-15)
    g_tau_fmax = 1.0 / (2 * np.pi * 1e16)

    # compile total pool of tau values
    # the (fixed) global frequency range spans 9 order of magnitude
    N = nr_decades * Nd
    g_tau = np.logspace(np.log10(g_tau_fmin), np.log10(g_tau_fmax), N)
    g_tau_frequencies = 1.0 / (2 * np.pi * g_tau)

    # the global pool
    g_pool = np.hstack((g_tau_frequencies[:, np.newaxis],
                        g_tau[:, np.newaxis]))

    # find nearest index
    fmin = minf / float(factor_left)
    fmax = maxf * float(factor_right)

    index_min = np.argmin(np.abs(g_pool[:, 0] - fmin))
    index_max = np.argmin(np.abs(g_pool[:, 0] - fmax))

    # fmin/fmax depend on the data frequency range
    # when we choose our tau value out of the (data independent) pool, it
    # is possible that we choose a tau value corresponding to a slightly
    # larger/smaller value of fmin/max. In those cases we just use the next
    # smaller/larger value of tau
    if(g_pool[index_min, 0] > fmin and index_min > 0):
        # logger.info('Reducing index_min by one')
        index_min -= 1

    if(g_pool[index_max, -1] < fmax and index_max < (g_pool.shape[0] - 1)):
        # logger.info('Increasing index_max by one')
        index_max += 1

    tau_data = g_pool[index_min:index_max + 1, :]

    # tau values should be sorted in ascending order
    if(tau_data[0, 1] > tau_data[-1, 1]):
        tau_data = tau_data[::-1, :]

    tau_s = tau_data[:, 1]
    f_s = tau_data[:, 0]
    s_s = np.log10(tau_s)

    return tau_s, s_s, f_s


class starting_pars_3():
    """Heuristic nr 3 for determining useful starting values for the fit.

    This function is aware if the conductivity or resistivity formulation is
    used.
    """
    def __init__(self, re, mim, frequencies, taus):
        self.re = re
        self.mim = mim
        self.frequencies = frequencies
        self.omega = 2 * np.pi * frequencies
        self.tau = taus

        # rho0 can be approximated by the low-frequency magnitude
        self.rho0 = np.sqrt(re[0] ** 2 + mim[0] ** 2)

        # Check if the conductivity formulation was turned on using the
        # environment variable DD_COND=1
        # the conductivity formulation uses sigma_\infty, i.e. the
        # high-frequency limit
        if int(os.environ.get('DD_COND', 0)) == 1:
            self.rho0 = np.sqrt(re[-1] ** 2 + mim[-1] ** 2)
            # self.rho0 = np.abs(re[-1])
            # print('debug: rho0=sigma_inf', re[-1], mim[-1], self.rho0)
            # print(re)

        # compute bins for each frequency decade
        self.minf = self.frequencies.min()
        self.maxf = self.frequencies.max()

        # round to nearest decade below/above min/max-f
        self.minbin = np.floor(np.log10(self.minf))
        self.maxbin = np.ceil(np.log10(self.maxf))

        # just to be sure, determine tau ranges outside the frequency-derived
        # limits
        self.tau_min = self.tau.min()
        self.tau_max = self.tau.max()
        self.f_tau_min = 1 / (2 * np.pi * self.tau_max)
        self.f_tau_max = 1 / (2 * np.pi * self.tau_min)

        # round to nearest decade below/above
        self.min_tau_bin = np.floor(np.log10(self.f_tau_min))
        self.max_tau_bin = np.ceil(np.log10(self.f_tau_max))

        # determine limits: we only work on the data range
        if(self.min_tau_bin < self.minbin):
            self.min_tau_bin_fl = self.minbin
        else:
            self.min_tau_bin_fl = None
        if(self.max_tau_bin >= self.maxbin):
            self.max_tau_bin_fl = self.maxbin
        else:
            self.max_tau_bin_fl = None

    def get_bins(self):
        # now we compute the frequency bins
        if(self.min_tau_bin_fl is None):
            self.bins_tau_lowf = None
        else:
            self.bins_tau_lowf = np.logspace(
                self.min_tau_bin, self.minbin,
                (self.minbin - self.min_tau_bin) + 1
            )
        self.bins_inside_f = np.logspace(
            self.minbin, self.maxbin, (self.maxbin - self.minbin) + 1
        )
        if(self.max_tau_bin_fl is None):
            self.bins_tau_highf = None
        else:
            self.bins_tau_highf = np.logspace(
                self.maxbin, self.max_tau_bin,
                (self.max_tau_bin - self.maxbin) + 1
            )

    def get_sec_data(self):
        sec_data = {}
        for key, bins, frequencies in (
            ('lowf', self.bins_tau_lowf, None),
            ('inside', self.bins_inside_f, self.frequencies),
            ('highf', self.bins_tau_highf, None),
        ):
            if(bins is None):
                continue

            # take logarithmic means of frequency data for the bins
            f_logmeans = (np.log10(bins[0:-1]) + np.log10(bins[1:])) / 2

            if frequencies is not None:
                # assign data points to bins
                data_in_f_bins = np.digitize(frequencies, bins)

                # now avarage the data points for each bin
                f_data_means = []
                fbins = []
                f_f_means = []

                for nr, bin_nr in enumerate(range(1, self.bins_inside_f.size)):
                    f_indices = np.where(data_in_f_bins == bin_nr)[0]
                    # bin_frequencies = frequencies[f_indices]
                    f_data = self.mim[f_indices]
                    f_data_mean = np.mean(f_data)
                    # DD can only handle negative imaginary parts, therefore
                    # replace all positive mim (minus imaginary) values by
                    # data_mean_tau
                    if(f_data_mean <= 0):
                        f_data_mean = self.data_mean_tau

                    f_data_means.append(f_data_mean)
                    fbins.append((bins[bin_nr - 1], bins[bin_nr]))
                    f_f_means.append(f_logmeans[nr])

                    outstr = 'The frequencies {0} belong into bin {1} - '
                    outstr += '{2} with mean {3} and flogmean {4}'
                    # print(outstr.format(
                    #   bin_frequencies, fbins[-1][0], fbins[-1][1],
                    #    f_data_mean,
                    #    f_logmeans[nr]))
            else:
                f_data_means = [self.data_mean_tau for x in f_logmeans]
            sec_data[key] = (f_logmeans, f_data_means, bins)
        return sec_data

    def estimate(self, obj):
        """ Determine a starting model by creating frequency-decade wise mean
        values of mim and then computing a fixed chargeability value for each
        frequency decade.
        """
        # print('Start determining initial parameters')

        # compute bins
        self.get_bins()

        # the value which will be assigned to tau-range outside the data range

        # if 'DD_COND' in os.environ and os.environ['DD_COND'] == '1':
        # select only the "valid" polarizations, i.e. capacitative effects
        capacitive_values = np.where(self.mim > 0)[0]
        if len(capacitive_values) > 0:
            self.data_mean_tau = self.mim[capacitive_values].min()
        else:
            # no valid value was found. We can assume this spectrum can not
            # be fitted using the DD. Use a really small m value here
            self.data_mean_tau = 1e-7

        sec_data = self.get_sec_data()

        # select chargeabilities for the frequency decades
        chargeabilities = np.empty_like(self.tau) * np.nan
        ersatz = 0
        for key in ('inside', ):  # sec_data.keys():
            # select tau values corresponding to bins
            tau_bins = 1 / (2 * np.pi * sec_data[key][2])
            tau_digi = np.digitize(self.tau, tau_bins)
            for nr, bin_nr in enumerate(range(1, tau_bins.size)):
                tau_indices = np.where(tau_digi == bin_nr)[0]
                # compute the chargeability for this tau span
                # we work with mim, therefore no minus sign
                m_dec = (sec_data[key][1][nr] / self.rho0)
                term = 1
                for i in tau_indices:
                    w = 2 * np.pi * sec_data[key][2][nr]
                    term += 1 / (w * self.tau[i] /
                                 (1 + (w * self.tau[i]) ** 2))
                m_dec *= term

                chargeabilities[tau_indices] = m_dec  # sec_data[key][1][nr]
                ersatz += 1

        where_are_numbers = np.where(~np.isnan(chargeabilities))[0]
        chargeabilities[0:where_are_numbers[0]] = chargeabilities[
            where_are_numbers[0]]
        chargeabilities[where_are_numbers[-1]:] = chargeabilities[
            where_are_numbers[-1]]
        """
        chargeabilities[0:where_are_numbers[0]] = 1e-6
        chargeabilities[where_are_numbers[-1]:] = 1e-6
        """
        # assign the nearest data chargeabilities to the outside regions
        # normalize chargeabilities to 1
        chargeabilities /= np.sum(chargeabilities)

        # test various scaling factors
        mim_list = []
        rms_list = []
        m_list = []
        scales = np.logspace(-7, 0, 15)
        # scales = np.array((1e-3, 0.5, 1))
        for scale in scales:
            # test forward modeling
            m_list.append(chargeabilities * scale)
            pars_linear = np.hstack((self.rho0, chargeabilities * scale))
            pars = obj.convert_parameters(pars_linear)
            re_mim = obj.forward(pars)
            mim_f = re_mim[:, 1]
            # print('mim_f', mim_f)
            # print('mim', self.mim)
            # print('--')
            # print('--')
            mim_list.append(mim_f)
            # compute rms_mim
            rms_mim = np.sqrt(
                (1.0 / float(self.mim.size)) * np.sum(
                    np.abs(mim_f - self.mim) ** 2)
            )
            rms_list.append(rms_mim)
        rms_list = np.array(rms_list)
        # print('rms_list', rms_list)

        # find minimum rms
        min_index = np.argmin(rms_list)

        # select three values to fit a parabola through
        # indices = [0, min_index, len(scales) - 1]
        indices = [min_index - 1, min_index, min_index + 1]

        # if min_index is the largest scaling factor, use this
        a = b = c = 0
        if indices[-1] == len(scales):
            logger.info('using largest scaling factor')
            x_min = scales[-1]
            # remove last entry from index because it points to a value outside
            # the 'scales' array
            del(indices[-1])
        elif indices[-1] == 0:
            logger.info('using smallest scaling factor')
            x_min = scales[0]
        else:
            # fit parabola to rms-values
            # fit parabola
            x = np.array(scales)[indices]
            y = np.array(rms_list)[indices]

            A = np.zeros((3, 3), dtype=np.float)
            A[:, 0] = x ** 2
            A[:, 1] = x
            A[:, 2] = 1
            a, b, c = np.linalg.solve(A, y)

            # compute minimum
            x_min = -b / (2 * a)

            # set to default, if we get a negative scaling factor
            if x_min < 0:
                logger.info(
                    'starting parameters: setting scaling factor to' +
                    '{}'.format(x_min)
                )
                # note that this is an arbitrarily small factor, adjusted by
                # experience! Please find a suitable automatic way for this!
                x_min = 0.0001
        logger.info('Scaling factor: {}'.format(x_min))
        # """

        # test for conductivity
        # x_min = 1
        # rms_list = []
        term = np.abs(1 -
                      np.sum(chargeabilities * x_min /
                             (1 + 1j * self.omega[0] * self.tau)))
        # print('term', term)
        # self.rho0 = self.re[0] * term
        # self.rho0 = self.re[0] / term
        pars_linear = np.hstack((self.rho0, chargeabilities * x_min))
        pars = obj.convert_parameters(pars_linear)

        # debug on:
        # re_mim = obj.forward(pars)
        # mim_f = re_mim[:, 1]
        # print('FINAL')
        # print('mim_f', mim_f)
        # print('mim', self.mim)
        # debug off
        plot_starting_model = False
        if(plot_starting_model):
            # # plot
            fig, axes = plt.subplots(4, 1, figsize=(6, 7))
            # plot spectrum
            pars_linear = np.hstack((self.rho0, chargeabilities * x_min))
            pars = obj.convert_parameters(pars_linear)
            re_mim = obj.forward(pars)
            re_f = re_mim[:, 0]
            mim_f = re_mim[:, 1]

            # real part
            ax = axes[0]
            ax.loglog(self.frequencies, self.re, '.-', color='k', alpha=0.5,
                      label='data')
            ax.loglog(self.frequencies, re_f, '-', color='green',
                      label='model')
            ax.set_xlabel('frequency [Hz]')
            ax.set_ylabel(r"$-\sigma'~[\Omega m]$")
            ax.set_xlim(self.frequencies.min(), self.frequencies.max())
            ax.legend(loc='best')

            # imaginary part
            ax = axes[1]
            ax.set_title('xmin: {0}'.format(x_min))
            for key in sec_data.keys():
                ax.scatter(10 ** np.array(sec_data[key][0]), sec_data[key][1],
                           s=30, color='blue',
                           label='')
            ax.loglog(self.frequencies, self.mim, '.-', color='k', alpha=0.5,
                      label='data')
            ax.set_xlabel('frequency [Hz]')
            ax.set_ylabel(r"$-\sigma''~[\Omega m]$")
            # for scaled_mim in mim_list:
            # print('mimf', mim_f)
            ax.loglog(self.frequencies, mim_f, '-', color='green',
                      label='model')
            ax.set_xlim([self.f_tau_min, self.f_tau_max])

            for scale in (0.1, 0.5, 1.0):
                pars_linear_plot = np.hstack(
                    (self.rho0, chargeabilities * scale))
                pars_plot = obj.convert_parameters(pars_linear_plot)
                re_mim = obj.forward(pars_plot)
                re_f = re_mim[:, 0]
                mim_f = re_mim[:, 1]
                ax.loglog(self.frequencies, mim_f, '-', color='red')
            ax.legend(loc='best')

            # plot RTD
            ax = axes[2]
            ax.loglog(self.tau, chargeabilities, '.-')
            ax.set_xlabel(r'$\tau~[s]$')
            ax.set_ylabel(r'$m_i$')

            ax.set_xlim([self.tau.min(), self.tau.max()])
            ax.invert_xaxis()

            # scales vs. rms_mim
            ax = axes[3]
            if(not np.all(np.isnan(rms_list))):
                ax.loglog(scales, rms_list, '.-')

                scale_range = np.linspace(0, 1, 30)
                ax.loglog(scale_range, a * (scale_range ** 2) +
                          b * scale_range + c, '-',
                          color='r')
                ax.scatter(scales[indices], rms_list[indices], color='c', s=30)
                ax.set_xlabel('scaling factor')
                ax.set_ylabel('RMS')
            fig.tight_layout()
            fig.savefig('starting_pars3.png', dpi=300)
            plt.close(fig)
            del(fig)
        # print('End determining initial parameters')
        # exit()
        return pars


class integrated_parameters():
    """
    Computation of integrated paramters. This class is not meant to be used
    alone, it is meant to be inherited by 'dd_resistivity_skeleton'
    """

    def compute_par_stats(self, pars):
        r"""
        For a given parameter set (i.e. a fit result), compute relevant
        statistical values such das :math:`m_{tot}`, :math:`m_{tot}^n`,
        :math:`\tau_{50}`, :math:`\tau_{mean}`, :math:`\tau_{peak}`

        Parameters
        ----------


        Returns
        -------
        stat_pars : dict containing the computed parameters

        Also store stat_pars in self.stat_pars
        """
        # integrated parameters are computed from the tau/chargeability values
        # corresponding to the data frequency ranges. Therefore we first create
        # linear representation of these values

        # mask all tau values outside the data ranges
        tau_extra_min = np.where(self.tau < self.tau_data_min)[0]
        tau_extra_max = np.where(self.tau > self.tau_data_max)[0]

        # work with linear parameters
        pars_lin = self.convert_pars_back(pars)

        pars_data = np.delete(pars_lin, tau_extra_max + 1)
        pars_data = np.delete(pars_data, tau_extra_min + 1)

        tau_data = self.tau.copy()
        tau_data = np.delete(tau_data, tau_extra_max)
        tau_data = np.delete(tau_data, tau_extra_min)
        s_data = np.log10(tau_data)

        # now compute the integrated parameters
        stat_pars = {}

        # the exception: we want to save the 'raw' pars, tau
        stat_pars['m_i'] = np.log10(pars_lin[1:])

        # coverages are computed on the whole parameter range
        covm, covf = self._compute_coverages(pars)
        stat_pars['covm'] = covm
        stat_pars['covf'] = covf

        # "regular" integrated pars
        int_par_keys = {'rho0': int_pars.rho0,
                        'm_data': int_pars.m_data,
                        'm_tot': int_pars.m_tot,
                        'm_tot_n': int_pars.m_tot_n,
                        'tau_x': int_pars.tau_x,
                        'tau_50': int_pars.tau_50,
                        'tau_mean': int_pars.tau_mean,
                        'tau_peaks': int_pars.tau_peaks,
                        'tau_max': int_pars.tau_max,
                        'U_tau': int_pars.U_tau,
                        'tau_arithmetic': int_pars.tau_arithmetic,
                        'tau_geometric': int_pars.tau_geometric,
                        'decade_loadings': int_pars.decade_loadings
                        }
        for key, func in int_par_keys.items():
            result = func(pars_data, tau_data, s_data)
            if(isinstance(result, dict)):
                stat_pars.update(result)
            else:
                stat_pars[key] = result

        self.stat_pars = stat_pars
        return self.stat_pars

    def _compute_coverages(self, pars):
        """

        """
        Jacobian = self.Jacobian(pars)
        Jsize = Jacobian.shape

        # extract dsigma''/dm
        del_mim_del_m = Jacobian[int(Jsize[0] / 2):, 1:]

        covf = np.abs(del_mim_del_m).sum(axis=1)
        covf /= np.max(covf)

        covm = np.abs(del_mim_del_m).sum(axis=0)
        covm /= np.max(covm)
        return covm, covf
