
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global config_opts --disable-static --with-thriftpath=%{_prefix} --with-fb303path=%{_prefix} --with-boost-system=boost_system --with-boost-filesystem=boost_filesystem

Name:             scribe
Version:          master
Release:          1%{?dist}
Summary:          A server for aggregating log data streamed in real time

Group:            Development/Libraries
License:          ASL 2.0
URL:              http://developers.facebook.com/scribe
Source0:          https://github.com/freneticpixel/scribe/archive/scribe-master.zip
Source1:          scribed.init
Source2:          scribed.sysconfig
BuildRoot:        %{_tmppath}/scribe-master.zip

BuildRequires:    automake
BuildRequires:    boost-devel >= 1.36
BuildRequires:    fb303-devel
BuildRequires:    libevent-devel
BuildRequires:    thrift
BuildRequires:    thrift-cpp-devel

Requires:         %{name}-python
Requires:         fb303
Requires(post):   chkconfig

%description
Scribe is a server for aggregating log data streamed in real time from a large
number of servers. It is designed to be scalable, extensible without
client-side modification, and robust to failure of the network or any specific
machine.

%package python
Summary:          Python bindings for %{name}
Group:            Development/Libraries
BuildRequires:    python-devel
Requires:         fb303-python

%description python
Python bindings for %{name}.

%package php
Summary:          PHP bindings for %{name}
Group:            Development/Libraries
Requires:         fb303-php

%description php
PHP bindings for %{name}.

%prep
%setup -q

%build
# Fix compile errors from mismatched return enum-based return types
sed -i -e 's/ --cpp --py --php/ --gen cpp:pure_enums --gen py --gen php/' src/Makefile.am
# Fix compile errors from netinet/in.h and inttypes.h not being included
sed -i -e 's/^AM_CPPFLAGS = /AM_CPPFLAGS = -DHAVE_NETINET_IN_H -DHAVE_INTTYPES_H /' src/Makefile.am
./bootstrap.sh %{config_opts}
%configure %{config_opts}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

# Install manually
%{__install} -D -m 755 ./examples/scribe_cat %{buildroot}%{_bindir}/scribe_cat
%{__install} -D -m 755 ./examples/scribe_ctrl %{buildroot}%{_bindir}/scribe_ctrl
%{__install} -D -m 755 ./src/libscribe.so %{buildroot}%{_libdir}/libscribe.so
%{__install} -D -m 644 ./examples/example1.conf %{buildroot}%{_sysconfdir}/scribed/default.conf
%{__install} -D -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/scribed
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/scribed

# PHP
%{__mkdir_p} %{buildroot}%{_datadir}/php/thrift/packages/%{name}
%{__cp} -r ./src/gen-php/%{name}/scribe.php %{buildroot}%{_datadir}/php/thrift/packages/%{name}/
%{__cp} -r ./src/gen-php/%{name}/scribe_types.php %{buildroot}%{_datadir}/php/thrift/packages/%{name}/

# Remove scripts
%{__rm} ./examples/scribe_*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE examples/
%config(noreplace) %{_sysconfdir}/scribed/default.conf
%config(noreplace) %{_sysconfdir}/sysconfig/scribed
%{_bindir}/scribed
%{_libdir}/libscribe.so
%{_sysconfdir}/rc.d/init.d/scribed
%{_bindir}/scribe_ctrl
/usr/lib/libdynamicbucketupdater.so
/usr/lib/libscribe.so

%files python
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info
%{_bindir}/scribe_cat

%files php
%defattr(-,root,root,-)
%{_datadir}/php/thrift/packages/%{name}/*.php

%post
/sbin/chkconfig --add scribed
/sbin/ldconfig

$postun
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /sbin/service scribed stop > /dev/null 2>&1
  /sbin/chkconfig --del scribed
fi

%changelog
* Mon Dec 07 2009 Silas Sewell <silas@sewell.ch> - 2.1-1
- Update to 2.1

* Fri May 01 2009 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Initial build
