%global changeset 7cecf64752fd

Name:             rabbitmq-c
Version:          0
Release:          0.3.%{changeset}%{?dist}
Summary:          RabbitMQ C client

Group:            Development/Libraries
License:          MPLv1.1
URL:              http://hg.rabbitmq.com/rabbitmq-c
Source0:          http://hg.rabbitmq.com/rabbitmq-c/archive/%{changeset}.tar.bz2

BuildRequires:    autoconf
BuildRequires:    libtool
BuildRequires:    rabbitmq-codegen

%description
A RabbitMQ C client.

%package          devel
Summary:          Development files for %{name}
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description      devel
A RabbitMQ C client.

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{changeset}

%build
ln -s %{_datarootdir}/rabbitmq-codegen codegen
autoreconf -i
%configure
%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=%{buildroot} install
# Remove misc files
%{__rm} -f %{buildroot}%{_libdir}/librabbitmq.a
%{__rm} -f %{buildroot}%{_libdir}/librabbitmq.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING LICENSE-GPL-2.0 LICENSE-MPL-RabbitMQ README
%{_libdir}/librabbitmq.so.*

%files devel
%defattr(-,root,root,-)
%doc TODO
%{_includedir}/amqp*.h
%{_libdir}/librabbitmq.so

%changelog
* Thu Dec 01 2011 Silas Sewell <silas@sewell.org> - 0-0.3.7cecf64752fd
- Update to latest build

* Sat Apr 30 2011 Silas Sewell <silas@sewell.ch> - 0-0.2.ab5bd3b3f8cc
- Initial build

* Wed Dec 29 2010 Silas Sewell <silas@sewell.ch> - 0-0.1.5ff94810e908
- Initial build
