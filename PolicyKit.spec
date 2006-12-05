%define	snap	20061203
Summary:	A framework for defining policy for system-wide components
Summary(pl):	Szkielet do definiowania polityki dla komponentów systemowych
Name:		PolicyKit
Version:	0.1
Release:	0.%{snap}.2
License:	GPL
Group:		Libraries
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	3eca471796753a36ee46495907d41525
Source1:	%{name}.init
URL:		http://webcvs.freedesktop.org/hal/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel >= 0.60
BuildRequires:	glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	pam-devel >= 0.80
BuildRequires:	xmlto
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

%description -l pl
PolicyKit to szkielet do definiowania polityki dla komponentów
systemowych oraz sk³adników pulpitu do konfigurowania ich. Jest
u¿ywany przez HAL-a.

%package devel
Summary:	Header files for PolicyKit
Summary(pl):	Pliki nag³ówkowe PolicyKit
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for PolicyKit.

%description devel -l pl
Pliki nag³ówkowe PolicyKit.

%package static
Summary:	Static PolicyKit libraries
Summary(pl):	Statyczne biblioteki PolicyKit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PolicyKit libraries.

%description static -l pl
Statyczne biblioteki PolicyKit.

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

install -d $RPM_BUILD_ROOT{%{_var}/run/polkit-console,/etc/rc.d/init.d}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/PolicyKit

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = "0" ]; then
	%service -q PolicyKit stop
	/sbin/chkconfig --del PolicyKit
fi

%post
/sbin/ldconfig
/sbin/chkconfig --add PolicyKit
%service PolicyKit restart

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README doc/spec/*.{html,png,dia} doc/TODO
%attr(755,root,root) %{_bindir}/polkit-*
%attr(755,root,root) %{_sbindir}/polkitd
%attr(755,root,root) %{_libdir}/libpolkit-grant.so.*.*.*
%attr(755,root,root) %{_libdir}/libpolkit.so.*.*.*
%attr(755,root,root) /%{_lib}/security/pam_polkit_console.so*
%{_sysconfdir}/PolicyKit
%{_sysconfdir}/dbus-1/system.d/PolicyKit.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/policy-kit
%dir %{_var}/run/polkit-console
%attr(754,root,root) /etc/rc.d/init.d/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpol*.so
%{_libdir}/libpol*.la
%{_includedir}/libpolkit
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpol*.a
