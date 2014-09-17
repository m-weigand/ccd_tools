Tests in this directory are concerned with the quality of the fit and find
regressions in the code.

Running tests
=============

To check the current version against recorded tests, just run

nosetests -s -v test_cases.py

Creating a new test
===================

* Create a new subdirectory, if possible following the convention t_%.2i
* copy the frequencies to a file named frequencies.dat (one frequency per
  line)
* copy the data to a file 'data.dat' (one spectrum per line)
* copy the file 'test_func.py' from 'SkeletonFiles/test_func.py' and edit
  according to your needs.
* Record the behaviour of the current debye_decomposition.py
  implementation with:

  dd_test.py --init --record

  vim will open with the test configuration file which can then be edited
  by the user. Save and close by typing:

  :wq

* The recording process can be executed at any time in the future, e.g.
  when a new version of the DD-programs was tested and a new base line
  for the tests needs to be set. Old results will not be deleted and
  there is the possibility to test against these old results.
