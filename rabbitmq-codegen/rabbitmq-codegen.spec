%global changeset 82b642218623

Name:             rabbitmq-codegen
Version:          0
Release:          0.3.%{changeset}%{?dist}
Summary:          RabbitMQ code-generation tool

Group:            Development/Libraries
License:          MPLv1.1
URL:              http://hg.rabbitmq.com/rabbitmq-codegen
Source0:          http://hg.rabbitmq.com/rabbitmq-codegen/archive/%{changeset}.tar.bz2
BuildArch:        noarch

Requires:         python

%description
RabbitMQ protocol code-generation and machine-readable spec.

%prep
%setup -q -n %{name}-%{changeset}

%build

%install
install -p -D -m 755 amqp_codegen.py %{buildroot}%{_datarootdir}/%{name}/amqp_codegen.py
for file in $( ls *.json ); do
  install -p -D -m 644 $file %{buildroot}%{_datarootdir}/%{name}/$file
done

%files
%defattr(-,root,root,-)
%doc LICENSE LICENSE-MPL-RabbitMQ README.extensions.md
%{_datarootdir}/%{name}/*.json
%{_datarootdir}/%{name}/*.py*

%changelog
* Thu Dec 01 2011 Silas Sewell <silas@sewell.org> - 0-0.3.82b642218623
- Update to latest build

* Sat Apr 30 2011 Silas Sewell <silas@sewell.ch> - 0-0.2.14faedb58703
- Update to latest build

* Wed Dec 29 2010 Silas Sewell <silas@sewell.ch> - 0-0.1.b20a37b1bee4
- Initial build
