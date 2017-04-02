#!/usr/bin/env python3

import argparse
from numpy import array
from numpy import inf, nan
import numpy as np
from json import dumps
from sys import stdout
from generator import STATS

# Hardcoded data stats for preprocessing.
# STATS = {'mean': array([  3.99764496e+02,   9.01243668e+01,   1.55931513e-04,
#           1.13176357e-03,   6.94682556e+02,   4.36270538e+02,
#          -6.22161955e-04,  -7.31336186e-04,   4.17721868e-01,
#           1.58483064e+00]),
#          'meanlogxp1': array([ 5.71247631,  4.27571605,  0.02735545,  0.4223016 ,  6.27538202,
#             5.78885174,        -inf,        -inf,  0.34158588,  0.91784849]),
#         'skew': array([  3.14232326e+00,   4.40089512e+00,  -3.24697903e-05,
#          -2.69548665e-03,   2.00086665e+00,   2.94293118e+00,
#           6.08206028e-04,   2.35658721e-03,  -1.29811163e-03,
#           9.92644310e-01]),
#         'std': array([  4.13315236e+02,   9.00398648e+01,   1.10274361e+00,
#           1.81264423e+00,   5.76709172e+02,   4.49498610e+02,
#           1.15015003e+00,   1.81232438e+00,   1.71759485e-01,
#           6.68603005e-01]),
#         'stdlogxp1': array([ 0.65487487,  0.60894499,  0.97026408,  0.99906426,  0.71204135,
#          0.67161112,         nan,         nan,  0.12284954,  0.25136898])}

def get_offset_scale_and_transform(i):
    if STATS['skew'][i] > 1.0:
        transform = 'log1p'
        # Take log of feature when it has high skew.
        assert not np.isnan(STATS['meanlogxp1'][i])
        assert not np.isinf(STATS['meanlogxp1'][i])
        assert not np.isnan(STATS['stdlogxp1'][i])
        assert not np.isinf(STATS['stdlogxp1'][i])
        assert STATS['stdlogxp1'][i] > 0.
        offset = -STATS['meanlogxp1'][i]
        scale = 1 / STATS['stdlogxp1'][i]
    else:
        transform = ''
        offset = -STATS['mean'][i]
        scale = 1 / STATS['std'][i]
    return offset, scale, transform

FEATURES = ['jet_pt', 'jet_m', 'jet_eta', 'jet_phi', 'photon_E', 'photon_pt', 'photon_eta', 'photon_phi', 'jet_tau21', 'jet_D2']

def run():
    out_dict = {
        'input_sequences': [],
        'inputs': [],
        'outputs': [
            {
                "labels": ["discriminant"],
                "name": "output_node"
            }
        ]
    }
    for fnum, fname in enumerate(FEATURES):
        offset, scale, transform = get_offset_scale_and_transform(fnum)
        feature = {
            "name": fname if not transform else f'{fname}_{transform}',
            "offset": offset,
            "scale": scale,
        }
        out_dict['inputs'].append(feature)
    stdout.write(dumps(out_dict, indent=2, sort_keys=True))

if __name__ == '__main__':
    run()
