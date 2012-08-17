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
* Create a job into jenkins

Files
-----
* build.sh (replace JOB_NAME, HOME and USER) ::

    #!/bin/sh
    export QA_RPATHS=$[ 0x0001|0x0002 ]
    RPM_VERSION="1.0.${BUILD_NUMBER}"
    JOB_NAME=project-website
    HOME=/data
    USER=projectuser
    TMP_DIR=$(mktemp -d $PWD/jenkins.
    mkdir $TMP_DIR/$JOB_NAME-$RPM_VERSION
    rm -fr ../eggs
    rm -rf BUILD BUILDROOT SOURCES SPECS SRPMS tmp RPMS
    mkdir -p BUILD RPMS SRPMS SOURCES tmp
    cp -r ../* $TMP_DIR/$JOB_NAME-$RPM_VERSION
    tar czvf SOURCES/$JOB_NAME-$RPM_VERSION.tar.gz --exclude=*.spec -C $TMP_DIR \
             $JOB_NAME-$RPM_VERSION
    rm simple.spec*
    wget https://raw.github.com/CIRB/Rpmizer/master/simple.spec
    rpmbuild --define "portal $JOB_NAME" \
             --define "home $HOME" \
             --define "user $USER" \
             --define "version ${RPM_VERSION}" \
             --define="_topdir $PWD" \
             --define="_tmppath $PWD/tmp" \
             -bb simple.spec
    rm -fr $TMP_DIR

* rpm.cfg (in extends, replace master by the last tag of plone-buildout)::

    [buildout]
    extends = 
        project.cfg
        https://raw.github.com/CIRB/plone-buildout/master/both.cfg?login=jenkins-cirb&token=4d0a9ab50e431868b36636193ae08c69

    [hosts]
    client1 = 127.0.0.1
    client2 = 127.0.0.1
    zeo = 127.0.0.1

    [ports]
    instance = 8080
    client1 = 8080
    client2 = 8081
    zeo = 8100

    [versions]
    zc.buildout = 1.4.4

Jobs
----
You have to construct rpms with a Jenkins job. For creating a jenkins job, 

* Go to http://jenkins.cirb.lan.
* Click on *Nouveau Job*.
* Choose a name a put it into *Nom du Job* input.
* Use the option *Copier un Job existant*. In the input *Copier à partir de*, put *Build-rpm-research*
* Change the github link, put the github link to the buildout project (with https and not ssh).

