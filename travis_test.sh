#!/usr/bin/env bash

# run tests
cd tests/
nosetests -s -v
cd ..

# build documentation
cd docs/doc
make clean
make html
cd ../..

