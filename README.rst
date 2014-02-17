.. contents::
====================
Build RPMs for Plone
====================
Intro
-----
This repo is used to create rpms for Plone site. RPMs are created with a buildout. 

Steps
-----
* Create a rpm.cfg buildout which used to create rpms.
* Create folder named `rpm` into your buildout repo.
* Create a build.sh file into rpm folder.
* Create a job into jenkins.

Files
-----
* build.sh (replace JOB_NAME, HOME and USER) ::

    #!/bin/bash
    set -e
    export QA_RPATHS=$[ 0x0001|0x0002 ]

    RPM_VERSION="1.0.${BUILD_NUMBER}"
    RPM_NAME=project-website
    HOME=/data
    USER=userproject

    SRC_DIR=$WORKSPACE/src
    
    BUILD_DIR=$WORKSPACE/build
    rm -rf $BUILD_DIR
    mkdir $BUILD_DIR

    # directory structure needed for rpmbuild
    RPM_ROOT_DIR=$BUILD_DIR/rpm_root
    mkdir $RPM_ROOT_DIR
    cd $RPM_ROOT_DIR
    mkdir -p BUILD RPMS SRPMS SOURCES tmp

    # prepare source before archive
    ARCHIVE_DIR=$BUILD_DIR/$RPM_NAME-$RPM_VERSION
    mkdir $ARCHIVE_DIR
    cp -r $SRC_DIR/* $ARCHIVE_DIR

    # make source archive
    tar czvf $RPM_ROOT_DIR/SOURCES/$RPM_NAME-$RPM_VERSION.tar.gz --exclude=*.spec -C $BUILD_DIR \
        $RPM_NAME-$RPM_VERSION

    rpmbuild --define "name $RPM_NAME" \
        --define "home $HOME" \
        --define "user $USER" \
        --define "version $RPM_VERSION" \
        --define="_topdir $RPM_ROOT_DIR" \
        --define="_tmppath $RPM_ROOT_DIR/tmp" \
        -bb $SRC_DIR/rpm/simple.spec

    #rm -fr $BUILD_DIR


Don't forget to add execution right ::
    
    $ chmod +x build.sh

* rpm.cfg : This file is used to construct rpm.


Jobs
----
You have to construct rpms with a Jenkins job. For creating a jenkins job, 

* Go to jenkins.
* Click on *Nouveau Job*.
* Choose a name a put it into *Nom du Job* input.
* Use the option *Copier un Job existant*. In the input *Copier à partir de*, put *Build-rpm-research*
* Change the github link, put the github link to the buildout project (with ssh and not http).

