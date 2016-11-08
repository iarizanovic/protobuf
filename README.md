# How To Build RPM Packages for Protocol Buffers on CentOS
### Overview
Protocol Buffers (a.k.a. `protobuf`) are Google's language-neutral,
platform-neutral, extensible mechanism for serializing structured data. You
can find [protobuf's documentation on the Google Developers site](https://developers.google.com/protocol-buffers/).

This README file contains instructions of packaging process for Protocol
Buffers.

### Development environment
There are a couple of thing you need to do before starting building your RPMs.
These mainly include the installation of the core development tools and
the creation of the building environment for your user.

1) Install the core development tools using YUM (as root):
```sh
# yum groupinstall "Development Tools"
```
2) Next, create the building environment for your user.
   Use YUM to install them (as root):
```sh
# yum install rpmdevtools
```
3) Then, create the directory structure in your home directory
   by issuing the command (as a user):
```sh
$ rpmdev-setuptree
```

### Environment for Protocol Buffers
1) First, install dependencies for Protocol Buffers:
```sh
$ yum install python-devel python-setuptools automake autoconf libtool pkgconfig zlib-devel
```
2) Then, download source and spec file:
```sh
$ wget https://github.com/iarizanovic/protobuf/raw/master/SPECS/protobuf3.1.0-1.cern.spec
$ mv protobuf3.1.0-1.cern.spec ~/rpmbuild/SPECS/
$ wget https://github.com/iarizanovic/protobuf/raw/master/SOURCES/v3.1.0.tar.gz
$ mv v3.1.0.tar.gz ~/rpmbuild/SOURCES/
```

### Build RPMs
Now, you can build the binary RPM package by issuing the command:
```sh
$ rpmbuild -bb --clean ~/rpmbuild/SPECS/protobuf3.1.0-1.cern.spec
```
If the operation finishes succesfully, you’ll find your RPM package
in the ~/rpmbuild/RPMS/ directory.
