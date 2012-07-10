%define __prelink_undo_cmd %{nil}
%define name %{portal}
%define installdir /data/prb/%{name}
%define rcscript /etc/init.d/%{name}
%define python /usr/bin/python2.6
%define user prb
%define portbase 13080

Name: %{name}
Version: %{version}
Release: 1
Summary: %{name} portal
URL: http://cirb.irisnet.be
License: GPL
Vendor: CIRB
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
Requires:   zlib freetype
#Requires:   openldap >= 2.4.11
AutoReqProv: no
%description core
%{summary}

%package    zeo
Summary:    %{summary} - core
Group: Applications/Database
Requires:   %{name}-core = %{version}
%description zeo
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

%prep
%setup

%build
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdir}
mkdir -p $RPM_BUILD_ROOT%{installdir}/downloads
cp $RPM_BUILD_DIR/%{name}-%{version}/table-default.diff $RPM_BUILD_ROOT%{installdir}/table-default.diff
%{python} bootstrap.py -c rpm.cfg
bin/buildout -N -c rpm.cfg buildout:directory=$RPM_BUILD_ROOT%{installdir} buildout:rpm-directory=%{installdir}

%install
#echo "effective-user %{user}" >> $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/etc/zeo.conf
#echo "effective-user %{user}" >> $RPM_BUILD_ROOT%{installdir}/parts/client1/etc/zope.conf
#echo "effective-user %{user}" >> $RPM_BUILD_ROOT%{installdir}/parts/client2/etc/zope.conf
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mv $RPM_BUILD_ROOT%{installdir}/%{name}-* $RPM_BUILD_ROOT/etc/init.d/
for file in `ls $RPM_BUILD_ROOT/etc/init.d/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT/etc/init.d/$file
done
#sed -i '/bin\/sh/a \
#' $RPM_BUILD_ROOT/etc/init.d/%{name}-client1
for file in `ls $RPM_BUILD_ROOT%{installdir}/bin/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/bin/$file
    sed -i s/${RPM_BUILD_DIR//\//\\/}\\/%{name}-%{version}\\/eggs/\\/data\\/prb\\/prb-website\\/eggs/g $RPM_BUILD_ROOT%{installdir}/bin/$file
done
#sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/etc/zeo.conf
#sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client1/etc/zope.conf
#sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/client2/etc/zope.conf
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/zc.buildout* $RPM_BUILD_ROOT%{installdir}/eggs
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/setuptools* $RPM_BUILD_ROOT%{installdir}/eggs
cd $RPM_BUILD_ROOT%{installdir}/
#rm  $RPM_BUILD_ROOT%{installdir}/.mr.developer.cfg
rm  $RPM_BUILD_ROOT%{installdir}/.installed.cfg
rm  $RPM_BUILD_ROOT%{installdir}/table-default.diff
rm -fr $RPM_BUILD_ROOT%{installdir}/downloads
rm -fr $RPM_BUILD_ROOT%{installdir}/parts/docs
#rm -fr $RPM_BUILD_ROOT%{installdir}/.svn
rm -fr $RPM_BUILD_ROOT%{installdir}/.git
#rm $RPM_BUILD_ROOT%{installdir}/bin/develop
rm $RPM_BUILD_ROOT%{installdir}/bin/instance
rm -rf $RPM_BUILD_ROOT%{installdir}/parts/instance
rm -rf $RPM_BUILD_ROOT%{installdir}/parts/lxml
#for i in `seq 2 2`
#do 
#    cp -r parts/client1 parts/client$i
#    sed -i s/client1/client$i/g parts/client$i/etc/zope.conf
#    sed -i "s/address 5011/address $((%portbase + 10#$i))/" parts/client$i/etc/zope.conf
#    cp $RPM_BUILD_ROOT/etc/init.d/%{name}-client1 $RPM_BUILD_ROOT/etc/init.d/%{name}-client$i
#    sed -i s/client1/client$i/g $RPM_BUILD_ROOT/etc/init.d/%{name}-client$i
#done
find $RPM_BUILD_ROOT%{installdir} -name "*.pyc" -delete;
find $RPM_BUILD_ROOT%{installdir} -name "*.pyo" -delete;
for file in `ls $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/bin/`
do
    sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/parts/zeoserver/bin/$file
done


%files core
%defattr(-, %{user}, %{user}, 0755)
#%{installdir}/bin/zopepy
#%{installdir}/bin/zodbconvert
#%{installdir}/bin/zodbconvert_to_filestorage.cfg
#%{installdir}/bin/zodbconvert_to_relstorage.cfg
#%{installdir}/bin/zodbpack.cfg
#%{installdir}/src/*
%{installdir}/develop-eggs
#%{installdir}/versions-picked.cfg
%{installdir}/eggs
#%{installdir}/parts/products
%{installdir}/var/log
%dir %{installdir}/bin
%dir %{installdir}/parts
#%dir %{installdir}/src
%dir %{installdir}/var

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

%files zeo
%defattr(-, %{user}, %{user} , 0755)
%{rcscript}-zeo
%config(noreplace) %{installdir}/parts/zeoserver/etc/zeo.conf
#%{installdir}/bin/zodbpack
%{installdir}/bin/backup
%{installdir}/bin/repozo
%{installdir}/bin/restore
%{installdir}/bin/snapshotbackup
%{installdir}/bin/snapshotrestore
%{installdir}/bin/zeopack
%{installdir}/bin/zeoserver
%{installdir}/parts/zeoserver
%{installdir}/var/zeoserver
%{installdir}/var/filestorage
%{installdir}/var/blobstorage

%files client1
%defattr(-, %{user}, %{user}, 0755)
%{rcscript}-client1
%config(noreplace) %{installdir}/parts/client1/etc/zope.conf
%{installdir}/bin/client1
%{installdir}/parts/client1
%{installdir}/var/client1

%files client2
%defattr(-, %{user}, %{user}, 0755)
%{rcscript}-client2
%config(noreplace) %{installdir}/parts/client2/etc/zope.conf
%{installdir}/bin/client2
%{installdir}/parts/client2
%{installdir}/var/client2

%clean
rm -rf $RPM_BUILD_ROOT%{installdir} $RPM_BUILD_ROOT/etc

%changelog
* Tue May 08 2012 - Benoît Suttor <bsuttor@cirb.irisnet.be> 0.2
- Used with puppet for one zeo server and two clients
* Tue Mar 22 2012 - Jean Francois Roche <jfroche@affinitic.be> 0.1
- initial build
