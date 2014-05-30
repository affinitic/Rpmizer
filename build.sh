#!/bin/bash
set -e

usage() { echo "Usage: $0 [-v rpmizer_version] project_id" 1>&2; exit 1; }

#default value
RPMIZER_VERSION="master"

while getopts ":v:p:" o; do
    case "${o}" in
        v)
            RPMIZER_VERSION=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

export QA_RPATHS=$[ 0x0001|0x0002 ]

PROJECT_ID=${1}
RPM_NAME=${PROJECT_ID}-website
USER=${PROJECT_ID}

RPM_VERSION="3.1.${BUILD_NUMBER:-undefined}"

HOME=/data


SRC_DIR=${WORKSPACE:=`pwd`}/src
BUILD_DIR=$WORKSPACE/build

rm -rf $BUILD_DIR
mkdir $BUILD_DIR

# directory structure needed for rpmbuild
RPM_ROOT_DIR=$BUILD_DIR/rpm_root
mkdir $RPM_ROOT_DIR
cd $RPM_ROOT_DIR
mkdir -p BUILD RPMS SRPMS SOURCES tmp

# prepare source before archive
# Archive is needed by %setup command in specfile %prep section
ARCHIVE_DIR=$BUILD_DIR/$RPM_NAME-$RPM_VERSION
mkdir $ARCHIVE_DIR
cp -r $SRC_DIR/* $ARCHIVE_DIR

# make source archive
tar czvf $RPM_ROOT_DIR/SOURCES/$RPM_NAME-$RPM_VERSION.tar.gz --exclude=*.spec -C $BUILD_DIR $RPM_NAME-$RPM_VERSION

# get simple.spec from Rpmizer repository
SIMPLE_SPEC=$BUILD_DIR/simple.spec
wget --no-cache -O $SIMPLE_SPEC https://raw.github.com/CIRB/Rpmizer/$RPMIZER_VERSION/simple.spec --no-check-certificate

RUN_BUILDOUT=$BUILD_DIR/run_buildout.sh
wget --no-cache -O $RUN_BUILDOUT https://raw.github.com/CIRB/Rpmizer/$RPMIZER_VERSION/run_buildout.sh --no-check-certificate
chmod +x $RUN_BUILDOUT

rpmbuild --define "name $RPM_NAME" \
    --define "home $HOME" \
    --define "user $USER" \
    --define "version $RPM_VERSION" \
    --define="_topdir $RPM_ROOT_DIR" \
    --define="_tmppath $RPM_ROOT_DIR/tmp" \
    --define="run_buildout $RUN_BUILDOUT" \
    -bb $SIMPLE_SPEC
