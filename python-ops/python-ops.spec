%global realname ops

Name:           python-%{realname}
Version:        0.4.6
Release:        1%{?dist}
Summary:        Library for scripting systems administration tasks

Group:          Development/Languages
License:        MIT
URL:            https://github.com/silas/ops
Source0:        http://pypi.python.org/packages/source/o/ops/ops-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:  python-sphinx
Requires:       python

%description
ops is a library for scripting systems administration tasks in Python.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build
pushd docs; make html; popd

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md docs/build/html
%{python_sitelib}/%{realname}.py*
%{python_sitelib}/%{realname}-%{version}-py*.egg-info

%changelog
* Wed Jul 11 2012 Silas Sewell <silas@sewell.org> - 0.4.6-1
- Version 0.4.6

* Wed Jul 11 2012 Silas Sewell <silas@sewell.org> - 0.4.5-1
- Version 0.4.5

* Thu Jul 05 2012 Silas Sewell <silas@sewell.org> - 0.4.4-1
- Version 0.4.4

* Thu Jan 27 2011 Silas Sewell <silas@sewell.ch> - 0.2.0-1
- Add settings module
- Remove utils.dir, utils.pushd, and utils.popd

* Sat Dec 18 2010 Silas Sewell <silas@sewell.ch> - 0.1.0-1
- Initial build
