Windows
=======

The installation for the Windows operating system consists of the following steps:

* Installation of a suitable Python distribution
* (optional) Installation of the MiKTeX Latex distribution (under Windows,
  Latex support is disabled by default, and has to be activated using the
  corresponding environment variable).
* Installation of the ccd_tools (via pip install)
* Installation of Git for installation of ccd_tools from local source.

There are multiple suitable Python distributions to choose from. At the moment
the Anaconda distribution is recommended: https://www.anaconda.com/download/ (use
Python 3.6, 64 bit)

Anaconda installation
---------------------

Anaconda is a Python distribution, simplifying package management and using the conda package management system.
Download Anaconda (Python 3.6 version) here: https://www.anaconda.com/download/
and follwow the installation instructions.
In addition, a installation guide can be found here: https://docs.anaconda.com/anaconda/install/windows.html

To make shure that the newest Anaconda version will be used, update Anaconda after the installation.
Open the Anaconda prompt and use: ::

    conda update conda
    
After the insterallation and the update of Anaconda, install and enable the Jupyter ipywidges via conda, using the following command: ::

    conda install -c conda-forge ipywidgets

Git installation
----------------

From our Git repositories you can download the required Python packages, to use them as local source.
To use Git as a version control system and to clone the Git repository, you need to download and install Git to your computer as well as a Git account.

Download Git for Windows from: https://git-for-windows.github.io
You can choose from Git BASH and Git GUI.

There are also some more alternative Git GUIS avalible: https://git-scm.com/download/gui/windows

Before cloning a Git repository to your local device the first time, you have to add your SSH authentication key to your Git account.
Adding SSH-Key: https://gitlab.geo.uni-bonn.de:443/help/ssh/README

For using the Git BASH, get yourself familiar with the following git commands:

    * git clone
    * git pull / git push
    * git add
    * git commit
    * git branch
    * git checkout
    * git merge

(Optional) MiKTeX
-----------------

MiKTeX is an implementation of the TeX typsetting system and used here as part of the plotting routines for lables.
To install the basic MiKTeX system on Windows, download and run the following installer: https://miktex.org/download

A detailed installation tutorial can be found here: https://miktex.org/howto/install-miktex

Installing ccd_tools
--------------------

via pip install
^^^^^^^^^^^^^^^

Stable versions of ccd-tools are released to pipy.
Open the Anaconda prompt (a terminal window should appear) and install ccd_tools, using the following command: ::

    pip install ccd_tools

The following Python packages are required and already part of the Anaconda distribution:
    
    * numpy
    * scipy
    * matplotlib

In addition, the folliwing Python packages are also required and part of the ccd-tools installation via 'pip install':

    * geccoinv
    * sip_models

via local source (Git clone)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create a working directory, e.g. *.../users/USERNAME/ccd-tools*.
2. Right click the folder and choose *Git Bash Here*, a terminal window should appear.
3. Clone the required Git repositories, using the following commands: ::

    git clone https://github.com/m-weigand/sip_models.git
    git clone https://github.com/m-weigand/geccoinv.git
    git clone https://github.com/m-weigand/ccd_tools.git    

4. Open the Anaconda prompt (a terminal window should appear).
5. To install geccoinv, navigate within the Anaconda promt to the corresponding directory *.../ccd-tools/geccoinv* and use the following commands: ::
    
    pip install -U pip
    pip install -r requirements.txt
    python setup.py install 

(to navigate within the Anaconda promt, use the 'cd' command.)

6. To install sip-models, navigate within the Anaconda promt to the corresponding directory .../ccd-tools/sip_models and use the following commands: ::

    pip install -r requirements.txt
    python setup.py install

7. To install ccd-tools, navigate within the Anaconda promt to the corresponding directory .../ccd-tools/ccd_tools and use the following commands: ::

    pip install -r requirements.txt
    python setup.py install

via local source (Zip download)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create a working directory, e.g. *.../users/USERNAME/ccd-tools*.
2. Download the required Git repositories to your working directory:

    * https://github.com/m-weigand/sip_models/archive/master.zip
    * https://github.com/m-weigand/geccoinv/archive/master.zip
    * https://github.com/m-weigand/ccd_tools/archive/master.zip

3. Unzip the ZIP-files and create the following subdirectories:

    * *.../ccd-tools/sip_models*
    * *.../ccd-tools/geccoinv*
    * *.../ccd-tools/ccd_tools*

4. Open the Anaconda prompt (a terminal window should appear).
5. To install geccoinv, navigate within the Anaconda promt to the corresponding directory *.../ccd-tools/geccoinv* and use the following commands: ::
    
    pip install -U pip
    pip install -r requirements.txt
    python setup.py install 

6. To install sip-models, navigate within the Anaconda promt to the corresponding directory .../ccd-tools/sip_models and use the following commands: ::

    pip install -r requirements.txt
    python setup.py install

7. To install ccd-tools, navigate within the Anaconda promt to the corresponding directory .../ccd-tools/ccd_tools and use the following commands: ::

    pip install -r requirements.txt
    python setup.py install

OLD
===

The installation for the Windows operating system consists of the following steps:

* Installation of a suitable Python distribution
* (optional) Installation of the MiKTex Latex distribution (under Windows,
  Latex support is disabled by default, and has to be activated using the
  corresponding environment variable).
* Installation of the Debye decomposition tools

There are multiple suitable Python distributions to choose from. At the moment
the Anaconda distribution is recommended: http://continuum.io/downloads (use
Python 2.7, 64 bit)

