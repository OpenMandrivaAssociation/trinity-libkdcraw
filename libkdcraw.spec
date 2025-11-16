#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg libkdcraw
%define tde_prefix /opt/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_includedir %{tde_prefix}/include
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_libdir %{tde_prefix}/%{_lib}

%if 0%{?mdkversion} || 0%{?mgaversion} || 0%{?pclinuxos}
%define libkdcraw %{_lib}kdcraw
%else
%define libkdcraw libkdcraw
%endif

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.1.9
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Raw picture decoding C++ library (runtime) [Trinity]
Group:		System/Libraries
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/libraries/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-filesystem >= %{tde_version}

BuildRequires: libtool
%if "%{?toolchain}" != "clang"
BuildRequires: gcc-c++
%endif
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
%if 0%{?mgaversion} || 0%{?mdkversion}
BuildRequires:	%{_lib}ltdl-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 5 || 0%{?suse_version} >= 1220
BuildRequires:	libtool-ltdl-devel
%endif

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
%{tde_libdir}/libkdcraw.so.4
%{tde_libdir}/libkdcraw.so.4.0.3

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
%{tde_datadir}/icons/hicolor/*/apps/kdcraw.png

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
%{tde_libdir}/libkdcraw.so
%{tde_libdir}/libkdcraw.la
%{tde_tdeincludedir}/libkdcraw/
%{tde_libdir}/pkgconfig/libkdcraw.pc

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DPLUGIN_INSTALL_DIR="%{tde_tdelibdir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}

# RHEL4: pkgconfig files do not support 'URL' keyword .
%if 0%{?rhel} == 4
%__sed -i %{?buildroot}%{tde_libdir}/pkgconfig/*.pc -e "s/^URL: /#URL: /"
%endif

