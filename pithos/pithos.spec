%global commit 07dcbd8

Name:           pithos
Version:        0.3.17
Release:        1.%{commit}%{?dist}
Summary:        A Pandora client for the GNOME Desktop

Group:          Applications/File
License:        GPLv3
URL:            http://kevinmehall.net/p/pithos/
# COMMIT=%{commit}
# wget -O "kevinmehall-pithos-${COMMIT}.tar.gz" \
#   "https://github.com/kevinmehall/pithos/tarball/${COMMIT}"
Source0:        kevinmehall-pithos-%{commit}.tar.gz
# Fix desktop icon location
Patch0:         fix-pithos-desktop.patch
# Use site-package pylast
Patch1:         site-package-pylast.patch

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  python-devel
BuildRequires:  python-distutils-extra

Requires:       dbus-python
Requires:       gstreamer-plugins-bad
Requires:       gstreamer-plugins-good
Requires:       gstreamer-python
Requires:       notify-python
Requires:       pygobject2
Requires:       pygtk2
Requires:       pylast
Requires:       pyxdg

%description
Pithos is a Pandora client for the GNOME Desktop. The official Flash-based
client is a CPU hog, and Pianobar is a great reverse-engineered implementation,
but is command-line only. Neither integrate with the desktop very well, missing
things like media key support and song notifications.

It is recommended that you purchase a Pandora One membership.

%prep
%setup -q -n kevinmehall-pithos-%{commit}
%patch0 -p1
%patch1 -p1
# Fix data path
sed -i 's|../data/|%{_datadir}/%{name}|g' %{name}/pithosconfig.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --prefix=%{buildroot}%{_prefix}
# Remove packaged pylast
rm -fr %{buildroot}%{python_sitelib}/%{name}/pylast.py*
# Install icon
desktop-file-install --delete-original \
                     --add-category="GTK" \
                     --dir=%{buildroot}%{_datadir}/applications \
                     %{name}.desktop

%files
%defattr(-,root,root,-)
%doc CHANGELOG
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-*.egg-info
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_docdir}/%{name}

%changelog
* Tue May 14 2012 Silas Sewell <silas@sewell.org> - 0.3.17-1.07dcbd8
- Update to 0.3.17

* Tue May 01 2012 Silas Sewell <silas@sewell.org> - 0.3.17-0.1.d66ff7a
- Update to JSON api version

* Sun Apr 29 2012 Silas Sewell <silas@sewell.org> - 0.3.16-2
- Get sync time from JJZ's server (James Burton)

* Wed Apr 25 2012 Silas Sewell <silas@sewell.org> - 0.3.16-1
- Update to 0.3.16

* Sat Dec 17 2011 Silas Sewell <silas@sewell.org> - 0.3.14-2
- Add GTK category

* Fri Dec 16 2011 Silas Sewell <silas@sewell.org> - 0.3.14-1
- Update to 0.3.14 (revision 181)
- Fix "You have no chance to survive make your time"

* Wed Nov 09 2011 Silas Sewell <silas@sewell.org> - 0.3.13-2
- Remove packaged pylast

* Wed Nov 09 2011 Silas Sewell <silas@sewell.org> - 0.3.13-1
- Update to 0.3.13
- Use SSL for login (fixes AUTH_WEB_LOGIN_NOT_ALLOWED)
- Fix icon

* Wed Nov 09 2011 Silas Sewell <silas@sewell.org> - 0.3.12-1
- Update to 0.3.12
- Update keys and to protocol v33

* Thu Sep 22 2011 Silas Sewell <silas@sewell.org> - 0.3.11-1
- Update to 0.3.11

* Mon Jul 11 2011 Silas Sewell <silas@sewell.ch> - 0.3.10-1
- Update to 0.3.10

* Wed Apr 29 2011 Silas Sewell <silas@sewell.ch> - 0.3.9-1
- Update to 0.3.9

* Tue Nov 30 2010 Silas Sewell <silas@sewell.ch> - 0.3.6-1
- Initial package
