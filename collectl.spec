Summary: A utility to collect various linux performance data
Name: collectl
Version: 3.4.0
Release: 3
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
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 3.4.0-2mdv2011.0
+ Revision: 610151
- rebuild

* Fri Jan 15 2010 Bruno Cornec <bcornec@mandriva.org> 3.4.0-1mdv2010.1
+ Revision: 491850
- Updated to 3.4.0 upstream
  use the new INSTALL script for installation + local patch reported upstream

* Wed Jan 06 2010 Frederik Himpe <fhimpe@mandriva.org> 3.3.6-1mdv2010.1
+ Revision: 486852
- update to new version 3.3.6

* Wed Sep 16 2009 Götz Waschk <waschk@mandriva.org> 3.3.5-1mdv2010.0
+ Revision: 443537
- new version
- update license
- remove packager tag
- fix rpmlint warning by adding default-stop
- spec cleanup

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 3.1.3-2mdv2010.0
+ Revision: 437096
- rebuild

* Mon Feb 02 2009 Bruno Cornec <bcornec@mandriva.org> 3.1.3-1mdv2009.1
+ Revision: 336485
- Do not install doc files twice and resolve a build issue
- Update to upstream 3.1.3

* Thu Dec 11 2008 Bruno Cornec <bcornec@mandriva.org> 3.1.1-1mdv2009.1
+ Revision: 312628
- Update to 3.1.1

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 2.2.8-3mdv2009.0
+ Revision: 240508
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jul 20 2007 Bruno Cornec <bcornec@mandriva.org> 2.2.8-1mdv2008.0
+ Revision: 53968
- Doc dir is now without version number
- introduction of collectl tool in Mandriva
  Work needs to be done with upstream to make it more conformant (.ph)
- Import collectl



* Fri May 18 2007 Mark Seger
- move to Open Source
* Tue Nov 29 2006 Mark Seger
- change locations for installation and build symlinks to everything
* Tue Apr 27 2006 Mark Seger
- remove relative links to /etc/init.d and put in specific paths to collect-X
  for suse and debian
* Tue Nov 08 2005 Darragh Bailey
- Changed the install section to set the permissions and removed the chmod
  line from the post script section
- Updated the postun scriptlet to support upgrades
- Added specific entry if redhat distro is detected
- Changed to use of double [, since use of single [ in tests which fail
  will result in an exit code of non 0.
- Changed install of init.d scripts so that rpm removes the files it adds
  and postun script will remove the symlinks added by the post script.
* Fri Nov 04 2005 Mark Seger
- use of /opt/hp/collectl directory
* Fri Jan 14 2005 Mark Seger
- changed to support mulitple man pages AND mulitple distros
* Mon Oct 13 2003 Mark Seger
- added collectl.ph support
* Mon Jun 23 2003 Mark Seger
- made starting of collectl optional
- changed location of man1
* Tue Jun 03 2003 Mark Seger <mark.seger@hp.com?
- first attempt to get rpm to do something
