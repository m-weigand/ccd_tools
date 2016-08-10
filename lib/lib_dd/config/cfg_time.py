import cfg_base


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

if __name__ == '__main__':
    options = cfg_time()
    options.parse_cmd_arguments()
