#!/bin/bash
set -e

usage() { echo "Usage: $0 [-d] [-v rpmizer_version] project_id" 1>&2; exit 1; }

#default values
RPMIZER_VERSION="master"
DEBUG="build"

if [ $# -lt 1 ]; then
    usage
fi

while getopts ":v:d" o; do
    case "${o}" in
        v)
            RPMIZER_VERSION=${OPTARG}
            ;;
        d)
            DEBUG="debug"
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

PROJECT_ID=${1}
RPM_NAME=${PROJECT_ID}-website
USER=${PROJECT_ID}

RPM_VERSION="3.1.${BUILD_NUMBER:-undefined}"

HOME=/data


SRC_DIR=${WORKSPACE:=$(pwd)}/src
BUILD_DIR=$WORKSPACE/build

rm -rf "$BUILD_DIR"
mkdir "$BUILD_DIR"

# directory structure needed for rpmbuild
RPM_ROOT_DIR=$BUILD_DIR/rpm_root
mkdir "$RPM_ROOT_DIR"
cd "$RPM_ROOT_DIR"
mkdir -p BUILD RPMS SRPMS SOURCES tmp

# prepare source before archive
if [ "$DEBUG" == "build" ]; then
  # Archive is needed by %setup command in specfile %prep section
  ARCHIVE_DIR=$BUILD_DIR/$RPM_NAME-$RPM_VERSION
  mkdir "$ARCHIVE_DIR"
  cp -r "$SRC_DIR"/* "$ARCHIVE_DIR"

  # make source archive
  tar czvf "$RPM_ROOT_DIR/SOURCES/$RPM_NAME-$RPM_VERSION.tar.gz" --exclude=*.spec -C "$BUILD_DIR" "$RPM_NAME-$RPM_VERSION"
fi

# get simple.spec from Rpmizer repository
SIMPLE_SPEC=$BUILD_DIR/simple.spec
if [ "$DEBUG" == "build" ]; then
  wget --no-cache -O "$SIMPLE_SPEC" "https://raw.github.com/CIRB/Rpmizer/$RPMIZER_VERSION/simple.spec" --no-check-certificate
else
  cp "$WORKSPACE/simple.spec" "$SIMPLE_SPEC"
fi

RUN_BUILDOUT=$BUILD_DIR/run_buildout.sh
if [ "$DEBUG" == "build" ]; then
  wget --no-cache -O "$RUN_BUILDOUT" "https://raw.github.com/CIRB/Rpmizer/$RPMIZER_VERSION/run_buildout.sh" --no-check-certificate
else
  cp "$WORKSPACE/run_buildout.sh" "$RUN_BUILDOUT"
fi
chmod +x "$RUN_BUILDOUT"

INSTALL_BUILDOUT=$BUILD_DIR/install_buildout.sh
if [ "$DEBUG" == "build" ]; then
  wget --no-cache -O "$INSTALL_BUILDOUT" "https://raw.github.com/CIRB/Rpmizer/$RPMIZER_VERSION/install_buildout.sh" --no-check-certificate
else
  cp "$WORKSPACE/install_buildout.sh" "$INSTALL_BUILDOUT"
fi
chmod +x "$INSTALL_BUILDOUT"

case $DEBUG in
  build )
    export QA_RPATHS=$(( 0x0001|0x0002 ))
    rpmbuild --define "name $RPM_NAME" \
        --define "home $HOME" \
        --define "user $USER" \
        --define "version $RPM_VERSION" \
        --define="_topdir $RPM_ROOT_DIR" \
        --define="_tmppath $RPM_ROOT_DIR/tmp" \
        --define="run_buildout $RUN_BUILDOUT" \
        --define="install_buildout $INSTALL_BUILDOUT" \
        -bb "$SIMPLE_SPEC"
     ;;
  debug )
     BUILDOUT_DIR=$WORKSPACE/buildout
     if [ -d "$BUILDOUT_DIR" ]; then
       rm -rf "$BUILDOUT_DIR"
     fi
     mkdir -p "$BUILDOUT_DIR"
     cd "$SRC_DIR"
     rm -rf "$SRC_DIR/bin" "$SRC_DIR/parts" "$SRC_DIR/.installed.cfg"
     "$RUN_BUILDOUT"  "$(which python2.7)" "$SRC_DIR" "$BUILDOUT_DIR" rpm.cfg
     TARGET_DIR=$HOME/$USER/$RPM_NAME
     RPM_BUILD_ROOT=$WORKSPACE/buildroot
     if [ -d "$RPM_BUILD_ROOT" ]; then
       rm -rf "$RPM_BUILD_ROOT"
     fi
     mkdir -p "$RPM_BUILD_ROOT"
     "$INSTALL_BUILDOUT" "$BUILDOUT_DIR" "$TARGET_DIR" "$RPM_BUILD_ROOT"
     exit 0 ;;
  * )
     echo "invalid value for DEBUG"
     exit 1 ;;
esac
