#!/bin/bash
set -e

if [ $# -lt 6 ]; then
    echo "Run buildout awaits path_to_python, rpm_build_directory, install_dir, buildout root, buildout version and setuptools version passed as arguments"
fi

PATH_TO_PYTHON=$1
RPM_BUILD_DIR=$2
INSTALL_DIR=$3
BUILDOUT_CFG=$4
BUILDOUT_VERSION=$5
SETUPTOOLS_VERSION=$6

"$PATH_TO_PYTHON" bootstrap.py -c "$BUILDOUT_CFG" --version="$BUILDOUT_VERSION" --setuptools-version="$SETUPTOOLS_VERSION"
bin/buildout -N -c "$BUILDOUT_CFG" install download
bin/buildout -N -c "$BUILDOUT_CFG" install install
mkdir -p "$INSTALL_DIR"
mv "$RPM_BUILD_DIR/buildout-cache/downloads" "$INSTALL_DIR"
mv "$RPM_BUILD_DIR/buildout-cache/eggs" "$INSTALL_DIR"
# workaround buildout 2.2 bug where buildout does not install its own egg
# in buildout:directory/eggs
cp -r eggs/zc.buildout* "$INSTALL_DIR/eggs"
bin/buildout -N -c "$BUILDOUT_CFG" buildout:directory="$INSTALL_DIR"
