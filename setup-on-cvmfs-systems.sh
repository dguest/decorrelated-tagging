# script to set up environment to compile lwtnn

# these may be done by default for ATLAS people
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'

echo -n "setting up eigen and boost..."
setupATLAS -q
localSetupSFT -q releases/LCG_84/eigen/3.2.7
localSetupBoost -q boost-1.60.0-python2.7-x86_64-slc6-gcc49
EIGEN_INC=$SFT_HOME_eigen/include/eigen3
BOOST_INC=$ALRB_BOOST_ROOT/include
export LWTNN_CXX_FLAGS="-I$(EIGEN_INC) -I$(BOOST_INC)"
echo "done"

if [[ ! type git-lfs ]] ; then
    echo "getting git lfs"
    wget https://github.com/git-lfs/git-lfs/releases/download/v2.0.2/git-lfs-linux-amd64-2.0.2.tar.gz
    cat <<EOF
put git-lfs somewhere in your PATH, and run

```
./git-lfs install
```

then run `git lfs pull` from this directory

EOF
fi
