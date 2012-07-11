====================
Build RPMs for Plone
====================
Intro
-----
This repo is used to create rpms for Plone site. RPMs are created with a buildout. 

Steps
----
* Create a rpm.cfg buildout which used to create rpms.
* Create folder rpm into your buildout repo.
* Create a build.sh file into rpm folder.

Files
----
- build.sh ::

    #!/bin/sh
    export QA_RPATHS=$[ 0x0001|0x0002]
    RPM_VERSION="0.2.${BUILD_NUMBER}"
    JOB_NAME=prb-website
    HOME=/data
    USER=prb
    TMP_DIR=$(mktemp -d $PWD/jenkins.

    mkdir $TMP_DIR/$JOB_NAME-$RPM_VERSION
    rm -fr ../eggs
    mkdir -p BUILD RPMS SRPMS SOURCES tmp
    cp -r ../* $TMP_DIR/$JOB_NAME-$RPM_VERSION
    tar czvf SOURCES/$JOB_NAME-$RPM_VERSION.tar.gz --exclude=*.spec -C $TMP_DIR \
             $JOB_NAME-$RPM_VERSION
    rm template.spec*
    wget https://raw.github.com/bsuttor/Rpmizer/master/template.spec
    rpmbuild --define "portal $JOB_NAME" \
             --define "home $HOME" \
             --define "user $USER" \
             --define "version ${RPM_VERSION}" \
             --define="_topdir $PWD" \
             --define="_tmppath $PWD/tmp" \
             -bb template.spec
    rm -fr $TMP_DIR

* rpm.cfg ::

    [buildout]
    extends = ...
