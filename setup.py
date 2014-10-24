#!/usr/bin/env python
from setuptools import setup
# from setuptools import find_packages
# find_packages

# under windows, run
# python.exe setup.py bdist --format msi
# to create a windows installer

version_short = '0.5'
version_long = '0.5.7'

if __name__ == '__main__':
    setup(name='dd_interface',
          version=version_long,
          description='Time-lapse Debye decomposition routines',
          author='Maximilian Weigand',
          author_email='mweigand@geo.uni-bonn.de',
          url='http://www.geo.uni-bonn.de/~mweigand',
          # find_packages() somehow does not work under Win7 when creating a
          # msi # installer
          # packages=find_packages(),
          package_dir={'': 'lib'},
          packages=['lib_dd', ],
          scripts=['src/dd_single/dd_single.py',
                   'src/dd_time/dd_time.py',
                   'src/dd_space_time/dd_space_time.py',
                   'src/dd_test/dd_test.py',
                   'src/ddps/ddps.py',
                   'src/ddpt/ddpt.py',
                   'src/ddpst/ddpst.py'],
          install_requires=['numpy', 'scipy>=0.12', 'matplotlib', 'geccoinv']
          )
