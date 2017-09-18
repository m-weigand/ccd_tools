#!/bin/bash
odir="results"
test -d "${odir}" && rm -r "${odir}"
dd_single.py -c 1 -o "${odir}" --lambda 300 --norm_mag 100
