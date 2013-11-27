Name:		isoqlog
Summary:	Isoqlog is an MTA log analysis program written in C.
Version:	2.2.1
Release:	0%{?dist}
License:	BSD
Group:		Monitoring
URL:		http://www.enderunix.org/isoqlog/
Source0:	http://www.enderunix.org/isoqlog/isoqlog-%{version}.tar.gz
Source1:	http://mirrors.qmailtoaster.com/active/isoqlog-toaster-templates.tar.gz
Requires:	control-panel-toaster
Obsoletes:	isoqlog-toaster
Obsoletes:	isoqlog-toaster-doc
BuildRoot:      %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define apacheuser    apache
%define apachegroup   apache
%define crontab       /etc/crontab
%define debug_package %{nil}
%define basedir       %{_datadir}/toaster
%define isoqdir       %{basedir}/isoqlog

#----------------------------------------------------------------------------
%description
#----------------------------------------------------------------------------
Isoqlog is an MTA log analysis program written in C. It is
designed to scan qmail, postfix, sendmail logfiles and
produce usage statistics in HTML format. for viewing through a
browser. It produces Top domains output according to Incoming,
Outgoing, total  mails and  bytes, it keeps your main domain
mail statistics with Days Top Domain, Top Users values for per
day, per month, and years.

#----------------------------------------------------------------------------
%prep
#----------------------------------------------------------------------------

%setup -q

# CVS cleanup
#----------------------------------------------------------------------------
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

#----------------------------------------------------------------------------
%build
#----------------------------------------------------------------------------

./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}									
make

#----------------------------------------------------------------------------
%install
#----------------------------------------------------------------------------
rm -rf %{buildroot}
make DESTDIR="%{buildroot}" install

# Write the module into the control panel
install isoqlog.module $RPM_BUILD_DIR/%{name}-%{version}/isoqlog.module

install -d                   %{buildroot}%{_docdir}/%{name}
install -d                   %{buildroot}%{basedir}/include
install -m644 isoqlog.module %{buildroot}%{basedir}/include

install -D isoqlog.conf      %{buildroot}%{_sysconfdir}/%{name}/isoqlog.conf
install -D isoqlog.cron.sh   %{buildroot}%{isoqdir}/bin/cron.sh

#mv %{buildroot}/%{basedir}/doc/isoqlog/* %{buildroot}/%{_docdir}/%{name}/

mv %{buildroot}/usr/etc/isoqlog.conf-dist %{buildroot}/%{_sysconfdir}/%{name}/.
mv %{buildroot}/usr/etc/isoqlog.domains-dist %{buildroot}/%{_sysconfdir}/%{name}/.

install -D *.html            %{buildroot}%{_datadir}/%{name}/htmltemp

#----------------------------------------------------------------------------
%clean
#----------------------------------------------------------------------------
rm -rf %{buildroot}

#----------------------------------------------------------------------------
%postun
#----------------------------------------------------------------------------
# Remove cron-job
if [ "$1" = "0" ]; then
  grep -v '* * * * root %{vdir}/bin/clearopensmtp' %{crontab} > %{crontab}.new
  mv -f %{crontab}.new %{crontab}
fi

#----------------------------------------------------------------------------
%post
#----------------------------------------------------------------------------
# Install cron-job
if ! grep '* * * * root %{isoqdir}/bin/cron.sh' %{crontab} > /dev/null; then
  echo "" >> %{crontab}
  echo "58 * * * * root %{isoqdir}/bin/cron.sh 2>&1 > /dev/null" >> %{crontab}
fi

#----------------------------------------------------------------------------
%files
#----------------------------------------------------------------------------
%defattr(-,root,root)

# Docs
%attr(0644,root,root) %doc %{_docdir}/%{name}/*

%attr(0644,root,root) %config(noreplace)      %{_sysconfdir}/%{name}/*
%attr(0755,root,root)                         %{_bindir}/%{name}
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{isoqdir}/bin
%attr(0755,root,root)                         %{isoqdir}/bin/cron.sh
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_datadir}/%{name}/htmltemp
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_datadir}/%{name}/htmltemp/images
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_datadir}/%{name}/htmltemp/library
%attr(0644,%{apacheuser},%{apachegroup})      %{_datadir}/%{name}/htmltemp/*
%attr(0755,%{apacheuser},%{apachegroup}) %dir %{_datadir}/%{name}/lang
%attr(0644,%{apacheuser},%{apachegroup})      %{_datadir}/%{name}/lang/*
%attr(0755,root,root)                    %dir %{_docdir}/%{name}/tr
%attr(0644,root,root)                         %{basedir}/include/*

#----------------------------------------------------------------------------"
%changelog
#----------------------------------------------------------------------------
* Fri Nov 15 2013 Eric Shubert <eric@datamatters.us> 2.2.1-0.qt
- Migrated to github
- Removed -toaster designation
- Added CentOS 6 support
- Removed unsupported cruft
- Bumped version to current upstream
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.7
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.7
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.6
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
* Sat Feb 14 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.5
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 2.1-1.3.5
- Added Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.3.4
- Added CentOS 5 i386 support
- Added CentOS 5 x86_64 support
* Fri Feb 23 2007 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.3.3
- Fix ownership of cron.sh to root:root
* Wed Nov 01 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 2.1-1.3.2
- Added Fedora Core 6 support
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.3.1
- Add SuSE 10.1 support
- Set apacheuser and apachegroup correctly in cron.sh
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.10
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.9
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.8
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.7
- Add CentOS 4 x86_64 support
* Fri Sep 22 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.6
- Remove automake config for Mandrake acct build failures
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.5
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 2.1-1.2.4
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Fri May 27 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.3
- Remove doc rpm
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.2
- Add Fedora Core 3 support
- Add CentOS 4 support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.2.1
- Add Fedora Core 2 support
* Wed Feb 11 2004 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.1.5
- Fix Trustix 2.0 crontab call to fcrontab
- Define crontab
- Define appacheuser and apachegroup
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.1.4
- Add Fedora Core 1 support
* Tue Nov 25 2003 Nick Hemmesch <nick@ndhsoft.com> 2.1-1.1.3
- Add Red Hat 9 support
- Add Trustix 2.0 support
- Add Mandrake 9.2 support
- Fix images to images-toaster
* Sun Mar 30 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.1-1.1.2
- Toaster HTML templates (alpha status)
* Sat Mar 29 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.1-1.1.1
- First rpm: everything is OK. Templates are NOT ok.
