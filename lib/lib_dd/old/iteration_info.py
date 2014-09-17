#!/usr/bin/python
from crlab_py.mpl import *
mpl.rcParams['font.size'] = 8
import numpy as np
import os
import scipy.signal as sp


class iteration_info():
    """
    Stores and computes information of one inversion iteration
    """
    def __init__(self, dd_obj):
        self.nr = None   #: iteration number
        self.errors = None  #: data weighting factors
        self.lam = None   #: regularization parameter lambda

        # stores the modelled real data for the active parameters
        self.re = None
        # stores the modelled imaginary data for the active parameters
        self.mim = None
        self.re_orig = None  #: original real data
        self.mim_orig = None  #: minus original imaginary data
        # root mean square of real data
        # :math:`\sqrt{
        # \frac{1}{N} \sum \left| \frac{Re - f_{re}(m)}{\epsilon}\right|
        # }^2`
        self.rms_re = None
        # root mean square of imaginary data
        # :math:`\sqrt{
        # \frac{1}{N} \sum \left| \frac{Im - f_{im}(m)}{\epsilon}\right|
        # }^2`
        self.rms_im = None
        self.rms = None   #: rms of both real and imaginary parts
        # rms without errors:
        # :math:`\sqrt{\frac{1}{N} \left| d - f|^2 \right|^2}`
        self.rms_no_err = None
        self.parameters = None
        self.m_tot = None
        self.m_tot_n = None
        self.tau_50 = None
        self.tau_mean = None
        self.tau_peak = None
        self.fit_results = {}  # stores fit results
        self.omega = None

        self.dd_obj = dd_obj
        self.set_labels()

    def set_labels(self):
        # Set default labels for fit results
        labels = {}
        labels['rho0'] = r'$\rho_0~(\Omega m)$'
        labels['m_tot'] = r'$m_{tot}$'
        labels['m_tot_n'] = r'$m^n_{tot}$'
        labels['tau_50'] = r'$\tau_{50}$'
        labels['tau_mean'] = r'$\tau_{mean}$'
        labels['tau_peak'] = r'$\tau_{peak}$'
        self.labels = labels

    def compute(self, re_orig, mim_orig, nr, parameters, s, omega, errors,
                lam):
        """
        Compute and store information of this iteration

        Parameters
        ----------
        re_orig: real part spectrum of data
        mim_orig: -imaginary part spectrum of data
        nr: number of spectrum (i.e. pixel of the image)
        parmeters: [rho0, m_i] fit results
        s: log10(tau) distribution corresponding to m_i values
        omega: angular freaquency of data spectrum
        errors: weighting factors
        lam: Lambda used for this iteration
        """
        self.lam = lam
        self.re_orig = re_orig
        self.mim_orig = mim_orig
        re, mim = self.dd_obj.forward_re_mim(omega, parameters, s)
        self.re = re
        self.mim = mim
        self.parameters = np.copy(parameters)
        self.s = np.copy(s)
        self.errors = errors
        self.omega = omega
        self.frequencies = self.omega / (2 * np.pi)
        self.nr = nr

        # compute rms
        self.diff_re = self.re_orig - self.re
        diff_re_err = self.diff_re / errors[0:errors.shape[0] / 2]
        self.rms_re = np.sqrt(
            1.0 / diff_re_err.shape[0] * np.sum(diff_re_err ** 2))

        self.diff_im = self.mim_orig - self.mim
        diff_im_err = self.diff_im / errors[errors.shape[0] / 2:]
        self.rms_im = np.sqrt(
            1.0 / diff_im_err.shape[0] * np.sum(diff_im_err ** 2))

        self.rms_re_no_err = np.sqrt(
            1.0 / self.diff_re.shape[0] * np.sum(self.diff_re ** 2))
        self.rms_im_no_err = np.sqrt(
            1.0 / self.diff_im.shape[0] * np.sum(self.diff_im ** 2))

        summed = np.sum(diff_re_err ** 2) + np.sum(diff_im_err ** 2)
        N = 1.0 / (omega.shape[0] * 2)
        rms = np.sqrt(N * summed)

        self.rms = rms

        self.rms_no_err = np.sqrt(
            N * (np.sum(self.diff_re ** 2) + np.sum(self.diff_im ** 2)))

        # compute m_tot
        self.m_tot = np.sum(10 ** (self.parameters[1:]))
        # m_tot_n = m_tot / rho0
        self.m_tot_n = self.m_tot / 10 ** self.parameters[0][0]

        # log10
        self.tau_mean = np.sum(self.s[:, np.newaxis] *
                               10 ** parameters[1:]) / (self.m_tot)

        # compute tau_50
        g_tau = 10 ** parameters[1:] / self.m_tot

        self.cums_gtau = np.cumsum(g_tau)
        index_median = np.argmin(np.abs(self.cums_gtau - 0.5))
        if(np.isnan(index_median)):
            self.tau_50 = np.nan
        else:
            # log10
            self.tau_50 = self.s[index_median]

        # compute m-distribution maxima
        self.m_maxima = sp.argrelmax(self.parameters[1:])[0]
        # reverse so the low-frequency peaks come first
        self.m_maxima = [x for x in reversed(self.m_maxima)]

        self.s_peaks = self.s[self.m_maxima]
        self.f_peaks = 1 / (2 * np.pi * 10 ** self.s_peaks)

        self.fit_results['rho0'] = parameters[0]
        self.fit_results['m_tot'] = self.m_tot
        self.fit_results['m_tot_n'] = self.m_tot_n
        self.fit_results['tau_50'] = self.tau_50
        self.fit_results['tau_mean'] = self.tau_mean
        self.fit_results['tau_peak'] = self.s_peaks

    def plot_m_diff(self, m_orig, suffix=''):
        """
        For a given set of original chargeability values, plot the difference
        to the file 'm_diff_it_{0}_{1}.png'.format(suffix)
        """
        m_diff = 10 ** m_orig[:, np.newaxis] - 10 ** self.parameters[1:]
        m_diff_rel = (10 ** m_orig[:, np.newaxis] -
                      10 ** self.parameters[1:]) / 10 ** m_orig[:, np.newaxis]

        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.plot(m_diff)
        ax.set_xlabel('Chargeability index')
        ax.set_ylabel(r'$m_{orig} - m_{fit}$')

        ax2 = ax.twinx()
        ax2.plot(m_diff_rel, 'r')
        ax2.set_ylabel('r$(m_{orig} - m_{fit})/m_{orig}$', color='r')

        fig.subplots_adjust(left=0.15, right=0.9)
        filename = 'm_diff_{1}_it_{0}.png'.format(self.nr, suffix)
        fig.savefig(filename, dpi=300, bbox_inches='tight')

    def plot_sensitivities(self, ax_covf, ax_covm, ax_covm_special):
        """
        Plot covf and covm to the two axes provided
        """
        del_mim_del_m = self.dd_obj.del_mim_del_chargeability(
            self.omega, self.parameters, self.s)

        #nr_m = del_mim_del_m.shape[1]
        #mtot = np.sum(self.parameters[1:])

        covf = np.abs(del_mim_del_m).sum(axis=1)
        covf /= np.max(covf)

        covm = np.abs(del_mim_del_m).sum(axis=0)
        covm /= np.max(covm)

        ax_covf.semilogx(self.omega / (2 * np.pi), covf)
        ax_covf.set_xlabel('Frequency (Hz)')
        ax_covf.set_ylabel('Covf')
        ax_covf.set_xlim([np.min(self.omega / (2 * np.pi)),
                          np.max(self.omega / (2 * np.pi))])

        ax_covm.plot(self.s, covm)
        ax_covm.set_xlabel(r'$s = log_{10}(\tau)$')
        ax_covm.set_ylabel('Covm')
        ax_covm.set_xlim([np.min(self.s), np.max(self.s)])
        ax_covm.invert_xaxis()

        # for the smallest s/m value, plot the whole frequency series
        ax_covm_special.semilogx(self.omega / (2 * np.pi),
                                 np.abs(del_mim_del_m[:, 0]))
        ax_covm_special.set_xlabel('Frequency (Hz)')
        ax_covm_special.set_title('s: {0:04}'.format(self.s[0]))

    def _plot_re(self, ax):
        """
        Plot real resistivity to axis object
        """
        ax.semilogx(self.frequencies, self.re_orig, 'b.', label='data')
        ax.semilogx(self.frequencies, self.re, 'r-', label='fit')
        ax.set_xlim([np.min(self.frequencies), np.max(self.frequencies)])
        ax.set_ylabel(r'$Re(\rho)$')
        ax.set_xlabel('Frequency (Hz)')
        ax.legend(loc='best')

        # set ylimits
        miny = np.min((np.min(self.re_orig), np.min(self.re)))
        miny -= 0.05 * miny  # go 5% down
        maxy = np.max((np.max(self.re_orig), np.max(self.re)))
        maxy += 0.05 * maxy  # go 5% up
        ax.set_ylim([miny, maxy])

    def plot_spectrum(self, suffix='', prefix='', output_dir='.'):
        """
        Plot re,re_orig; im,mim_orig to the file
        spectrum_it_{0:03}_{suffix}.png

        Parameters
        ----------
        suffix: string to append to output filename
        prefix: string to prepend to the output filename
        output_dir: Output directory for plots

        """
        fig, [[ax1, ax2], [ax3, ax4], [ax5, ax6], [ax7, ax8], [ax9, ax10]] =\
            plt.subplots(5, 2, figsize=(8, 8))

        self.plot_sensitivities(ax2, ax4, ax6)
        self._plot_re(ax1)

        ax3.semilogx(self.frequencies, self.mim_orig, 'b.', label='data')
        ax3.semilogx(self.frequencies, self.mim, 'r-', label='fit')
        ax3.set_xlim([np.min(self.frequencies), np.max(self.frequencies)])

        # mark frequencies corresponding to tau_mean and tau_50
        f_mean = 1.0 / (2.0 * np.pi * 10 ** self.tau_mean)
        f_50 = 1.0 / (2.0 * np.pi * 10 ** self.tau_50)
        ax3.axvline(f_mean, color='r')
        ax3.axvline(f_50, color='g')
        ax3.set_title('red: mean, green: median')
        ax3.set_ylabel(r"$-\rho''~(\Omega m)$")
        ax3.set_xlabel('Frequency (Hz)')

        for f in self.f_peaks:
            ax3.axvline(f, color='b')

        # set ylimits
        miny = np.min((np.min(self.mim_orig), np.min(self.mim)))
        if(miny == 0):
            miny = -0.05
        else:
            miny -= 0.05 * miny  # go 5% down

        maxy = np.max((np.max(self.mim_orig), np.max(self.mim)))
        maxy += 0.05 * maxy  # go 5% up

        ax3.set_ylim([miny, maxy])

        # phase
        phase_orig = np.arctan(-self.mim_orig / self.re_orig) * 1000
        phase = np.arctan(-self.mim / self.re) * 1000

        ax5.semilogx(self.frequencies, -phase_orig, 'b.', label='data')
        ax5.semilogx(self.frequencies, -phase, 'r-', label='fit')
        ax5.set_xlim([np.min(self.frequencies), np.max(self.frequencies)])
        ax5.set_ylabel('-Phase (mrad)')
        ax5.set_xlabel('Frequency (Hz)')
        for f in self.f_peaks:
            ax5.axvline(f, color='b')

        # s-m distribution
        ax7.plot(self.s, self.parameters[1:], '.-')
        ax7.set_xlim([np.min(self.s), np.max(self.s)])
        #ax.axhline(y=np.log10(self.m_tot), color='r')
        ax7.set_title('log10(m\_tot): {0}'.format(np.log10(self.m_tot)))
        ax7.axvline(self.tau_mean, color='r')
        ax7.axvline(self.tau_50, color='g')

        # plot maxima
        for peak in self.s_peaks:
            ax7.axvline(peak, color='b')

        ax7.set_xlabel(r'$log_{10}(\tau)$')
        ax7.set_ylabel(r'$g = log_{10}(m)$')
        ax7.invert_xaxis()

        ax9.plot(self.s, self.cums_gtau)
        ax9.set_xlim([np.min(self.s), np.max(self.s)])
        ax9.set_ylabel('cums\_gtau')

        fig.subplots_adjust(hspace=0.9, left=0.15)
        filename = output_dir + os.sep
        filename += '{2}spectrum_{1}_it_{0:03}.png'.format(self.nr, suffix,
                                                           prefix)
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close(fig)
