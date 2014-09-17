#!/bin/bash

function dd(){
    # parameters
    Nd=$2
    
    lambdas=(1 5 50 100)
    for lam in ${lambdas[@]}
    do
        output=dd_`printf %.4i ${lam}`_$1
        test -d ${output} && rm -r ${output}
        dd_single.py -f frequencies.dat -d data.dat -n ${Nd} -o ${output}\
            --lambda ${lam}
        cp ${output}/spec*_iteration*.png spec_`printf %.2i ${Nd}`.png
    done
}

declare -a Ndlist
#Ndlist=(2 3 4)
Ndlist=(`seq 1 99`)

for Nd in ${Ndlist[@]}
do
    echo $Nd
    dd Nd_`printf %.2i ${Nd}` ${Nd}
done
