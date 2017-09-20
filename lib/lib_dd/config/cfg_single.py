import lib_dd.config.cfg_base as cfg_base


class cfg_single(cfg_base.cfg_base):
    def __init__(self):
        # call the init function of cfg_base
        super(cfg_single, self).__init__()

        self['nr_cores'] = 1
        self.cfg['nr_cores'] = self.cfg_obj(
            type='int',
            help='Numer of CPU cores to use',
            cmd_dict={
                'short': '-c',
                'long': '--nr_cores',
                'metavar': 'INT',
            }
        )

        self['fixed_lambda'] = None
        self.cfg['fixed_lambda'] = self.cfg_obj(
            type='float',
            help='Use a fixed lambda (integer)',
            cmd_dict={
                'short': None,
                'long': '--lambda',
                'metavar': 'INT',
            }
        )

    def split_options(self):
        """

        Notes
        -----

        Extract options for two groups:

        prep_opts) these options are used to prepare the actual inversion,
        i.e.,  which regularization objects to use. Those options do not enter
        the NDimInv objects

        inv_opts) these options are directly passed through to the NDimInv
        object

        """
        prep_opts, inv_opts = self.split_options_base()

        # now add options specific to dd_single
        prep_opts['lambda'] = self['fixed_lambda']
        prep_opts['nr_cores'] = self['nr_cores']

        return prep_opts, inv_opts
