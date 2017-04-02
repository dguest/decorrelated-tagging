#!/usr/bin/env python3

from generator import STATS
from keras.models import model_from_json
import numpy as np

model = model_from_json(open('data/arch.json').read())
model.load_weights('data/weights.h5')

def get_test_pattern():
    X = np.ones(10)[None,:]
    for i in range(X.shape[1]):
        V = X[:,i]
        if STATS['skew'][i] > 1.0:
            # Take log of feature when it has high skew.
            assert not np.isnan(STATS['meanlogxp1'][i])
            assert not np.isinf(STATS['meanlogxp1'][i])
            assert not np.isnan(STATS['stdlogxp1'][i])
            assert not np.isinf(STATS['stdlogxp1'][i])
            assert STATS['stdlogxp1'][i] > 0.
            V = np.log(V + 1.0)
            V = V - STATS['meanlogxp1'][i]
            V = V / STATS['stdlogxp1'][i]
        else:
            V = V - STATS['mean'][i]
            V = V / STATS['std'][i]
        X[:,i]  = V
    return X

x = get_test_pattern()
y = model.predict(x)
print(y)
