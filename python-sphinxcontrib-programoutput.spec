%global srcname sphinxcontrib-programoutput
%global _docdir_fmt %{name}

Name:           python-sphinxcontrib-programoutput
Version:        0.8
Release:        1%{?dist}
Summary:        Sphinx extension to insert the output of arbitrary commands into documents

License:        BSD
URL:            https://pythonhosted.org/%{srcname}/
# https://github.com/lunaryorn/sphinxcontrib-programoutput
Source0:        https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%package -n python3-%{srcname}
Summary:       %{summary}
%description -n python3-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%prep
%autosetup -n %{srcname}-%{version}

%build
%{__python2} setup.py build
%{__python3} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
%{__python3} setup.py install --skip-build --root %{buildroot}

%check
%{__python2} setup.py check
%{__python3} setup.py check

%files
%license LICENSE
%doc CHANGES.rst README.rst
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license LICENSE
%doc CHANGES.rst README.rst
%{python3_sitelib}/*

%changelog
* Tue Jul 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-1
- Initial packaging
