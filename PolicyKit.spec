# TODO:
# - add init scripts
%define	snap	20061203
Summary:	A framework for defining policy for system-wide components
Name:		PolicyKit
Version:	0.1
Release:	0.%{snap}.1
Group:		Libraries
URL:		http://webcvs.freedesktop.org/hal/
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	3eca471796753a36ee46495907d41525
License:	GPL
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel >= 0.60
BuildRequires:	glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	pam-devel >= 0.80
BuildRequires:	xmlto
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

%package devel
Summary:	Devel package for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

This package contains header files need for development.

%package static
Summary:	Static libraries package for %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

This package contains static libraries and header files need for
development.


%prep
%setup -q -n %{name}

%build
./autogen.sh
%configure \
	--with-pam-module-dir=/%{_lib}/security
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_var}/run/polkit-console

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README doc/spec/*.{html,png,dia} doc/TODO
%attr(755,root,root) %{_bindir}/polkit-*
%attr(755,root,root) %{_sbindir}/polkitd
%{_sysconfdir}/PolicyKit
%{_sysconfdir}/dbus-1/system.d/PolicyKit.conf
/etc/pam.d/policy-kit
%attr(755,root,root) /%{_lib}/security/pam_polkit_console.*
%attr(755,root,root) %{_libdir}/libpolkit-grant.so.*
%attr(755,root,root) %{_libdir}/libpolkit.so.*
%dir %{_var}/run/polkit-console

%files devel
%defattr(644,root,root,755)
%{_includedir}/libpolkit
%{_pkgconfigdir}/*.pc
%{_libdir}/libpol*.la
%attr(755,root,root) %{_libdir}/libpol*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libpol*.a
