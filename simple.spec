%define __prelink_undo_cmd %{nil}
%define installdir %{home}/%{user}/%{name}
%define python /usr/bin/python2.6
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
BuildRequires:  subversion, git, zlib-devel, freetype-devel, libjpeg-devel, gcc
BuildRequires:  python >= 2.6.6, libxslt-devel
AutoReqProv: no

%description
%{summary}

%package    core
Summary:    %{summary} - core without any clients
Group: Applications/Database
Requires:   python >= 2.6.6
Requires:   openssl-devel
Requires:   python-devel
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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdir}
mkdir -p $RPM_BUILD_ROOT%{installdir}/downloads
mkdir -p $RPM_BUILD_ROOT%{installdir}/buildout-cache/downloads
mkdir -p buildout-cache/downloads
%{python} bootstrap.py -c rpm.cfg
bin/buildout -N -c rpm.cfg install download buildout:directory=$RPM_BUILD_ROOT%{installdir} buildout:rpm-directory=%{installdir}
bin/buildout -N -c rpm.cfg install install buildout:directory=$RPM_BUILD_ROOT%{installdir} buildout:rpm-directory=%{installdir}
bin/buildout -N -c rpm.cfg buildout:directory=$RPM_BUILD_ROOT%{installdir} buildout:rpm-directory=%{installdir}

%install
mkdir -p $RPM_BUILD_ROOT%{installdir}/etc
for file in `ls $RPM_BUILD_ROOT%{installdir}/bin/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/bin/$file
    sed -i s/${RPM_BUILD_DIR//\//\\/}\\/%{name}-%{version}\\/eggs/\\%{home}\\/%{user}\\/%{name}\\/eggs/g $RPM_BUILD_ROOT%{installdir}/bin/$file
done
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/zc.buildout* $RPM_BUILD_ROOT%{installdir}/eggs
#cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/setuptools* $RPM_BUILD_ROOT%{installdir}/eggs
cd $RPM_BUILD_ROOT%{installdir}/
rm  $RPM_BUILD_ROOT%{installdir}/.installed.cfg
rm -fr $RPM_BUILD_ROOT%{installdir}/downloads
rm -fr $RPM_BUILD_ROOT%{installdir}/parts/docs
rm -fr $RPM_BUILD_ROOT%{installdir}/.git
rm $RPM_BUILD_ROOT%{installdir}/bin/instance
rm $RPM_BUILD_ROOT%{installdir}/bin/pil*.py
rm $RPM_BUILD_ROOT%{installdir}/bin/copy_ckeditor_code
rm -rf $RPM_BUILD_ROOT%{installdir}/parts/instance
rm -rf $RPM_BUILD_ROOT%{installdir}/parts/lxml
find $RPM_BUILD_ROOT%{installdir} -name "*.pyc" -delete;
find $RPM_BUILD_ROOT%{installdir} -name "*.pyo" -delete;
for file in `ls $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/bin/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/bin/$file
done
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/etc/zeo.conf
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client1/etc/zope.conf
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client2/etc/zope.conf
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client3/etc/zope.conf
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client4/etc/zope.conf

sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client1/bin/interpreter
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client2/bin/interpreter
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client3/bin/interpreter
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client4/bin/interpreter

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
rm -rf $RPM_BUILD_ROOT%{installdir} $RPM_BUILD_ROOT/etc

%changelog
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
