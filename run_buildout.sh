#!/bin/bash
set -ex

if [ $# -lt 4 ]; then
    echo "Run buildout awaits path_to_python, rpm_build_directory, install_dir, and buildut root passed as arguments"
fi

PATH_TO_PYTHON=$1
RPM_BUILD_DIR=$2
INSTALL_DIR=$3
BUILDOUT_CFG=$4

"$PATH_TO_PYTHON" bootstrap.py -c "$BUILDOUT_CFG"
bin/buildout -N -c "$BUILDOUT_CFG" install download
bin/buildout -N -c "$BUILDOUT_CFG" install install
mkdir -p "$INSTALL_DIR/downloads" "$INSTALL_DIR/eggs"
mv "$RPM_BUILD_DIR/buildout-cache/downloads/"* "$INSTALL_DIR/downloads/"
mv "$RPM_BUILD_DIR/buildout-cache/eggs/"* "$INSTALL_DIR/eggs/"
bin/buildout -N -c "$BUILDOUT_CFG" buildout:directory="$INSTALL_DIR"
