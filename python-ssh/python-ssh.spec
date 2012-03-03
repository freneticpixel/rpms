%global realname ssh

%if 0%{?fedora} > 16 || 0%{?rhel} > 6
%global with_python3 0
%endif

Name:           python-%{realname}
Version:        1.7.13
Release:        2%{?dist}
Summary:        A Python SSH2 library

Group:          Development/Languages
License:        LGPLv2+
URL:            https://github.com/bitprophet/ssh
Source0:        http://pypi.python.org/packages/source/s/ssh/ssh-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-crypto
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  /usr/bin/2to3
BuildRequires:  python3-crypto
%endif # with_python3

Requires:       python-crypto

%description
This is a library for making SSH2 connections (client or server). Emphasis is
on using SSH2 as an alternative to SSL for making secure connections between
python scripts. All major ciphers and hash methods are supported. SFTP client
and server mode are both supported too.

%if 0%{?with_python3}
%package -n     python3-%{realname}
Summary:        A Python 3 SSH2 library
Group:          Development/Languages

Requires:       python3-crypto

%description -n python3-%{realname}
This is a library for making SSH2 connections (client or server). Emphasis is
on using SSH2 as an alternative to SSL for making secure connections between
python scripts. All major ciphers and hash methods are supported. SFTP client
and server mode are both supported too.
%endif # with_python3

%prep
%setup -q -n %{realname}-%{version}

rm -rf ssh.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
# Convert tabs to 8 spaces
find %{py3dir} -name '*.py' -exec sed -i 's|\t|        |g' {} \;
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python} setup.py build

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} test.py --verbose
popd
%endif # with_python3

%{__python} test.py --verbose

%files
%doc LICENSE README
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}*%{version}*.egg-info

%if 0%{?with_python3}
%files -n python3-%{realname}
%doc LICENSE README
%{python_sitelib3}/%{realname}
%{python_sitelib3}/%{realname}*%{version}*.egg-info
%endif # with_python3

%changelog
* Sat Mar 03 2012 Silas Sewell <silas@sewell.org> - 1.7.13-2
- Add check section and python3 (disabled)

* Sat Feb 25 2012 Silas Sewell <silas@sewell.org> - 1.7.13-1
- Initial package
