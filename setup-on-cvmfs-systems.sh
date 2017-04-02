# script to set up environment to compile lwtnn

# these may be done by default for ATLAS people
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'

echo -n "setting up eigen and boost..."
setupATLAS -q
localSetupROOT -q
localSetupSFT -q releases/LCG_84/eigen/3.2.7
localSetupBoost -q boost-1.60.0-python2.7-x86_64-slc6-gcc49
EIGEN_INC=$SFT_HOME_eigen/include/eigen3
BOOST_INC=$ALRB_BOOST_ROOT/include
export LWTNN_CXX_FLAGS="-I${EIGEN_INC} -I${BOOST_INC}"
echo -e "done\n"

if ! type git-lfs &> /dev/null ; then
    echo "run get-git-lfs.sh to get input data"
fi
