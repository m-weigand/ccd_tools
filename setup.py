#!/usr/bin/env python
import os
import glob
from setuptools import setup

version_short = '0.8'
version_long = '0.8.15'

# generate entry points
entry_points = {'console_scripts': []}
scripts = [os.path.basename(script)[0:-3] for script in glob.glob('src/*.py')]
for script in scripts:
    print(script)
    entry_points['console_scripts'].append(
        '{0} = {0}:main'.format(script)
    )

if __name__ == '__main__':
    setup(name='ccd_tools',
          version=version_long,
          description='Time-lapse Cole-Cole decomposition routines',
          long_description=open('Readme.md', 'r').read(),
          author='Maximilian Weigand and Department of Geophysics,'
          'University of Bonn, Germany',
          author_email='mweigand@geo.uni-bonn.de',
          url='https://github.com/m-weigand/ccd_tools',
          license='GPL-3',
          keywords=['SIP, Cole-Cole model', 'Debye decomposition',
                    'Cole-Cole decomposition'],
          classifiers=[
              "Development Status :: 5 - Production/Stable",
              "License :: OSI Approved :: GNU Lesser General Public License " +
              "v3 (LGPLv3)",
              "Programming Language :: Python :: 3.4",
              "Programming Language :: Python :: 3.5",
              "Programming Language :: Python :: 3.6",
              "Intended Audience :: Science/Research",
          ],
          # find_packages() somehow does not work under Win7 when creating a
          # msi # installer
          # packages=find_packages(),
          package_dir={
              '': 'src',
              'lib_dd': 'lib/lib_dd',
              'lib_ccd_test': 'lib/lib_ccd_test',
          },
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
          entry_points=entry_points,
          py_modules=scripts,
          scripts=[
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
          )
