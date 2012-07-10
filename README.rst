EXEMPLE BUILD.SH FILE
====================
Intro
-----
This repo is used to create rpms for Plone site. RPMs are created with a buildout. 

Step
----
* Create a rpm.cfg buildout which used to create rpms.
* Create folder rpm into your buildout repo.
* Create a build.sh file into rpm folder.

File
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
    rpmbuild --define "portal $JOB_NAME" \
             --define "home $HOME" \
             --define "user $USER" \
             --define "version ${RPM_VERSION}" \
             --define="_topdir $PWD" \
             --define="_tmppath $PWD/tmp" \
             -bb https://raw.github.com/bsuttor/Rpmizer/master/template.spec

* rpm.cfg ::

    [buildout]
    extends = ...
