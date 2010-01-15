Summary: A utility to collect various linux performance data
Name: collectl
Version: 3.4.0
Release: %mkrel 1
License: GPL+ or Artistic
Group: Monitoring
Source0: http://prdownloads.sourceforge.net/%name/%{name}-%{version}.src.tar.gz
Source1:collectl-mdv
patch0: collectl-3.4.0-install.patch
Url: http://collectl.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildArch: noarch

%description
A utility to collect linux performance data

%prep
%setup -q
%patch0

%build

%clean
%{__rm} -Rf $RPM_BUILD_ROOT

%install
%{__rm}  -rf $RPM_BUILD_ROOT
export PREFIX=$RPM_BUILD_ROOT
./INSTALL

# lspci is under /usr/bin
echo "Lspci = /usr/bin/lspci" >> ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}.conf

%files
%defattr(-,root,root)
%doc RELEASE-%{name} docs/*.html README GPL ARTISTIC COPYING
%config(noreplace) %{_sysconfdir}/%{name}.conf
#gw AFAIK logrotate is not needed as collectl does that itself
%dir /var/log/%{name}
%{_sbindir}/*
%{_mandir}/man1/*
%{_sysconfdir}/init.d/%{name}
%{_datadir}/%{name}

%preun
# If collectl is running, stop it before removing.
/etc/init.d/%{name} stop
chkconfig --del %{name} 2>&1 > /dev/null

%post
chkconfig --add %{name} 2>&1 > /dev/null
/etc/init.d/%{name} start

%changelog
