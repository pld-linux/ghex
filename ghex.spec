Summary:	GNOME2 binary editor
Summary(pl):	Edytor binarny dla GNOME2
Name:		ghex
Version:	2.6.1
Release:	1
Group:		Applications/Editors
License:	GPL
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.6/%{name}-%{version}.tar.bz2
# Source0-md5:	fce2cb6f26c2082a9dc2687e504dc6c6
Patch0:		%{name}-schema.patch
Patch1:		%{name}-locale-names.patch
URL:		http://www.gnu.org/directory/text/editors/ghex.html
BuildRequires:	GConf2-devel >= 2.6.1
BuildRequires:	atk-devel >= 1.6.1
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gail-devel >= 1.6.5
BuildRequires:	gtk+2-devel >= 2:2.4.1
BuildRequires:	intltool >= 0.30
BuildRequires:	libglade2-devel >= 1:2.4.0
BuildRequires:	libgnomeui-devel >= 2.6.1
BuildRequires:	libgnomeprintui-devel >= 2.6.1
BuildRequires:	libtool
BuildRequires:	popt-devel
BuildRequires:	scrollkeeper
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GHex allows the user to load data from any file, view and edit it in
either hex or ascii. A must for anyone playing games that use
non-ascii format for saving.

%description -l pl
GHex pozwala u¿ytkownikowi na wczytanie danych z dowolnego pliku,
przegl±danie i edycjê ich w trybie szesnastkowym i ASCII. Obowi±zkowe
narzêdzie dla wszystkich graczy, których gry zapisuj± stan w formacie
innym ni¿ tekstowy.

%package devel
Summary:	GHex devel files
Summary(pl):	Pliki nag³ówkowe GHex
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gail-devel >= 1.6.5
Requires:	gtk+2-devel >= 2:2.4.1

%description devel
GHex devel files.

%description devel -l pl
Pliki nag³ówkowe GHex.

%package static
Summary:	GHex static library
Summary(pl):	Biblioteka statyczna GHex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GHex static library.

%description static -l pl
Biblioteka statyczna GHex.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

mv po/{no,nb}.po

%build
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal}
%{__autoconf}
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
/usr/bin/scrollkeeper-update
%gconf_schema_install

%postun
/sbin/ldconfig
/usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libgtkhex.so.*.*.*
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_datadir}/gnome-2.0/ui/*
%{_sysconfdir}/gconf/schemas/*
%{_omf_dest_dir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkhex.so
%{_libdir}/libgtkhex.la
%{_includedir}/*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
