import sys
already_loaded = 'matplotlib' in sys.modules

# just make sure we can access matplotlib as mpl
import matplotlib as mpl
if(not already_loaded):
    mpl.use('Agg')


# hack-around for https://github.com/matplotlib/matplotlib/pull/2012
if(mpl.__version__ == '1.3.0'):
    pass
else:
    pass
    mpl.rcParams['font.family'] = 'Open Sans'
mpl.rcParams['mathtext.default'] = 'regular'

mpl.rcParams['text.usetex'] = True
# mpl sometimes has problems with latex and unicde. If you work on utf-8, the
# following string conversion should do the trick:

# sans-serif fonts
if(True):
    preamble = r'\usepackage{droidsans}\usepackage[T1]{fontenc} '
    preamble += r'\usepackage{sfmath} \renewcommand{\rmfamily}{\sffamily} '
    preamble += r'\renewcommand\familydefault{\sfdefault} '
    preamble += r'\usepackage{mathastext} '
    mpl.rc('text.latex', preamble=preamble)

import matplotlib.pyplot as plt
plt

# general settings
mpl.rcParams["lines.linewidth"] = 1.5
mpl.rcParams["lines.markeredgewidth"] = 1.5
mpl.rcParams["lines.markersize"] = 1.5
mpl.rcParams["font.size"] = 8
