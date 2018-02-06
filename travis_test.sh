#!/usr/bin/env bash

# run tests
echo "Entering test/ directory and running nosetests -s -v:"
cd tests/ccd_single

	cd ColeCole1Term
	nosetests -s -v
	cd ..

	cd Fitquality/
	nosetests -s -v
	cd ..

	cd Functionality/StartingModels
	nosetests -s -v
	cd ../..

	cd NoCrashTests
	nosetests -s -v
	cd ..

	cd NormMag
	nosetests -s -v
	cd ..

cd ../../

echo "Build documentation:"
# build documentation
cd docs/doc
make clean
make html
cd ../..

