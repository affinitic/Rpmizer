%define __prelink_undo_cmd %{nil}
%define installdir %{home}/%{user}/%{name}
%define python /usr/bin/python2.7
%define portbase 13080

Name: %{name}
Version: %{version}
Release: 1
Summary: %{name} website
URL: http://cirb.irisnet.be
License: GPL
Vendor: CIRB-CIBG
Packager: bsuttor <bsuttor@cirb.irisnet.be>
Group: Applications/Database
Buildroot: %{_tmppath}/%{name}-buildroot
Source: %{name}-%{version}.tar.gz
BuildRequires:  git, zlib-devel, freetype-devel, libjpeg-devel, gcc
BuildRequires:  libxslt-devel
AutoReqProv: no

%description
%{summary}

%package    core
Summary:    %{summary} - core without any clients
Group: Applications/Database
Requires:   openssl-devel
Requires:   python27-devel
Requires:   zlib freetype
AutoReqProv: no
%description core
%{summary}

%package    zeoserver
Summary:    %{summary} - core
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description zeoserver
%{summary}

%package    client1
Summary:    %{summary} - client1
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client1
%{summary}

%package    client2
Summary:    %{summary} - client2
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client2
%{summary}

%package    client3
Summary:    %{summary} - client3
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client3
%{summary}

%package    client4
Summary:    %{summary} - client4
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description client4
%{summary}

%prep
%setup

%build
# BUILD
%{run_buildout} %{python} $RPM_BUILD_DIR/%{name}-%{version} $RPM_BUILD_DIR%{installdir} rpm.cfg

%install
# BUILDROOT
mkdir -p $RPM_BUILD_ROOT
cp -r $RPM_BUILD_DIR%{home} $RPM_BUILD_ROOT
INSTALL_DIR=$RPM_BUILD_ROOT%{installdir}
mkdir -p $INSTALL_DIR/etc
for file in `ls $INSTALL_DIR/bin/`
do
    sed -i s:${RPM_BUILD_DIR/:/\\:}::g $INSTALL_DIR/bin/$file
    sed -i s:${RPM_BUILD_DIR/:/\\:}/%{name}-%{version}/eggs:%{installdir}/eggs:g $INSTALL_DIR/bin/$file
done
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/zc.buildout* $INSTALL_DIR/eggs
#cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/setuptools* $INSTALL_DIR/eggs
cd $INSTALL_DIR/
rm  $INSTALL_DIR/.installed.cfg
rm -fr $INSTALL_DIR/downloads
rm -fr $INSTALL_DIR/parts/docs
rm -fr $INSTALL_DIR/.git
rm $INSTALL_DIR/bin/instance
rm $INSTALL_DIR/bin/pil*.py
rm $INSTALL_DIR/bin/copy_ckeditor_code
rm -rf $INSTALL_DIR/parts/instance
rm -rf $INSTALL_DIR/parts/lxml
find $INSTALL_DIR -name "*.pyc" -delete;
find $INSTALL_DIR -name "*.pyo" -delete;
for file in `ls $INSTALL_DIR/parts/zeoserver/bin/`
do
    sed -i s:${RPM_BUILD_DIR/:/\\:}::g $INSTALL_DIR/parts/zeoserver/bin/$file
done
TO_CLEAN_UP=( \
    zeoserver/etc/zeo.conf \
    client1/etc/zope.conf \
    client2/etc/zope.conf \
    client3/etc/zope.conf \
    client4/etc/zope.conf \
    client1/bin/interpreter \
    client2/bin/interpreter \
    client3/bin/interpreter \
    client4/bin/interpreter \
)
for file in "${TO_CLEAN_UP[@]}"
do
    sed -i s:${RPM_BUILD_DIR/:/\\:}::g $INSTALL_DIR/parts/zeoserver/bin/$file
done

%files core
%defattr(-, %{user}, %{user}, 0755)
%{installdir}/eggs
%{installdir}/var/log
%dir %{installdir}/bin
%dir %{installdir}/parts
%dir %{installdir}/var
%dir %{installdir}/etc

%pre core
exit 0


%post core
/sbin/ldconfig

%preun core
find %{installdir} -name "*.pyc" -delete;
find %{installdir} -name "*.pyo" -delete;
find %{installdir} -name "*.mo" -delete;

%postun core
/sbin/ldconfig

%files zeoserver
%defattr(-, %{user}, %{user} , 0755)
%config(noreplace) %{installdir}/parts/zeoserver/etc/zeo.conf
#%{installdir}/bin/zodbpack
%{installdir}/bin/backup
%{installdir}/bin/restore
%{installdir}/bin/snapshotbackup
%{installdir}/bin/snapshotrestore
%{installdir}/bin/fullbackup
%{installdir}/bin/repozo
%{installdir}/bin/zeopack
%{installdir}/bin/zeoserver
%{installdir}/parts/zeoserver
%{installdir}/var/zeoserver
%{installdir}/var/filestorage
%{installdir}/var/blobstorage

%files client1
%defattr(-, %{user}, %{user}, 0755)
%config(noreplace) %{installdir}/parts/client1/etc/zope.conf
%{installdir}/bin/client1
%{installdir}/parts/client1
%{installdir}/var/client1

%files client2
%defattr(-, %{user}, %{user}, 0755)
%config(noreplace) %{installdir}/parts/client2/etc/zope.conf
%{installdir}/bin/client2
%{installdir}/parts/client2
%{installdir}/var/client2

%files client3
%defattr(-, %{user}, %{user}, 0755)
%config(noreplace) %{installdir}/parts/client3/etc/zope.conf
%{installdir}/bin/client3
%{installdir}/parts/client3
%{installdir}/var/client3

%files client4
%defattr(-, %{user}, %{user}, 0755)
%config(noreplace) %{installdir}/parts/client4/etc/zope.conf
%{installdir}/bin/client4
%{installdir}/parts/client4
%{installdir}/var/client4


%clean
rm -rf $INSTALL_DIR $RPM_BUILD_ROOT/etc $RPM_BUILD_DIR%{installdir}
#echo NOOP

%changelog
* Thu Jun 07 2013 - Benoît Suttor <bsuttor@cirb.irisnet.be>
- Use python2.7
- Use, like tracis-ci, unified installer for downloading eggs.
* Thu May 14 2013 - Benoît Suttor <bsuttor@cirb.irisnet.be>
- Replace backup files (from recipe)
- Add fullbackup script
* Thu Dec 20 2012 - Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1.3
- Add client3 and client4, and no replace backup files
* Tue Oct 2 2012 -  Godefroid Chapelle <gotcha@bubblenet.be> 0.1.2
- Use 'name' instead of 'portal' as input parameter
- Add etc/ in install_dir
- Do not distribute develop-eggs
* Wed Jul 25 2012 -  Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1.1
- Add client2 construction
- Clean path into zope.conf file and zeo.conf file
* Tue Jul 10 2012 - Benoît Suttor <bsuttor@cirb.irisnet.be> 0.1
- initial build
