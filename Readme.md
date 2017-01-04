Cole-Cole decomposition routines
================================

## Introduction

This package contains an implementation of the Cole-Cole decomposition (CCD)
scheme, which is used in near-surface geophysical applications to describe
electrical polarization signatures measured for frequencies in the mHz range up
to multiple kHz.

In the CCD, spectral induced polarization (SIP) signatures are described by a
superposition of elementary polarization terms, which are suitably distributed
to cover at least the frequency range spanned by the measurement data.

![example output](docs/example_for_readme/results_3/plot_spec_000_iteration0004.png)

Parts of this code were described in two open-access publications:

[1. Weigand and Kemna, 2016, Computers and Geosciences](http://www.sciencedirect.com/science/article/pii/S0098300415300625)

[2. Weigand and Kemna, 2016, Geophysical Journal International](http://gji.oxfordjournals.org/content/205/3/1414)


## Licence

This program is licenced under the GPL3 or later licence. See LICENCE.txt and
headers of individual files for more information.

Some third-party packages used for the homepage (gh-pages branch) have
individual licences.

## Requirements

For requirements to use the ccd tools, please refer to the
[requirements.txt](requirements.txt). When pip is used, all requirements can be
installed using: ::

	pip install -r requirements.txt

Additional requirements to build the documentation can be found in the file
[requirements_doc.txt](requirements_doc.txt), and can be installed using: ::

	pip install -r requirements_doc.txt

On Debian Linux systems, the following Python packages are required to run the
Cole-Cole decomposition routines: ::

	numpy
	scipy
	matplotlib
	geccoinv
	sip_models

In order to build the documentation, the additional packages are required: ::

	sphinx

Under Debian-related Linux systems, these packages can be installed using the
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


## Installation

Stable versions are released to pipy and can be installed using: ::

	pip install ccd_tools

Install the source package using setuptools: ::

    python setup.py build
    python setup.py install

The package can also be installed to a user-defined directory: ::

    export PYTHONUSERBASE=$HOME/inst/pip_installs
    export PYTHONPATH=$HOME/inst/pip_installs/lib/python3.4/\
        site-packages/:$PYTHONPATH
    python setup.py install --user
    export PATH=$HOME/inst/pip_installs/bin:$PATH


For developers: ::

    python seutp.py develop --user

To build the documentation ::

    cd docs/doc
    make html

Setuptools developer guide:

https://pythonhosted.org/setuptools/setuptools.html

Documentation
-------------

 * Documentation is located in docs/
 * The sphinx-generated documentation is located in docs/doc

## Roadmap

The following functionality is planned to be implemented in the near future
(Q1-Q3 2017). After that, new feature will probably only be implemented when
required. For additional todo-items, please refer to the issues of this project
and to the file [TODO](TODO).

The current version is 0.8.

### 0.8.1

* first version under the new name 'Cole-Cole decomposition tools' (CCD)
* first (proper) version uploaded to pypi
* first Python 3 version
* first version with a DOI (via Zenoodo)
* initial homepage with online-documentation

### 0.9

* improve testing framework for **dd_time.py**
* implement Cole-Cole decomposition (c less than 1) also for conductivity
  formulation
* improve Jupyter integration and provide examples
* provide mybinder-integration

### 1.0

* proof-of-concept web interface
* implement the addition of a high-frequency EM-Cole-Cole term, decoupled from
  the other polarization terms
