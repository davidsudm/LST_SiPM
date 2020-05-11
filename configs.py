#! /anaconda3/envs/Flasher/bin/python
"""
Safe threshold computation

Usage:
    safe_threshold --output_dir=PATH

Options:
    -h --help                   Show this screen.
    --output_dir=PATH           Path to the output directory, where the outputs (pdf files) will be saved.

"""

import os
import yaml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import interpolate
from docopt import docopt
from digicampipe.utils.docopt import convert_int, convert_text


def entry():

    args = docopt(__doc__)
    output_dir = convert_text(args['--output_dir'])

    with open('/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/safe_threshold/config_1/various_parameters.yml') as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)

    pdf = PdfPages(os.path.join(output_dir, 'new_configs_rate.pdf'))
    #pdf = PdfPages(os.path.join(output_dir, 'old_configs_rate.pdf'))

    data = []
    temp_row = []
    for a_key, sub_values in configs.items():
        for key, value in sub_values.items():
            temp_row.append(value)
        data.append(temp_row)
        temp_row = []
    data = np.array(data)

    columns = []
    rows = []
    for key in configs.keys():
        columns.append(key)
    for key in configs['config_1']:
    #for key in configs['david_1_1_1']:
        rows.append(key)

    #info = np.hsplit(data, (5, -4))[-1].T
    #data = np.hsplit(data, (5, -4))[0].T

    info = np.hsplit(data, (16, -4))[-1].T
    data = np.hsplit(data, (16, -4))[0].T

    # Get some pastel shades for the colors
    colors = ['forestgreen', 'limegreen', 'springgreen',
              'xkcd:red', 'orangered', 'tomato', 'coral',
              'skyblue', 'xkcd:sky blue', 'deepskyblue', 'dodgerblue', 'cornflowerblue',
              'mediumpurple']

    colors = ['xkcd:medium green', 'xkcd:soft green', 'limegreen',
              'xkcd:tangerine', 'xkcd:amber', 'xkcd:goldenrod', 'xkcd:yellow orange',
              'skyblue', 'xkcd:sky blue', 'deepskyblue', 'dodgerblue', 'cornflowerblue',
              'mediumpurple']

    colors = ['xkcd:orangered', 'xkcd:coral', 'salmon',
              'xkcd:periwinkle blue', 'xkcd:periwinkle', 'xkcd:pale violet', 'xkcd:pale lavender',
              'skyblue', 'xkcd:sky blue', 'deepskyblue', 'dodgerblue', 'cornflowerblue',
              'xkcd:grey blue']

    n_columns = len(columns)
    n_rows = len(rows)

    index = np.arange(len(columns)) + 0.0

    # Plot bars and create text labels for the table
    cell_text = []
    rate = np.array(info[0]).astype(float)
    triggered = np.array(info[1]).astype(int)
    total = np.array(info[2]).astype(int)
    parameter_label = info[3]

    rows = rows[0: 16]
    for parameter in range(len(rows)):
        cell_text.append([x for x in data[parameter]])

    fig, ax1 = plt.subplots(figsize=(24, 10))

    for config in range(n_columns):
        ax1.plot(index[config], rate[config], color=colors[config], marker='s', ms=7, mec='gray', mew=0.5)

    ax2 = ax1.twinx()

    for config in range(n_columns):
        ax2.plot(index[config], 100 * triggered[config]/total[config], mfc=colors[config], marker='*', ms=9, mec='gray', mew=0.5)

    # Add a table at the bottom of the axes
    the_table = ax1.table(cellText=cell_text,
                          rowLabels=rows,
                          cellLoc='center',
                          colLoc='center',
                          rowLoc='right',
                          colColours=colors,
                          colLabels=columns,
                          loc='bottom')

    prop = the_table.properties()
    cell = prop['child_artists']
    for i in range(len(cell)):
        cell[i].set_height(6.1 * cell[i].get_height())

    # Adjust layout to make room for the table:
    fig.subplots_adjust(left=0.2, bottom=0.64, right=0.9, top=0.9)
    ax1.set_ylim(1500, 3500)
    ax2.set_ylim(0.14, 0.18)
    ax1.set_ylabel("■ : Rate [Hz]")
    ax2.set_ylabel("★ : Triggered / Total [%]")
    ax1.set_xticks([])
    #plt.title('Yves  @ thr = 1500 mV | David @ thr = 400 LSB')
    pdf.savefig(fig)
    pdf.close()

    #print(the_table.properties())


if __name__ == '__main__':
    entry()