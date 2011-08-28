Name:		usbmuxd
Version:	1.0.2
Release:	1%{?dist}
Summary:	Daemon for communicating with Apple's iPod Touch and iPhone

Group:		Applications/System
# All code is dual licenses as GPLv3+ or GPLv2+, except libusbmuxd which is LGPLv2+.
License:	GPLv3+ or GPLv2+ and LGPLv2+
URL:		http://marcansoft.com/uploads/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:	http://marcansoft.com/uploads/usbmuxd/%{name}-%{version}.tar.bz2
Patch0:		usbmuxd-udevuser.patch

ExcludeArch:	s390
ExcludeArch:	s390x

BuildRequires:	libusb1-devel
BuildRequires:	cmake
Requires(pre): shadow-utils

%description
usbmuxd is a daemon used for communicating with Apple's iPod Touch and iPhone
devices. It allows multiple services on the device to be accessed
simultaneously.

%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: usbmuxd = %{version}-%{release}
Requires: pkgconfig
Requires: libusb1-devel

%description devel
Files for development with %{name}.

%prep
%setup -q
%patch0 -p1 -b .udevuser

%build
export CMAKE_PREFIX_PATH=/usr
%{cmake} .

make %{?_smp_mflags}

%install
export CMAKE_PREFIX_PATH=/usr$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group usbmuxd >/dev/null || groupadd -r usbmuxd -g 113
getent passwd usbmuxd >/dev/null || \
useradd -r -g usbmuxd -d / -s /sbin/nologin \
	-c "usbmuxd user" -u 113 usbmuxd
exit 0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS README COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1 README.devel
/lib/udev/rules.d/85-usbmuxd.rules
%{_bindir}/iproxy
%{_sbindir}/usbmuxd
%{_libdir}/libusbmuxd.so.*

%files devel
%defattr(-,root,root,-)
%doc README.devel
%{_includedir}/*.h
%{_libdir}/libusbmuxd.so
%{_libdir}/pkgconfig/libusbmuxd.pc

%changelog
* Tue Feb 09 2010 Bastien Nocera <bnocera@redhat.com> 1.0.2-1
- Update to usbmuxd 1.0.2
- Add ExcludeArch for s390, no USB support there
Related: rhbz#563159

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.1.4-2.1
- Rebuilt for RHEL 6

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 0.1.4-2
- Make usbmuxd autostart on newer kernels
- (Still doesn't exit properly though)

* Mon Aug 10 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.4-1
- Update to 0.1.4

* Tue Aug  4 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.3-1
- Update to 0.1.3, review input

* Mon Aug  3 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.2-1
- Update to 0.1.2

* Mon Aug  3 2009 Peter Robinson <pbrobinson@gmail.com> 0.1.1-1
- Initial packaging
