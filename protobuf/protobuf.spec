%define without_gtest %{?_without_gtest:  1} %{?!_without_gtest:  0}
%define with_python   %{?_without_python: 0} %{?!_without_python: 1}
%define with_java     %{?_without_java:   0} %{?!_without_java:   1}

%if 0%{?el5}
%define without_gtest 1
%define with_java 0
%endif

%if %{with_python}
%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%endif

Summary:        Protocol Buffers - Google's data interchange format
Name:           protobuf
Version:        2.3.0
Release:        1%{?dist}
License:        BSD
Group:          Development/Libraries
Source:         http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
Source1:        ftdetect-proto.vim
# Remove version of gtest included with source
Patch1:         protobuf-%{version}-fedora-gtest.patch
# Fix various Java build issues
Patch2:         protobuf-java-fixes.patch
# Remove setuptools version requirement for epel
Patch3:         protobuf-python-fix-epel.patch
URL:            http://code.google.com/p/protobuf/
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  automake autoconf libtool pkgconfig 
%if !%{without_gtest}
BuildRequires:  gtest-devel
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%if 0%{?el5}
BuildRequires: chrpath
%endif

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary: Protocol Buffers C++ headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-compiler = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for Protocol Buffers

%package lite
Summary: Protocol Buffers LITE_RUNTIME libraries
Group: Development/Libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary: Protocol Buffers LITE_RUNTIME development libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}

%description lite-devel
This package contains development libraries built with 
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-static
Summary: Static development files for %{name}-lite
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description lite-static
This package contains static development libraries built with 
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%if %{with_python}
%package python
Summary: Python bindings for Google Protocol Buffers
Group: Development/Languages
BuildRequires: python-devel
BuildRequires: python-setuptools
Conflicts: %{name}-compiler > %{version}
Conflicts: %{name}-compiler < %{version}

%description python
This package contains Python libraries for Google Protocol Buffers
%endif

%package vim
Summary: Vim syntax highlighting for Google Protocol Buffers descriptions
Group: Development/Libraries
Requires: vim-enhanced

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor

%if %{with_java}
%package java
Summary: Java Protocol Buffers runtime library
Group:   Development/Languages
BuildRequires:    java-devel >= 1:1.6
BuildRequires:    jpackage-utils
BuildRequires:    maven2
BuildRequires:    maven2-plugin-antrun
BuildRequires:    maven2-plugin-compiler
BuildRequires:    maven2-plugin-install
BuildRequires:    maven2-plugin-jar
BuildRequires:    maven2-plugin-javadoc
BuildRequires:    maven-doxia-sitetools
BuildRequires:    maven2-plugin-resources
BuildRequires:    maven2-plugin-surefire
Requires:         java >= 1:1.6
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils
Conflicts:        %{name}-compiler > %{version}
Conflicts:        %{name}-compiler < %{version}

%description java
This package contains Java Protocol Buffers runtime library.

%package javadoc
Summary: Javadocs for %{name}-java
Group:   Documentation
Requires: jpackage-utils
Requires: %{name}-java = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}-java.

%endif

