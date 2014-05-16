#!/bin/bash
set -e

if [ $# -lt 3 ]; then
    echo "Run buildout awaits path_to_python, install_dir and rpm_build_directory passed as arguments"
fi

PATH_TO_PYTHON=$1
RPM_BUILD_DIR=$2
INSTALL_DIR=$3

mkdir -p $INSTALL_DIR/downloads $INSTALL_DIR/eggs
$PATH_TO_PYTHON bootstrap.py -c rpm.cfg
bin/buildout -N -c rpm.cfg install download
bin/buildout -N -c rpm.cfg install install
cp -r $RPM_BUILD_DIR/buildout-cache/downloads/* $INSTALL_DIR/downloads/
cp -r $RPM_BUILD_DIR/buildout-cache/eggs/* $INSTALL_DIR/eggs/
bin/buildout -N -c rpm.cfg buildout:directory=$INSTALL_DIR
