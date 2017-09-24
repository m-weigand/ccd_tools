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
import numpy as np
import logging

import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()
import sip_formats.convert as sip_convert


class plot_iteration():
    """ This class defines an override function for the default plot function
    of the Iteration class. The new plot function is aware of the Cole-Cole
    Decomposition approach and will plot more information (i.e. the RTD)

    In addition, it will renormalise data if necessary.
    """
    def plot(self, it, norm_factors=None):
        try:
            if norm_factors is None:
                self.norm_factors = 1.0
            else:
                self.norm_factors = norm_factors
            self._plot(it)
        except Exception as e:
            logging.info('Exception in plot routine', e)

        return self.fig

    def create_figure(self):
        space_top = 1.2
        size_x = 14
        size_y = 2 * self.nr_spectra + space_top

        fig, axes = plt.subplots(
            self.nr_spectra, 5,
            figsize=(size_x, size_y)
        )
        self.top_margin = (size_y - space_top) / float(size_y)
        axes = np.atleast_2d(axes)
        self.fig = fig
        self.axes = axes
        return fig, axes

    def finalize_fig(self):
        ax = self.axes[0, 0]
        title = 'Cole-Cole decomposition, iteration {0}'.format(self.it.nr)
        ax.annotate(
            title,
            xy=(0.0, 1.00),
            xytext=(15, -30),
            textcoords='offset points',
            xycoords='figure fraction'
        )
        dd_c = 'c = {0}'.format(os.environ.get('DD_C', '1.0'))
        if 'DD_COND' in os.environ and os.environ['DD_COND'] == '1':
            model_title = 'conductivity model'
        else:
            model_title = 'resistivity model'
        logging.info('dd_c: {0}'.format(dd_c))
        model_title += ', {0}'.format(dd_c)
        ax.annotate(
            model_title,
            xy=(1.0, 1.0),
            xytext=(-160, -30),
            textcoords='offset points',
            xycoords='figure fraction',
        )

        self.fig.tight_layout()
        self.fig.subplots_adjust(top=self.top_margin)

    def _plot(self, it):
        """Plot one or more spectra
        """
        self.it = it

        D = it.Data.D / self.norm_factors
        M = it.Model.convert_to_M(it.m)
        # renormalize here? why do we compuate the forward solution again?
        F = it.Model.F(M) / self.norm_factors
        extra_size = int(
            np.sum([x[1][1] for x in it.Data.extra_dims.items()]))
        self.nr_spectra = max(1, extra_size)

        fig, axes = self.create_figure()

        # iterate over spectra
        for nr, (d, m) in enumerate(it.Model.DM_iterator()):
            self._plot_rre_rim(nr, axes[nr, 0:2], D[d], F[d], it)
            self._plot_rmag_rpha(nr, axes[nr, 2:4], D[d], F[d], it)
            self._plot_rtd(nr, axes[nr, 4], M[m], it)
            ax1 = axes[nr, 0].twinx()
            ax2 = axes[nr, 1].twinx()
            self._plot_cre_cim(nr, [ax1, ax2], D[d], F[d], it)

        self.finalize_fig()

    def _plot_rtd(self, nr, ax, m, it):
        ax.semilogx(it.Data.obj.tau, m[1:], '.-', color='k')
        ax.set_xlim(it.Data.obj.tau.min(), it.Data.obj.tau.max())
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=5))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        self._mark_tau_parameters_tau(nr, ax, it)
        ax.invert_xaxis()
        # mark limits of data frequencies, converted into the tau space
        tau_min = np.min(it.Model.obj.tau)
        tau_max = np.max(it.Model.obj.tau)
        d_fmin = np.min(it.Data.obj.frequencies)
        d_fmax = np.max(it.Data.obj.frequencies)
        t_fmin = 1 / (2 * np.pi * d_fmin)
        t_fmax = 1 / (2 * np.pi * d_fmax)
        ax.axvline(t_fmin, c='y', alpha=0.7)
        ax.axvline(t_fmax, c='y', alpha=0.7)
        ax.axvspan(tau_min, t_fmax, hatch='/', color='gray', alpha=0.5)
        ax.axvspan(t_fmin, tau_max, hatch='/', color='gray', alpha=0.5,
                   label='area outside data range')

        ax.set_xlabel(r'$\tau~[s]$')
        ax.set_ylabel(r'$log_{10}(m)$')

        title_string = r'$\lambda:$ '
        for lam in it.lams:
            if(type(lam) == list):
                lam = lam[0]
            if(isinstance(lam, float) or isinstance(lam, int)):
                title_string += '{0} '.format(lam)
            else:
                pass
                # individual lambdas
                # title_string += '{0} '.format(
                #     lam[m_indices[nr], m_indices[nr]])
        ax.set_title(title_string)

    def _plot_rmag_rpha(self, nr, axes, orig_data, fit_data, it):
        rmag_rpha_orig = sip_convert.convert(
            it.Data.obj.data_format,
            'rmag_rpha',
            orig_data
        )

        rmag_rpha_fit = sip_convert.convert(
            it.Data.obj.data_format,
            'rmag_rpha',
            fit_data
        )

        frequencies = it.Data.obj.frequencies

        ax = axes[0]
        ax.semilogx(frequencies, rmag_rpha_orig[:, 0], '.', color='k')
        ax.semilogx(frequencies, rmag_rpha_fit[:, 0], '-', color='k')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r'$|\rho|~[\Omega m]$')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))

        ax = axes[1]
        ax.semilogx(frequencies, -rmag_rpha_orig[:, 1], '.', color='k')
        ax.semilogx(frequencies, -rmag_rpha_fit[:, 1], '-', color='k')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r'$-\phi~[mrad]$')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))
        ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(5))
        self._mark_tau_parameters_f(nr, ax, it)

    def _plot_cre_cim(self, nr, axes, orig_data, fit_data, it):
        cre_cim_orig = sip_convert.convert(it.Data.obj.data_format,
                                           'cre_cim',
                                           orig_data)

        cre_cim_fit = sip_convert.convert(it.Data.obj.data_format,
                                          'cre_cim',
                                          fit_data)
        frequencies = it.Data.obj.frequencies
        ax = axes[0]
        ax.semilogx(frequencies, cre_cim_orig[:, 0], '.', color='gray')
        ax.semilogx(frequencies, cre_cim_fit[:, 0], '-', color='gray')
        # ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\sigma'~[S/m]$", color='gray')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        ax = axes[1]
        ax.semilogx(frequencies, cre_cim_orig[:, 1], '.', color='gray',
                    label='data')
        ax.semilogx(frequencies, cre_cim_fit[:, 1], '-', color='gray',
                    label='fit')
        # ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\sigma''~[S/m]$", color='gray')
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

    def _plot_rre_rim(self, nr, axes, orig_data, fit_data, it):
        rre_rim_orig = sip_convert.convert(it.Data.obj.data_format,
                                           'rre_rim',
                                           orig_data)

        rre_rim_fit = sip_convert.convert(it.Data.obj.data_format,
                                          'rre_rim',
                                          fit_data)
        frequencies = it.Data.obj.frequencies
        ax = axes[0]
        ax.semilogx(frequencies, rre_rim_orig[:, 0], '.', color='k')
        ax.semilogx(frequencies, rre_rim_fit[:, 0], '-', color='k')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\rho'~[\Omega m]$")
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        ax = axes[1]
        ax.semilogx(frequencies, -rre_rim_orig[:, 1], '.', color='k',
                    label='data')
        ax.semilogx(frequencies, -rre_rim_fit[:, 1], '-', color='k',
                    label='fit')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel(r"$-\rho''~[\Omega m]$")
        ax.xaxis.set_major_locator(mpl.ticker.LogLocator(numticks=4))

        self._mark_tau_parameters_f(nr, ax, it)

        # legend is created from first plot
        if nr == 0:
            ax.legend(loc="upper center", ncol=5,
                      bbox_to_anchor=(0, 0, 1, 1),
                      bbox_transform=ax.get_figure().transFigure)
            leg = ax.get_legend()
            ltext = leg.get_texts()
            plt.setp(ltext, fontsize='6')

    def _mark_tau_parameters_tau(self, nr, ax, it):
        # mark relaxation time parameters
        # mark tau_peak
        for index in range(1, 3):
            try:
                tpeak = it.stat_pars['tau_peak{0}'.format(index)][nr]
                if(not np.isnan(tpeak)):
                    ax.axvline(x=10**tpeak, color='k', label=r'$\tau_{peak}^' +
                               '{0}'.format(index) + '$',
                               linestyle='dashed')
            except:
                pass

        try:
            ax.axvline(x=10**it.stat_pars['tau_50'][nr], color='g',
                       label=r'$\tau_{50}$')
        except:
            pass

        try:
            ax.axvline(x=10**it.stat_pars['tau_mean'][nr], color='c',
                       label=r'$\tau_{mean}$')
        except:
            pass

    def _mark_tau_parameters_f(self, nr, ax, it):
        # mark relaxation time parameters
        # mark tau_peak
        for index in range(1, 3):
            try:
                fpeak = it.stat_pars['f_peak{0}'.format(index)][nr]
                if(not np.isnan(fpeak)):
                    ax.axvline(x=fpeak, color='k', label=r'$\tau_{peak}^' +
                               '{0}'.format(index) + '$',
                               linestyle='dashed')
            except:
                pass

        try:
            ax.axvline(x=it.stat_pars['f_50'][nr], color='g',
                       label=r'$\tau_{50}$')
        except:
            pass

        try:
            ax.axvline(x=it.stat_pars['f_mean'][nr], color='c',
                       label=r'$\tau_{mean}$')
        except:
            pass
