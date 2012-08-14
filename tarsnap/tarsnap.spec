Name:             tarsnap
Version:          1.0.33
Release:          1%{?dist}
Summary:          Online backups for the truly paranoid

Group:            Applications/File
License:          Tarsnap
URL:              https://www.tarsnap.com/
Source0:          https://www.tarsnap.com/download/%{name}-autoconf-%{version}.tgz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    e2fsprogs-devel
BuildRequires:    openssl-devel

%description
Tarsnap is a secure online backup service for BSD, Linux, OS X, Solaris,
Cygwin, and can probably be compiled on many other UNIX-like operating systems.

The Tarsnap client code provides a flexible and powerful command-line interface
which can be used directly or via shell scripts.

%prep
%setup -q -n %{name}-autoconf-%{version}

%build
%configure
make %{?_smp_mflags} all

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}
# rename conf file
mv %{buildroot}%{_sysconfdir}/%{name}.conf.sample \
   %{buildroot}%{_sysconfdir}/%{name}.conf
# compress man files
gzip %{buildroot}%{_mandir}/man*/%{name}*
# create etc and cache directories
mkdir -m 700 -p \
  %{buildroot}%{_sysconfdir}/%{name} \
  %{buildroot}%{_localstatedir}/cache/%{name}
# tweak default configuration file
sed -i 's|/usr/local/tarsnap-cache|%{_localstatedir}/cache/%{name}|g' \
  %{buildroot}%{_sysconfdir}/%{name}.conf
sed -i 's|/root/tarsnap.key|%{_sysconfdir}/%{name}/%{name}.key|g' \
  %{buildroot}%{_sysconfdir}/%{name}.conf

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}*
%{_localstatedir}/cache/%{name}
%{_mandir}/man*/%{name}*
%{_sysconfdir}/%{name}

%changelog
* Tue Aug 14 2012 Silas Sewell <silas@sewell.org> - 1.0.33-1
- Update to 1.0.33

* Mon Feb 13 2012 Silas Sewell <silas@sewell.org> - 1.0.31-1
- Initial build
