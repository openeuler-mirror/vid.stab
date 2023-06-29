# https://github.com/georgmartius/vid.stab/commit/aeabc8daa7904f9edf7441a11f293965a5ef53b8
%global commit aeabc8daa7904f9edf7441a11f293965a5ef53b8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20190213

Name:           vid.stab
Version:        1.1.0
Release:        2
Summary:        Video stabilize library for fmpeg, mlt or transcode
License:        GPLv2+
URL:            http://public.hronopik.de/vid.stab
Source0:        https://github.com/georgmartius/vid.stab/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch0:         fix-clang.patch

BuildRequires:  gcc gcc-c++ cmake
BuildRequires:  orc-devel

Requires:       glibc
#To be removed more or less in Fedora 32
Provides:	%{name}-libs = %{version}-%{release}
Obsoletes:	%{name}-libs < %{version}-%{release}

%description
Vidstab is a video stabilization library which can be plugged-in with Ffmpeg
and Transcode.

%package devel
Summary:        Development files for vid.stab
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development files (library and header files).

%prep
%setup -q -n %{name}-%{commit}
# remove SSE2 flags
sed -i 's|-DUSE_SSE2 -msse2||' tests/CMakeLists.txt
# fxi warning _FORTIFY_SOURCE requires compiling with optimization (-O)
sed -i 's|-Wall -O0|-Wall -O|' tests/CMakeLists.txt
# use macros EXIT_SUCCESS and EXIT_FAILURE instead for portability reasons.
sed -i 's|return units_failed==0;|return units_failed>0;|' tests/testframework.c
%if "%toolchain" == "clang"
%patch0 -p1
%endif

%build
%cmake .
%make_build

# build the tests program
pushd tests
%cmake .
%make_build
popd

%install
%make_install

%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} tests/tests || :

%ldconfig_scriptlets -n %{name}

%files
%doc README.md
%license LICENSE
%{_libdir}/libvidstab.so.*

%files devel
%{_includedir}/vid.stab/
%{_libdir}/libvidstab.so
%{_libdir}/pkgconfig/vidstab.pc

%changelog
* Thu Jun 29 2023 yoo <sunyuechi@iscas.ac.cn> - 1.1.0-2
- fix clang build error: omp

* Fri May 07 2021 weidong <weidong@uniontech.com> - 1.1.0-1
- Initial package.
