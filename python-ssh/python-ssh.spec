%global realname ssh

Name:           python-%{realname}
Version:        1.7.13
Release:        1%{?dist}
Summary:        A Python SSH2 library

Group:          Development/Languages
License:        LGPLv2+
URL:            https://github.com/bitprophet/ssh
Source0:        http://pypi.python.org/packages/source/s/ssh/ssh-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-crypto

%description
This is a library for making SSH2 connections (client or server). Emphasis is
on using SSH2 as an alternative to SSL for making secure connections between
python scripts. All major ciphers and hash methods are supported. SFTP client
and server mode are both supported too.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc LICENSE README
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}*%{version}*.egg-info

%changelog
* Sat Feb 25 2012 Silas Sewell <silas@sewell.org> - 1.7.13-1
- Initial package
