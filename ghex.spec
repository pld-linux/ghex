# TODO: use gtk4-update-icon-cache
#
# Conditional build:
%bcond_without	apidocs		# API documentation

Summary:	GNOME binary editor
Summary(pl.UTF-8):	Edytor binarny dla GNOME
Name:		ghex
Version:	42.3
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	https://download.gnome.org/sources/ghex/42/%{name}-%{version}.tar.xz
# Source0-md5:	4c08a5ea634c4f989aa79509ef0de3c7
Patch0:		%{name}-no-update.patch
URL:		https://wiki.gnome.org/Apps/Ghex
BuildRequires:	gettext-tools
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.66.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk4-devel >= 4.0.0
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.66.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GHex allows the user to load data from any file, view and edit it in
either hex or ascii. A must for anyone playing games that use
non-ascii format for saving.

%description -l pl.UTF-8
GHex pozwala użytkownikowi na wczytanie danych z dowolnego pliku,
przeglądanie i edycję ich w trybie szesnastkowym i ASCII. Obowiązkowe
narzędzie dla wszystkich graczy, których gry zapisują stan w formacie
innym niż tekstowy.

%package libs
Summary:	GHex library
Summary(pl.UTF-8):	Biblioteka GHex
Group:		X11/Libraries
Requires:	glib2 >= 1:2.66.0
Requires:	gtk4 >= 4.0.0

%description libs
GHex library.

%description libs -l pl.UTF-8
Biblioteka GHex.

%package devel
Summary:	GHex devel files
Summary(pl.UTF-8):	Pliki nagłówkowe GHex
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk4-devel >= 4.0.0

%description devel
GHex devel files.

%description devel -l pl.UTF-8
Pliki nagłówkowe GHex.

%package static
Summary:	GHex static library
Summary(pl.UTF-8):	Biblioteka statyczna GHex
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GHex static library.

%description static -l pl.UTF-8
Biblioteka statyczna GHex.

%package apidocs
Summary:	API documentation for GHex library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GHex
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for GHex library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GHex.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/gtkhex-4.0 $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/ghex
%dir %{_libdir}/gtkhex-4.0
%attr(755,root,root) %{_libdir}/gtkhex-4.0/libhex-buffer-mmap.so
%{_datadir}/glib-2.0/schemas/org.gnome.GHex.gschema.xml
%{_datadir}/metainfo/org.gnome.GHex.appdata.xml
%{_desktopdir}/org.gnome.GHex.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.GHex.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.GHex.Devel.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.GHex-symbolic.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex-4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtkhex-4.so.0
%{_libdir}/girepository-1.0/Hex-4.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex-4.so
%{_includedir}/gtkhex-4
%{_datadir}/gir-1.0/Hex-4.gir
%{_pkgconfigdir}/gtkhex-4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtkhex-4.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gtkhex-4.0
%endif
