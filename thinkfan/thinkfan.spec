Name:             thinkfan
Version:          0.8.0
Release:          1%{?dist}
Summary:          A simple fan control program

Group:            Applications/Databases
License:          BSD
URL:              http://thinkfan.sourceforge.net/
Source0:          http://sourceforge.net/projects/thinkfan/files/thinkfan-%{version}.tar.gz
Source1:          %{name}.init
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Works with any linux hwmon driver, especially with thinkpad_acpi. It is
designed to eat as little CPU power as possible. The development was inspired
by the excellent work people have done on thinkwiki.org.

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS='%{optflags}'

%install
rm -fr %{buildroot}
install -p -D -m 755 %{name} %{buildroot}%{_sbindir}/%{name}
install -p -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add thinkfan

%preun
if [ $1 = 0 ]; then
  /sbin/service thinkfan stop &> /dev/null
  /sbin/chkconfig --del thinkfan &> /dev/null
fi

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog NEWS README examples/
%{_sbindir}/%{name}
%{_initrddir}/%{name}

%changelog
* Tue May 16 2012 Silas Sewell <silas@sewell.ch> - 0.8.0-1
- Initial package
