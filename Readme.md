Cole-Cole decomposition routines
================================

Introduction
------------

This package contains an implementation of the Cole-Cole decomposition (CCD)
scheme, which is used in near-surface geophysical applications to describe
electrical polarization signatures measured for frequencies in the mHz range up
to multiple kHz.

In the CCD, spectral induced polarization (SIP) signatures are described by a
superposition of elementary polarization terms, which are suitably distributed
to cover at least the frequency range spanned by the measurement data.

![example output](docs/example_for_readme/results_3/plot_spec_000_iteration0004.png)

Parts of this code were described in two open access publications:

[1. Weigand and Kemna, 2016, Computers and Geosciences](http://www.sciencedirect.com/science/article/pii/S0098300415300625)

[2. Weigand and Kemna, 2016, Geophysical Journal International](http://gji.oxfordjournals.org/content/205/3/1414)


Licence
-------

This program is licenced under the GPL3 or later licence. See LICENCE.txt and
headers of individual files for more information.

Requirements
------------

The following Python packages are required to run the Debye decomposition
routines:

	numpy
	scipy
	matplotlib
	geccoinv
	sip_models

In order to build the documentation, the additional packages are required:

	sphinx

Under Debian-related linux systems, these packages can be installed using the
commands: ::

    sudo apt-get install texlive-latex-base texlive-latex-extra\
        texlive-fonts-recommended texlive-fonts-extra dvipng
    sudo apt-get install python2.7-numpy python-matplotlib python2.7-scipy\
        python-setuptools python-nose python-tornado

In order to build the documentation, the following sphinx-related packages must
be installed: ::

    sudo apt-get install python-sphinx
    sudo apt-get install python-sphinx python-sphinxcontrib.blockdiag
    pip install sphinxcontrib-programoutput


geccoinv and sip_models have to be installed according to their own documentation.

Under Windows, the program was tested using the 'pythonxy' distribution
(https://code.google.com/p/pythonxy/).


Installation
------------

Install the source package using setuptools: ::

    python setup.py build
    python setup.py install


The package can also be installed to a user-defined directory: ::

    export PYTHONUSERBASE=$HOME/inst/pip_installs
    export PYTHONPATH=$HOME/inst/pip_installs/lib/python2.7/\
        site-packages/:$PYTHONPATH
    python setup.py install --user
    export PATH=$HOME/inst/pip_installs/bin:$PATH


For developers: ::

    python seutp.py develop --user

To build the documentation ::

    cd docs/doc
    make html

Setuptools Developer Guide:

https://pythonhosted.org/setuptools/setuptools.html

Documentation
-------------

 * Documentation is located in docs/
 * The sphinx-generated documentation is found in docs/doc

