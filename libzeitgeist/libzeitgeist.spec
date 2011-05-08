Name:           libzeitgeist
Version:        0.3.6
Release:        1%{?dist}
Summary:        Client library for applications that want to interact with the Zeitgeist daemon

Group:          System Environment/Libraries
License:        LGPLv3 and GPLv3
URL:            https://launchpad.net/libzeitgeist
Source0:        http://launchpad.net/%{name}/0.3/%{version}/+download/%{name}-%{version}.tar.gz

BuildRequires:  glib2-devel gtk-doc
# zeitgeist is just a runtime and the reason to install libzeitgeist
Requires:       zeitgeist

%description
This project provides a client library for applications that want to interact
with the Zeitgeist daemon. The library is written in C using glib and provides
an asynchronous GObject oriented API.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make V=1 %{?_smp_mflags}


%check
#make check


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d -m 755 %{buildroot}%{_datadir}/vala/vapi
install -D -m 644 bindings/zeitgeist-1.0.{vapi,deps} %{buildroot}%{_datadir}/vala/vapi
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# remove duplicate documentation
rm -fr %{buildroot}%{_defaultdocdir}/%{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)

# documentation
%doc COPYING COPYING.GPL

# essential
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)

# Documentation
%doc AUTHORS ChangeLog COPYING COPYING.GPL MAINTAINERS NEWS README
%doc examples/*.vala examples/*.c
%doc %{_datadir}/gtk-doc/html/zeitgeist-1.0/

# essential
%{_includedir}/zeitgeist-1.0/
%{_libdir}/*.so
%{_libdir}/pkgconfig/zeitgeist-1.0.pc

# extra
%{_datadir}/vala/vapi/


%changelog
* Fri Mar 11 2011 Silas Sewell <silas@sewell.ch> - 0.3.6-1
- Update to 0.3.6

* Thu Mar 10 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.4-2
- Cleaned up old stuff (BuildRoot, Clean and stuff of sorts)
    https://fedoraproject.org/wiki/Packaging/Guidelines#BuildRoot_tag
    https://fedoraproject.org/wiki/Packaging/Guidelines#.25clean
- Added glib2-devel and gtk-doc as a BuildRequires
- Added GPLv3 since it covers the documentation examples
- Updated Requires to use the new arch specification macro when accordingly
    https://fedoraproject.org/wiki/Packaging/Guidelines#Requires
- Configured install to preserve timestamps
- Added V=1 to the make flags for more verbosity on build
- Added a check section
- Removed disable-module from configure statement since it's not needed anymore: 
    https://bugs.launchpad.net/libzeitgeist/+bug/683805

* Thu Feb 24 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.4-1
- updated to latest version

* Sun Feb 06 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.2-3
- got rid of INSTALL from docs
- got rid ot dorcdir and used doc to include html docs

* Sat Feb 05 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.3.2-2
- removed duplicate documentation
- added the use of macros for everything; including source and build dir.
- revised path syntax

* Thu Jan 27 2011 - Renich Bon Ciric <renich@woralelandia.com> - 0.3.2-1
- First build
