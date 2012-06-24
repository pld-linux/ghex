Summary:	GNOME2 binary editor
Summary(pl):	Edytor binarny dla GNOME2
Name:		ghex
Version:	2.3.0
Release:	1
Group:		Applications/Editors
License:	GPL
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/ghex/2.3/%{name}-%{version}.tar.bz2
Patch0:		%{name}-schema.patch
URL:		http://pluton.ijs.si/~jaka/gnome.html#GHEX
Requires(post):	/usr/bin/scrollkeeper-update
Requires(post):	GConf2
BuildRequires:	gtk+2-devel 
BuildRequires:	libgnomeprint-devel >= 2.2.0
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GHex allows the user to load data from any file, view and edit it in
either hex or ascii. A must for anyone playing games that use
non-ascii format for saving.

%description -l pl
GHex pozwala u�ytkownikowi na wczytanie danych z dowolnego pliku,
przegl�danie i edycj� ich w trybie szesnastkowym i ASCII. Obowi�zkowe
narz�dzie dla wszystkich graczy, kt�rych gry zapisuj� stan w formacie
innym ni� tekstowy.

%package devel
Summary:	GHex devel files
Summary(pl):	Pliki nag��wkowe GHex
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
GHex devel files

%description devel -l pl
Pliki nag��wkowe GHex

%package static
Summary:	GHex static lib
Summary(pl):	Biblioteka statyczna GHex
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
GHex static lib

%description static -l pl
Biblioteka statyczna GHex

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/scrollkeeper-update
%gconf_schema_install
/sbin/ldconfig

%postun -p /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libgtkhex.so.*.*.*
%{_datadir}/applications/*
%{_pixmapsdir}/*
%{_datadir}/gnome-2.0/ui/*
%{_sysconfdir}/gconf/schemas/*
%{_omf_dest_dir}/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}
%{_libdir}/libgtkhex.so
%{_libdir}/libgtkhex.la
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
