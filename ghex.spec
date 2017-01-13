Summary:	GNOME binary editor
Summary(pl.UTF-8):	Edytor binarny dla GNOME
Name:		ghex
Version:	3.18.3
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ghex/3.18/%{name}-%{version}.tar.xz
# Source0-md5:	b17d66b9a52a87684468b06c75c4ba3e
Patch0:		%{name}-desktop.patch
URL:		https://wiki.gnome.org/Apps/Ghex
BuildRequires:	atk-devel >= 1:1.22.0
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gnome-common
BuildRequires:	gtk+3-devel >= 3.4.0
BuildRequires:	intltool >= 0.41.1
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	glib2 >= 1:2.26.0
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
Requires:	atk >= 1:1.22.0
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+3 >= 3.4.0

%description libs
GHex library.

%description libs -l pl.UTF-8
Biblioteka GHex.

%package devel
Summary:	GHex devel files
Summary(pl.UTF-8):	Pliki nagłówkowe GHex
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+3-devel >= 3.4.0

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

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile \
	--disable-silent-rules \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --with-gnome --all-name

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
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/ghex
%{_datadir}/GConf/gsettings/ghex.convert
%{_datadir}/appdata/ghex.appdata.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GHex.gschema.xml
%{_desktopdir}/ghex.desktop
%{_iconsdir}/hicolor/*x*/apps/ghex.png
%{_iconsdir}/hicolor/scalable/apps/ghex-symbolic.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtkhex-3.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex-3.so
%{_includedir}/gtkhex-3
%{_pkgconfigdir}/gtkhex-3.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtkhex-3.a