%prep
%setup -q
%if !%{without_gtest}
rm -rf gtest
%patch1 -p1
%endif
chmod 644 examples/*
%if %{with_java}
%patch2 -p1
rm -fr java/src/test
%endif
%if 0%{?el5}
%patch3 -p1
%endif

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
%if !0%{?el5}
./autogen.sh
%endif
%configure

make %{?_smp_mflags}

%if %{with_python}
pushd python
python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with_java}
pushd java
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL
mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL install javadoc:javadoc
popd
%endif

%check
make %{?_smp_mflags} check

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;

# Fix rpath in epel because we can't run autogen.sh
%if 0%{?el5}
chrpath --delete %{buildroot}%{_libdir}/libprotoc.so.*
chrpath --delete %{buildroot}%{_bindir}/protoc
%endif

%if %{with_python}
pushd python
python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with_java}
pushd java
install -d -m 755 %{buildroot}%{_javadir}
install -pm 644 target/%{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml %{buildroot}%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap org.apache.maven %{name} %{version} JPP %{name}

%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post lite -p /sbin/ldconfig
%postun lite -p /sbin/ldconfig

%post compiler -p /sbin/ldconfig
%postun compiler -p /sbin/ldconfig

%if %{with_java}
%post java
%update_maven_depmap

%postun java
%update_maven_depmap
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_libdir}/libprotobuf.so.*
%doc CHANGES.txt CONTRIBUTORS.txt COPYING.txt README.txt

%files compiler
%defattr(-, root, root, -)
%{_bindir}/protoc
%{_libdir}/libprotoc.so.*
%doc COPYING.txt README.txt

%files devel
%defattr(-, root, root, -)
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files static
%defattr(-, root, root, -)
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files lite
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.so.*

%files lite-devel
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%files lite-static
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.a

%if %{with_python}
%files python
%defattr(-, root, root, -)
%dir %{python_sitelib}/google
%{python_sitelib}/google/protobuf/
%{python_sitelib}/protobuf-%{version}-*.egg-info/
%{python_sitelib}/protobuf-%{version}-*-nspkg.pth
%doc python/README.txt 
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%files vim
%defattr(-, root, root, -)
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with_java}
%files java
%defattr(-, root, root, -)
%{_datadir}/maven2/poms/JPP-protobuf.pom
%{_mavendepmapfragdir}/protobuf
%{_javadir}/*
%doc examples/AddPerson.java examples/ListPeople.java

%files javadoc
%defattr(-, root, root, -)
%{_javadocdir}/%{name}
%endif

%changelog
* Wed Apr 21 2010 Silas Sewell <silas@sewell.ch> - 2.3.0-1
- Update to 2.3.0
- Add epel support
- Include partial patch from Bradley Baetz to re-enable Java

* Wed Sep 30 2009 Lev Shamardin <shamardin@gmail.com> - 2.2.0-2
- added export PTHREAD_LIBS="-lpthread"

* Fri Sep 18 2009 Lev Shamardin <shamardin@gmail.com> - 2.2.0-1
- Upgraded to upstream protobuf-2.2.0
- New -lite packages

* Sun Mar 01 2009 Caolán McNamra <caolanm@redhat.com> - 2.0.2-8
- add stdio.h for sprintf, perror, etc.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-6
- Small fixes for python 2.6 eggs.
- Temporarily disabled java subpackage due to build problems, will be fixed and
  turned back on in future.

* Thu Nov 27 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-5
- No problems with ppc & ppc64 arch in rawhide, had to do a release bump.

* Sat Nov 22 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-4
- Added patch from subversion r70 to workaround gcc 4.3.0 bug (see
  http://code.google.com/p/protobuf/issues/detail?id=45 for more
  details).

* Tue Nov 11 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-3
- Added conflicts to java and python subpackages to prevent using with
  wrong compiler versions.
- Fixed license.
- Fixed BuildRequires for -python subpackage.
- Fixed Requires and Group for -javadoc subpackage.
- Fixed Requires for -devel subpackage.
- Fixed issue with wrong shebang in descriptor_pb2.py.
- Specify build options via --with/--without.
- Use Fedora-packaged gtest library instead of a bundled one by
  default (optional).

* Fri Oct 31 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-2
- Use python_sitelib macro instead of INSTALLED_FILES.
- Fix the license.
- Fix redundant requirement for -devel subpackage.
- Fix wrong dependences for -python subpackage.
- Fix typo in requirements for -javadoc subpackage.
- Use -p option for cp and install to preserve timestamps.
- Remove unneeded ldconfig call for post scripts of -devel subpackage.
- Fix directories ownership.

* Sun Oct 12 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.2-1
- Update to version 2.0.2
- New -java and -javadoc subpackages.
- Options to disable building of -python and -java* subpackages

* Mon Sep 15 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.1-2
- Added -p switch to install commands to preserve timestamps.
- Fixed Version and Libs in pkgconfig script.
- Added pkgconfig requires for -devel package.
- Removed libtool archives from -devel package.

* Thu Sep 04 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.1-1
- Updated to 2.0.1 version.

* Wed Aug 13 2008 Lev Shamardin <shamardin@gmail.com> - 2.0.0-0.1.beta
- Initial package version. Credits for vim subpackage and pkgconfig go
  to Rick L Vinyard Jr <rvinyard@cs.nmsu.edu>
