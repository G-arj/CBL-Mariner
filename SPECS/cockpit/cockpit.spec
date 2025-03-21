Summary:        A package to provide cockpit for mariner
Name:           cockpit
Version:        248
Release:        1%{?dist}
License:        LGPLv2+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/cockpit-project/cockpit
Source0:        https://github.com/cockpit-project/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  python3
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  e2fsprogs-devel
BuildRequires:  gcc
BuildRequires:  gettext >= 0.19.7
BuildRequires:  glib-devel
BuildRequires:  glib-networking
BuildRequires:  gnutls-devel >= 3.4.3
BuildRequires:  json-glib-devel
BuildRequires:  krb5-devel >= 1.11
BuildRequires:  libssh-devel >= 0.8.5
BuildRequires:  make
BuildRequires:  openssh
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  polkit-devel
BuildRequires:  sed
BuildRequires:  sudo
BuildRequires:  systemd-devel >= 235
BuildRequires:  which
BuildRequires:  zlib-devel

%description
cockpit for mariner

%prep
%setup -q
mkdir -p %{buildroot}%{_sysconfdir}/pam.d

%build
./configure --sysconfdir=%{_sysconfdir} --prefix=%{_prefix} --disable-pcp --disable-doc
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
cat > %{buildroot}%{_sysconfdir}/pam.d/cockpit << EOF
    #%PAM-1.0
    # this MUST be first in the "auth" stack as it sets PAM_USER
    # user_unknown is definitive, so die instead of ignore to avoid subsequent modules mess up the error code
    -auth      [success=done new_authtok_reqd=done user_unknown=die default=ignore]   pam_cockpit_cert.so
    auth       substack     system-auth
    auth       optional     pam_ssh_add.so
    account    required     pam_nologin.so
    account    include      system-account
    password   include      system-password
    session    required     pam_loginuid.so
    session    optional     pam_keyinit.so force revoke
    session    optional     pam_ssh_add.so
    session    include      system-session
EOF
chmod -R go+rx %{buildroot}%{_datadir}/cockpit
chmod o+rx %{buildroot}%{_sysconfdir}/cockpit

%check
# These tests cannot be run as root
chmod g+w . -R
useradd test -G root -m
sudo -u test make check

%files
%license COPYING COPYING.node
%{_datadir}/cockpit
%{_sysconfdir}/cockpit
%{_sysconfdir}/pam.d/cockpit
%{_datadir}/metainfo/*cockpit*.xml
%{_datadir}/polkit-1/actions/org.cockpit-project.cockpit-bridge.policy
%{_datadir}/pixmaps/cockpit*.png
%{_libdir}/tmpfiles.d/cockpit-tempfiles.conf
/lib/systemd/system/cockpit*.socket
/lib/systemd/system/cockpit*.service
/lib/systemd/system/system-cockpithttps.slice
%{_sysconfdir}/issue.d/cockpit.issue
%{_sysconfdir}/motd.d/cockpit
%{_bindir}/cockpit-bridge
%{_libdir}/security/pam_cockpit_cert.so
%{_libdir}/security/pam_ssh_add.so
%{_libexecdir}/cockpit-*
%{_sbindir}/remotectl
%{_datadir}/locale/ca/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/cs/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/de/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/es/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/fi/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/fr/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/he/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/it/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/ja/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/ko/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/nb_NO/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/nl/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/pl/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/pt_BR/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/ru/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/sk/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/sv/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/tr/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/uk/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/zh_CN/LC_MESSAGES/cockpit.mo
%{_datadir}/locale/zh_TW/LC_MESSAGES/cockpit.mo

%changelog
* Mon Jul 26 2021 Shane Guan <shaneguan@microsoft.com> - 248-1
- Original version for CBL-Mariner.
- License verified.
