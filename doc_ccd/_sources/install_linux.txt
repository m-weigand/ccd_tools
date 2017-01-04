Linux
=====

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
