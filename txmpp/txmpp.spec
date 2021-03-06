Name:             txmpp
Version:          0.0.3
Release:          1%{?dist}
Summary:          A C++ XMPP library
Group:            System Environment/Libraries
License:          BSD
URL:              http://www.tidg.org/txmpp
Source0:          http://github.com/downloads/tidg/txmpp/%{name}-%{version}.tar.bz2
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    expat-devel >= 2.0.1
BuildRequires:    openssl-devel
BuildRequires:    scons

%description
txmpp is a permissively licensed C++ XMPP library.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description      devel
txmpp is a permissively licensed C++ XMPP library.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
scons %{?_smp_mflags} --flags="%{optflags}"

%install
rm -rf %{buildroot}
scons %{?_smp_mflags} --flags="%{optflags}" --install \
  --includedir=%{buildroot}/%{_includedir} \
  --libdir=%{buildroot}/%{_libdir}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGELOG CONTRIBUTORS LICENSE README.md
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/txmpp
%{_libdir}/*.so

%changelog
* Fri Aug 06 2010 Silas Sewell <silas@sewell.ch> - 0.0.3-1
- Update to 0.0.3

* Sun Jul 25 2010 Silas Sewell <silas@sewell.ch> - 0.0.2-3
- Remove expat2

* Sun Jul 25 2010 Silas Sewell <silas@sewell.ch> - 0.0.2-2
- Remove documentation from devel package
- Fix main package group

* Fri Jul 02 2010 Silas Sewell <silas@sewell.ch> - 0.0.2-1
- Release 0.0.2
- Include AUTHORS & CHANGELOG

* Tue Jun 15 2010 Silas Sewell <silas@sewell.ch> - 0.0.1-1
- Initial build
