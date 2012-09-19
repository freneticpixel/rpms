Name:           libgit2
Version:        0.17.0
Release:        1%{?dist}
Summary:        A C git library

Group:          System Environment/Libraries
License:        GPLv2 with linking exception
URL:            https://github.com/libgit2/libgit2
Source0:        https://github.com/downloads/libgit2/libgit2/libgit2-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
libgit2 is a portable, pure C implementation of the Git core methods provided
as a re-entrant linkable library with a solid API, allowing you to write native
speed custom Git applications in any language with bindings.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
libgit2 is a portable, pure C implementation of the Git core methods provided
as a re-entrant linkable library with a solid API, allowing you to write native
speed custom Git applications in any language with bindings.

The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q

%build
%cmake . -DINSTALL_LIB=%{_libdir}
make %{?_smp_mflags}

%check
ctest

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}

# move pkgconfig
mkdir -p %{buildroot}%{_datadir}/pkgconfig
mv %{buildroot}%{_libdir}/pkgconfig/%{name}.pc \
   %{buildroot}%{_datadir}/pkgconfig/%{name}.pc
rmdir %{buildroot}%{_libdir}/pkgconfig

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README.md
%{_libdir}/libgit2.so.*

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/libgit2.so
%{_includedir}/git2.h
%{_includedir}/git2

%changelog
* Wed Sep 19 2012 Silas Sewell <silas@sewell.org> - 0.17.0-1
- Update to 0.17.0

* Sat Jan 22 2011 Silas Sewell <silas@sewell.ch> - 0.2.0-1
- Initial package
