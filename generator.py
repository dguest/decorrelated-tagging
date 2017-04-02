# Define generator for classifier on Atlas adversarial data.
import os,random
import numpy as np
from numpy import array
from numpy import inf,nan
import h5py

# Hardcoded data stats for preprocessing.
STATS = {'mean': array([  3.99764496e+02,   9.01243668e+01,   1.55931513e-04,
          1.13176357e-03,   6.94682556e+02,   4.36270538e+02,
         -6.22161955e-04,  -7.31336186e-04,   4.17721868e-01,
          1.58483064e+00]),
         'meanlogxp1': array([ 5.71247631,  4.27571605,  0.02735545,  0.4223016 ,  6.27538202,
            5.78885174,        -inf,        -inf,  0.34158588,  0.91784849]),
        'skew': array([  3.14232326e+00,   4.40089512e+00,  -3.24697903e-05,
         -2.69548665e-03,   2.00086665e+00,   2.94293118e+00,
          6.08206028e-04,   2.35658721e-03,  -1.29811163e-03,
          9.92644310e-01]),
        'std': array([  4.13315236e+02,   9.00398648e+01,   1.10274361e+00,
          1.81264423e+00,   5.76709172e+02,   4.49498610e+02,
          1.15015003e+00,   1.81232438e+00,   1.71759485e-01,
          6.68603005e-01]),
        'stdlogxp1': array([ 0.65487487,  0.60894499,  0.97026408,  0.99906426,  0.71204135,
         0.67161112,         nan,         nan,  0.12284954,  0.25136898])}

def get_data_stats():
    # Get data stats used for normalization in order to hardcode these for Dan.
    h5file = '/extra/pjsadows0/ml/physics/adversarial_atlas/data/atlas_train.h5' # Same stats in train/valid/test.
    stats = {}
    with h5py.File(h5file, 'r') as f:
        # Stats computed from data are used to standardize NN input.
        # E.G. f['features'].attrs['meanlogxp1'] = np.log(X + 1.).mean(axis=0)
        for k in ['mean', 'std', 'skew', 'meanlogxp1', 'stdlogxp1']:
            stats[k] = f['features'].attrs[k]
    return stats
 
def generator_single(h5file, batchsize, start=0, stop=None):
    # Serve batches of modified train/valid/test data.
    if not stop:
        with h5py.File(h5file, 'r') as f:
            stop = f['features'].shape[0]
    stop = ((stop-start) // batchsize) * batchsize + start # Make sure all batches are full.
    assert (stop-start) % batchsize     == 0  # Batches will not exceed stop.
    with h5py.File(h5file, 'r') as f:
        assert f['features'].shape[0] >= stop
        iexample = start
        while True:
            assert iexample >= start
            assert iexample+batchsize <= stop
            batch = slice(iexample, iexample + batchsize)

            # Load data batch.
            # 10 features:['jet_pt', 'jet_m', 'jet_eta', 'jet_phi', 'photon_E', 'photon_pt', 'photon_eta', 'photon_phi', 'jet_tau21', 'jet_D2']
            X  = f['features'][batch,:]
            Y  = f['targets'][batch] # Target: (0:bg, 1:sig)
            W  = f['weights'][batch]
            
            # Standardize feature data using hardcoded STATS.
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
            
            # Scale background weight total to signal weight total. Use this when events are mixed, because there are more bg events.
            # We don't really need this for validation.
            #W[Y==0] = W[Y==0] * (f['weights'].attrs['total_sig'] / f['weights'].attrs['total_bg']) # Signal weights = 1.
            
            yield {'input':X}, {'output':Y}, {'output':W}

            iexample += batchsize
            if iexample >= stop:
                assert iexample == stop
                iexample = start  

if __name__ == '__main__':
    # Train a single network with metaparameters specified here.
    path = '/extra/pjsadows0/ml/physics/adversarial_atlas/data/'
    file_valid = path+'./atlas_valid.h5'
    batchsize  = 100
    gvalid = generator_single(file_valid, batchsize=batchsize)

    # Test generator.
    for i in range(10):
        batch = gvalid.next()
        assert batch[0]['input'].shape == (batchsize, 10)
        print(batch)
    
    
