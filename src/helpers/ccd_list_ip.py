#!/usr/bin/python
# *-* coding: utf-8 *-*
# List the contents of the file "integrated_parameters.dat" on the command line
import os
import pandas as pd
import numpy as np


filename = "integrated_paramaters.dat"
if not os.path.isfile(filename):
    print('Filename not found: "{0}"'.format(filename))

with open(filename, 'r') as fid:
    fid.readline()
    fid.readline()
    fid.readline()
    header = fid.readline().strip()[1:].split(' ')

    indices = np.argsort(header)

    data = np.atleast_2d(np.loadtxt(fid)).T
    print data.shape
    # for label, subdata in zip(header, np.atleast_2d(data).T):
    for index in indices:
        label = header[index]
        subdata = data[index, :]
        print '{0:20} - {1}'.format(label, subdata)


    # df = pd.DataFrame(np.atleast_2d(data)) #, columns=header)
    # print df

