Summary: A utility to collect various linux performance data
Name: collectl
Version: 2.2
Release: 8
License: Artistic, GPL
Group: Application/Performance
Source: %{name}-%{version}.%{release}-src.tar.gz
Url: http://collectl.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-root

%description
A utility to collect linux performance data

%prep
%setup -n %{name}-%{version}.%{release}

%build
mv collectl.pl collectl

%clean
rm -Rf $RPM_BUILD_ROOT

%install
cd $RPM_BUILD_DIR/%{name}-%{version}.%{release}
/bin/rm -rf %{buildroot}

# create required directories
mkdir -p        $RPM_BUILD_ROOT/etc/init.d \
	        $RPM_BUILD_ROOT/opt/hp/collectl \
                $RPM_BUILD_ROOT/opt/hp/collectl/docs \
                $RPM_BUILD_ROOT/opt/hp/collectl/etc \
                $RPM_BUILD_ROOT/opt/hp/collectl/etc/init.d \
                $RPM_BUILD_ROOT/opt/hp/collectl/man1 \
                $RPM_BUILD_ROOT/opt/hp/collectl/sbin \
                $RPM_BUILD_ROOT/usr/bin \
                $RPM_BUILD_ROOT/usr/sbin \
		$RPM_BUILD_ROOT/usr/share/man/man1/ \
                $RPM_BUILD_ROOT/var/log/collectl

# install the files, setting the mode

install -m 755  collectl \
                $RPM_BUILD_ROOT/opt/hp/collectl/sbin
install -m 444  formatit.ph \
                $RPM_BUILD_ROOT/opt/hp/collectl/sbin
install -m 444  FAQ-collectl.html \
                $RPM_BUILD_ROOT/opt/hp/collectl/docs
install -m 444  RELEASE-collectl \
                $RPM_BUILD_ROOT/opt/hp/collectl/docs
install -m 644  man1/collectl*.1 \
                $RPM_BUILD_ROOT/opt/hp/collectl/man1/
install -m 644  collectl.conf \
                $RPM_BUILD_ROOT/opt/hp/collectl/etc
install -m 755  initd/collectl* \
                $RPM_BUILD_ROOT/opt/hp/collectl/etc/init.d

# compress man pages
gzip $RPM_BUILD_ROOT/opt/hp/collectl/man1/*

# create symlinks
cd $RPM_BUILD_ROOT/usr/share/man/man1/
ln -sf /opt/hp/collectl/man1/collectl.1.gz
ln -sf /opt/hp/collectl/man1/collectl-data.1.gz
ln -sf /opt/hp/collectl/man1/collectl-files.1.gz
ln -sf /opt/hp/collectl/man1/collectl-logging.1.gz
ln -sf /opt/hp/collectl/man1/collectl-lustre.1.gz
ln -sf /opt/hp/collectl/man1/collectl-process.1.gz
ln -sf /opt/hp/collectl/man1/collectl-themath.1.gz
cd $RPM_BUILD_ROOT/usr/bin
ln -sf /opt/hp/collectl/sbin/collectl
cd $RPM_BUILD_ROOT/usr/sbin
ln -sf /opt/hp/collectl/sbin/collectl
cd $RPM_BUILD_ROOT/etc
ln -sf /opt/hp/collectl/etc/collectl.conf
cd $RPM_BUILD_ROOT/etc/init.d
ln -sf /opt/hp/collectl/etc/init.d/collectl

%files
%defattr(-,root,root)
%doc /opt/hp/collectl/docs/RELEASE-collectl
%config /etc/collectl.conf
%dir /var/log/collectl
%dir /opt/hp
%dir /opt/hp/collectl
%dir /opt/hp/collectl/docs
%dir /opt/hp/collectl/etc/init.d
%dir /opt/hp/collectl/man1
%dir /opt/hp/collectl/sbin
/opt/hp/collectl/sbin/collectl
/opt/hp/collectl/sbin/formatit.ph
/opt/hp/collectl/docs/FAQ-collectl.html
/opt/hp/collectl/etc/collectl.conf
/opt/hp/collectl/etc/init.d/collectl*
/opt/hp/collectl/man1/collectl.1.gz
/opt/hp/collectl/man1/collectl-data.1.gz
/opt/hp/collectl/man1/collectl-files.1.gz
/opt/hp/collectl/man1/collectl-logging.1.gz
/opt/hp/collectl/man1/collectl-lustre.1.gz
/opt/hp/collectl/man1/collectl-process.1.gz
/opt/hp/collectl/man1/collectl-themath.1.gz
/etc/init.d/collectl
/usr/bin/collectl
/usr/sbin/collectl
/usr/share/man/man1/collectl.1.gz
/usr/share/man/man1/collectl-data.1.gz
/usr/share/man/man1/collectl-files.1.gz
/usr/share/man/man1/collectl-logging.1.gz
/usr/share/man/man1/collectl-lustre.1.gz
/usr/share/man/man1/collectl-process.1.gz
/usr/share/man/man1/collectl-themath.1.gz

%pre
# remove any stale versions in case the names numbers used have changed.
rm -f /etc/init.d/rc*.d/*collectl
rm -f /etc/rc.d/rc*.d/*collectl

%post
# Try and decide which distro this is based on distro specific files.
distro=1
if [[ -f /sbin/yast ]]; then
    distro=2
    ln -sf /opt/hp/collectl/etc/init.d/collectl-suse /etc/init.d/collectl
fi

# debian
if [[ -f /usr/sbin/update-rc.d ]]; then
    distro=3
    ln -sf /opt/hp/collectl/init.d/collectl-debian /etc/init.d/collectl
    update-rc.d collectl defaults
fi

# redhat
if [[ -f /etc/redhat-release ]]; then
    distro=4
    chkconfig --add collectl
fi

if [[ ${distro} = 1 ]]; then
    ln -sf /etc/rc.d/init.d/collectl /etc/rc.d/rc5.d/K99collectl
fi

%preun
# If collectl is running, stop it before removing.
/etc/init.d/collectl stop > /dev/null

%postun
# perform the test to make sure that we are removing and not upgrading.
if [ $1 = 0 ]; then
# remove links - some distros store them in /etc/init.d/rc*d while
# others put them in /etc/rc.d/rc* so remove them all!
    rm -f /usr/bin/collectl
    rm -f /usr/sbin/collectl
    rm -f /etc/init.d/rc*.d/*collectl
    rm -f /etc/rc.d/rc*.d/*collectl
    rm -f /usr/share/man/man1/collectl*.1.gz
fi
