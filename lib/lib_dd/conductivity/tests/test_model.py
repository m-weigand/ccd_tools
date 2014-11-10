"""
Test the conductivity formulation of the Debye decomposition
"""
import numpy as np
from NDimInv.plot_helper import *


def test_forward():
    """Test the forward model by comparing the output to the analytical
    formulations for real/imaginary parts
    """
    frequencies = np.logspace(-3, 3, 40)
    omega = 2 * np.pi * frequencies
    m = 0.1
    sigma0 = 1.0 / 100.0  # 1 / 100 Ohm m
    sigmai = sigma0 / (1 - m)
    print '100', sigma0, sigmai

    tau = 0.04

    def cc(c):
        sigma = sigmai * (1 - m / (1 + (1j * omega * tau)**c))
        rho = 1 / sigma
        return sigma, rho

    def cc_real(c):
        creal = sigmai * (1 - m / (1 + omega**2 * tau**2))
        return creal

    def cc_imag(c):
        cimag = (sigmai * m * omega * tau) / (1 + omega**2 * tau**2)
        return cimag

    sigma1, rho1 = cc(1.0)
    sigre = cc_real(1.0)
    sigim = cc_imag(1.0)
    # sigma2, rho2 = cc(0.5)

    fig, axes = plt.subplots(4, 1, figsize=(10, 10))
    ax = axes[0]
    ax.semilogx(frequencies, np.real(sigma1), '.')
    ax.semilogx(frequencies, sigre, '-')

    ax = axes[1]
    ax.semilogx(frequencies, np.imag(sigma1), '.')
    ax.semilogx(frequencies, sigim, '-')
    # ax.semilogx(frequencies, np.imag(sigma2), '.-')

    ax = axes[2]
    ax.semilogx(frequencies, np.real(rho1), '.-')

    ax = axes[3]
    ax.semilogx(frequencies, np.imag(rho1), '.-')


def test_Jacobian():
    """Compare the Jacobian to the correponding numerical Jacobian
    """
    break
    import numdifftools as ndt
    m0 = ND.iterations[0].m

    J = ddc.Jacobian(m0)
    J_re = J[0: J.shape[0] / 2, :]
    J_im = J[J.shape[0] / 2:, :]

    def get_num_re():
        def ffunc_re(pars):
            return ddc.forward(pars)[:, 0]

        Jfunc = ndt.Jacobian(ffunc_re, order=4)
        Jt_re = Jfunc(pars)

        print 'Approximation', Jt_re.shape
        return Jt_re

    Jt_re = get_num_re()


    def get_num_im():
        ffunc_im = lambda pars:ddc.forward(m0)[:, 1]
        Jfunc = ndt.Jacobian(ffunc_im)
        Jt_im = Jfunc(pars)
        return Jt_im

    def test_der():
        for i in xrange(0, 20):
            print 'frequency index', i
            for j in xrange(0, 2): # re/im
                f = lambda x0: ddc.forward(np.hstack((x0, m0[1:])))[i, j]
                fder = ndt.Derivative(f)
                print fder(m0[0]), J[i + (j * 20),0], (fder(m0[0]) - J[i + (j * 20), 0])

    def test_der2():
        diffs = []
        for z in xrange(1, 162):
            print 'z', z
            for i in xrange(0, 20):
                print 'frequency index', i
                for j in xrange(0, 2):
                    f = lambda x0: ddc.forward(np.hstack((m0[0:z], x0, m0[z+1:])))[i, j]
                    fder = ndt.Derivative(f)
                    #print fder(m0[1]), J[i + (j*20), z], fder(m0[1])- J[i + (j*20), z]fder(m0[1])- J[i + (j*20), z]
                    diffs.append(fder(m0[1])- J[i + (j*20), z])
                    print diffs
                    import pdb
                    pdb.set_trace()


# test_der2()
    Jt_im = get_num_im()
    print J_re[0, 0], Jt_re[0, 0]
    diff = J_re - Jt_re
    print diff.shape
    D = diff
    # D = np.abs(diff)
    # D = np.log10(D)

    fig, axes = plt.subplots(2, 1, figsize=(10, 5))
    ax = axes[0]
    ax.imshow(J_re)

    ax = axes[1]
    ax.imshow(J_im)

    fig, axes = plt.subplots(4, 1, figsize=(10, 5))
    ax = axes[0]
    im = ax.imshow(D)
    fig.colorbar(im, cax=axes[1], orientation='horizontal')

    ## im
    DIM = (J_im - Jt_im)
    ax = axes[2]
    im = ax.imshow(DIM)
    fig.colorbar(im, orientation='horizontal', cax=axes[3])
