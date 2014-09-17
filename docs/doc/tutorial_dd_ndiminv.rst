Build you own inversion
-----------------------

::

    #!/usr/bin/python
    import numpy as np
    import NDimInv
    import NDimInv.regs as RegFuncs
    import NDimInv.reg_pars as LamFuncs

    if __name__ == '__main__':
    ######## test calls #######
        # init the object
        model_settings = {}
        model_settings['Nd'] = 5
        model_settings['frequencies'] = np.loadtxt('frequencies.dat')
        ND = NDimInv.Inversion('dd_log10rho0log10m', model_settings)
        ND.finalize_dimensions()

        # print overview
        ND.overview_data()

        # Read in data
        filename = 'data.dat'
        data = np.loadtxt(filename)
        data = data.reshape((2, data.size / 2)).T
        ND.Data.add_data(data, 'rmag_rpha', extra=[])

        ## now we can prepare the model

        # now that we know the frequencies we can call the post_frequency
        # handler for the model side
        ND.update_model()
        ND.set_custom_plot_func(NDimInv.main.DD_plot())

        # add a frequency regularization for the DD model
        ND.Model.add_regularization(0,
                                    RegFuncs.SmoothingFirstOrder(
                                        decouple=[0, ]),
                                    LamFuncs.FixedLambda(50)
                                    #NDimInv.main.SearchLambda(
                                    #NDimInv.main.Lam0_Fixed(50))
                                    )

        # choose from a fixed set of step lengths
        ND.Model.steplength_selector = NDimInv.main.SearchSteplength()

        # run the inversion
        ND.run_inversion()
        for it in ND.iterations:
            it.plot()

