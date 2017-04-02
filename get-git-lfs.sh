#!/usr/bin/env bash

if [[ $- == *i* ]] ; then
    echo "BAD: Don't source me!" >&2
    exit 1
else
    set -eu
fi

if type git-lfs &> /dev/null ; then
    echo "git lfs already installed"
    exit 0
fi
echo "getting git-lfs"
DIR=git-lfs-download
mkdir -p $DIR
echo "downloading"
wget -q https://github.com/git-lfs/git-lfs/releases/download/v2.0.2/git-lfs-linux-amd64-2.0.2.tar.gz -O $DIR/git-lfs.tgz
(
    cd $DIR
    echo "extracting"
    tar xf git-lfs.tgz
)
mv $(find $DIR -name git-lfs) .
cat <<EOF

put git-lfs somewhere in your PATH, and run

./git-lfs install

then run "git lfs pull" from this directory

EOF
