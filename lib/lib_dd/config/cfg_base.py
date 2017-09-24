# *-* coding: utf-8 *-*
import logging
from optparse import OptionParser
import platform
import os

import lib_dd.version as version
import NDimInv.data_weighting as data_weighting


class cfg_base(dict):

    class cfg_obj(object):
        def __init__(self, type, help, cmd_dict, possible_values=None):
            self.type = type
            self.help_text = help
            self.cmd_dict = cmd_dict
            self.possible_values = possible_values

    def __init__(self):
        self.web_order = [
            'nr_terms_decade',
        ]

        # these options will not be shown in the web interface
        self.web_blacklist = [
            'version',
            'frequency_file',
            'data_file',
            'output_dir',
            'nr_cores',
            'silent',
            'output_format',
            'use_tmp',
            'data_format',
        ]

        # will store the command line parser object
        self.cmd_parser = None
        # store the cfg objects here
        self.cfg = {}

        # add the actual configs here
        self['frequency_file'] = 'frequencies.dat'
        self.cfg['frequency_file'] = self.cfg_obj(
            type='string',
            help='Frequency file',
            cmd_dict={
                'short': '-f',
                'long': '--frequency_file',
                'metavar': 'FILE',
            }
        )

        self['ignore_frequencies'] = None
        self.cfg['ignore_frequencies'] = self.cfg_obj(
            type='string',
            help=''.join((
                'Frequency ids to ignore, example:',
                "12,13,14",
                '. Starts with index 0.',
            )),
            cmd_dict={
                'short': None,
                'long': '--ignore',
                'metavar': 'STRING',
            },

        )

        self['data_fmin'] = None
        self.cfg['data_fmin'] = self.cfg_obj(
            type='float',
            help=''.join((
                'Ignore frequencies below this value',
            )),
            cmd_dict={
                'short': None,
                'long': '--fmin',
                'metavar': 'FLOAT',
            },
        )

        self['data_fmax'] = None
        self.cfg['data_fmax'] = self.cfg_obj(
            type='float',
            help=''.join((
                'Ignore frequencies above this value',
            )),
            cmd_dict={
                'short': None,
                'long': '--fmax',
                'metavar': 'FLOAT',
            },
        )

        self['plot_spectra'] = False
        self.cfg['plot_spectra'] = self.cfg_obj(
            type='bool',
            help='Plot final iterations (default: False)',
            cmd_dict={
                'short': '-p',
                'long': '--plot',
                'action': 'store_true',
            },

        )

        self['data_file'] = 'data.dat'
        self.cfg['data_file'] = self.cfg_obj(
            type='string',
            help='data file',
            cmd_dict={
                'short': '-d',
                'long': '--data_file',
                'metavar': 'FILE'
            },
        )

        self['data_format'] = 'rmag_rpha'
        self.cfg['data_format'] = self.cfg_obj(
            type='string',
            help=''.join((
                'Input data format, possible values are: ',
                'rmag_rpha, lnrmag_rpha, log10rmag_rpha, rmag_rpha, ',
                ' rre_rim rre_rmim, cmag_cpha, cre_cim, cre_cmim. ',
                '"r" stands for resistance/',
                'resistivity, and "c" stands for conductance/',
                'conductivity',
            )),
            cmd_dict={
                'short': None,
                'long': '--data_format',
                'metavar': 'FORMAT',
            },
            possible_values=[
                'rmag_rpha',
                'cre_cim',
            ],
        )

        self['nr_terms_decade'] = 20
        self.cfg['nr_terms_decade'] = self.cfg_obj(
            type='int',
            help="Number of polarization terms per frequency decade",
            cmd_dict={
                'short': '-n',
                'long': '--nr_terms',
                'metavar': 'INT',
            },
        )

        self['output_dir'] = 'results'
        self.cfg['output_dir'] = self.cfg_obj(
            type='string',
            help='Output directory',
            cmd_dict={
                'short': '-o',
                'long': '--output',
                'metavar': 'DIR',
            }
        )

        self['plot_spectra'] = False
        self.cfg['plot_spectra'] = self.cfg_obj(
            type='bool',
            help='Plot final iterations',
            cmd_dict={
                'short': '-p',
                'long': '--plot',
                'action': 'store_true',
            },
        )

        self['plot_reg_strength'] = False
        self.cfg['plot_reg_strength'] = self.cfg_obj(
            type='bool',
            help='Plot regularization strengths of final iterations',
            cmd_dict={
                'short': None,
                'long': '--plot_reg_strength',
                'action': 'store_true',
            },
        )

        self['plot_it_spectra'] = False
        self.cfg['plot_it_spectra'] = self.cfg_obj(
            type='bool',
            help='Plot spectra of each iteration',
            cmd_dict={
                'short': '-i',
                'long': '--plot_its',
                'action': 'store_true',
            }
        )

        self['silent'] = False
        self.cfg['silent'] = self.cfg_obj(
            type='bool',
            help='Do not plot any logs to STDOUT',
            cmd_dict={
                'short': None,
                'long': '--silent',
                'action': 'store_true',
            }
        )

        self['use_tmp'] = False
        self.cfg['use_tmp'] = self.cfg_obj(
            type='bool',
            help=''.join((
                "Create the output in a temporary directory and ",
                "later move it later to its destination",
            )),
            cmd_dict={
                'short': None,
                'long': '--tmp',
                'action': 'store_true',
            }
        )

        self['tausel'] = 'data_ext'
        self.cfg['tausel'] = self.cfg_obj(
            type='string',
            help=''.join((
                "Tau selection strategy:\ndata: Use ",
                "data frequency limits for tau selection\ndata_ext ",
                "(default): Extend tau ranges by one frequency decade ",
                "compared to the 'data' strategy. Factors can be set ",
                "for the low and high frequency by separating with a ",
                "',': LEFT,RIGHT, e.g. '10,100'"
            )),
            cmd_dict={
                'short': None,
                'long': '--tausel',
                'metavar': 'STRATEGY',
            },
        )

        self['norm'] = None
        self.cfg['norm'] = self.cfg_obj(
            type='float',
            help=''.join((
                'Normalize lowest frequency real part to this value',
            )),
            cmd_dict={
                'short': None,
                'long': '--norm',
                'metavar': 'FLOAT',
            },
        )

        self['plot_lambda'] = None
        self.cfg['plot_lambda'] = self.cfg_obj(
            type='int',
            help=''.join((
                "Plot the l-curve for a selected iteration. ",
                "WARNING: This only plots the l-curve and does not ",
                "use it in the inversion process. Use -1 for last ",
                "iteration.",
            )),
            cmd_dict={
                'short': None,
                'long': '--plot_lcurve',
                'metavar': 'INT',
            },
        )

        self['max_iterations'] = 20
        self.cfg['max_iterations'] = self.cfg_obj(
            type='int',
            help='Maximum number of iterations',
            cmd_dict={
                'short': None,
                'long': '--max_it',
                'metavar': 'INT',
            },
        )

        self['version'] = False
        self.cfg['version'] = self.cfg_obj(
            type='bool',
            help='Print version information',
            cmd_dict={
                'short': '-v',
                'long': '--version',
                'action': 'store_true',
            },
        )

        self['output_format'] = 'ascii_audit'
        self.cfg['output_format'] = self.cfg_obj(
            type='string',
            help='Output format(ascii| ascii_audit)',
            cmd_dict={
                'short': None,
                'long': '--output_format',
                'metavar': 'STRING',
            },
        )

        self['data_weighting'] = 're_vs_im'
        self.cfg['data_weighting'] = self.cfg_obj(
            type='string',
            help='Data weighting scheme to use.',
            cmd_dict={
                'short': None,
                'long': '--data_weighting',
                'metavar': 'SCHEME',
            },
            possible_values=sorted(data_weighting.functions.keys()),
        )

    def get_cmd_parser(self):
        parser = OptionParser()
        for key in sorted(self.cfg.keys()):
            helptext = ''.join((
                self.cfg[key].help_text,
                ' (default: ',
                '{0}'.format(self[key]) + ')'
            ))
            opts = {
                'type': self.cfg[key].type,
                'dest': key,
                'help': helptext,
                'default': self[key],
            }

            # if self[key] is None:
            #     opts['default'] = None

            for label in ('action', 'metavar'):
                if label in self.cfg[key].cmd_dict:
                    opts[label] = self.cfg[key].cmd_dict[label]

            if 'action' in opts:
                del(opts['type'])

            if self.cfg[key].cmd_dict['short'] is not None:
                lso = [self.cfg[key].cmd_dict['short'], ]
            else:
                lso = []

            lso.append(self.cfg[key].cmd_dict['long'])

            parser.add_option(
                *lso,
                **opts
            )

        self.cmd_parser = parser
        return parser

    def parse_cmd_arguments(self):
        """
        Parse the command line arguments and update the dictionary
        """
        if self.cmd_parser is None:
            self.get_cmd_parser()

        (options, args) = self.cmd_parser.parse_args()

        # multi threading does not work on Windows
        if platform.system() == "Windows":
            options.nr_cores = 1

        # print version information if requested
        if options.version:
            logging.info(version._get_version_numbers())
            exit()

        # update the self-dict with the new values
        for key in self.keys():
            self[key] = getattr(options, key)

        return options

    def split_options_base(self):
        """
        Prepare dicts containing preparation and inversion settings common to
        all cdd_* programs
        """
        prep_opts = {key: self[key] for key in (
            'plot_it_spectra',
            'plot_reg_strength',
            'output_dir',
            'data_format',
            'plot_lambda',
        )
        }
        # prep_opts['plot_it_spectra'] = options.plot_it_spectra
        prep_opts['plot'] = self['plot_spectra']
        # prep_opts['plot_reg_strength'] = options.plot_reg_strength
        # prep_opts['output_dir'] = options.output_dir
        # prep_opts['data_format'] = options.data_format
        # prep_opts['plot_lambda'] = options.plot_lambda

        inv_opts = {key: self[key] for key in (
            'tausel',
            'max_iterations',
            'data_weighting',
        )
        }
        # inv_opts['tausel'] = options.tausel
        inv_opts['Nd'] = self['nr_terms_decade']
        # inv_opts['max_iterations'] = options.max_iterations

        return prep_opts, inv_opts

    def check_input_files(self, additional_files=[]):
        """Check if the input files exist. In addition to the base files for
        data and frequency, also test for all filenames stored in the
        corresponding attributes as provided by the extra list.
        """
        none_missing = True
        base_files = ['frequency_file', 'data_file']
        for attr in base_files + additional_files:
            filename = self[attr]
            if not os.path.isfile(filename):
                logging.info(
                    'Filename not found for attribute {0}: {1}'.format(
                        attr, filename
                    )
                )
                none_missing = False
        else:
            if not none_missing:
                exit()

        # check if output directory already exists
        if os.path.isdir(self['output_dir']):
            raise IOError(
                'Output directory already exists. Please choose another ' +
                'output directory, or delete the existing one.')

    def __repr__(self):
        output = '\n'
        output += 'CCD configuration:\n'
        for key in sorted(self.keys()):
            output += 'Entry {0}:{1}\n'.format(key, self[key])

        output += '--- end ---'

        return output
