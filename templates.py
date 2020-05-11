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
from matplotlib.backends.backend_pdf import PdfPages
from scipy import interpolate
from docopt import docopt
from digicampipe.utils.docopt import convert_int, convert_text


def entry():

    args = docopt(__doc__)
    output_dir = convert_text(args['--output_dir'])

    pdf = PdfPages(os.path.join(output_dir, 'templates.pdf'))

    path_spe = '/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/SPE_distribution'
    path_template = '/Volumes/GreyWind/CTA/Data/LST/LST_small_pixels/template'

    spe = ['SPE_12ns.dat',
           'SPE_12ns.dat',
           'SPE_20ns.dat',
           'SPE_Gentile_oxt0d08_spe0d05_d2018-10-04.txt']

    template = ['Template07ns_original.txt',
                'Template12ns_original.txt',
                'Template20ns_original.txt',
                'pulse_CTA-Fx3.dat']

    label_spe = ['SPE 12 ns', 'SPE 12 ns', 'SPE 20 ns', 'SPE Gentile']
    label_template = ['FWHM : 07 ns', 'FWHM : 12 ns', 'FWHM : 20 ns', 'Fx3']

    # Old configuration (Yves)
    spe_yves = os.path.join(path_spe, spe[3])
    template_yves = os.path.join(path_template, template[3])

    # config 1:
    spe_config_1 = os.path.join(path_spe, spe[0])
    template_config_1 = os.path.join(path_template, template[0])

    # config 2: (same as config 3, but with Sampling rate 1.0 GHz)
    spe_config_2 = os.path.join(path_spe, spe[2])
    template_config_2 = os.path.join(path_template, template[2])

    # config 3: (same as config 2, but with Sampling rate 0.5 GHz)
    spe_config_3 = os.path.join(path_spe, spe[2])
    template_config_3 = os.path.join(path_template, template[2])

    spe_list = [spe_yves,
                spe_config_1,
                spe_config_2,
                spe_config_3]

    template_list = [template_yves,
                     template_config_1,
                     template_config_2,
                     template_config_3]

    template_labels = ['config 0: FWHM 3.2ns, CTA Fx3',
                       'config 1: FWHM 07ns',
                       'config 2: FWHM 20ns',
                       'config 3: FWHM 20ns']

    spe_labels = ['config 0: SST1M, LVR3',
                  'config 1: SPE 12ns',
                  'config 2: SPE 20ns',
                  'config 3: SPE 20ns']

    colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
    lines = ['solid', 'solid', 'solid', 'dashed']

    fig, (ax1, ax2) = plt.subplots(2, 1)

    for i, file in enumerate(spe_list):

        with open(spe_list[i], 'r') as f:
            pe, prob = np.loadtxt(f, delimiter=None, usecols=(0, 1), unpack=True)

        with open(template_list[i], 'r') as f:
            time, amp = np.loadtxt(f, delimiter=None, usecols=(0, 1), unpack=True)
            amp /= np.max(amp)

            centered = True

            if centered is True:
                max_index = np.argmax(amp)
                time -= time[max_index]

        if i == 0:
            initial = 0
            final = -1
        else:
            initial = 0
            final = 90

        ax1.plot(time[initial:final], amp[initial:final], label=template_labels[i], color=colors[i], linestyle=lines[i])
        ax2.semilogy(pe, prob, label=spe_labels[i], color=colors[i], linestyle=lines[i])

    ax1.legend()
    ax1.set_ylabel('Normalized Amplitude')
    ax1.set_xlabel('Time [ns]')

    ax2.legend()
    ax2.set_ylim(1e-8, 20)
    ax2.set_xlabel('Number of p.e')
    ax2.set_ylabel('SPE distribution')

    plt.tight_layout()
    pdf.savefig(fig)
    pdf.close()

    plt.show()

    # Waveform cutter
    # with open(template_config_1, 'r') as f:
    #     time, amp = np.loadtxt(f, delimiter=None, usecols=(0, 1), unpack=True)
    #
    # f = interpolate.interp1d(time, amp)
    #
    # time = np.arange(10, 50, 0.2)
    # amp = f(time)
    # time = np.arange(0, 40, 0.2)
    #
    # plt.plot(time, amp, label='config 1')
    # plt.show()
    # print('')
    #
    # file_name =  os.path.join(path_template, 'Template07ns_cut.txt')
    #
    # np.savetxt(file_name, np.c_[time, amp], fmt=['%.2f', '%10.10f'], header='Waveform with FWHM 7ns')


if __name__ == '__main__':
    entry()
