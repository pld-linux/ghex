Summary:	GNOME2 binary editor
Summary(pl.UTF-8):	Edytor binarny dla GNOME2
Name:		ghex
Version:	2.22.0
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ghex/2.22/%{name}-%{version}.tar.bz2
# Source0-md5:	6f1ee7a56f7dd04bfba5ee74a639948a
Patch0:		%{name}-desktop.patch
URL:		http://www.gnu.org/directory/text/editors/ghex.html
BuildRequires:	GConf2-devel >= 2.20.0
BuildRequires:	atk-devel >= 1:1.22.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gail-devel >= 1.22.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gtk+2-devel >= 2:2.12.9
BuildRequires:	intltool >= 0.36.1
BuildRequires:	libgnomeprintui-devel >= 2.18.0
BuildRequires:	libgnomeui-devel >= 2.22.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
# sr@Latn vs. sr@latin
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

%package devel
Summary:	GHex devel files
Summary(pl.UTF-8):	Pliki nagłówkowe GHex
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	atk-devel >= 1:1.22.0
Requires:	gail-devel >= 1.22.0
Requires:	gtk+2-devel >= 2:2.12.9

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

%prep
%setup -q
%patch0 -p1

sed -i -e 's#sr@Latn#sr@latin#' po/LINGUAS
mv po/sr@{Latn,latin}.po

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-install
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install ghex2.schemas
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall ghex2.schemas

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/ghex2
%attr(755,root,root) %{_libdir}/libgtkhex.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtkhex.so.0
%{_desktopdir}/ghex.desktop
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/gnome-2.0/ui/*
%{_sysconfdir}/gconf/schemas/ghex2.schemas

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex.so
%{_libdir}/libgtkhex.la
%{_includedir}/gtkhex
%{_pkgconfigdir}/gtkhex.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtkhex.a
