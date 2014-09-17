Introduction
------------

This directory contains tests/simulation to determine the influence of the
number of relaxation times per frequency decade (Nd) on the fit results. A
bi-modal polarization response is modelled (created using two Cole-Cole terms).

Tested Situations
-----------------

Noise: Relative noise was added to both magnitude and phase values before
       fitting.
NoNoise: No noise was added prior to fitting
NoNoiseDense: The number of frequencies for the data was increased from 25 to
              60.
