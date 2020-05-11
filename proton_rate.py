#! /anaconda3/envs/LST_SiPM/bin/python
"""
NSB rate for the safethreshold

Usage:
    proton_rate --output_dir=PATH

Options:
    -h --help                   Show this screen.
    --output_dir=PATH           Path to the output directory, where the outputs (pdf files) will be saved.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from docopt import docopt
from digicampipe.utils.docopt import convert_int, convert_text


def proton_rate(file_list, factor):
    """

    :param file_list:
    :param factor:
    :return:
    """

    print('factor = ', factor)

    threshold_list = []
    rates_list = []

    for i, file in enumerate(file_list):

        with open(file, 'r') as f:
            threshold, proton_rate, = np.loadtxt(f, delimiter=' ', usecols=(0, 1), unpack=True)

        threshold = np.array(threshold)
        proton_rate = np.array(proton_rate)

        ind = np.argsort(threshold)
        threshold = threshold[ind]
        proton_rate = proton_rate[ind]

        proton_rate *= factor

        threshold_list.append(threshold)
        rates_list.append(proton_rate)

    return threshold_list, rates_list


def entry():

    args = docopt(__doc__)
    output_dir = convert_text(args['--output_dir'])

    factor = 1.5
    proton_path = '/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/safe_threshold'
    proton_rate_files = [os.path.join(proton_path, 'config_1', 'trigger_rate_proton.dat'),
                         os.path.join(proton_path, 'config_2', 'trigger_rate_proton.dat'),
                         os.path.join(proton_path, 'config_3', 'trigger_rate_proton.dat')]

    threshold_list, rates_list = proton_rate(file_list=proton_rate_files, factor=factor)

    #print(threshold_list, rates_list)

    pdf = PdfPages(os.path.join(output_dir, 'proton_rates.pdf'))
    proton_config_label = ['Proton rate x{} : \n 07ns FWHM, \n SPE 12ns, 1GHz'.format(factor),
                           'Proton rate x{} : \n 20ns FWHM, \n SPE 20ns, 1GHz'.format(factor),
                           'Proton rate x{} : \n 20ns FWHM, \n SPE 20ns, 0.5GHz'.format(factor)]

    fig_rate, ax_rate = plt.subplots()

    for k in range(len(proton_rate_files)):

        ax_rate.semilogy(threshold_list[k], rates_list[k], label=proton_config_label[k])
        # ax_rate.semilogy(threshold_list[k], nsrates_listb_rate[k], label=nsb_config_label[k], linestyle='None', marker='o')
        # ax_rate.plot(threshold_list[k], rates_list[k], label=nsb_config_label[k])

        ax_rate.set_xlabel('Threshold [LSB]')
        ax_rate.set_ylabel('Rate [Hz]')

    ax_rate.legend()
    fig_rate.tight_layout()

    pdf.savefig(fig_rate)

    pdf.close()


if __name__ == '__main__':
    entry()
