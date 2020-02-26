%define __strip /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress
%define debug_package %{nil}

%define name v8_monolith
%define __prefix /usr/local
%define version %{lua:print(os.getenv("V8_VERSION"))}

Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: JavaScript Engine
License: BSD
Group: System Environment/Libraries

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: git
BuildRequires: make
BuildRequires: centos-release-scl
BuildRequires: devtoolset-9-gcc
BuildRequires: devtoolset-9-gcc-c++
BuildRequires: devtoolset-9-libatomic-devel
BuildRequires: glib2-devel

%description
V8 is Google's open source high-performance JavaScript engine, written in C++ and used in Google Chrome, the open source browser from Google. It implements ECMAScript as specified in ECMA-262, 3rd edition, and runs on Windows XP or later, Mac OS X 10.5+, and Linux systems that use IA-32, ARM or MIPS processors. V8 can run standalone, or can be embedded into any C++ application.

%prep
if [ -d %{buildroot}%{__prefix}/%{name} ]; then
  echo "Cleaning out stale build directory" 1>&2
  rm -rf %{buildroot}%{__prefix}/%{name}
fi
#%setup -TDn /src

%build
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git --depth=1
export PATH=$PATH:$PWD/depot_tools
fetch v8
cd v8
git checkout %{version}
gclient sync
tools/dev/v8gen.py x64.release --no-goma -- \
    is_debug=false \
    is_clang=false \
    clang_use_chrome_plugins=false \
    symbol_level=0 \
    v8_monolithic=true \
    treat_warnings_as_errors=false \
    v8_static_library=true \
    v8_enable_i18n_support=false \
    v8_enable_test_features=false \
    v8_use_external_startup_data=false \
    use_custom_libcxx=false \
    use_sysroot=false \
    use_gold=false
scl enable devtoolset-9 "ninja -C out.gn/x64.release v8_monolith"

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}/usr/{include,lib64,include/libplatform}

## binary & lib
install -p -m0644 v8/out.gn/x64.release/obj/libv8_monolith.a %{buildroot}/usr/lib64

## header files
install -p -m0644 v8/include/*.h %{buildroot}/usr/include
install -p -m0644 v8/include/libplatform/* %{buildroot}/usr/include/libplatform

%files
%{_libdir}/*
%{_includedir}/*

%clean
[ "%{buildroot}" != "/" ] && rm -fr %{buildroot}

%post

%preun
