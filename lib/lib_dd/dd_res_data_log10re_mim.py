# -*- coding: utf-8 -*-
"""
Copyright 2014 Maximilian Weigand

"""
import Jacobian


class add_log10re_mim_derivatives():
    """
    Add a :math:`log_{10}(Re)` parameterisation to an otherwise finished
    resistivity object.
    """
    def Jacobian_log10re_mim(self, pars):
        r"""
        Jacobian for the input data :math:`(log_{10}(\sigma'), -\sigma'')`
        """
        partials = [self.del_log10re_del_dc,
                    self.del_log10re_del_chargeability,
                    self.del_mim_del_dc,
                    self.del_mim_del_chargeability]
        return Jacobian.Jacobian(self.omega, pars, self.s, partials)
