# ----------------------------------------------------------------------
# File: protobuf3.1.0.spec
# Author: Ivan Arizanovic - ComTrade Solutions Engineering
# ----------------------------------------------------------------------
Summary:        Protocol Buffers - Google's data interchange format
Name:           protobuf
Version:        3.1.0
Release:        1.cern
License:        BSD
Group:          Development/Libraries
Source:         https://github.com/google/protobuf/archive/v%{version}.tar.gz
URL:            https://github.com/google/protobuf
BuildRequires:  automake autoconf libtool pkgconfig zlib-devel

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary: Protocol Buffers C++ headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-compiler = %{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
Static libraries for Protocol Buffers

%package lite
Summary: Protocol Buffers LITE_RUNTIME libraries
Group: Development/Libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary: Protocol Buffers LITE_RUNTIME development libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}

%description lite-devel
This package contains development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-static
Summary: Static development files for %{name}-lite
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description lite-static
This package contains static development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package python
Summary: Python bindings for Google Protocol Buffers
Group: Development/Languages
BuildRequires: python-devel
BuildRequires: python-setuptools
Conflicts: %{name}-compiler > %{version}
Conflicts: %{name}-compiler < %{version}

%description python
This package contains Python libraries for Google Protocol Buffers

%prep
%setup -q
chmod 644 examples/*

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure

make %{?_smp_mflags}

pushd python
python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd

%check
make %{?_smp_mflags} check

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;

pushd python
python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post lite -p /sbin/ldconfig
%postun lite -p /sbin/ldconfig

%post compiler -p /sbin/ldconfig
%postun compiler -p /sbin/ldconfig

%files
%{_libdir}/libprotobuf.so.*
%doc CHANGES.txt CONTRIBUTORS.txt README.md
%license LICENSE

%files compiler
%{_bindir}/protoc
%{_libdir}/libprotoc.so.*
%doc README.md
%license LICENSE

%files devel
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files static
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files lite
%{_libdir}/libprotobuf-lite.so.*

%files lite-devel
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%files lite-static
%{_libdir}/libprotobuf-lite.a

%files python
%dir %{python_sitelib}/google
%{python_sitelib}/google/protobuf/
%{python_sitelib}/protobuf-%{version}-py2.?.egg-info/
%{python_sitelib}/protobuf-%{version}-py2.?-nspkg.pth
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto

%changelog
* Thu Nov 3 2016 Ivan Arizanovic <Ivan.Arizanovic@comtrade.com> - 3.1.0-1.cern
- bump to 3.1.0
