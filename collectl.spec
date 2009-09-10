#
# $Id$
#
Summary: A utility to collect various linux performance data
Name: collectl
Version: 3.1.3
Packager: Bruno Cornec <bcornec@mandriva.org>
Release: %mkrel 2
License: GPL
Group: Monitoring
Source0: %{name}-%{version}.src.tar.gz
Source1: %{name}-mdv
Url: http://collectl.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildArch: noarch

%description
A utility to collect linux performance data

%prep
%setup -n %{name}-%{version}

%build

%clean
%{__rm} -Rf $RPM_BUILD_ROOT

%install
%{__rm}  -rf $RPM_BUILD_ROOT

# create required directories
mkdir -p  ${RPM_BUILD_ROOT}/var/log/%{name} ${RPM_BUILD_ROOT}%{_sbindir} ${RPM_BUILD_ROOT}%{_docdir}/%{name} ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/ ${RPM_BUILD_ROOT}%{_mandir}/man1/

# install the files, setting the mode
install -m 755  %{name}.pl ${RPM_BUILD_ROOT}%{_sbindir}/%{name}

# Should be put elsewhere normaly
install -m 755  formatit.ph lexpr.ph sexpr.ph vmstat.ph ${RPM_BUILD_ROOT}/%{_sbindir}
install -m 755  %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/%{name}
install -m 644  %{name}.conf ${RPM_BUILD_ROOT}%{_sysconfdir}
install -m 644  man1/%{name}*.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/

# lspci is under /usr/bin
echo "Lspci = /usr/bin/lspci" >> ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}.conf

%files
%defattr(-,root,root)
%doc RELEASE-%{name} docs/*.html README GPL ARTISTIC COPYING
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir /var/log/%{name}
%{_sbindir}/*
%{_mandir}/man1/*
%{_sysconfdir}/init.d/%{name}

%preun
# If collectl is running, stop it before removing.
/etc/init.d/%{name} stop
chkconfig --del %{name} 2>&1 > /dev/null

%post
chkconfig --add %{name} 2>&1 > /dev/null
/etc/init.d/%{name} start

%changelog