In the following, please install only one of the Python distributions, and then
proceed with the installation of the DD-Tools, and optionally the MikTex
distribution.

Installing the Anaconda Python distribution
-------------------------------------------

* Download the Python 2.7, 64 bit version of the Anaconda distribution:
  http://continuum.io/downloads

* Start by opening the file manager in the download directoy:

  .. image:: install/windows/anaconda/file_explorer.png
    :scale: 65%

* The following screenshots show the steps of the setup wizard. Usually all
  presets can be accepted by clicking on the 'next' button.

  .. image:: install/windows/anaconda/setup1.png
    :scale: 65%

  .. image:: install/windows/anaconda/setup2.png
    :scale: 65%

  .. image:: install/windows/anaconda/setup3.png
    :scale: 65%


  .. image:: install/windows/anaconda/setup4.png
    :scale: 65%

.. warning::

    Note that Anaconda (as tested in Juli, 2015) does not register the .py
    extension with the Python interpreter. That means that, at this point, you
    cannot click on a Python file and execute it as any executable. The
    following screenshots show you how to register Python with the **.py**
    extension.

* Find the file **fix_registry_windows.py** that resides in the root directory
  of the zip-archive (or the extracted directory). Note that sometimes the file
  extension *.py* is not shown.  Right click on the file, and select
  "Open with".

  .. image:: install/windows/anaconda/setup5.png
    :scale: 65%

* The following dialog in Windows 7 looks like:

  .. image:: install/windows/anaconda/open_with_01_win7.png
    :scale: 65%

* The Windows 8.1 version looks like this:

  .. image:: install/windows/anaconda/open_with_01.png
    :scale: 65%

* Click on 'More options' to expand the window:

  .. image:: install/windows/anaconda/setup6.png
    :scale: 65%

* Check the box "Use this app for all .py files". Scroll down and click on
  "Look for another app on this PC" at the bottom:

  .. image:: install/windows/anaconda/setup7.png
    :scale: 65%

* A file-open dialog appears. Select the python.exe binary in the Anaconda
  installation directory (in this example **C:\\Users\Maximilian\\Anaconda**),
  and click "open".

  .. image:: install/windows/anaconda/setup8.png
    :scale: 65%

* The icon next to all Python (.py) files should now show the Python logo:

  .. image:: install/windows/anaconda/setup11.png
    :scale: 65%

.. note::

    During the process of associating the file type .py with the Python.exe
    executable the Python script **fix_registry_windows.py** was executed. This
    script tries to fix some common problems with the file type association. If
    you associated the extension via another way, please execute this script
    once.

Installing the DD tools
-----------------------

* The DD tools are provided in **.zip** file which contains the source code,
  the documentation, examples, and a Windows installation file. Extract the
  archive file to a new directory:

  .. image:: install/windows/dd_tools_msi/setup01.png

* We provide a MSI-Installation file called **dd_tools_0.5.4.win.amd64.msi**
  (the version number can vary). Execute this installer by double clicking on
  it, and follow the installation instructions (usually all preset settings can
  be accepted by clicking 'next').

  .. image:: install/windows/dd_tools_msi/setup02.png

* After the installation, open the following subdirectory in the extracted
  directory: **dd_interfaces/examples/dd_single/01**. Execute the file
  **run_dd** by double clicking on it:

  .. image:: install/windows/dd_tools_msi/setup03.png

* A terminal window should appear with the output of the call.

  .. image:: install/windows/dd_tools_msi/setup04.png

  The window should close itself after the decomposition finished. The
  installation was successful if a directory **results/** was created with the
  fit results.

(optional) Installing MiKTex
----------------------------

* MiKTex can be obtained from the homepage http://miktex.org/download.

.. note::

    We had some problems and long waiting times during the installation of
    MiKTex. Therefore we disabled the Latex support in the DD tools for the
    Windows installation, and made MiKTex an optional requirement.

.. note::

    The first plotting call will take a LONG time, as MiKTex will
    (automatically) install (and download) all required latex packages.
    Subsequent calls should be much faster!

.. image:: install/windows/miktex/setup01.png
    :scale: 65%

.. image:: install/windows/miktex/setup02.png
    :scale: 65%

.. image:: install/windows/miktex/setup03.png
    :scale: 65%

.. image:: install/windows/miktex/setup04.png
    :scale: 65%

.. image:: install/windows/miktex/setup05.png
    :scale: 65%

.. image:: install/windows/miktex/setup06.png
    :scale: 65%

.. image:: install/windows/miktex/setup07.png
    :scale: 65%

Problems
--------

* We experienced some Problems with Anaconda 2.4 on Windows 64-bit with the
  mock-module missing:

  ::

    pkg_resources.DistributionNotFound: The 'mock' distribution was not found and is
     required by matplotlib

  Open the Anaconda command prompt an execute: ::

    pip install mock

* if the decomposition starts, but command line options are not recognized,
  this is usually a problem with incorrect file type associations. We provide a
  file **fix_registry_windows.py** (which normally already executed during the
  installation process) which tries to fix some of these problems. Just execute
  it in order to implement the fixes.

  In addition, the following web links discuss solutions to this kind of problems:

  * http://stackoverflow.com/questions/9880540/python-command-line-arguments-windows
  * http://bugs.python.org/issue7936
  * http://eli.thegreenplace.net/2010/12/14/problem-passing-arguments-to-python-scripts-on-windows/


