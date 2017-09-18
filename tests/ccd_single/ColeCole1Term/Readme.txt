Generate various CR spectra from 1-term Cole-Cole models and fit them with the
Debye model.

run test_cases.py to generate the results:

python test_cases.py

Structure of generated CR spectra
---------------------------------

rho0_variation/
    + set1/
        + colecole.pars -> each line contains one CC-parameters set (4 values) used to generate one spectrum
        + data.dat
        + frequencies.dat
        + DD_results/
            + [output from dd_single.py]
    + set2/
        + [...]
m_variation/
    + set1/
        + [...]
tau_variation/
    + set1/
        + [...]
c_variation/
    + set1/
        + [...]

Workflow
--------

generate_spectra([None, m, tau, c], [10,20,30,40,100,200,1000])
    + find next free set-nr for varied variable ()
    + loop through the values and generate spectra
-> do this for as many variables/sets you want

generate debye-decomposition calls for all sets

run bash script

for each set:
    - read in original CC values
    - read in DD results
    - create plots

Output
------
Then plot:
    - rho0_cc vs rho0_dd
    - m vs m_tot
    - m vs m_tot_n
    - tau vs tau_mean
    - tau vs tau_50

