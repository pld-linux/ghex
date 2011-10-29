Summary:	GNOME2 binary editor
Summary(pl.UTF-8):	Edytor binarny dla GNOME2
Name:		ghex
Version:	3.0.0
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://ftp.gnome.org/pub/GNOME/sources/ghex/3.0/%{name}-%{version}.tar.xz
# Source0-md5:	ffa346d6fa97b9e787680159a5479b84
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-static.patch
URL:		http://www.gnu.org/directory/text/editors/ghex.html
BuildRequires:	atk-devel >= 1:1.22.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils >= 0.12.0
BuildRequires:	gtk+3-devel
BuildRequires:	intltool >= 0.36.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GHex allows the user to load data from any file, view and edit it in
either hex or ascii. A must for anyone playing games that use
non-ascii format for saving.

%description -l pl.UTF-8
GHex pozwala użytkownikowi na wczytanie danych z dowolnego pliku,
przeglądanie i edycję ich w trybie szesnastkowym i ASCII.
Obowiązkowe narzędzie dla wszystkich graczy, których gry zapisują
stan w formacie innym niż tekstowy.

%package devel
Summary:	GHex devel files
Summary(pl.UTF-8):	Pliki nagłówkowe GHex
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	atk-devel >= 1:1.22.0
Requires:	gtk+3-devel

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
%patch1 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_icon_cache hicolor
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/ghex
%attr(755,root,root) %{_libdir}/libgtkhex-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtkhex-3.so.0
%{_datadir}/GConf/gsettings/ghex.convert
%{_datadir}/glib-2.0/schemas/org.gnome.GHex.gschema.xml
%{_desktopdir}/ghex.desktop
%{_iconsdir}/hicolor/*/*/*
%{_datadir}/ghex/ghex-ui.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex-3.so
%{_libdir}/libgtkhex-3.la
%{_includedir}/gtkhex-3
%{_pkgconfigdir}/gtkhex-3.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtkhex-3.a
