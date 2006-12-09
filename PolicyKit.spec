# TODO:
# - polkit user/group
%define	snap	20061203
Summary:	A framework for defining policy for system-wide components
Summary(pl):	Szkielet do definiowania polityki dla komponentów systemowych
Name:		PolicyKit
Version:	0.1
Release:	0.%{snap}.6
License:	GPL v2
Group:		Libraries
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	3eca471796753a36ee46495907d41525
Source1:	%{name}.init
Patch0:		%{name}-conf.patch
URL:		http://webcvs.freedesktop.org/hal/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	dbus-devel >= 0.60
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libtool
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-libs >= 0.60
Requires:	glib2 >= 1:2.6.0
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

%description -l pl
PolicyKit to szkielet do definiowania polityki dla komponentów
systemowych oraz sk³adników pulpitu do konfigurowania ich. Jest
u¿ywany przez HAL-a.

%package libs
Summary:	PolicyKit libraries
Summary(pl):	Biblioteki PolicyKit
License:	AFL v2.1 or GPL v2
Group:		Libraries
Conflicts:	PolicyKit < 0.1-0.20061203.6

%description libs
PolicyKit libraries.

%description libs -l pl
Biblioteki PolicyKit.

%package devel
Summary:	Header files for PolicyKit
Summary(pl):	Pliki nag³ówkowe PolicyKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for PolicyKit.

%description devel -l pl
Pliki nag³ówkowe PolicyKit.

%package static
Summary:	Static PolicyKit libraries
Summary(pl):	Statyczne biblioteki PolicyKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PolicyKit libraries.

%description static -l pl
Statyczne biblioteki PolicyKit.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir} \
	--with-pam-module-dir=/%{_lib}/security
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_var}/run/polkit-console,/etc/rc.d/init.d}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/PolicyKit

rm -f $RPM_BUILD_ROOT/%{_lib}/security/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add PolicyKit
%service PolicyKit restart

%preun
if [ "$1" = "0" ]; then
	%service -q PolicyKit stop
	/sbin/chkconfig --del PolicyKit
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README doc/spec/*.{html,png,dia} doc/TODO
%attr(755,root,root) %{_bindir}/polkit-*
%attr(755,root,root) %{_sbindir}/polkitd
%attr(755,root,root) /%{_lib}/security/pam_polkit_console.so*
%{_sysconfdir}/PolicyKit
%{_sysconfdir}/dbus-1/system.d/PolicyKit.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/policy-kit
%dir %{_var}/run/polkit-console
%attr(754,root,root) /etc/rc.d/init.d/*

%files libs
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_libdir}/libpolkit-grant.so.*.*.*
%attr(755,root,root) %{_libdir}/libpolkit.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpolkit*.so
%{_libdir}/libpolkit*.la
%{_includedir}/libpolkit
%{_pkgconfigdir}/polkit.pc
%{_gtkdocdir}/polkit

%files static
%defattr(644,root,root,755)
%{_libdir}/libpolkit*.a
