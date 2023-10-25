#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	The FOX 1.6 C++ GUI Toolkit
Summary(pl.UTF-8):	FOX 1.6 - toolkit graficzny w C++
Name:		fox16
Version:	1.6.57
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	http://fox-toolkit.org/ftp/fox-%{version}.tar.gz
# Source0-md5:	675ddeac64eef88d9f7360abaa56b995
Patch0:		%{name}-opt.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-format.patch
URL:		http://www.fox-toolkit.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	bzip2-devel >= 1.0.2
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.5
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel >= 3.5.7
BuildRequires:	libtool >= 2:1.5
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	zlib-devel >= 1.1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FOX is a C++-Based Library for Graphical User Interface Development
FOX supports modern GUI features, such as Drag-and-Drop, Tooltips, Tab
Books, Tree Lists, Icons, Multiple-Document Interfaces (MDI), timers,
idle processing, automatic GUI updating, as well as OpenGL/Mesa for 3D
graphics. Subclassing of basic FOX widgets allows for easy extension
beyond the built-in widgets by application writers.

This package contains FOX 1.6.x series.

%description -l pl.UTF-8
FOX jest biblioteką bazującą na C++ do projektowania graficznych
interfejsów użytkownika. Obsługuje wiele właściwości współczesnych
GUI: Drag-and-Drop, listy, ikony, interfejsy wielodokumentowe (MDI),
liczniki, przetwarzanie w tle, automatyczne uaktualnianie GUI, obsługę
grafiki OpenGL. Bazowe klasy widgetów FOX pozwalają na łatwe
rozszerzanie.

Ten pakiet zawiera FOX z serii 1.6.x.

%package progs
Summary:	FOX 1.6 example applications
Summary(pl.UTF-8):	Przykłady aplikacji wykorzystujących FOX 1.6
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	fox-example-apps < 0.99.173
Obsoletes:	fox-progs < 1.7
Conflicts:	fox-progs >= 1.7

%description progs
Editor and file browser, written with FOX 1.6.

%description progs -l pl.UTF-8
Edytor i przeglądarka plików napisane z użyciem toolkitu FOX 1.6.

%package devel
Summary:	Header files for FOX 1.6 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FOX 1.6
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-GLU-devel
Requires:	bzip2-devel >= 1.0.2
Requires:	libjpeg-devel >= 6b
Requires:	libpng-devel >= 1.2.5
Requires:	libstdc++-devel
Requires:	libtiff-devel >= 3.5.7
Requires:	xorg-lib-libXcursor-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXft-devel
Requires:	xorg-lib-libXrandr-devel
Requires:	zlib-devel >= 1.1.4

%description devel
Header files for FOX 1.6 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FOX 1.6.

%package static
Summary:	FOX 1.6 static libraries
Summary(pl.UTF-8):	Biblioteki statyczne FOX 1.6
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
FOX 1.6 static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne FOX 1.6.

%package doc
Summary:	Development documentation for FOX 1.6 library
Summary(pl.UTF-8):	Dokumentacja programisty do biblioteki FOX 1.6
Group:		X11/Development/Libraries

%description doc
Development documentation for FOX 1.6 library.

%description doc -l pl.UTF-8
Dokumentacja programisty do biblioteki FOX 1.6.

%package examples
Summary:	FOX 1.6 - example programs
Summary(pl.UTF-8):	FOX 1.6 - programy przykładowe
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description examples
FOX 1.6 - example programs.

%description examples -l pl.UTF-8
FOX 1.6 - przykładowe programy.

%prep
%setup -q -n fox-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?debug:--enable-debug}%{!?debug:--enable-release} \
	--enable-static%{!?with_static_libs:=no} \
	--with-opengl \
	--with-xft \
	--with-shape \
	--with-xshm \
	--with-xcursor \
	--with-xrandr \
	--with-xim

%{__make}

%{__make} -C doc docs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C tests clean
cp -a tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

mv -v $RPM_BUILD_ROOT%{_bindir}/fox-config $RPM_BUILD_ROOT%{_bindir}/fox16-config
mv -v $RPM_BUILD_ROOT%{_bindir}/reswrap $RPM_BUILD_ROOT%{_bindir}/reswrap16
mv -v $RPM_BUILD_ROOT%{_mandir}/man1/reswrap.1 $RPM_BUILD_ROOT%{_mandir}/man1/reswrap16.1
mv -v $RPM_BUILD_ROOT%{_pkgconfigdir}/fox.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/fox-1.6.pc

%{__rm} doc/Makefile* doc/*/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE_ADDENDUM README
%attr(755,root,root) %{_libdir}/libCHART-1.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCHART-1.6.so.0
%attr(755,root,root) %{_libdir}/libFOX-1.6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libFOX-1.6.so.0

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Adie.stx
%attr(755,root,root) %{_bindir}/PathFinder
%attr(755,root,root) %{_bindir}/adie
%attr(755,root,root) %{_bindir}/calculator
%attr(755,root,root) %{_bindir}/shutterbug
%{_mandir}/man1/PathFinder.1*
%{_mandir}/man1/adie.1*
%{_mandir}/man1/calculator.1*
%{_mandir}/man1/shutterbug.1*

%files devel
%defattr(644,root,root,755)
%doc ADDITIONS TRACING
%attr(755,root,root) %{_bindir}/fox16-config
%attr(755,root,root) %{_bindir}/reswrap16
%attr(755,root,root) %{_libdir}/libCHART-1.6.so
%attr(755,root,root) %{_libdir}/libFOX-1.6.so
%{_libdir}/libCHART-1.6.la
%{_libdir}/libFOX-1.6.la
%{_includedir}/fox-1.6
%{_pkgconfigdir}/fox-1.6.pc
%{_mandir}/man1/reswrap16.1*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libCHART-1.6.a
%{_libdir}/libFOX-1.6.a
%endif

%files doc
%defattr(644,root,root,755)
%doc doc/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
