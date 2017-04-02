#!/usr/bin/env python3

"""This scirpt dumps the input 'variables' file needed to run the
lwtnn converter kerasfunc2json.py.
"""
import argparse
from numpy import array
from numpy import inf, nan
import numpy as np
from json import dumps
from sys import stdout
from generator import STATS

# Took this from Peter's generator
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
        'inputs': [
            {
                'name': 'inputs',
                'variables': [],
            }
        ],
        'outputs': [
            {
                "labels": ["discriminant"],
                "name": "output_node"
            }
        ]
    }
    for fnum, fname in enumerate(FEATURES):
        offset, scale, transform = get_offset_scale_and_transform(fnum)
        if transform:
            name = '{}_{}'.format(fname, transform)
        else:
            name = fname
        feature = {
            "name": name,
            "offset": offset,
            "scale": scale,
        }
        out_dict['inputs'][0]['variables'].append(feature)
    stdout.write(dumps(out_dict, indent=2, sort_keys=True))

if __name__ == '__main__':
    run()
