Summary:        Open Source Security Compliance Solution
Name:           openscap
Version:        1.3.2
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.open-scap.org
Source0:        https://github.com/OpenSCAP/openscap/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  dbus-devel
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libselinux-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  pcre-devel
BuildRequires:  perl-XML-Parser
BuildRequires:  popt-devel
BuildRequires:  python2-devel
BuildRequires:  rpm-devel
BuildRequires:  swig
BuildRequires:  util-linux-devel
Requires:       curl
Requires:       popt

%description
SCAP is a multi-purpose framework of specifications that supports automated configuration, vulnerability and patch checking, technical control compliance activities, and security measurement.
OpenSCAP has received a NIST certification for its support of SCAP 1.2.

%package devel
Summary:        Development Libraries for openscap
Group:          Development/Libraries
Requires:       libxml2-devel
Requires:       openscap = %{version}-%{release}

%description devel
Header files for doing development with openscap.

%package perl
Summary:        openscap perl scripts
Requires:       openscap = %{version}-%{release}
Requires:       perl

%description perl
Perl scripts.

%package python
Summary:        openscap python
Group:          Development/Libraries
BuildRequires:  python2-devel
Requires:       openscap = %{version}-%{release}

%description python
Python bindings.

%prep
%setup -q
mkdir build

%build
cd build
%cmake -DENABLE_PERL=ON \
       -DENABLE_SCE=ON \
       ..
make %{?_smp_flags}

%install
cd build
%make_install
#make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

#%check
#make check need BuildRequires per-XML-XPATH and bzip2
#no per-XML-XPATH so disable make check
#make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/*
%exclude %{_prefix}/src/debug
%exclude %{_libdir}/debug
%{_bindir}/*
#%{_libexecdir}/*
%{_mandir}/man8/*
%{_datadir}/openscap/*
%{_libdir}/libopenscap_sce.so.*
%{_libdir}/libopenscap.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libopenscap_sce.so
%{_libdir}/libopenscap.so
%{_libdir}/pkgconfig/*

%files perl
%defattr(-,root,root)
%{_libdir}/perl5/*
%{_datadir}/perl5/vendor_perl/openscap_pm.pm

%files python
%defattr(-,root,root)
%{_libdir}/python2.7/*

%changelog
* Mon Oct 18 2021 Chris Co <chrco@microsoft.com> - 1.3.2-1
- Update to 1.3.2 to fix --stig-viewer output

* Thu Oct 07 2021 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.1-4
- Add BuildRequires dbus-devel to support systemd unit module

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.3.1-3
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.3.1-2
-   Renaming XML-Parser to perl-XML-Parser

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.3.1-1
-   Update to 1.3.1. Remove probe directory. License fixed.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.17-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.2.17-1
-   Update to 1.2.17

*   Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.14-3
-   Disable make check which need per-XML-XPATH for bug 1900358

*   Fri May 5 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2.14-2
-   Remove BuildRequires XML-XPath.

*   Mon Mar 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.14-1
-   Update to latest version.

*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-2
-   BuildRequires curl-devel.

*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.10-1
-   Initial build. First version
