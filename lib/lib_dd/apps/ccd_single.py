# jupyter notebook app for ccd_single
import os
import logging
import tempfile
import shutil
import datetime

import ipywidgets
import ipywidgets as widgets
import IPython
from IPython.core.display import display, HTML
import numpy as np

import NDimInv.plot_helper
plt, mpl = NDimInv.plot_helper.setup()
import lib_dd.decomposition.ccd_single as ccd_single
import lib_dd.config.cfg_single as cfg_single
import lib_dd.plot


class ccd_single_app(object):
    def __init__(self, frequency_file, data_file, no_logging=False):
        self._setup_logger(disabled=no_logging)
        self._check_versions()
        self.style = {'description_width': 'initial'}
        self.frequencies = np.loadtxt(frequency_file)
        self.data = np.loadtxt(data_file)
        self.widgets = {}
        # items to be arranged in a VBox later
        self.items = []
        # store containers for parameter groups here
        self.containers = {}
        self.vbox = None
        self.print_data_summary()

        # we generate links to the online documentation. To simplify things,
        # use the url-prefix from here
        self.url = 'https://m-weigand.github.io/ccd_tools/doc_ccd/'
        self._init_app_widgets()

    def _check_versions(self):
        if int(ipywidgets.__version__[0]) < 7:
            raise Exception(
                'ipywidgets version is too old. Need at least major ' +
                'version number 7, is: {0}'.format(ipywidgets.__version__)
            )

    def _setup_logger(self, disabled=False):
        logging.basicConfig(level=logging.INFO)
        if disabled:
            logging.disable(100)

    def enable_logger(self):
        logging.disable(logging.NOTSET)

    def disable_logger(self):
        logging.disable(100)

    def print_data_summary(self):
        """Print a summary of the data, e.g., number of frequencies, min/max
        values
        """
        summary = []
        # frequency statistics
        summary.append(
            'Number of frequencies: {0}'.format(len(self.frequencies))
        )
        summary.append(
            'Minimum frequency: {0} Hz'.format(self.frequencies.min())
        )
        summary.append(
            'Maximum frequency: {0} Hz'.format(self.frequencies.max())
        )

        # data statistics
        summary.append('')
        summary.append('number of SIP spectra: {0}'.format(
            np.atleast_2d(self.data).shape[0])
        )

        summary.append('<hr />')
        display(HTML('<h2>Data summary</h2>'))
        display(HTML('<br />'.join(summary)))

    def _help_url(self, postfix):
        help_str = '<a href="{0}/{1}"'.format(
            self.url, postfix
        ) + ' target="_blank">Help</a>'
        return help_str

    def _add_dformat_selection(self):
        w_dformat = widgets.Dropdown(
            options=[
                'rmag_rpha',
                'lnrmag_rpha',
                'log10rmag_rpha',
                'rmag_rpha',
                'rre_rim',
                'rre_rmim',
                'cmag_cpha',
                'cre_cim',
                'cre_cmim',
            ],
            value='rmag_rpha',
            description='Input data format:',
            style=self.style,
        )
        h_dformat = widgets.HTML(
            value=self._help_url('data_formats.html#input-data-formats')
        )
        hb_dformat = widgets.HBox(
            children=[w_dformat, h_dformat]
        )
        self.widgets['data_format'] = w_dformat
        self.items.append(hb_dformat)

    def _add_condres_selection(self):
        w_condres = widgets.Dropdown(
            options={
                'resistivity formulation': '0',
                'conductivity formulation': '1',
            },
            value='0',
            description='Type of kernel:',
            style=self.style,
        )
        h_condres = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#" ' +
            'target="_blank">Help</a>',
        )
        hb_condres = widgets.HBox(
            children=[w_condres, h_condres]
        )
        self.widgets['type_formulation'] = w_condres
        self.items.append(hb_condres)

    def _add_flimits(self):
        w_fmin = widgets.FloatText(
            value=self.frequencies.min(),
            description='Frequency min:',
            style=self.style,
        )
        w_fmax = widgets.FloatText(
            value=self.frequencies.max(),
            description='Frequency max:',
            style=self.style,
        )

        h_fminmax = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#" ' +
            'target="_blank">Help</a>',
        )
        hb_fminmax = widgets.HBox(
            children=[w_fmin, w_fmax, h_fminmax]
        )
        self.widgets['fmin'] = w_fmin
        self.widgets['fmax'] = w_fmax
        self.items.append(hb_fminmax)
        self.containers['fminmax'] = hb_fminmax

        def fminmax_change(change):
            if change['name'] == 'value':
                fmin = self.widgets['fmin'].value
                fmax = self.widgets['fmax'].value

                # hide all frequencies in fignore that are outside the range
                fign = self.widgets['fignore']
                indices = np.where(
                    (fmin <= self.frequencies) &
                    (self.frequencies <= fmax)
                )[0]
                for nr, wdg in enumerate(fign):
                    if nr in indices:
                        wdg.layout.visibility = 'visible'
                    else:
                        wdg.layout.visibility = 'hidden'

        w_fmin.observe(fminmax_change)
        w_fmax.observe(fminmax_change)

    def _add_fignore(self):
        f_ign = []
        for i in range(0, self.frequencies.size):
            wid = widgets.Checkbox(
                value=True,
                description='{0:.3f} Hz'.format(self.frequencies[i]),
                disabled=False,
                # width=50,
            )
            f_ign.append(wid)
        box_layout = widgets.Layout(
            width='100%',
            flex_flow='row wrap',
            display='inline-flex',
        )
        vb_fignore = widgets.VBox(
            children=f_ign,
            layout=box_layout,
        )
        accordion = widgets.Accordion(
            children=[vb_fignore, ]
        )
        accordion.set_title(0, 'Ignore frequencies')
        if ipywidgets.__version__[0] == '6':
            accordion.selected_index = -1
        else:
            accordion.selected_index = None

        self.widgets['fignore'] = f_ign
        self.items.append(accordion)
        self.containers['fignore'] = accordion

    def _add_max_its(self):
        w_max_its = widgets.IntSlider(
            value=20,
            min=0,
            max=40,
            step=1,
            description='Maximum nr of iterations:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            style=self.style,
        )
        h_max_its = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#" ' +
            'target="_blank">Help</a>',
        )
        hb_max_its = widgets.HBox(
            children=[w_max_its, h_max_its]
        )
        self.widgets['max_its'] = w_max_its
        self.items.append(hb_max_its)
        self.containers['hb_max_its'] = hb_max_its

    def _add_nr_terms(self):
        w_nr_terms = widgets.IntText(
            value=20,
            description='Nr of terms per frequency decade:',
            disabled=False,
            style=self.style,
        )
        h_nr_terms = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#" ' +
            'target="_blank">Help</a>',
        )
        # h_nr_terms = widgets.HTML(
        #     value='<iframe src="https://m-weigand.github.io/ccd_tools/' +
        #     'doc_ccd/"></iframe>',
        # )
        hb_nr_terms = widgets.HBox(
            children=[w_nr_terms, h_nr_terms]
        )
        self.widgets['nr_terms'] = w_nr_terms
        self.items.append(hb_nr_terms)
        self.containers['nr_terms'] = hb_nr_terms

    def _add_tausel(self):
        w_tausel = widgets.Dropdown(
            options=[
                'data_ext',
                'data',
                'individual',
            ],
            value='data_ext',
            description='Range of tau values:',
            style=self.style,
        )
        w_tausel_ind_left = widgets.SelectionSlider(
            options=[1, 10, 100, 1000],
            value=100,
            description='left:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True
        )
        w_tausel_ind_left.layout.visibility = 'hidden'
        w_tausel_ind_right = widgets.SelectionSlider(
            options=[1, 10, 100, 1000],
            value=100,
            description='right:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True
        )
        w_tausel_ind_right.layout.visibility = 'hidden'

        h_tausel = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#" ' +
            'target="_blank">Help</a>',
        )

        hb_tausel = widgets.HBox(
            children=[
                w_tausel, w_tausel_ind_left, w_tausel_ind_right, h_tausel
            ]
        )
        self.widgets['tausel'] = w_tausel
        self.widgets['tausel_left'] = w_tausel_ind_left
        self.widgets['tausel_right'] = w_tausel_ind_right
        self.items.append(hb_tausel)
        self.containers['tausel'] = hb_tausel

        def tausel_change(change):
            if change['name'] == 'value':
                if change['new'] == 'individual':
                    w_tausel_ind_left.layout.visibility = 'visible'
                    w_tausel_ind_right.layout.visibility = 'visible'
                else:
                    w_tausel_ind_left.layout.visibility = 'hidden'
                    w_tausel_ind_right.layout.visibility = 'hidden'

        w_tausel.observe(tausel_change)

    def _add_plot_options(self):
        w_generate_plot = widgets.Checkbox(
            value=True,
            description='Generate plot',
            disabled=False
        )
        w_generate_it_plots = widgets.Checkbox(
            value=False,
            description='Generate plots for all iterations',
            disabled=False,
        )
        w_generate_lcurve = widgets.Checkbox(
            value=False,
            description='Plot lcurve',
            disabled=False
        )
        w_generate_reg_strength = widgets.Checkbox(
            value=False,
            description='Plot regularization strength ',
            disabled=False
        )
        w_generate_output = widgets.Checkbox(
            value=False,
            description='Generate output for download',
            disabled=False
        )
        box_layout = widgets.Layout(
            width='100%',
            flex_flow='row wrap',
            display='inline-flex',
            border='3px solid black',
        )
        hb_output = widgets.VBox(
            [
                w_generate_plot,
                w_generate_it_plots,
                w_generate_lcurve,
                w_generate_reg_strength,
                w_generate_output,
            ],
            layout=box_layout,
        )
        self.widgets['generate_plot'] = w_generate_plot
        self.widgets['generate_output'] = w_generate_output
        self.widgets['generate_it_plots'] = w_generate_it_plots
        self.widgets['generate_lcurve'] = w_generate_lcurve
        self.widgets['generate_reg_strength'] = w_generate_reg_strength

        self.items.append(hb_output)

    def _add_data_weighting(self):
        w_data_weighting = widgets.Dropdown(
            options=[
                're_vs_im',
                'avg_im',
                'avg_im_err',
                'one',
                'all_to_one',
                'rel_abs_error',
            ],
            value='re_vs_im',
            description='Data weighting scheme:',
            style=self.style,
        )
        h_data_weighting = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#data_weighting" ' +
            'target="_blank">Help</a>',
        )
        hb_data_weighting = widgets.HBox(
            children=[w_data_weighting, h_data_weighting]
        )
        self.widgets['data_weighting'] = w_data_weighting
        self.items.append(hb_data_weighting)
        self.containers['data_weighting'] = hb_data_weighting

    def _add_lambda(self):
        w_lambda = widgets.IntText(
            value=10,
            description='Lambda',
            disabled=False,
        )
        h_lambda = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'usage_and_implementation.html#data_weighting" ' +
            'target="_blank">Help</a>',
        )
        hb_lambda = widgets.HBox(
            children=[w_lambda, h_lambda]
        )
        self.widgets['lambda'] = w_lambda
        self.items.append(hb_lambda)

    def _add_c(self):
        w_c = widgets.FloatSlider(
            value=1.0,
            min=0.1,
            max=1.0,
            step=0.1,
            description='C-value:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )
        h_c = widgets.HTML(
            value='<a href="https://m-weigand.github.io/ccd_tools/doc_ccd/' +
            'theory.html" ' +
            'target="_blank">Help</a>',
        )
        hb_c = widgets.HBox(
            children=[w_c, h_c]
        )
        self.widgets['c'] = w_c
        self.items.append(hb_c)

    def _add_normalization(self):
        w_normalization = widgets.Checkbox(
            value=False,
            description='Activate normalization',
            disabled=False,
            style=self.style,
        )
        help_normalization = widgets.HTML(
            value=self._help_url(
                'usage_and_implementation.html#normalization'
            )
        )
        w_norm_value = widgets.FloatText(
            value=10,
            step=1,
            description='Normalization value:',
            disabled=True,
            style=self.style,
        )
        hb_norm = widgets.HBox(
            children=[
                w_normalization,
                w_norm_value,
                help_normalization,
            ],
        )
        self.containers['hb_norm'] = hb_norm

        def use_norm_change(change):
            if change['name'] == 'value':
                if change['new'] is True:
                    w_norm_value.disabled = False
                else:
                    w_norm_value.disabled = True

        w_normalization.observe(use_norm_change)

        self.widgets['use_norm'] = w_normalization
        self.widgets['norm_value'] = w_norm_value
        self.items.append(hb_norm)

    def _add_toggles(self):
        w_advanced = widgets.ToggleButton(
            value=True,
            description='Show advanced options',
            disabled=False,
            button_style='',
            tooltip='',
            icon='check',
            style=self.style,
            layout=widgets.Layout(width='50%'),
        )

        def toggle_advanced(change):
            if change['name'] == 'value':
                keys = [
                    'hb_norm',
                    'hb_max_its',
                    'fignore',
                    'fminmax',
                    'nr_terms',
                    'data_weighting',
                    'tausel',
                ]
                if change['new'] is True:
                    # advanced mode
                    for key in keys:
                        self.containers[key].layout.visibility = 'visible'
                else:
                    for key in keys:
                        self.containers[key].layout.visibility = 'hidden'

        w_show_output = widgets.ToggleButton(
            value=True,
            description='Show output',
            disabled=False,
            button_style='',
            tooltip='',
            # icon='check'
            style=self.style,
            layout=widgets.Layout(width='50%'),
        )

        hb_toggles = widgets.HBox(
            children=[w_advanced, w_show_output],
            layout=widgets.Layout(
                width='80%',
            )
        )

        w_advanced.observe(toggle_advanced)
        self.widgets['nb_show_output'] = w_show_output
        self.items.append(hb_toggles)

    def _init_app_widgets(self):
        self._add_toggles()
        self._add_dformat_selection()
        self._add_condres_selection()
        self._add_lambda()
        self._add_c()
        self._add_flimits()
        self._add_fignore()
        self._add_max_its()
        self._add_nr_terms()
        self._add_tausel()
        self._add_data_weighting()
        self._add_normalization()
        self._add_plot_options()

        w_run = widgets.Button(
            description='Run CCD',
            disabled=False,
            tooltip='Run the Cole-Cole decomposition',
            layout=widgets.Layout(width='50%', height='80px')
        )
        w_run.on_click(self.run_ccd)

        w_clear = widgets.Button(
            description='Reset app',
            layout=widgets.Layout(width='50%', height='80px'),
        )

        def clear_cell(button):
            IPython.display.clear_output()

        w_clear.on_click(clear_cell)

        hb_run = widgets.HBox(
            children=[
                w_run,
                w_clear,
            ],
            layout=widgets.Layout(
                width='100%',
                align_items='center'
            ),
        )

        self.widgets.update({
            'run': w_run,
        })

        header = widgets.HTML(
            value='<h3>Settings</h3>'
        )

        self.items.insert(0, header)
        self.items += [
            hb_run,
        ]

        self.vbox = widgets.VBox(self.items)

    def show(self):
        display(self.vbox)
        display(HTML('<hr />'))

    def run_ccd(self, button):
        """Based on the GUI input, generate a configuration for the CCD and run
        it
        """
        if self.widgets['nb_show_output'].value is True:
            self.enable_logger()
        else:
            # show at least this note
            print('Running CCD')
            self.disable_logger()
        logging.info('running CCD')
        # set environment variables
        os.environ['DD_COND'] = self.widgets['type_formulation'].value
        os.environ['DD_C'] = '{0:.2f}'.format(
            self.widgets['c'].value
        )

        # set options using this dict-like object
        config = cfg_single.cfg_single()
        config['frequency_file'] = self.frequencies
        config['data_file'] = self.data
        config['fixed_lambda'] = int(self.widgets['lambda'].value)
        # config['plot_it_spectra'] = self.widgets['generate_it_plots'].value
        config['max_iterations'] = self.widgets['max_its'].value
        config['nr_terms_decade'] = self.widgets['nr_terms'].value
        config['data_format'] = self.widgets['data_format'].value

        config['data_fmin'] = self.widgets['fmin'].value
        config['data_fmax'] = self.widgets['fmax'].value

        ignores_raw = self.widgets['fignore']
        ignores = ['{0}'.format(
            nr
        ) for nr, x in enumerate(ignores_raw) if x.value is False]
        if len(ignores) == 0:
            ign_str = None
        else:
            ign_str = ','.join(ignores)
        config['ignore_frequencies'] = ign_str

        # tausel
        w_tausel = self.widgets['tausel']
        w_tausel_ind_left = self.widgets['tausel_left']
        w_tausel_ind_right = self.widgets['tausel_right']
        if w_tausel.value == 'individual':
            tausel_opt = '{0},{1}'.format(
                w_tausel_ind_left.value,
                w_tausel_ind_right.value,
            )
        else:
            tausel_opt = w_tausel.value
        config['tausel'] = tausel_opt

        if self.widgets['use_norm'].value is True:
            config['norm'] = self.widgets['norm_value'].value

        # generate a ccd object
        ccd_obj = ccd_single.ccd_single(config)

        # commence with the actual fitting
        ccd_obj.fit_data()

        # extract the last iteration
        last_it = ccd_obj.results[0].iterations[-1]
        if self.widgets['generate_plot'].value is True:
            logging.info('plotting ... this may take a while')
            # don't show in notebook
            # plt.ioff()
            # _ = last_it.plot()
            # _
            for spectrum in ccd_obj.results:
                last_it = spectrum.iterations[-1]
                self._plot(ccd_obj, last_it)

        if self.widgets['generate_lcurve'].value is True:
            for spectrum in ccd_obj.results:
                last_it = spectrum.iterations[-1]
                last_it.plot_lcurve()

        if self.widgets['generate_reg_strength'].value is True:
            for spectrum in ccd_obj.results:
                last_it = spectrum.iterations[-1]
                last_it.plot_reg_strengths()

        if self.widgets['generate_it_plots'].value is True:
            for spectrum in ccd_obj.results:
                for iteration in spectrum.iterations:
                    self._plot(ccd_obj, iteration)

        if self.widgets['generate_output'].value is True:
            with tempfile.TemporaryDirectory() as outdir:
                ccd_obj.save_to_directory(outdir)

                outfile = 'sip_results_{0}'.format(
                    datetime.datetime.strftime(
                        datetime.datetime.now(),
                        '%Y%m%d_%H%M',
                    )
                )

                shutil.make_archive(
                    outfile,
                    format='zip',
                    root_dir=outdir + os.sep,
                    verbose=True
                )

            display(HTML(
                self._help_url('data_formats.html#ascii-audit-format')
            ))
            display(HTML(
                '<a href="{0}.zip" download>Download results</a>'.format(
                    outfile
                )
            ))

        print('finished')

    def _plot(self, ccd_obj, it):
        obj = lib_dd.plot.plot_iteration()

        norm_factors = ccd_obj.data.get('norm_factors', 1)
        D = it.Data.D / norm_factors
        M = it.Model.convert_to_M(it.m)
        # renormalize here? Why do we compute the forward solution again?
        F = it.Model.F(M) / norm_factors
        # extra_size = int(
        #     np.sum([x[1][1] for x in it.Data.extra_dims.items()])
        # )
        # nr_spectra = max(1, extra_size)

        mpl.rcParams['figure.dpi'] = 250
        # iterate over spectra
        for nr, (d, m) in enumerate(it.Model.DM_iterator()):
            # plot spectrum
            fig, axes = plt.subplots(1, 2, figsize=(10 / 2.54, 5 / 2.54))
            obj._plot_rre_rim(nr, axes, D[d], F[d], it)
            # self._plot_rmag_rpha(nr, axes[nr, 2:4], D[d], F[d], it)
            ax1 = axes[0].twinx()
            ax2 = axes[1].twinx()
            obj._plot_cre_cim(nr, [ax1, ax2], D[d], F[d], it)
            fig.tight_layout()
            fig.subplots_adjust(top=0.7)

            # plot spectrum rmag_rpha
            fig, axes = plt.subplots(1, 2, figsize=(10 / 2.54, 5 / 2.54))
            obj._plot_rmag_rpha(nr, axes, D[d], F[d], it)
            ax1 = axes[0].twinx()
            ax2 = axes[1].twinx()
            fig.tight_layout()
            fig.subplots_adjust(top=0.7)

            # plot rtd
            fig, axes = plt.subplots(1, 1, figsize=(10 / 2.54, 5 / 2.54))
            obj._plot_rtd(nr, axes, M[m], it)
            fig.tight_layout()
