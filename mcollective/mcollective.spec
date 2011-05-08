%define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")

Summary: A framework to build server orchestration or parallel job execution systems
Name: mcollective
Version: 1.1.3
Release: 3%{?dist}
Group: System Tools
License: Apache License, Version 2

URL: http://marionette-collective.org/

Source0: http://puppetlabs.com/downloads/mcollective/%{name}-%{version}.tgz
Source1: mcollective.service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ruby
%if 0%{?fedora} >= 15
BuildRequires: systemd-units
%endif

Requires: ruby
Requires: rubygem(stomp)
Requires: mcollective-common = %{version}-%{release}

%if 0%{?fedora} >= 15
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

BuildArch: noarch

%package common
Summary: Common libraries for the mcollective clients and servers
Group: System Tools
Requires: ruby
Requires: rubygems
Requires: rubygem-stomp

%description common
Common libraries for the mcollective clients and servers

%package client
Summary: Client tools for the mcollective application server
Requires: mcollective-common = %{version}-%{release}
Requires: ruby
Requires: rubygems
Requires: rubygem-stomp
Group: System Tools

%description client
Client tools for the mcollective application server

%description
The Marionette Collective is a framework to build server orchestration
or parallel job execution systems.

%prep
%setup -q

%build
%if 0%{?fedora} <= 14 || 0%{?rhel}
%{__sed} -i -e 's/^daemonize = .*$/daemonize = 1/' etc/server.cfg.dist
%endif
%if 0%{?fedora} >= 15
%{__sed} -i -e 's/^daemonize = .*$/daemonize = 0/' etc/server.cfg.dist
%endif

%install
rm -rf %{buildroot}

%{__install} -d -m0755  %{buildroot}/%{ruby_sitelib}/mcollective
cp --preserve=timestamps --recursive lib/* %{buildroot}/%{ruby_sitelib}

%{__install} -d -m0755  %{buildroot}/usr/sbin
%{__install} -p -m0755 mcollectived.rb %{buildroot}/usr/sbin/mcollectived
for f in mc-*
do
  %{__install} -p -m0755 $f %{buildroot}/usr/sbin/$f
done

%if 0%{?fedora} <= 14 || 0%{?rhel}
%{__install} -d -m0755  %{buildroot}/etc/init.d
%{__install} -p -m0755 mcollective.init %{buildroot}/etc/init.d/mcollective
%endif

%if 0%{?fedora} >= 15
%{__install} -d -m0755  %{buildroot}%{_unitdir}
%{__install} -p -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/mcollective.service
%endif

%{__install} -d -m0755  %{buildroot}/usr/libexec/mcollective
cp --preserve=timestamps --recursive plugins/* %{buildroot}/usr/libexec/mcollective

%{__install} -d -m0755  %{buildroot}/etc/mcollective
%{__install} -d -m0755  %{buildroot}/etc/mcollective/ssl
%{__install} -d -m0755  %{buildroot}/etc/mcollective/ssl/clients
%{__install} -m0440 etc/server.cfg.dist %{buildroot}/etc/mcollective/server.cfg
%{__install} -m0444 etc/client.cfg.dist %{buildroot}/etc/mcollective/client.cfg
%{__install} -m0444 etc/facts.yaml.dist %{buildroot}/etc/mcollective/facts.yaml
%{__install} -m0444 etc/rpc-help.erb %{buildroot}/etc/mcollective/rpc-help.erb

%clean
rm -rf %{buildroot}

%post
%if 0%{?fedora} <= 14 || 0%{?rhel}
/sbin/chkconfig --add mcollective || :
%endif
%if 0%{?fedora} >= 15
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif

%postun
%if 0%{?fedora} <= 14 || 0%{?rhel}
if [ "$1" -ge 1 ]; then
	/sbin/service mcollective condrestart &>/dev/null || :
fi
%endif
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mcollective.service >/dev/null 2>&1 || :
fi
%endif

%preun
%if 0%{?fedora} <= 14 || 0%{?rhel}
if [ "$1" = 0 ] ; then
  /sbin/service mcollective stop > /dev/null 2>&1
  /sbin/chkconfig --del mcollective || :
fi
%endif
%if 0%{?fedora} >= 15
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mcollective.service > /dev/null 2>&1 || :
    /bin/systemctl stop mcollective.service > /dev/null 2>&1 || :
fi
%endif

%files common
%doc COPYING
%{ruby_sitelib}/mcollective.rb
%{ruby_sitelib}/mcollective
/usr/libexec/mcollective
%dir /etc/mcollective
%dir /etc/mcollective/ssl

%files client
%attr(0755, root, root)/usr/sbin/mc-*
%doc COPYING
%config(noreplace)/etc/mcollective/client.cfg
%config/etc/mcollective/rpc-help.erb

%files
%doc COPYING
/usr/sbin/mcollectived
%if 0%{?fedora} <= 14 || 0%{?rhel}
/etc/init.d/mcollective
%endif
%if 0%{?fedora} >= 15
%{_unitdir}/mcollective.service
%endif
%config(noreplace)/etc/mcollective/server.cfg
%config(noreplace)/etc/mcollective/facts.yaml
%dir /etc/mcollective/ssl/clients

%changelog
* Wed Apr 20 2011 Jeffrey Ollie <jeff@ocjtech.us> - 1.1.3-3
- First version for Fedora

