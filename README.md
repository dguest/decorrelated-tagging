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

Look in `src/dtf-main.cxx` for more info.

Setup on systems with CVMFS
---------------------------

Most hep clusters have old versions of boost or eigen, which means
this code won't build out of the box on e.g. lxplus. There's an
attached script to fix this on any machine with cvmfs. Just run

```bash
. setup-on-cvmfs-systems.sh
```
