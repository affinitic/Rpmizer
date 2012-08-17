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

* rpm.cfg (This is just a example)::

    [buildout]
    parts = instance
    extends = http://dist.plone.org/release/4.2-latest/versions.cfg
    find-links = http://dist.repoze.org/

    [instance]
    recipe = plone.recipe.zope2instance
    eggs = 
        Pillow

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

