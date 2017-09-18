#!/bin/bash
rm -r Data/
./test_cases.py
cd Data/
debye_decomposition.py -f frequencies.dat -d data.dat  --plot -c 2
