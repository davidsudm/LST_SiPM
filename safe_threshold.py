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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import find_intersection as inter
from proton_rate import proton_rate
from nsb_rate import nsb_rate
from matplotlib.backends.backend_pdf import PdfPages
from docopt import docopt
from digicampipe.utils.docopt import convert_int, convert_text


def entry():

    args = docopt(__doc__)
    output_dir = convert_text(args['--output_dir'])

    colors = ['tab:blue', 'tab:green', 'tab:orange']
    nsb_factor = 2

    fadc_bins = 55
    fadc_frequencies = np.array([1e9, 1e9, 0.5e9])
    nsb_path = '/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/safe_threshold'
    nsb_rate_files = [os.path.join(nsb_path, 'config_1', 'rate_scan_NSBx2.txt'),
                      os.path.join(nsb_path, 'config_2', 'rate_scan_NSBx2.txt'),
                      os.path.join(nsb_path, 'config_3', 'rate_scan_NSBx2.txt')]
    nsb_threshold_list, nsb_rates_list, nsb_triggered_list, nsb_events_list = nsb_rate(file_list=nsb_rate_files, fadc_freq=fadc_frequencies, fadc_bins=fadc_bins)

    nsb_config_label = ['NSB x{}'.format(nsb_factor),
                        'NSB x{}'.format(nsb_factor),
                        'NSB x{}'.format(nsb_factor)]

    nsb_config_label = ['config 1 : NSB x{}'.format(nsb_factor),
                        'config 2 : NSB x{}'.format(nsb_factor),
                        'config 3 : NSB x{}'.format(nsb_factor)]

    proton_factor = 1.5
    proton_path = '/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/safe_threshold'
    proton_rate_files = [os.path.join(proton_path, 'config_1', 'trigger_rate_proton.dat'),
                         os.path.join(proton_path, 'config_2', 'trigger_rate_proton.dat'),
                         os.path.join(proton_path, 'config_3', 'trigger_rate_proton.dat')]

    proton_threshold_list, proton_rates_list = proton_rate(file_list=proton_rate_files, factor=proton_factor)

    proton_config_label = ['proton x{} : \n 07ns FWHM, SPE 12ns, 1GHz'.format(proton_factor),
                           'proton x{} : \n 20ns FWHM, SPE 20ns, 1GHz'.format(proton_factor),
                           'proton x{} : \n 20ns FWHM, SPE 20ns, 0.5GHz'.format(proton_factor)]

    proton_config_label = ['config 1 : proton x{}'.format(proton_factor),
                           'config 2 : proton x{}'.format(proton_factor),
                           'config 3 : proton x{}'.format(proton_factor)]

    # GET THE VALUE FROM INTERPOLATION
    config_labels = ['07ns FWHM, SPE 12ns, 1GHz',
                     '20ns FWHM, SPE 20ns, 1GHz',
                     '20ns FWHM, SPE 20ns, 0.5GHz']

    x_int = []
    y_int = []

    for i in range(len(nsb_rate_files)):
        x_temp, y_temp = inter.intersection(nsb_threshold_list[i], nsb_rates_list[i],
                                            proton_threshold_list[i], proton_rates_list[i])
        print('{} --> threshold = {} , rate = {}'.format(config_labels[i], x_temp, y_temp))
        x_int.append(x_temp)
        y_int.append(y_temp)

    # PLOTS
    fig_rate, ax = plt.subplots()
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    for k in range(len(nsb_rate_files)):
        if k == 1:
            ax.semilogy(nsb_threshold_list[k], nsb_rates_list[k], label=nsb_config_label[k], linestyle='dashed',
                    color=colors[k])
            ax.semilogy(proton_threshold_list[k], proton_rates_list[k], label=proton_config_label[k], color=colors[k])
            ax.semilogy(x_int[k], y_int[k], color='black', marker='*', linestyle='None', alpha=0.5)
            ax.axvline(x=x_int[k], linestyle='dotted', color='gray')
            ax.axhline(y=y_int[k], linestyle='dotted', color='gray')

    ax.set_xlabel('Threshold [LSB]')
    ax.set_ylabel('Rate [Hz]')
    ax.legend(loc=1)

    fig_rate.tight_layout()
    pdf = PdfPages(os.path.join(output_dir, 'safe_threshold.pdf'))
    pdf.savefig(fig_rate)
    pdf.close()


if __name__ == '__main__':
    entry()

