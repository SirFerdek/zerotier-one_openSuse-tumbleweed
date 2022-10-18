Name:           zerotier-one
Version:        1.6.2
Release:        1%{?dist}
Summary:        ZeroTier network virtualization service

License:        BUSL-1.1
URL:            https://www.zerotier.com
Source0:        https://github.com/zerotier/ZeroTierOne/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-user.conf

BuildRequires:  systemd-rpm-macros gcc-c++ clang sysuser-tools
%sysusers_requires
Requires:       iproute

%description
ZeroTier One allows systems to join and participate in ZeroTier virtual networks.

%prep
%setup -q -n %{name}-%{version}

%build
make LDFLAGS="-pie -Wl,-z,relro,-z,now -Wl,-z,noexecstack" ZT_USE_MINIUPNPC=1 %{?_smp_mflags} one
%sysusers_generate_pre %{SOURCE1} %{name}

%install
%make_install
mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 debian/zerotier-one.service %{buildroot}%{_unitdir}/%{name}.service
ln -s %{_sbindir}/service %{buildroot}%{_sbindir}/rczerotier-one

mkdir -p %{buildroot}%{_sysusersdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/

%files
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}-user.conf
# compatibility symlinks to binaries
%dir %{_sharedstatedir}/%{name}
%{_sharedstatedir}/%{name}/*
%doc AUTHORS.md README.md
%license COPYING

%pre -f %{name}.pre
%service_add_pre zerotier-one.service

%post
%service_add_post zerotier-one.service

%preun
%service_del_preun zerotier-one.service

%postun
%service_del_postun zerotier-one.service

%changelog
