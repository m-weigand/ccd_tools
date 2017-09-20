# jupyter notebook app for ccd_single
import os
import shutil
import ipywidgets as widgets
from IPython.core.display import display, HTML
import numpy as np
import lib_dd.decomposition.ccd_single as ccd_single
import lib_dd.config.cfg_single as cfg_single


class ccd_single_app(object):
    def __init__(self, frequency_file, data_file):
        self.frequencies = np.loadtxt(frequency_file)
        self.data = np.loadtxt(data_file)
        self.widgets = []
        self.vbox = None
        self.print_data_summary()
        self._init_app_widgets()

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

    def _init_app_widgets(self):
        style = {'description_width': 'initial'}
        w_condres = widgets.Dropdown(
            options={
                'resistivity formulation': '0',
                'conductivity formulation': '1',
            },
            value='0',
            description='Type of kernel:',
            style=style,
        )
        w_lambda = widgets.IntText(
            value=10,
            description='Lambda',
            disabled=False,
        )
        w_run = widgets.Button(
            description='Run CCD',
            disabled=False,
            tooltip='Run the Cole-Cole decomposition',
        )
        w_c = widgets.FloatSlider(
            value=0.5,
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

        w_normalization = widgets.Checkbox(
            value=False,
            description='Activate normalization',
            disabled=False,
            style=style,
        )
        w_norm_value = widgets.FloatText(
            value=10,
            step=1,
            description='Normalization value:',
            disabled=True,
            style=style,
        )
        w_generate_plot = widgets.Checkbox(
            value=True,
            description='Generate plot',
            disabled=False
        )
        w_generate_output = widgets.Checkbox(
            value=True,
            description='Generate output for download',
            disabled=False
        )
        w_run.on_click(self.run_ccd)

        def use_norm_change(change):
            if change['name'] == 'value':
                if change['new'] is True:
                    w_norm_value.disabled = False
                else:
                    w_norm_value.disabled = True

        w_normalization.observe(use_norm_change)
        self.widgets = {
            '00_type_formulation': w_condres,
            '01_lambda': w_lambda,
            '02_c_selection': w_c,
            '03_use_normalization': w_normalization,
            '04_norm_value': w_norm_value,
            # output settings
            '80_generate_plot': w_generate_plot,
            '81_generate_output': w_generate_output,
            # run button
            '99_run': w_run,
        }

        self.vbox = widgets.VBox(
            [self.widgets[key] for key in sorted(self.widgets.keys())]
        )

    def show_app(self):
        display(self.vbox)
        display(HTML('<hr />'))

    def run_ccd(self, button):
        print('running CCD')
        print('lambda', self.widgets['01_lambda'].value)
        # set environment variables
        os.environ['DD_COND'] = self.widgets['00_type_formulation'].value
        os.environ['DD_C'] = '{0:.2f}'.format(
            self.widgets['02_c_selection'].value
        )

        # set options using this dict-like object
        config = cfg_single.cfg_single()
        config['frequency_file'] = self.frequencies
        config['data_file'] = self.data
        config['fixed_lambda'] = int(self.widgets['01_lambda'].value)

        if self.widgets['03_use_normalization'].value is True:
            config['norm'] = self.widgets['04_norm_value'].value

        # generate a ccd object
        ccd_obj = ccd_single.ccd_single(config)

        # commence with the actual fitting
        ccd_obj.fit_data()

        # extract the last iteration
        last_it = ccd_obj.results[0].iterations[-1]
        if self.widgets['80_generate_plot'].value is True:
            print('plotting ... this may take a while')
            _ = last_it.plot()
            _

        if self.widgets['81_generate_output'].value is True:
            outdir = 'output'
            if os.path.isdir(outdir):
                shutil.rmtree(outdir)
            ccd_obj.save_to_directory('output')

            shutil.make_archive(
                'output', format='zip', root_dir='output/', verbose=True
            )

            display(HTML('<a href="output.zip" download>Download results</a>'))
