Summary:        Fast distributed version control system
Name:           git
Version:        2.33.0
Release:        3%{?dist}
License:        GPLv2
URL:            https://git-scm.com/
Group:          System Environment/Programming
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
BuildRequires:  curl-devel
BuildRequires:  python2
Requires:       openssl
Requires:       curl
Requires:       expat
Requires:       perl-interpreter
Requires:       perl-YAML
Requires:       perl-DBI
Requires:       perl-CGI
Requires:       subversion-perl
Requires:       python2

Provides:       git-core = %{version}-%{release}

%description
Git is a free and open source, distributed version control system
designed to handle everything from small to very large projects with
speed and efficiency. Every Git clone is a full-fledged repository
with complete history and full revision tracking capabilities, not
dependent on network access or a central server. Branching and
merging are fast and easy to do. Git is used for version control of
files, much like tools such as Mercurial, Bazaar,
Subversion-1.7.8, CVS-1.11.23, Perforce, and Team Foundation Server.

%package lang
Summary: Additional language files for git
Group: System Environment/Programming
Requires: git >= 2.1.2
%description lang
These are the additional language files of git.


%global with_daemon 1
%global with_subtree 1
%global with_svn 1
%global with_email 0

%if %{with_daemon}
%package daemon
Summary:        Git protocol daemon
Requires:       git-core = %{version}-%{release}
Requires:       systemd
Requires(post): systemd
Requires(preun):  systemd
Requires(postun): systemd

%description daemon
The git daemon for supporting git:// access to git repositories
%endif


%if %{with_email}
%package email
Summary:        Git tools for sending patches via email
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Net::SMTP::SSL)
%description email
%{summary}.
%endif


%if %{with_subtree}
%package subtree
Summary:        Git tools to merge and split repositories
Requires:       git-core = %{version}-%{release}
%description subtree
Git subtrees allow subprojects to be included within a subdirectory
of the main project, optionally including the subproject's entire
history.
%endif


%if %{with_svn}
%package svn
Summary:        Git tools for interacting with Subversion repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Digest::MD5)
Requires:       subversion
%description svn
%{summary}.
%endif

%prep
%setup -q
%build
%configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --libexec=%{_libexecdir} \
    --with-gitconfig=/etc/gitconfig
make %{?_smp_mflags} CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/usr/share/bash-completion/completions
install -m 0644 contrib/completion/git-completion.bash %{buildroot}/usr/share/bash-completion/completions/git
%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} test

%post
if [ $1 -eq 1 ];then
    # This is first installation.
    git config --system http.sslCAPath /etc/ssl/certs
    exit 0
fi

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_datarootdir}/perl5/*
%{_libexecdir}/git-core/*
%{_datarootdir}/git-core/*
%{_datarootdir}/git-gui/*
%{_datarootdir}/gitk/*
%{_datarootdir}/gitweb/*
%{_datarootdir}/bash-completion/

%files lang -f %{name}.lang
%defattr(-,root,root)

%if %{with_daemon}
%files daemon
%{_libexecdir}/git-core/git-daemon
%endif

%if %{with_email}
%files email
%{_libexecdir}/git-core/git-send-email
%endif

%if %{with_subtree}
%files subtree
%{_libexecdir}/git-core/git-merge-subtree
%endif

%if %{with_svn}
%files svn
%{_libexecdir}/git-core/git-svn
%endif

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.33.0-3
- Removing the explicit %%clean stage.
- License verified.

* Fri Sep 03 2021 Muhammad Falak <mwani@microsoft.com> - 2.33.0-2
- Export `daemon`, `subtree` & `svn` subpackages.

* Wed Sep 01 2021 Muhammad Falak <mwani@microsoft.com> - 2.33.0-1
- Bump version 2.23.4 -> 2.33.0

* Wed Apr 07 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.23.4-1
- Update to version 2.23.4 for CVE-2021-21300 fix.

* Mon Oct 19 2020 Andrew Phelps <anphel@microsoft.com> - 2.23.3-4
- Fix check test

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.23.3-2
- Use new perl package names.
- Provide git-core.

* Thu May 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.23.3-1
- Update to version 2.23.3 for fix CVE-2020-11008 and CVE-2020-5260.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.20.2-2
- Added %%license line automatically

* Mon Apr 06 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.20.2-1
- Update to latest version.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.19.0-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.19.0-3
- Added Requires python2

* Thu Oct 04 2018 Dweep Advani <dadvani@vmware.com> - 2.19.0-2
- Using %configure and changing for perl upgrade

* Tue Oct 02 2018 Siju Maliakkal <smaliakkal@vmware.com> - 2.19.0-1
- Update to latest version

* Tue Jul 31 2018 Ajay Kaher <akaher@vmware.com> - 2.14.2-2
- Excluded the perllocal.pod for aarch64.

* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> - 2.14.2-1
- Updated to version 2.14.2, fix CVE-2017-14867

* Mon Aug 21 2017 Rui Gu <ruig@vmware.com> - 2.9.3-4
- Fix make check with non-root mode.

* Wed May 31 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.9.3-3
- Remove python2 from requires.

* Mon Apr 17 2017 Robert Qi <qij@vmware.com> - 2.9.3-2
- Update since perl version got updated.

* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> - 2.9.3-1
- Updated to version 2.9.3

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.8.1-7
- BuildRequires curl-devel.

* Fri Aug 19 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.8.1-6
- Add bash completion file

* Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.8.1-5
- Excluded the perllocal.pod log.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.8.1-4
- GA - Bump release of all rpms

* Wed May 18 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.8.1-3
- Fix if syntax

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> - 2.8.1-2
- Handling the upgrade scenario.

* Fri Apr 15 2016 Anish Swaminathan <anishs@vmware.com> - 2.8.1-1
- Updated to version 2.8.1

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.7.1-1
- Updated to version 2.7.1

* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> - 2.1.2-2
- Add requires for perl-CGI.

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> - 2.1.2-1
- Initial build. First version
