%define vendor_name Avago
%define vendor_label avago
%define driver_name mpt3sas

# XCP-ng: install to the override directory
%define module_dir override

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}-alt
Version: 38.00.00.00
Release: 1.1%{?dist}
License: GPL

# Extracted from latest XS driver disk
Source0: avago-mpt3sas-38.00.00.00.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{vendor_label}-%{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
# The installed by default avago-mpt3sas RPM already provides the configuration file, so we don't include it here.
#%{__install} -d %{buildroot}%{_sysconfdir}/modprobe.d
#echo 'options mpt3sas prot_mask=0x07' > %{driver_name}.conf
#%{__install} %{driver_name}.conf %{buildroot}%{_sysconfdir}/modprobe.d
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
#%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Wed Sep 20 2023 Gael Duperrey <gduperrey@vates.tech> - 38.00.00.00-1.1
- initial package, version 38.00.00.00-1.1
- Synced from XS driver SRPM avago-mpt3sas-38.00.00.00-1.el7.centos.src.rpm
