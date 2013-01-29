Name:             cmogstored
Version:          1.1.0
Release:          1%{?dist}
Summary:          An alternative mogstored implementation for MogileFS

Group:            Applications/System
License:          GPLv3
URL:              http://bogomips.org/cmogstored.git
Source0:          http://bogomips.org/cmogstored/files/cmogstored-%{version}.tar.gz
Source1:          %{name}.init
Source2:          %{name}.conf
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    help2man

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
cmogstored is an alternative implementation of the "mogstored" storage
component of MogileFS.  cmogstored is implemented in C and does not use
Perl at runtime.  cmogstored is the only component you need to install
on a MogileFS storage node.

Read more about MogileFS here: http://mogilefs.org/ cmogstored is not directly
affiliated with the MogileFS project nor any commercial interests behind
MogileFS.

%prep
%setup -q

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -fr %{buildroot}

%{__make} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sbindir}

mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}.conf
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

%clean
rm -fr %{buildroot}

%post
if [ $1 -eq 1 ]; then
  /sbin/chkconfig --add cmogstored
fi

%pre
getent group mogstored >/dev/null || groupadd -r mogstored
getent passwd mogstored >/dev/null || \
  useradd -r -g mogstored -d / -s /sbin/nologin \
  -c "MogileFS storage daemon" mogstored
exit 0

%preun
if [ $1 -eq 0 ]; then
  /sbin/service cmogstored stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del cmogstored
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING HACKING README TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755, mogstored, root) %{_localstatedir}/run/%{name}
%{_initrddir}/%{name}
%{_mandir}/man*/%{name}.*
%{_sbindir}/%{name}

%changelog
* Tue Jan 22 2013 Silas Sewell <silas@sewell.org> - 1.1.0-1
- Update to 1.1.0

* Thu Jan 03 2013 Silas Sewell <silas@sewell.org> - 1.0.0-1
- Update to 1.0.0

* Thu Sep 13 2012 Silas Sewell <silas@sewell.org> - 0.5.0-1
- Update to 0.5.0

* Wed Jul 18 2012 Silas Sewell <silas@sewell.org> - 0.4.0-1
- Initial package
