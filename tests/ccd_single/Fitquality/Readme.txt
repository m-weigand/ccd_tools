Tests in this directory are concerned with the quality of the fit and find
regressions in the code.

Running tests
-------------

To check the current version of dd_single.py against recorded tests, just run
::

	nosetests -s -v test_cases.py

Creating a new tests
--------------------

* Create a new subdirectory, if possible following the convention t_%.2i
* copy the frequencies to a file named frequencies.dat (one frequency per
  line)
* copy the data to a file 'data.dat' (one spectrum per line)
* copy the file 'test_func.py' from 'SkeletonFiles/test_func.py' and edit it
  according to your needs.
* Initialise the test using ::

	dd_test.py --init

  vim will open with the test configuration file which can then be edited
  by the user. Save and close by typing::

   :wq

  This will create a new configuration file called "test.cfg" in the test
  directory.
* A new test can now be recorded using::

	dd_test.py --record

  This will run the previously created test, and save it in a new subdirectory
  in "test_results". Tests are numbered with the format %.2i
* The recording process can be re-executed at any time in the future, e.g.
  when a new version of the DD-programs was tested and a new base-line
  for the tests needs to be set. Old results will not be deleted, new result
  directories will be created.
* Testing is done by executing::

	dd_test.py --test

  in the top directory of a test (which contains "data.dat", "frequencies.dat",
  , "test_func.py", and "test.cfg".

  To test against an older test result, append the name of the corresponding
  subdirectory in the "test_results/" directory, e.g. ::

	dd_test.py --test 02


