# TODO: package bash-completion in proper way
Summary:	A framework for defining policy for system-wide components
Summary(pl.UTF-8):	Szkielet do definiowania polityki dla komponentów systemowych
Name:		PolicyKit
Version:	0.9
Release:	4
License:	MIT
Group:		Libraries
Source0:	http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	802fd13ae41f73d79359e5ecb0a98716
URL:		http://www.freedesktop.org/wiki/Software/PolicyKit
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.7
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.73
BuildRequires:	expat-devel >= 1:1.95.8
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk-doc >= 1.3
BuildRequires:	libselinux-devel >= 1.30
BuildRequires:	libtool
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires(triggerpostun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ConsoleKit >= 0.4.1
Requires:	dbus >= 1.1.2-5
Provides:	group(polkituser)
Provides:	user(polkituser)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
PolicyKit is a framework for defining policy for system-wide
components and for desktop pieces to configure it. It is used by HAL.

%description -l pl.UTF-8
PolicyKit to szkielet do definiowania polityki dla komponentów
systemowych oraz składników pulpitu do konfigurowania ich. Jest
używany przez HAL-a.

%package apidocs
Summary:	PolicyKit API documentation
Summary(pl.UTF-8):	Dokumentacja API PolicyKit
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
PolicyKit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API PolicyKit.

%package libs
Summary:	PolicyKit libraries
Summary(pl.UTF-8):	Biblioteki PolicyKit
Group:		Libraries
Requires:	dbus-libs >= 1.0
Requires:	glib2 >= 1:2.6.0
Conflicts:	PolicyKit < 0.1-0.20061203.6

%description libs
PolicyKit libraries.

%description libs -l pl.UTF-8
Biblioteki PolicyKit.

%package devel
Summary:	Header files for PolicyKit
Summary(pl.UTF-8):	Pliki nagłówkowe PolicyKit
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	expat-devel >= 1:1.95.8
# polkit-grant
#Requires:	glib2-devel >= 1:2.6.0
# polkit-dbus and polkit-grant
#Requires:	dbus-devel >= 1.0
# polkit-dbus
#Requires:	libselinux-devel >= 1.30

%description devel
Header files for PolicyKit.

%description devel -l pl.UTF-8
Pliki nagłówkowe PolicyKit.

%package static
Summary:	Static PolicyKit libraries
Summary(pl.UTF-8):	Statyczne biblioteki PolicyKit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PolicyKit libraries.

%description static -l pl.UTF-8
Statyczne biblioteki PolicyKit.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir} \
	--with-pam-include=system-auth \
	--with-pam-module-dir=/%{_lib}/security
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/PolicyKit/modules/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerun -- PolicyKit < 0.3
%service -q PolicyKit stop
/sbin/chkconfig --del PolicyKit

%pre
%groupadd -g 220 polkituser
%useradd -u 220 -d %{_datadir}/empty -c "PolicyKit User" -g polkituser polkituser

%post
umask 022
touch /var/lib/misc/PolicyKit.reload
chown polkituser:polkituser /var/lib/misc/PolicyKit.reload
chmod 775 /var/lib/misc/PolicyKit.reload

%postun
if [ "$1" = "0" ]; then
	%userremove polkituser
	%groupremove polkituser
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README doc/TODO
%attr(755,root,root) %{_bindir}/polkit-action
%attr(755,root,root) %{_bindir}/polkit-auth
%attr(755,root,root) %{_bindir}/polkit-config-file-validate
%attr(755,root,root) %{_bindir}/polkit-policy-file-validate
%dir %{_libexecdir}
%attr(2755,root,polkituser) %{_libexecdir}/polkit-explicit-grant-helper
%attr(2755,root,polkituser) %{_libexecdir}/polkit-grant-helper
%attr(4754,root,polkituser) %{_libexecdir}/polkit-grant-helper-pam
%attr(2755,root,polkituser) %{_libexecdir}/polkit-read-auth-helper
%attr(4755,root,polkituser) %{_libexecdir}/polkit-resolve-exe-helper
%attr(2755,root,polkituser) %{_libexecdir}/polkit-revoke-helper
%attr(4755,polkituser,root) %{_libexecdir}/polkit-set-default-helper
%attr(755,root,root) %{_libexecdir}/polkitd
%dir %{_sysconfdir}/PolicyKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PolicyKit/PolicyKit.conf
/etc/dbus-1/system.d/org.freedesktop.PolicyKit.conf
/etc/pam.d/polkit
%{_datadir}/PolicyKit
%{_datadir}/dbus-1/interfaces/org.freedesktop.PolicyKit.AuthenticationAgent.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.PolicyKit.service
%attr(775,polkituser,polkituser) %ghost /var/lib/misc/PolicyKit.reload
%attr(770,root,polkituser) /var/lib/PolicyKit
%attr(755,polkituser,root) /var/lib/PolicyKit-public
%attr(770,root,polkituser) /var/run/PolicyKit
%{_mandir}/man1/polkit-action.1*
%{_mandir}/man1/polkit-auth.1*
%{_mandir}/man1/polkit-config-file-validate.1*
%{_mandir}/man1/polkit-policy-file-validate.1*
%{_mandir}/man5/PolicyKit.conf.5*
%{_mandir}/man8/PolicyKit.8*

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/polkit

%files libs
%defattr(644,root,root,755)
# notes which license applies to which package part, AFL text (and GPL text copy)
%doc COPYING
%attr(755,root,root) %{_libdir}/libpolkit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit.so.2
%attr(755,root,root) %{_libdir}/libpolkit-dbus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit-dbus.so.2
%attr(755,root,root) %{_libdir}/libpolkit-grant.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolkit-grant.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpolkit.so
%attr(755,root,root) %{_libdir}/libpolkit-dbus.so
%attr(755,root,root) %{_libdir}/libpolkit-grant.so
%{_libdir}/libpolkit.la
%{_libdir}/libpolkit-dbus.la
%{_libdir}/libpolkit-grant.la
%{_includedir}/PolicyKit
%{_pkgconfigdir}/polkit.pc
%{_pkgconfigdir}/polkit-dbus.pc
%{_pkgconfigdir}/polkit-grant.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpolkit.a
%{_libdir}/libpolkit-dbus.a
%{_libdir}/libpolkit-grant.a
