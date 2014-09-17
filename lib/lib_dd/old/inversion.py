#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Debye Decomposition - Resistivity inversion routines
"""
import os
import logging
import numpy as np
from crlab_py.mpl import *
import iteration_info


class inversion():
    def __init__(self, dd_obj, silent=False):
        self.dd_obj = dd_obj

        #self.setup_logger('dd.dd_res_inv')
        self.logger = logging.getLogger('dd.dd_res_inv')
        self.rms_eps = 0.01
        self.rms_upd_eps = 1e-5  # min. requested rms change between iterations
        self.allowed_rms_im_increase_first_iteration = 1e2

        # inversion settings
        self.switch_lambda_use_fixed = True
        self.switch_lambda_use_l_curve = False
        self.switch_lambda_use_factor_quotient = False

        self.use_damping = True
        self.use_tikhonov = False   # default

        self.lambda_initial_method = None
        self.lam_user = None

        self.lam = None  # can be changed by user

    @staticmethod
    def setup_logger(logger_name, log_dir='.', silent=True):
        r"""
        Setup the logging facilities.

        For some reason this function should only be called once.

        Parameters
        ----------
        logger_name : the parent of all loggers, e.g. dd.
                        Use subloggers for all loggers, i.e. dd.interface
        log_dir : Directory in which to store the log file
        silent : True - Do not print anything to STDOUT
                 False - Print some infos to STDOUT

        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # create file handler which logs even debug messages
        fh = logging.FileHandler(log_dir + os.sep + 'debyedecomp.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        # add the handlers to logger
        logger.addHandler(fh)
        if(not silent):
            logger.addHandler(ch)

    def dump_options(self):
        """
        print the inversion options to the console
        """
        self.logger.info('=====================================')
        self.logger.info('Using damping regularization: {0}'.format(
                         self.use_damping))
        self.logger.info('Using Tikhonov regularization: {0}'.format(
                         self.use_tikhonov))

        self.logger.info('Lambda 0')
        self.logger.info('Method: {0}'.format(self.lambda_initial_method))

        self.logger.info('Lambda selection during inversion:')
        self.logger.info('Use fixed lambda: {0}'.format(
                         self.switch_lambda_use_fixed))
        self.logger.info('Use l-curve lambda: {0}'.format(
                         self.switch_lambda_use_l_curve))
        self.logger.info('Use factor/quotient search for lambda: {0}'.format(
                         self.switch_lambda_use_factor_quotient))
        self.logger.info('=====================================')

    def get_roughness_matrix_first_order(self, m):
        """
        Return the roughness matrix of first order
        """

        R = np.zeros((m.shape[0] - 1, m.shape[0]))
        for i in range(0, m.shape[0] - 1):
            R[i, i] = 1
            R[i, i + 1] = -1

        # we do not regularize for rho0
        R[:, 0] = 0
        R[0, :] = 0

        return R

    def create_l_curve(self, d, W, omega, m, s):
        """
        Create the l-curve and try to determine the optimal lambda value
        """
        # copy m so we do not overwrite anything
        ml = np.zeros_like(m)
        ml[:] = m[:]

        # save lambda
        lambda_save = self.lam

        R = self.get_regularization_matrix(m)

        Lx = []
        Axb = []
        #1e-7, 1e-6, 1e-5, 0.0001, 0.001, 0.01, 0.1, 1,
        lams = (0.01, 0.1, 1, 10, 100, 200, 500, 1000, 10000,
                1e5, 1e6, 1e7, 1e8, 1e9, 1e10)
        for lami in lams:
            self.logger.info('Computing tikhonov-solution for lambda', lami)
            try:
                self.lam = lami
                update = self.inverse_step(d, W, omega, m, s)
                m1 = ml + update

                # compute parameters for L-curve
                Lx.append(np.log(np.sum(R.dot(m1) ** 2)))

                re_it, im_it = self.dd_obj.forward_re_mim(omega, m1, s)
                f = np.hstack((re_it, im_it))
                residuum_t = (d - f)[:, np.newaxis]

                Axb.append(np.log(np.sum(np.abs(residuum_t ** 2))))

                it = iteration_info.iteration_info(self.dd_obj)
                it.compute(d[0:d.shape[0] / 2], d[d.shape[0] / 2:], 0, m1, s,
                           omega, np.diag(W), self.lam)
                it.plot_spectrum('l-curve_{0:015.7f}'.format(lami))
            except:
                self.logger.warn('Lambda {0} failed. Caught the exception,\
                                 trying next one.'.format(lami))

        # plot l-curve
        fig = plt.figure()
        ax = fig.add_subplot(211)
        ax.plot(Axb, Lx)
        for index, i in enumerate(lams):
            ax.annotate('{0}'.format(i), xy=(Axb[index], Lx[index]))

        ax.set_xlabel(r'$log||d - f||^2$')
        ax.set_ylabel(r'$log||R \underline{m}||^2$')

        ax = fig.add_subplot(212)
        ax.plot(Axb, np.array(Lx) / np.array(Axb))
        fig.savefig('lcurve.png')

        # restore lambda
        self.lam = lambda_save

    def lambda_set_initial_method(self, method, value=None):
        r"""
        Set the method by which the initial lambda value is selected:

        method - 'easylam': Number of model parameters
                 'jacobian': Determine from :math:`A^T W_d W A`
                 'user': Set user specified value

        value  - for method 'user', use this value

        """
        self.lambda_initial_method = method
        if(method == 'user'):
            self.lam_user = value

    def lambda_use_fixed(self):
        self.switch_lambda_use_fixed = True
        self.switch_lambda_use_l_curve = False
        self.switch_lambda_use_factor_quotient = False

    def lambda_use_l_curve(self):
        self.switch_lambda_use_fixed = False
        self.switch_lambda_use_l_curve = True
        self.switch_lambda_use_factor_quotient = False

    def lambda_use_factor_quotient(self):
        self.switch_lambda_use_fixed = False
        self.switch_lambda_use_l_curve = False
        self.switch_lambda_use_factor_quotient = True

    def lambda_search_factor_quotient(self, d, W, omega, pars, s):
        """
        For the actual lambda value, compute model updates for
        lambda / 10; lambda * 10
        and choose the version with the best rms
        """
        self.logger.info('######################################')
        self.logger.info('     lambda factor/quotient search    ')
        self.logger.info('######################################')

        # forward computation for last lambda
        re, mim = self.dd_obj.forward_re_mim(omega, pars, s)
        it0 = iteration_info.iteration_info(self.dd_obj)
        it0.compute(self.re_orig, self.mim_orig, 0, pars, s, omega,
                    self.errors, self.lam)

        # save lambda
        lambda_save = self.lam

       #test_lams_raw = []
       #for factor in range(5,205,5):
       #    test_lams_raw.append(self.lam / factor)
       #    test_lams_raw.append(self.lam * factor)

        test_lams_raw = (self.lam / 200, self.lam / 100, self.lam / 50,
                         self.lam / 10, self.lam / 5, self.lam * 5,
                         self.lam * 10, self.lam * 100)

        test_its = []
        test_lams = []
        for test_lam in test_lams_raw:
            try:
                self.lam = test_lam
                update = self.inverse_step(d, W, omega, pars, s)
                # save infos
                it = iteration_info.iteration_info(self.dd_obj)
                it.compute(self.re_orig, self.mim_orig, 0, pars + update, s,
                           omega, self.errors, self.lam)
                test_its.append(it)
                test_lams.append(test_lam)
            except:
                self.logger.warn('There was an error in the lambda test for ' +
                                 'lambda: {0}. Trying next lambda.'.format(
                                     test_lam))
                continue

        #    it.plot_spectrum(prefix='{0}'.format(test_lam))
        all_rms = [x.rms_no_err for x in test_its] + [it0.rms_no_err, ]
        all_rms_im = [x.rms_im for x in test_its] + [it0.rms_im, ]

        test_lams += (lambda_save,)

        self.logger.debug('RMS values (RMS, RMS_im, lams)')
        self.logger.debug(all_rms)
        self.logger.debug(all_rms_im)
        self.logger.debug('Lambdas')
        self.logger.debug(test_lams)

        self.lam = test_lams[np.argmin(all_rms_im)]
        self.logger.debug('New lambda: {0}'.format(self.lam))
        self.logger.debug('######################################')

    def get_initial_lambda_easylam(self, pars):
        """
        A reasonable initial value for lambda is the number of parameters.
        """
        return pars.shape[0]

    def get_initial_lambda_atwtwa(self, W, omega, pars, s):
        """
        Determine the initial lambda value based on

        - Newman and Alaumbaugh, 1997
        - Kemna, 2000 (p.76)

        by using the mean value of the diagonal entries of A^T W_d^T D_d A
        """
        J = self.dd_obj.Jacobian_re_mim(omega, pars, s)

        M = J.T.dot(W.T.dot(W.dot(J)))
        lam0 = np.mean(np.diag(M))
        return lam0

    def set_initial_lambda(self, W, omega, pars, s):
        """

        """
        if(self.lambda_initial_method == 'easylam'):
            self.lam = self.get_initial_lambda_easylam(pars)
        elif(self.lambda_initial_method == 'jacobian'):
            self.lam = self.get_initial_lambda_atwtwa(W, omega, pars, s)
        elif(self.lambda_initial_method == 'user'):
            self.lam = self.lam_user
        self.logger.info('Initial lambda value: {0}'.format(self.lam))

    def set_lambda(self, d, W, omega, m, s):
        """
        Set/update lambda value depending on the settings
        """
        # do we need to set an initial value?
        if(self.lam is None):
            self.set_initial_lambda(W, omega, m, s)

        if(self.switch_lambda_use_fixed):
            pass
        elif(self.switch_lambda_use_l_curve):
            self.logger.warn('L-curve currently not implemented!')
            self.create_l_curve(d, W, omega, m, s)
            exit()
        elif(self.switch_lambda_use_factor_quotient):
            self.lambda_search_factor_quotient(d, W, omega, m, s)

    def get_regularization_matrix(self, parameters):
        if(self.use_damping):
            R = np.eye(parameters.shape[0])
        elif(self.use_tikhonov):
            R = self.get_roughness_matrix_first_order(parameters)
        return R

    def inverse_step(self, d, W, omega, m, s):
        self.logger.debug('Compute inverse step...')
        J = self.dd_obj.Jacobian_re_mim(omega, m, s)
        #J = self.Jacobian_log10(omega, m, s)
        #re_it, im_it = self.calculate_reim_log10(omega, m, s)
        re_it, im_it = self.dd_obj.forward_re_mim(omega, m, s)
        f = np.hstack((re_it, im_it))
        residuum = (d - f)[:, np.newaxis]
        JJ = J.T.dot(W.T.dot(W.dot(J)))

        R = self.get_regularization_matrix(m)

        if(self.use_damping):
            RR = R
            b_add = 0
        elif(self.use_tikhonov):
            RR = R.T.dot(R)
            b_add = - self.lam * R.T.dot(R).dot(m)

        else:
            self.logger.error('No regularization method selected!')
            exit()

        ## compute solution
        B = JJ + self.lam * RR

        b = J.T.dot(W.T.dot(W.dot(residuum))) + b_add
        update = np.linalg.solve(B, b)
        return update

    def find_alpha(self, pars, update, it_infos, re, mim, omega, s, errors):
        best_index = -1
        #best_rms_im = None
        for nr, a in enumerate(alphas):
            it = iteration_info.iteration_info(self.dd_obj)
            it.compute(re, mim, -1, pars + a * update, s, omega, errors,
                       self.lam)
            if(best_index == -1):
                best_index = nr
                best_rms_im_no_err = it.rms_im_no_err
            else:
                if(it.rms_im_no_err < best_rms_im_no_err):
                    best_index = nr
                    best_rms_im_no_err = it.rms_im_no_err

        best_value = alphas[best_index]
        return best_value

    def check_update_before_application(self, pars, it_list, re, mim, omega,
                                        s, errors):
        """
        Apply various checks before applying the update
        """
        self.logger.debug('check_update_before_application')
        self.logger.debug(type(it_list[-1]))

        self.logger.debug('len(it_list): {0}'.format(len(it_list)))
        rms_old = it_list[-1].rms_no_err
        rms_im_old = it_list[-1].rms_im_no_err

        # compute iteration infos of the new (to be checked) iteration
        it = iteration_info.iteration_info(self.dd_obj)
        try:
            it.compute(re, mim, -1, pars, s, omega, errors, self.lam)
        except FloatingPointError:
            self.logger.warn('The update leads to a floating point error.')
            return True
        except ArithmeticError:
            self.logger.warn('The update leads to an arithmetic error.')
            return True
        except:
            self.logger.warn('The update leads to an unknown error.')
            return True

        rms_new = it.rms_no_err
        rms_im_new = it.rms_im_no_err
        self.logger.info('Old rms_no_err: {0}'.format(rms_old))
        self.logger.info('New rms_no_err: {0}'.format(rms_new))
        self.logger.info('Old rms_im_no_err: {0}'.format(rms_im_old))
        self.logger.info('New rms_im_np_err: {0}'.format(rms_im_new))

        # if this is the first iteration then the RMS-check doesn't make sense
        # as the old rms ist only the rms computed using the starting values
        if(it_list[-1].nr > 0 and rms_im_new > rms_im_old):
            self.logger.info('Imag RMS increase')
            return True

        # if we are in the first iteration, then we allow a slight increase in
        # the imaginary RMS, but not above a certain threshold
        if(it_list[-1].nr == 0 and rms_im_new > rms_im_old):
            increase = (rms_im_new - rms_im_old)
            if(increase > self.allowed_rms_im_increase_first_iteration):
                self.logger.info(
                    'First iteration RMS-IM increase lies above: {0}'.format(
                        self.allowed_rms_im_increase_first_iteration))
                return True

        rms_diff = np.abs(rms_new - rms_old)
        rms_im_diff = np.abs(rms_im_new - rms_im_old)
        if(rms_im_diff < self.rms_upd_eps):
            self.logger.info(
                'Imaginary RMS update difference below {0}'.format(
                    self.rms_upd_eps))
            self.logger.info('Diff: {0} {1} {2}'.format(rms_diff, rms_new,
                                                        rms_old))
            self.logger.info('Im-Diff: '.format(rms_im_diff, rms_im_new,
                                                rms_im_old))
            return True
        return False

    def check_update_after_application(self, pars, it_list):
        """
        Check after applying the update of this iteration
        """
        rms = it_list[-1].rms_no_err

        if(np.abs(rms) == 0):
            self.logger.info('RMS is numerically zero.')
            return(True)

        return False

    def get_weighting_re_vs_im(self, re, im):
        """
        Return a vector of weighting factors that equals the mean of real and
        imaginary parts.
        """

        re_mean = np.mean(np.abs(re))
        im_mean = np.mean(np.abs(im))

        factor_im = re_mean / im_mean
        # factor_im *= 10
        errors = np.ones(re.shape[0] * 2)
        errors[re.shape[0]:] *= factor_im
        return errors

    def check_data(self, re, mim):
        """
        We restrict the fit to positive m values. This implies also positive
        imaginary parts!
        Reject a data set if the data mean is negative
        """
        if(np.mean(mim) < 0):
            self.logger.info('Imaginary part mean is negative. Exiting fit')
            return False

        nr_mim = mim.shape[0]
        nr_negative_mim = len(np.where(mim < 0)[0])
        if(nr_negative_mim > 0 and nr_mim / nr_negative_mim <= 2):
            self.logger.info(
                'Too many negative mim entries: {0} from: {1}'.format(
                    nr_negative_mim, nr_mim))
            return False

        return True

    def fit_simple_spectrum_reim_linear(self, omega, pars_start, s, re, mim,
                                        plot_iterations=False):
        """
        Fit a debye model with the minimum of user settings

        Parameters
        ----------
        omega : angular frequencies of data points
        pars_start : start parameters (linear, will be converted to the
                     parameterisation used)
        s : log10 tau values
        re : real parts
        mim : negative imaginary parts
        plot_iterations : True: create plots of each iteration

        Returns
        -------
        m : parameters (rho0, chargeabilities)
        m_infos : list containing the iteration informations

        Notes
        -----
        This function should be renamed - currently it is the only fit function

        """
        pars_start_converted = self.dd_obj.convert_parameters(pars_start)

        it_infos = []  # store information on each iteration

        #K = omega.shape[0]

        # prepare fit parameter vector
        m = np.empty_like(pars_start_converted)
        m[:] = pars_start_converted[:]
        m = m[:, np.newaxis]
        self.logger.info('Using {0} chargeability values'.format(m.shape[0]))

        self.dump_options()

        d = np.hstack((re, mim))
        self.re_orig = re
        self.mim_orig = mim

        # error matrix
        # weight with inverse frequency
        errors = self.get_weighting_re_vs_im(re, mim)
        self.errors = errors

        W = np.diag(errors)

        # info on iteration 0
        it0 = iteration_info.iteration_info(self.dd_obj)
        it0.compute(re, mim, 0, m, s, omega, errors, self.lam)
        if(plot_iterations):
            it0.plot_spectrum()
        it_infos.append(it0)

        check_data = self.check_data(re, mim)
        if(check_data):
            try:
                # the iterations
                for iteration in range(1, 20):
                    self.logger.info(
                        '-----------------------------------------------' +
                        '------')
                    self.logger.info('Iteration {0}'.format(iteration))

                    self.set_lambda(d, W, omega, m, s)
                    try:
                        update = self.inverse_step(d, W, omega, m, s)
                        alpha = self.find_alpha(m, update, it_infos, re, mim,
                                                omega, s, errors)

                        self.logger.info('Alpha: {0}'.format(alpha))
                        update = alpha * update
                    except:
                        self.logger.error('Some error in inverse step')
                        break

                    break_off = self.check_update_before_application(
                        m + update, it_infos, re, mim, omega, s, errors)

                    if(break_off):
                        self.logger.info('Breaking before applying update')
                        break
                    m = m + update

                    self.logger.debug('Computing iteration infos')

                    # save infos
                    it = iteration_info.iteration_info(self.dd_obj)
                    it.compute(re, mim, iteration, m, s, omega, errors,
                               self.lam)
                    it_infos.append(it)
                    self.logger.info('RMS Values of this iteration:\
                                                        (rms, rms_no_err):')
                    self.logger.info('{0} {1}'.format(it.rms, it.rms_no_err))

                    if(plot_iterations):
                        it.plot_spectrum()

                    break_off = self.check_update_after_application(m,
                                                                    it_infos)
                    if(break_off):
                        self.logger.info('Breaking after applying update')
                        break
            except np.linalg.LinAlgError:
                self.logger.error('Exception thrown')
                self.logger.error('LinAlgError')
        else:
            self.logger.warn('Check data not successful')
        self.logger.info('Finished')
        return m, it_infos
