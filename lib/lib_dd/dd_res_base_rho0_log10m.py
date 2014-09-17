import numpy as np
import dd_res_base_rho0_m

class dd_res_base(dd_res_base_rho0_m.dd_res_base):
    r"""
    Provide forward function and derivatives for the Debye-Decomposition using
    the parameterization :math:`(\rho_0, log_{10}(m_i))`
    """
    def convert_parameters(self, pars):
        r"""
        Convert parameters given as (:math:`\rho_0, m_i`) to the
        parameterisation used by this class.
        """
        pars_converted = np.empty_like(pars)
        pars_converted[0] = pars[0]
        pars_converted[1:] = np.log10(pars[1:])

        return pars_converted

    def forward_re(self, omega, pars, s):
        """
        Real part of debye distribution

        pars = (rho0, log_10(m_i))
        """
        debye_terms = np.zeros(omega.shape[0], dtype=np.float64)
        np.seterr(over='raise')

        for index,rel_time in enumerate(s):
           #try:
           #    term = 10**pars[index+1] * (omega * 10**rel_time)**2 / (1 + (omega * 10**rel_time)**2)
           #except FloatingPointError:
           #    print('Arithmetic Error')
           #    print(pars[index+1])
           #    print(10**rel_time)
           #    exit()
            term = 10**pars[index+1] * (omega * 10**rel_time)**2 / (1 + (omega * 10**rel_time)**2)

            debye_terms += term
        debye_terms = pars[0] * (1 - debye_terms)
        return (debye_terms)

    def forward_mim(self, omega, pars, s):
        r"""
        Return :math:`-Im (\rho)`
        """
        debye_terms = np.zeros(omega.shape[0], dtype=np.float64)
        for index,rel_time in enumerate(s):
            term = 10**pars[index+1] * (omega * 10**rel_time) / (1 + (omega * 10**rel_time)**2)
            debye_terms += term

        debye_terms = pars[0] * debye_terms
        return debye_terms

    def del_re_del_dc(self, omega, pars, s):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{Re}}{\partial \rho_0}`

        Return an K x 1 vector.
        """
        K = omega.shape[0]

        derivative = np.ones((K,1), dtype=np.float64)
        for index,rel_time in enumerate(s):
            derivative[:, 0] -= (10**pars[index+1] * (omega * 10**rel_time)**2 / (1 + (omega * 10**rel_time)**2))
        return derivative

    def del_re_del_chargeability(self, omega, pars, s):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial m_i}`

        Return an K x N vector.

        """
        K = omega.shape[0]

        derivative = np.ones((K,s.shape[0]), dtype=np.float64)

        for column in range(0, s.shape[0]):
            derivative[:,column] = - pars[0] * np.log(10) * 10**pars[column+1] * (omega * 10**s[column])**2 / (1 + (omega * 10**s[column])**2)

        return derivative

    def del_mim_del_dc(self, omega, pars, s):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial \rho_0}`

        Return an K x 1 vector.
        """
        K = omega.shape[0]

        derivative = np.zeros((K,1), dtype=np.float64)
        for index,rel_time in enumerate(s):
            derivative[:, 0] += (10**pars[index+1] * (omega * 10**rel_time) / (1 + (omega * 10**rel_time)**2))
        return derivative


    def del_mim_del_chargeability(self, omega, pars, s):
        r"""
        Calculate the derivate :math:`\frac{\partial \underline{-Im}}{\partial m_i}`

        Return an K x N vector.

        """
        K = omega.shape[0]

        derivative = np.ones((K,s.shape[0]), dtype=np.float64)

        for column in range(0, s.shape[0]):
            derivative[:,column] = np.log(10) * 10**pars[column+1] * (omega * 10**s[column]) / (1 + (omega * 10**s[column])**2)

        derivative *= pars[0]
        return derivative
