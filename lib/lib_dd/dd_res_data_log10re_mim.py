# -*- coding: utf-8 -*-
"""
Copyright 2014 Maximilian Weigand

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
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
