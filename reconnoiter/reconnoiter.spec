%global commit 960593b

Name:             reconnoiter
Version:          0
Release:          1.%{commit}%{?dist}
Summary:          Large-scale Monitoring and Trend Analysis System

Group:            Applications/System
License:          BSD and MIT and ASL 2.0 and LGPLv2 and GPLv2
URL:              https://github.com/omniti-labs/reconnoiter
# COMMIT=%{commit} curl -sL "https://github.com/omniti-labs/reconnoiter/tarball/%{COMMIT}" > "omniti-labs-reconnoiter-${COMMIT}.tar.gz"
Source0:          omniti-labs-reconnoiter-%{commit}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    apr-devel
BuildRequires:    apr-util-devel
BuildRequires:    autoconf
BuildRequires:    java-devel
BuildRequires:    libssh2-devel
BuildRequires:    libtermcap-devel
BuildRequires:    libuuid-devel
BuildRequires:    libxslt-devel
BuildRequires:    ncurses-devel
BuildRequires:    net-snmp-devel
BuildRequires:    openldap-devel
BuildRequires:    openssl-devel
BuildRequires:    pcre-devel
BuildRequires:    postgresql-devel
BuildRequires:    protobuf-c-devel
BuildRequires:    udns-devel
BuildRequires:    uuid-devel
BuildRequires:    zlib-devel

%description
Reconnoiter is a monitoring and trend analysis system designed to cope with
large architectures (thousands of machines and hundreds of thousands of
metrics).

Heavy focus is placed on decoupling the various components of the system to
allow for disjoint evolution of each component as issues arise or new
requirements are identified. Resource monitoring, metric aggregation, metric
analysis and visualization are all cleanly separated.

%package     -n noitd
Summary:        Reconnoiter monitor
Group:          Applications/System

%description -n noitd
The monitor, noitd, is written in C and designed to support highly concurrent
and rapid checks with an expected capability of monitoring 100,000 services per
minute (6 million checks per hour.) While it is hard to make writing checks
"easy" in this high-performance environment, efforts have been made to ensure
that custom check scripting does not require the expertise of writing
highly-concurrent, event-driven C code. Instead, glue is provided via scripting
languages such as Lua that attempt to handle aspects of this high-concurrency
environment transparently. As with any high-performance system, you can easily
introduce non-performant code and jeopardize performance system-wide.

%package     -n noitd-devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       noitd = %{version}-%{release}

%description -n noitd-devel
The monitor, noitd, is written in C and designed to support highly concurrent
and rapid checks with an expected capability of monitoring 100,000 services per
minute (6 million checks per hour.)

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package     -n stratcond
Summary:        Reconnoiter aggregator
Group:          Applications/System

%description -n stratcond
The aggregator, stratcond, is also written in C and responsible for the simple
task of securely gathering data from all of the distributed noitd instances and
transforming them into the data storage facility (currently PostgreSQL).

The data storage facility (PostgreSQL) holds all information about individual
checks, their statuses and the individual metrics associated with them.
Automatic processes are in place that summarize the numeric metrics into
windowed averages for expedient graphing at a variety of time window
resolutions (hour, day, month, year, etc.).

%package     -n stratcond-devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       stratcond = %{version}-%{release}

%description -n stratcond-devel
The aggregator, stratcond, is also written in C and responsible for the simple
task of securely gathering data from all of the distributed noitd instances and
transforming them into the data storage facility (currently PostgreSQL).

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n omniti-labs-reconnoiter-%{commit}

%build
autoconf
export LDFLAGS="$LDFLAGS -ldl"
%configure
make %{?_smp_mflags}

%install
rm -fr %{buildroot}
make DESTDIR=%{buildroot} install

mv %{buildroot}%{_sysconfdir}/noit.conf.sample \
   %{buildroot}%{_sysconfdir}/noit.conf

mv %{buildroot}%{_sysconfdir}/stratcon.conf.sample \
   %{buildroot}%{_sysconfdir}/stratcon.conf

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README.md

%files -n noitd
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/noit.conf
%config(noreplace) %{_sysconfdir}/config_templates.conf
%{_bindir}/noit*
%{_libexecdir}/noit
%{_mandir}/man8/noitd.8*
%{_sbindir}/noitd
%{_localstatedir}/db/noit-iep/log4j.xml
%{_bindir}/run-iep.sh

%files -n noitd-devel
%defattr(-,root,root,-)
%doc LICENSE
%{_includedir}/noit_*.h
%{_includedir}/noitedit
%{_includedir}/utils/noit_*.h

%files -n stratcond
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/default-ca-chain.crt
%config(noreplace) %{_sysconfdir}/stratcon.conf
%{_bindir}/jezebel
%{_datarootdir}/reconnoiter/crontab
%{_datarootdir}/reconnoiter/schema.sql
%{_mandir}/man8/stratcond.8.gz
%{_prefix}/java/activemq-all-5.2.0.jar
%{_prefix}/java/antlr-runtime-3.1.1.jar
%{_prefix}/java/cglib-nodep-2.2.jar
%{_prefix}/java/commons-cli-1.1.jar
%{_prefix}/java/commons-codec-1.5.jar
%{_prefix}/java/commons-dbcp-1.2.2.jar
%{_prefix}/java/commons-io-1.2.jar
%{_prefix}/java/commons-logging-1.1.1.jar
%{_prefix}/java/commons-pool-1.4.jar
%{_prefix}/java/esper-4.5.0.jar
%{_prefix}/java/jetty-6.1.20.jar
%{_prefix}/java/jetty-util-6.1.20.jar
%{_prefix}/java/jezebel.jar
%{_prefix}/java/log4j-1.2.15.jar
%{_prefix}/java/postgresql-8.3-604.jdbc3.jar
%{_prefix}/java/protobuf-java-2.4.1.jar
%{_prefix}/java/rabbitmq-client-2.4.1.jar
%{_prefix}/java/reconnoiter.jar
%{_prefix}/java/servlet-api-2.5-20081211.jar
%{_prefix}/java/spring-beans-2.5.5.jar
%{_prefix}/java/spring-context-2.5.5.jar
%{_sbindir}/stratcond

%files -n stratcond-devel
%defattr(-,root,root,-)
%doc LICENSE
%{_includedir}/eventer/OETS_asn1_helper.h
%{_includedir}/eventer/eventer.h
%{_includedir}/eventer/eventer_POSIX_fd_opset.h
%{_includedir}/eventer/eventer_SSL_fd_opset.h
%{_includedir}/eventer/eventer_jobq.h
%{_includedir}/jlog/jlog.h
%{_includedir}/jlog/jlog_config.h
%{_includedir}/jlog/jlog_hash.h
%{_includedir}/jlog/jlog_io.h
%{_includedir}/stratcon_datastore.h
%{_includedir}/stratcon_iep.h
%{_includedir}/stratcon_jlog_streamer.h
%{_includedir}/stratcon_realtime_http.h

%changelog
* Tue May 22 2012 Silas Sewell <silas@sewell.org> - 0.-1.960593b
- Initial package
