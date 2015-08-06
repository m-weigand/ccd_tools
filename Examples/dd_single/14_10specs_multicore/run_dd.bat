REM we use a Warburg decomposition here
set DD_C=0.5
set DD_STARTING_MODEL=3

dd_single.py -f frequencies.dat -d data.dat -n 20 -o results --tausel data_ext^
    --tausel data_ext^
    --lambda 1.0^
    -c 2

pause
