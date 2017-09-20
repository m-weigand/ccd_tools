import lib_dd.config.cfg_base as cfg_base


class cfg_time(cfg_base.cfg_base):

    def __init__(self):
        super(cfg_time, self).__init__()

        self['times'] = 'times.dat'
        self.cfg['times'] = self.cfg_obj(
            type='string',
            help='Time index file',
            cmd_dict={
                'short': None,
                'long': '--times',
                'metavar': 'FILE',
            }
        )

        self['freq_lambda'] = None
        self.cfg['freq_lambda'] = self.cfg_obj(
            type='float',
            help='Use a fixed lambda for the tau regularization',
            cmd_dict={
                'short': None,
                'long': '--f_lambda',
                'metavar': 'FLOAT',
            }
        )

        self['time_rho0_lambda'] = 0
        self.cfg['time_rho0_lambda'] = self.cfg_obj(
            type='float',
            help='Fixed time regularization lambda for rho0',
            cmd_dict={
                'short': None,
                'long': '--trho0_lambda',
                'metavar': 'FLOAT',
            }
        )

        self['time_m_i_lambda'] = 0
        self.cfg['time_m_i_lambda'] = self.cfg_obj(
            type='float',
            help='Fixed time regularization lambda for chargeabilities m_i',
            cmd_dict={
                'short': None,
                'long': '--tm_i_lambda',
                'metavar': 'FLOAT',
            }
        )

        self['individual_lambdas'] = False
        self.cfg['individual_lambdas'] = self.cfg_obj(
            type='bool',
            help="Use individual lambdas for f-regularization",
            cmd_dict={
                'short': None,
                'long': '--ind_lams',
                'action': 'store_true',
            }
        )

        self['f_lam0'] = None
        self.cfg['f_lam0'] = self.cfg_obj(
            type='float',
            help='Initial lambda for f-regularization',
            cmd_dict={
                'short': None,
                'long': '--lam0',
                'metavar': 'FLOAT',
            }
        )

        self['trho0_first_order'] = False
        self.cfg['trho0_first_order'] = self.cfg_obj(
            type='bool',
            help=''.join((
                "Use first order smoothing for rho_0 ",
                "(instead of second order smoothing)"
            )),
            cmd_dict={
                'short': None,
                'long': '--trho0_first_order',
                'action': 'store_true',
            },
        )

        self['time_weighting_rho0'] = False
        self.cfg['time_weighting_rho0'] = self.cfg_obj(
            type='bool',
            help=''.join((
                "Use time-weighting (only in combination with",
                " --trho0_first_order)",
            )),
            cmd_dict={
                'short': None,
                'long': '--tw_rho0',
                'action': 'store_true',
            },
        )

        self['tmi_first_order'] = False
        self.cfg['tmi_first_order'] = self.cfg_obj(
            type='bool',
            help=''.join((
                "Use first order smoothing for m_i ",
                "(instead of second order smoothing)",
            )),
            cmd_dict={
                'short': None,
                'long': '--tmi_first_order',
                'action': 'store_true',
            }
        )

        self['time_weighting_mi'] = False
        self.cfg['time_weighting_mi'] = self.cfg_obj(
            type='bool',
            help=''.join((
                "Use time-weighting (only in combination with ",
                "--tmi_first_order)",
            )),
            cmd_dict={
                'short': None,
                'long': '--tw_mi',
                'action': 'store_true',
            }
        )

    def split_options(self):
        """
        Extract options for two groups:
        1) prep_opts : these options are used to prepare the actual inversion,
        i.e.  which regularization objects to use
        2) inv_opts : these options are directly passed through to the NDimInv
        object
        """
        prep_opts, inv_opts = self.split_options_base()

        prep_opts['f_lambda'] = self['freq_lambda']
        prep_opts['t_rho0_lambda'] = self['time_rho0_lambda']
        prep_opts['t_m_i_lambda'] = self['time_m_i_lambda']
        prep_opts['individual_lambdas'] = self['individual_lambdas']
        prep_opts['f_lam0'] = self['f_lam0']
        prep_opts['trho0_first_order'] = self['trho0_first_order']
        prep_opts['tmi_first_order'] = self['tmi_first_order']
        prep_opts['time_weighting_rho0'] = self['time_weighting_rho0']
        prep_opts['time_weighting_mi'] = self['time_weighting_mi']
        return prep_opts, inv_opts


if __name__ == '__main__':
    options = cfg_time()
    options.parse_cmd_arguments()
