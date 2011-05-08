%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%endif


%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%global checkout 18f5d061558a176f5496aa8e049182c1a7da64f6

%global srcname pyzmq

%global run_tests 0

Name:           python-zmq
Version:        2.1.1
Release:        1%{?dist}
Summary:        Software library for fast, message-based applications

Group:          Development/Libraries
License:        LGPLv3+ and ASL 2.0
URL:            http://www.zeromq.org/bindings:python
# VCS:          git:http://github.com/zeromq/pyzmq.git
# git checkout with the commands:
# git clone http://github.com/zeromq/pyzmq.git pyzmq.git
# cd pyzmq.git
# git archive --format=tar --prefix=pyzmq-%%{version}/ %%{checkout} | xz -z --force - > pyzmq-%%{version}.tar.xz
Source0:        http://cloud.github.com/downloads/zeromq/pyzmq/pyzmq-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  zeromq-devel
BuildRequires:  python-nose

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# needed for 2to3
BuildRequires:  python-tools
# not yet build
#BuildRequires:  python3-nose
%endif

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.


%if 0%{?with_python3}
%package -n python3-zmq
Summary:        Software library for fast, message-based applications
Group:          Development/Libraries
License:        LGPLv3+
%description -n python3-zmq
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the python bindings.
%endif


%prep
%setup -q -n %{srcname}-%{version}
# remove shebangs
for lib in zmq/eventloop/*.py; do
    sed '/\/usr\/bin\/env/d' $lib > $lib.new &&
    touch -r $lib $lib.new &&
    mv $lib.new $lib
done

# remove excecutable bits
chmod -x examples/pubsub/topics_pub.py
chmod -x examples/pubsub/topics_sub.py

# delete hidden files
#find examples -name '.*' | xargs rm -v


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
rm -r %{py3dir}/examples

%endif


%build
CFLAGS="%{optflags}" %{__python} setupegg.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3



%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

# remove tests doesn't work here, do that after running the tests

popd
%endif # with_python3


%{__python} setupegg.py install -O1 --skip-build --root %{buildroot}

# remove tests doesn't work here, do that after running the tests



%check
%if 0%{?run_tests}
    rm zmq/__*
    PYTHONPATH=%{buildroot}%{python_sitearch} \
    %{__python} setup.py test
    rm -r %{buildroot}%{python_sitearch}/zmq/tests

    %if 0%{?with_python3}
    # there is no python3-nose yet
    pushd %{py3dir}
    rm zmq/__*
    #PYTHONPATH=%{buildroot}%{python3_sitearch} \
    #    %{__python3} setup.py test
    rm -r %{buildroot}%{python3_sitearch}/zmq/tests
    popd
    %endif
%endif


%files
%defattr(-,root,root,-)
%doc README.rst COPYING.LESSER examples/
%{python_sitearch}/%{srcname}-*.egg-info
%{python_sitearch}/zmq


%if 0%{?with_python3}
%files -n python3-zmq
%defattr(-,root,root,-)
%doc README.rst COPYING.LESSER
# examples/
%{python3_sitearch}/%{srcname}-*.egg-info
%{python3_sitearch}/zmq
%endif


%changelog
* Wed Mar 23 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.1.1-1
- update to new version (#682201)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.0.10.1-1
- update to new version (fixes memory leak)
- no need to run 2to3 on python3 subpackage

* Thu Jan 13 2011 Thomas Spura <tomspur@fedoraproject.org> - 2.0.10-1
- update to new version
- remove patch (is upstream)
- run tests differently

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.8-2
- rebuild for newer python3

* Thu Sep 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.0.8-1
- update to new version to be comply with zeromp

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Aug  5 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-3
- add missing BR for 2to3

* Tue Aug  3 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-2
- build python3 subpackage
- rename to from pyzmq to python-zmq
- change license

* Sun Jul 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.1.20100725git18f5d06-1
- renew git snapshot
- start from version 0.1 like upstream (not the version from zeromq)
- remove buildroot / %%clean

* Sat Jun 12 2010 Thomas Spura <tomspur@fedoraproject.org - 2.0.7-1
- initial package (based on upstreams example one)
