#!/bin/bash
set -e

if [ $# -lt 4 ]; then
    echo "Run buildout awaits path_to_python, install_dir, rpm_build_directory and buildout config passed as arguments"
fi

PATH_TO_PYTHON=$1
RPM_BUILD_DIR=$2
INSTALL_DIR=$3
BUILDOUT_CFG=$4

$PATH_TO_PYTHON bootstrap.py -c $BUILDOUT_CFG
bin/buildout -N -c $BUILDOUT_CFG install download
bin/buildout -N -c $BUILDOUT_CFG install install
mkdir -p $INSTALL_DIR/downloads $INSTALL_DIR/eggs
cp -r $RPM_BUILD_DIR/buildout-cache/downloads/* $INSTALL_DIR/downloads/
cp -r $RPM_BUILD_DIR/buildout-cache/eggs/* $INSTALL_DIR/eggs/
bin/buildout -N -c $BUILDOUT_CFG buildout:directory=$INSTALL_DIR