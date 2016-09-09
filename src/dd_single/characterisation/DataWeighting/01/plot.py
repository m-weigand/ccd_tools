#!/usr/bin/env python3
import matplotlib as mpl
import pylab as plt
mpl.rcParams['font.size'] = 8.0
import numpy as np
import glob
import sip_formats.convert as SC

symbols = ('x', 'o', '+', '.', '/', '#')
colors = ('k', 'r', 'b', 'c', 'y', 'g', 'm')

directories = sorted(glob.glob('results_*'))

fig, axes = plt.subplots(1, 2, figsize=(10 / 2.54, 8 / 2.54))

for nr, directory in enumerate(reversed(directories)):
    print(directory)

    g = {}
    g['frequencies'] = np.loadtxt(directory + '/frequencies.dat')

    # data in cre_cim
    data = np.loadtxt(directory + '/data.dat')
    g['cre'], g['cim'] = SC.split_data(data, True)

    # forward response
    f = np.loadtxt(directory + '/f.dat')
    g['fcre'], g['fcim'] = SC.split_data(f, True)

    # convert to rmag/rpha
    rmag_rpha = SC.convert('cre_cim', 'rmag_rpha', data)
    g['rmag'], g['rpha'] = SC.split_data(rmag_rpha, True)

    frmag_rpha = SC.convert('cre_cim', 'rmag_rpha', f)
    g['frmag'], g['frpha'] = SC.split_data(frmag_rpha, True)

    # cre
    ax = axes[0]
    ax.loglog(
        g['frequencies'],
        g['cre'],
        '.',
        color=colors[nr],
    )

    ax.loglog(
        g['frequencies'],
        g['fcre'],
        '-',
        color=colors[nr],
        label=directory,
    )

    # cim
    ax = axes[1]
    ax.loglog(
        g['frequencies'],
        g['cim'],
        '.',
        color=colors[nr],
    )

    ax.loglog(
        g['frequencies'],
        g['fcim'],
        '-',
        color=colors[nr],
    )

    fig.tight_layout()
    fig.subplots_adjust(
        bottom=0.3,
        wspace=0.3,
        right=0.99,
        left=0.1,
    )

    leg = axes[0].legend(
        loc="lower center",
        ncol=axes.size,
        bbox_to_anchor=(0, 0, 1, 1),
        bbox_transform=fig.transFigure
    )

    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=7)

    fig.savefig('comparison.png', dpi=300)
