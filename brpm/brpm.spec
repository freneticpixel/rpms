Name:           brpm
Version:        0.4.0
Release:        1%{?dist}
Summary:        Build rpms

Group:          Development/Languages
License:        MIT
URL:            https://github.com/silas/brpm
Source0:        https://github.com/downloads/silas/brpm/brpm-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       mock
Requires:       rpm-build
Requires:       python-ops >= 0.4.4

%description
A simple tool for building RPMs.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%{python_sitelib}/%{name}.py*
%{python_sitelib}/%{name}-%{version}-py*.egg-info

%changelog
* Thu Jul 05 2012 Silas Sewell <silas@sewell.org> - 0.4.0-1
- Initial build
