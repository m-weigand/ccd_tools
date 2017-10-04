Linux
=====

Python - general
----------------

Install a Python 3 environment, e.g. Anaconda or Virtualenv, and make sure the following Python packages are installed:
  
    * numpy, matplotlib, pandas, sphinx

For the case of missing packages you can either use conda (provided the
Anaconda stack was installed) ::

    conda install numpy matplotlib scipy pandas sphinx

or pip ::

    pip install numpy matplotlib scipy pandas sphinx

How to setup Anaconda
^^^^^^^^^^^^^^^^^^^^^

Anaconda can be downloaded here: https://www.anaconda.com/download/
An installation guide for Linux (and for other platforms) can be found here: https://docs.anaconda.com/anaconda/install/linux


How to setup Virtualenv
^^^^^^^^^^^^^^^^^^^^^^^

Virtualenv is a tool to create isolated Python environments.
An installation guide and all virtualenv-support can be found here: https://virtualenv.pypa.io/en/stable/installation/

Creat a virtual environment ::

    mkvirtualenv --python /usr/bin/python3 NAME

with *NAME* as the name of your virtual environment. For e.g. CRTomo tool you can set *NAME* to *crtomo* or for EDF to *edf*.
Open your virtual environment with ::

    workon *NAME*

Setup a working directory
^^^^^^^^^^^^^^^^^^^^^^^^^

Create the directory: */home/USERNAME/ccd-tools* and subdirectories for the different git repositiries.

How to use the Git repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An installation guide for Git can be found here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
Install git and get yourself familiar with the following git commands:

    * git clone
    * git pull / git push
    * git add
    * git commit
    * git branch
    * git checkout 
    * git merge

Simply clone the following repositories::

    git clone https://github.com/m-weigand/sip_models.git
    git clone https://github.com/m-weigand/geccoinv.git
    git clone https://github.com/m-weigand/ccd_tools.git

into the corresponding folder */home/USERNAME/ccd-tools*.

Getting Started: CCD-tools with Anaconda
----------------------------------------

.. todo::
	
    Edit: Installation of ccd with Anaconda


Getting Started: CCD-tools with Virtualenv
------------------------------------------

Python and Virtualenv
^^^^^^^^^^^^^^^^^^^^^

1. Install Python and Virtualenv as described above.
3. Create a virtual environment (named *ccd-tools*), using the following commands: ::

    mkvirtualenv --python /usr/bin/python3 ccd-tools
    pip install --upgrade pip

If the virtual environment already exists, you can enter it, using the following command: ::

    workon ccd-tools

A) Installation of ccd-tools and required packages via pip install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enter your virtual environment and install ccd-tools including sip-models and geccoinv, using the following commands: ::
    
    workon ccd-tools
    pip install ccd_tools

For the installation via pip install is no local copy of the git-repositories needed.

B) Installation of ccd-tools and required packages via local source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install Git as described above.
2. Create a working directory and clone the Git repositories into the corresponding folder.
3. Enter your virtual environment, using the following commands: ::
    
    workon ccd-tools

4. To install geccoinv, go to the corresponding directory *.../ccd-tools/geccoinv* and use the following commands: ::
	
    pip install -U pip
    pip install -r requirements.txt
    python setup.py install

5. To install sip-models, go to the corresponding directory *.../ccd-tools/sip_models* and use the following commands: ::
	
    pip install -r requirements.txt
    python setup.py install

6. To install ccd-tools, go to the corresponding directory *.../ccd-tools/ccd_tools* and use the following commands: ::
	
    pip install -r requirements.txt
    python setup.py install

Getting Started: ccd-tools with Jupyter Notebooks and Virtualenv
----------------------------------------------------------------

Installing Jupyter Notebook
^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Install Python and Virtualenv, create a virtual environment and install ccd-tools as described above (A or B, both possible)
2. Enter your virtual environment and install Jupyter Notebooks, using the following commands: ::

    pip3 install --upgrade pip
    pip3 install jupyter

3. Install and enable the Jupyter Widget JavaScript library, using the following commands: ::

    pip install ipywidgets
    jupyter nbextension enable --py widgetsnbextension --sys-prefix

Starting the Notebook Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Navigate to the Notebook example directory *.../ccd-tools/ccd_tools/Examples/notebooks* and open Jupyter Notebooks: ::

    jupyter notebook

This will print some information about the notebook server in your terminal, including the URL of the web application (by default, http://localhost:8888)
It will then open your default web browser to this URL.
When the notebook opens in your browser, you will see the Notebook Dashboard, which will show a list of the notebooks, files, and subdirectories in the directory where the notebook server was started:

    *.../ccd-tools/ccd_tools/Examples/notebooks*

Using the Notebooks
^^^^^^^^^^^^^^^^^^^

.. todo::
	
    Edit: Insert a guide with screenshots

Old installation guide
======================

The *setuptools* distribution tools to manage the installation procedure:

::

    python setup.py install

should suffice to install the libraries and scripts.

::

    python setup.py build
    python setup.py install --prefix=$HOME/inst/dd

    export PYTHONUSERBASE=$HOME/inst/pip_installs
    export PYTHONPATH=$HOME/inst/pip_installs/lib/python2.7/\
        site-packages/:$PYTHONPATH
    python setup.py install --user
    export PATH=$HOME/inst/pip_installs/bin:$PATH
    python seutp.py develop --user

To build the documentation, execute ::

    cd docs/doc
    python setup.py sphinx_build

For certain versions of numpy (Debian Wheezy), there exist problems with
libopenblas (CPU goes to 100% and the program freezes). These problems are
related to multithreading issues in Python

Workarounds:

* Use only one thread in openblas:
  ::

    OPENBLAS_NUM_THREADS=1 dd_single.py [...]

* switch to atlas/libblas:

  ::

    update-alternatives --config libblas.so
    update-alternatives --config libblas.so.3
