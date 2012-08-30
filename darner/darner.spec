%global extra g2dd8482
%global rev 2dd8482

Name:             darner
Version:          0.1.4
Release:          1%{?dist}
Summary:          A simple message queue server

Group:            Applications/Databases
License:          ASL 2.0
URL:              https://github.com/wavii/darner
# curl -JOLs https://github.com/wavii/darner/tarball/v%{version}
Source0:          wavii-darner-v%{version}-0-%{extra}.tar.gz
Source1:          %{name}.conf
Source2:          %{name}.service
Patch0:           darner-v0.1.4-pthread.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    boost-devel
BuildRequires:    cmake
BuildRequires:    leveldb-devel
BuildRequires:    snappy-devel

Requires(pre):    shadow-utils
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description
Darner is a very simple message queue server. Unlike in-memory servers such as
redis, Darner is designed to handle queues much larger than what can be held in
RAM. And unlike enterprise queue servers such as RabbitMQ, Darner keeps all
messages out of process, relying instead on the kernel's virtual memory manager
via log-structured storage.

%prep
%setup -q -n wavii-darner-%{rev}
%patch0 -p1

%build
%cmake .
make %{?_smp_mflags}

%check
ctest

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}

install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}

%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add darner
%systemd_post darner.service

%pre
%systemd_preun darner.service
getent group darner &> /dev/null || groupadd -r darner &> /dev/null
getent passwd darner &> /dev/null || \
useradd -r -g darner -d %{_sharedstatedir}/darner -s /sbin/nologin \
-c 'Darner Server' darner &> /dev/null
exit 0

%preun
%systemd_postun_with_restart darner.service 

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README.md
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_unitdir}/%{name}.service
%dir %attr(0755, darner, root) %{_sharedstatedir}/%{name}
%{_bindir}/%{name}

%changelog
* Thu Aug 30 2012 Silas Sewell <silas@sewell.org> - 0.1.4-1
- Initial package
