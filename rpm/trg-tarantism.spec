
%global __python %(which python2.7)

%define name trg-tarantism
%define version 0.2.0
%define unmangled_version 0.2.0
%define release 1
%define package_name tarantism

Summary: Tiny ORM for Tarantool NoSQL storage.
Name: %{name}
Version: %{version}
Release: %{release}
License: Proprietary
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Mail.Ru
Url: https://gitlab.corp.mail.ru/target-web/tarantism
Source0: %{name}-%{version}.tar.gz

BuildRequires: trg-setuptools
BuildRequires: tarantool-python = 0.3.4

Requires: tarantool-python = 0.3.4

%description
Tiny ORM for Tarantool NoSQL storage.

%prep
%setup -n %{name}-%{unmangled_version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{python_sitelib}/%{package_name}/
%{python_sitelib}/%{package_name}/*
%{python_sitelib}/%{package_name}*egg-info
