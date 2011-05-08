Name:           synapse
Version:        0.2.4
Release:        1%{?dist}
Summary:        A semantic launcher written in Vala

Group:          Applications/Productivity
License:        GPLv3
URL:            http://synapse.zeitgeist-project.com/wiki/index.php?title=Main_Page
Source0:        http://launchpad.net/%{name}-project/0.2/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libzeitgeist-devel gettext libnotify-devel intltool vala
Requires:       zeitgeist

%description
Synapse is a semantic launcher written in Vala that you can use to start
applications as well as find and access relevant documents and files by making
use of the Zeitgeist engine.


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
%configure --disable-static --enable-zeitgeist --enable-indicator=auto
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d -m 755 %{buildroot}%{_datadir}/vala/vapi
install -D -m 644 vapi/*.vapi %{buildroot}%{_datadir}/vala/vapi

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/synapse
%{_datadir}/applications/synapse.desktop
%{_datadir}/icons/hicolor/scalable/apps/synapse.svg

%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%{_datadir}/vala/vapi

%changelog
* Thu Feb 24 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.2.4-1
- Updated to latest version

* Thu Jan 28 2011 Renich Bon Ciric <renich@woralelandia.com> - 0.2.2.2-1
- First build
