%define short_name pika

Name:           python-%{short_name}
Version:        0.9.3
Release:        1%{?dist}
Summary:        AMQP 0-9-1 client library for Python

Group:          Development/Libraries
License:        MPLv1.1 or GPLv2
URL:            http://github.com/tonyg/pika
Source0:        http://pypi.python.org/packages/source/p/pika/pika-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-setuptools
BuildRequires:  python-devel
Requires:       python

%description
Pika is a pure-Python implementation of the AMQP 0-9-1 protocol that tries to
stay fairly independent of the underlying network support library. Pika was
developed primarily for use with RabbitMQ, but should also work with other AMQP
0-9-1 brokers.

%prep
%setup -q -n %{short_name}-v%{version}

# Fix on-executable-script error
sed -i '/^#!\/usr\/bin\/env python/d' \
  pika/adapters/select_connection.py \
  pika/adapters/tornado_connection.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{python_sitelib}/%{short_name}*
%{python_sitelib}/%{short_name}*/*
%doc COPYING
%doc LICENSE-GPL-2.0
%doc LICENSE-MPL-Pika
%doc README.md
%doc THANKS
%doc TODO
%doc examples

%changelog
* Wed Feb 16 2011 Silas Sewell <silas@sewell.ch> - 0.9.3-1
- Update to 0.9.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 2 2010 Ilia Cheishvili <ilia.cheishvili@gmail.com> - 0.5.2-1
- Initial Package
