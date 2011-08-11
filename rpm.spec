# Neither of these variables are set on CentOS, and I wasn't able to find
# a CentOS-specific equivalent in CentOS 5.5.  These might need to be
# removed when we switch to an RHEL6-based distribution.
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name: %(%{__python} %{_sourcedir}/../setup.py --name)
Summary: %(%{__python} %{_sourcedir}/../setup.py --description)
Version: %(%{__python} %{_sourcedir}/../setup.py --version)
Release: 1%{?dist}

# Not for public use, therefore no license
License: None

# Group is chosen from /usr/share/doc/rpm-*/GROUPS
Group: System Environment/Libraries

Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch


%description
%(%{__python} setup.py --long-description)


%prep
%setup -q -n %{name}-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --optimize=1 --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{python_sitelib}
