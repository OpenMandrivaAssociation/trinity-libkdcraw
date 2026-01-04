%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 5

%define tde_pkg libkdcraw

%define tde_prefix /opt/trinity

%define libkdcraw %{_lib}kdcraw

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.9
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-filesystem >= %{tde_version}

BuildRequires: libtool

%{!?with_clang:BuildRequires: gcc-c++}

BuildRequires: desktop-file-utils
BuildRequires: pkgconfig
BuildRequires: gettext

# LCMS support
BuildRequires:  pkgconfig(lcms)

# JPEG support
BuildRequires:  pkgconfig(libjpeg)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

# AUTOTOOLS
BuildRequires:	%{_lib}ltdl-devel

%description
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

##########

%package -n trinity-%{libkdcraw}4
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Group:		System/Libraries
Requires:	trinity-libkdcraw-common = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg} < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkdcraw}4
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

%files -n trinity-%{libkdcraw}4
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/libkdcraw.so.4
%{tde_prefix}/%{_lib}/libkdcraw.so.4.0.3

##########

%package -n trinity-libkdcraw-common
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Group:		System/Libraries
Requires:	trinity-filesystem >= %{tde_version}

%description -n trinity-libkdcraw-common
C++ interface around dcraw binary program used to decode RAW
picture files.
This library is used by kipi-plugins, digiKam and others kipi host programs.
libkdcraw contains the library of libkdcraw.

%files -n trinity-libkdcraw-common -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_prefix}/share/icons/hicolor/*/apps/kdcraw.png

##########

%package -n trinity-%{libkdcraw}-devel
Summary:	RAW picture decoding C++ library (development) [Trinity]
Group:		Development/Libraries/Other
Requires:	trinity-%{libkdcraw}4 = %{?epoch:%{epoch}:}%{version}-%{release}

Obsoletes:	trinity-%{tde_pkg}-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-%{tde_pkg}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n trinity-%{libkdcraw}-devel
Libkdcraw is a C++ interface around dcraw binary program used to
decode Raw picture files.
libkdcraw-devel contains development files and documentation. The
library documentation is available on kdcraw.h header file.

%files -n trinity-%{libkdcraw}-devel
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/libkdcraw.so
%{tde_prefix}/%{_lib}/libkdcraw.la
%{tde_prefix}/include/tde/libkdcraw/
%{tde_prefix}/%{_lib}/pkgconfig/libkdcraw.pc


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

