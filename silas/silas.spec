Name:           silas
Version:        1
Release:        1%{?dist}
Summary:        Silas's packages

Group:          Development/Languages
License:        MIT
URL:            http://silas.sewell.org

BuildArch:      noarch
Requires:       curl
Requires:       git
Requires:       ipython
Requires:       nc
Requires:       screen
Requires:       strace
Requires:       vim-enhanced
Requires:       wget

%description
Silas's standard packages.

%package dev
Summary:        Development packages
Requires:       fedpkg
Requires:       gcc
Requires:       gcc-c++
Requires:       mock
Requires:       python-devel
Requires:       python-virtualenv
Requires:       rpmdevtools
Requires:       rpmlint
Requires:       ruby-devel

%description dev
Silas's development packages.

%package games
Summary:        Games packages
Requires:       xmoto

%description games
Silas's games packages.

%package gui
Summary:        Gui packages
Requires:       keepassx

%description gui
Silas's gui packages.

%package thirdparty
Summary:        Thirdparty packages
Requires:       flash-plugin
Requires:       google-chrome-stable
Requires:       nautilus-dropbox
Requires:       pithos
Requires:       rpmfusion-free-release

%description thirdparty
Silas's thirdparty packages (not in Fedora).

%changelog
* Tue Nov 09 2011 Silas Sewell <silas@sewell.org> - 1-1
- Initial package
