import numpy as np

import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()


class _plot_stats(object):

    def plot_stats(self, prefix):
        """
        Plot various statistics. Requires self.stat_pars to be present.
        """
        self._plot_coverages(prefix)

    def _plot_coverages(self, prefix):
        f = self.frequencies
        fig, axes = plt.subplots(2, 2, figsize=(5, 4))
        # plot data/fig
        pars = np.hstack((self.stat_pars['rho0'], self.stat_pars['m_i']))
        rre_rim = self.forward(pars)
        rre = rre_rim[:, 0]
        rmim = -rre_rim[:, 1]

        ax = axes[0, 0]
        try:
            ax.semilogx(f, rre, '.-', color='k', label='fit')
        except:
            pass
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel(r"$\rho'$")

        ax = axes[1, 0]
        try:
            ax.semilogx(f, rmim, '.-', color='k', label='fit')
        except:
            pass
        ax.set_xlabel('f (Hz)')
        ax.set_ylabel(r"$\rho''$")

        # plot coverages
        ax = axes[0, 1]
        try:
            ax.semilogx(f, self.stat_pars['covf'], '.-', color='k')
        except:
            pass
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Covf')
        ax.set_xlim([f.min(), f.max()])

        ax = axes[1, 1]
        s = self.s
        try:
            ax.plot(s, self.stat_pars['covm'], '.-', color='k')
        except:
            pass
        ax.set_xlabel(r'$s = log_{10}(\tau)$')
        ax.set_ylabel('Covm')
        ax.set_xlim([s.min(), s.max()])
        ax.invert_xaxis()

        fig.tight_layout()
        outfile = '{0}_coverages_nr.png'.format(prefix)
        fig.savefig(outfile)
        fig.clf()
        plt.close(fig)
        del(fig)
