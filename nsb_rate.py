#! /anaconda3/envs/LST_SiPM/bin/python
"""
NSB rate for the safethreshold

Usage:
    nsb_rate --output_dir=PATH

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


def nsb_rate(file_list, fadc_freq, fadc_bins):
    """

    :param file_list:
    :param fadc_freq:
    :param fadc_bins:
    :return:
    """

    print('f_ADC / n_ADC bins = ', fadc_freq / fadc_bins)
    print('n_ADC bins / f_ADC  = ', fadc_bins / fadc_freq)
    T_event = fadc_bins / fadc_freq

    threshold_list = []
    rates_list = []

    triggered_list = []
    events_list = []

    for i, file in enumerate(file_list):

        with open(file, 'r') as f:
            threshold, triggered, events = np.loadtxt(f, delimiter=' ', usecols=(0, 1, 2), unpack=True)

        threshold = np.array(threshold)
        triggered = np.array(triggered)
        events = np.array(events)

        ind = np.argsort(threshold)
        threshold = threshold[ind]
        triggered = triggered[ind]
        events = events[ind]

        nsb_rate = (triggered / events) * (1 / T_event[i])
        nsb_rate = np.array(nsb_rate)

        threshold_list.append(threshold)
        rates_list.append(nsb_rate)

        triggered_list.append(triggered)
        events_list.append(events)

    return threshold_list, rates_list, triggered_list, events_list,


def entry():

    args = docopt(__doc__)
    output_dir = convert_text(args['--output_dir'])

    factor = 2
    fadc_bins = 55
    fadc_frequencies = np.array([1e9, 1e9, 0.5e9])
    nsb_path = '/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/safe_threshold'
    nsb_rate_files = [os.path.join(nsb_path, 'config_1', 'rate_scan_NSBx2.txt'),
                      os.path.join(nsb_path, 'config_2', 'rate_scan_NSBx2.txt'),
                      os.path.join(nsb_path, 'config_3', 'rate_scan_NSBx2.txt')]

    threshold_list, rates_list, triggered_list, events_list = nsb_rate(file_list=nsb_rate_files, fadc_freq=fadc_frequencies, fadc_bins=fadc_bins)


    pdf = PdfPages(os.path.join(output_dir, 'nsb_rates.pdf'))
    # nsb_config_label = ['NSB rate x{} : config 1'.format(factor),
    #                     'NSB rate x{} : config 2'.format(factor),
    #                     'NSB rate x{} : config 3'.format(factor)]

    nsb_config_label = ['NSB rate x{} : \n 07ns FWHM, \n SPE 12ns, 1GHz'.format(factor),
                        'NSB rate x{} : \n 20ns FWHM, \n SPE 20ns, 1GHz'.format(factor),
                        'NSB rate x{} : \n 20ns FWHM, \n SPE 20ns, 0.5GHz'.format(factor)]

    fig_rate, ax_rate = plt.subplots()
    fig_triggered, ax_triggered = plt.subplots()
    fig_events, ax_events = plt.subplots()
    fig_prob, ax_prob = plt.subplots()

    for k in range(len(nsb_rate_files)):

        ax_rate.semilogy(threshold_list[k], rates_list[k], label=nsb_config_label[k])
        # ax_rate.semilogy(threshold_list[k], nsrates_listb_rate[k], label=nsb_config_label[k], linestyle='None', marker='o')
        # ax_rate.plot(threshold_list[k], rates_list[k], label=nsb_config_label[k])
        ax_triggered.plot(threshold_list[k], triggered_list[k], label=nsb_config_label[k])
        ax_events.plot(threshold_list[k], events_list[k], label=nsb_config_label[k])
        ax_prob.plot(threshold_list[k], triggered_list[k] / events_list[k], label=nsb_config_label[k])

        ax_rate.set_xlabel('Threshold [LSB]')
        ax_rate.set_ylabel('Rate [Hz]')
        ax_triggered.set_xlabel('Threshold [LSB]')
        ax_triggered.set_ylabel('Triggered events')
        ax_events.set_xlabel('Threshold [LSB]')
        ax_events.set_ylabel('Total events')
        ax_prob.set_xlabel('Threshold [LSB]')
        ax_prob.set_ylabel('Trigger probability')

    ax_rate.legend()
    ax_triggered.legend()
    ax_events.legend()
    ax_prob.legend()

    fig_rate.tight_layout()
    fig_events.tight_layout()
    fig_triggered.tight_layout()
    fig_prob.tight_layout()

    pdf.savefig(fig_events)
    pdf.savefig(fig_triggered)
    pdf.savefig(fig_prob)
    pdf.savefig(fig_rate)

    pdf.close()


if __name__ == '__main__':
    entry()
