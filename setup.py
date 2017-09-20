#!/usr/bin/env python
# import sys
from setuptools import setup
# from setuptools import find_packages
# find_packages

# under windows, run
# python.exe setup.py bdist --format msi
# to create a windows installer

version_short = '0.8'
version_long = '0.8.9'
# if we are in a git directory, use the last git commit as the version

extra = {}
# if sys.version_info >= (3,):
#     print('V3')
#     extra['use_2to3'] = True

if __name__ == '__main__':
    setup(name='ccd_tools',
          version=version_long,
          description='Time-lapse Cole-Cole decomposition routines',
          author='Maximilian Weigand',
          author_email='mweigand@geo.uni-bonn.de',
          url='https://github.com/m-weigand/ccd_tools',
          license='GPL-3',
          keywords=['SIP, Cole-Cole model, Debye decomposition'],
          classifiers=[
              # "Development Status :: 5 - Production/Stable",
              "Development Status :: 4 - Beta",
              "License :: OSI Approved :: GNU Lesser General Public License " +
              "v3 (LGPLv3)",
              "Programming Language :: Python :: 3.4",
              "Intended Audience :: Science/Research",
          ],
          # find_packages() somehow does not work under Win7 when creating a
          # msi # installer
          # packages=find_packages(),
          package_dir={'': 'lib'},
          packages=[
              'lib_dd',
              'lib_dd.apps',
              'lib_dd.models',
              'lib_dd.conductivity',
              'lib_dd.decomposition',
              'lib_dd.io',
              'lib_dd.config',
              'lib_ccd_test',
          ],
          scripts=[
              'src/dd_single/dd_single.py',
              'src/dd_time/dd_time.py',
              'src/dd_space_time/dd_space_time.py',
              'src/dd_test/dd_test.py',
              'src/ddps/ddps.py',
              'src/ddpt/ddpt.py',
              'src/ddpst/ddpst.py',
              'src/ddplot/ddplot.py',
              'src/helpers/ccd_list_ip.py',
          ],
          install_requires=[
              'numpy',
              'scipy',
              'matplotlib',
              'geccoinv',
              'sip_models',
          ],
          **extra
          )
