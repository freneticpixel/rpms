%global changeset c1296af77528

Name:             ldapd
Version:          0
Release:          0.1.%{changeset}%{?dist}
Summary:          A small LDAP daemon

Group:            System Environment/Daemons
License:          MIT
URL:              http://www.bzero.se/ldapd/
Source0:          https://bitbucket.org/bzero/ldapd-portable/get/%{changeset}.tar.bz2
Source1:          %{name}.conf
Source2:          %{name}.init
# elinks http://www.bzero.se/ldapd/ > README
Source10:         README
# Set LDAPD_USER and DATADIR
Patch0:           ldapd-portable-c1296af77528-config.patch
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    byacc
BuildRequires:    libevent-devel
BuildRequires:    openssl-devel

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
ldapd is a daemon which implements version 3 of the LDAP protocol.

%prep
%setup -q -n bzero-ldapd-portable-%{changeset}
%patch0 -p1
cp -p %{SOURCE10} README

%build
./bootstrap
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# Config
install -p -D -m 600 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

# Schema
for path in $( ls ldapd/schema/*.schema ); do
  file=$( basename "$path" )
  install -p -D -m 644 "ldapd/schema/$file" \
    "%{buildroot}%{_sysconfdir}/ldap/schema/$file"
done

# Misc other
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}

%post
/sbin/chkconfig --add ldapd

%pre
getent group ldapd &> /dev/null || groupadd -r ldapd &> /dev/null
getent passwd ldapd &> /dev/null || \
useradd -r -g ldapd -d %{_sharedstatedir}/ldapd -s /sbin/nologin \
-c 'LDAP daemon' ldapd &> /dev/null
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service ldapd stop &> /dev/null
  /sbin/chkconfig --del ldapd &> /dev/null
fi

%files
%defattr(-,root,root,-)
%doc README
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/ldap/schema/*.schema
%dir %attr(0700, ldapd, root) %{_sharedstatedir}/%{name}
%{_initddir}/%{name}
%{_bindir}/ldapctl
%{_sbindir}/ldapd
%{_mandir}/man5/ldapd.conf.5*
%{_mandir}/man8/ldapctl.8*
%{_mandir}/man8/ldapd.8*

%changelog
* Fri Dec 10 2010 Silas Sewell <silas@sewell.ch> - 0-0.1.c1296af77528
- Initial package
