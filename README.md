Decorrelated Tagging Functions
==============================

You can get this code by running

```bash
git clone --recursive git@github.com:dguest/dtf-example.git
```

Quickstart
----------

Make sure you have boost `property_tree` (the JSON parser) and
`eigen3`. If you don't, and you're working on lxplus, see below. Then
type

```bash
make
```

and then

```bash
./bin/dtf-main
```

This should produce the same output as the Keras test script
`./test-pattern.sh`

Look in `src/dtf-main.cxx` for an example of the C++ interface in use.

Setup on systems with CVMFS
---------------------------

Most hep clusters have old versions of boost or eigen, which means
this code won't build out of the box on e.g. lxplus. There's an
attached script to fix this on any machine with cvmfs. Just run

```bash
. setup-on-cvmfs-systems.sh
```

Regenerating the NN configuration
---------------------------------

The NN configuration files are in `data/`.

The `arch.json` and `weights.h5` files were generated from Keras (by
reading in the `classifier.h5` file Peter provided and saving it out
as weights and architecture separately). The `inputs.json` file is
from `make-input-variables-file.py` in this repository.

These files are combined into the json file which the C++ code reads
using a "converter" in lwtnn, specifically by calling

```bash
kerasfunc2json.py arch.json weights.h5 inputs.json > lwtnn-dtf-config.json
```
