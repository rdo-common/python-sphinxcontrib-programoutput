%global srcname sphinxcontrib-programoutput
%global _docdir_fmt %{name}

Name:           python-sphinxcontrib-programoutput
Version:        0.8
Release:        2%{?dist}
Summary:        Extension to insert output of commands into documents

License:        BSD
URL:            https://pythonhosted.org/%{srcname}/
# https://github.com/lunaryorn/sphinxcontrib-programoutput
Source0:        https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0:         https://github.com/lunaryorn/%{srcname}/commit/592078e0386c2a36d50a6528b6e49d91707138bf.patch
Patch1:         https://github.com/lunaryorn/%{srcname}/commit/83502056efa0aaed2a5edbd1f44a28d9d5d4815d.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-sphinx
BuildRequires:  pytest
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-pytest
BuildRequires:  git
BuildRequires:  web-assets-devel

Requires:       python-sphinx
Requires:       js-jquery

Provides:       python2-%{srcname}

%description
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%package -n python3-%{srcname}
Summary:       %{summary}
Requires:       python3-sphinx
Requires:       js-jquery
%description -n python3-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%prep
%autosetup -n %{srcname}-%{version} -S git

%build
%{__python2} setup.py build
%{__python3} setup.py build
PYTHONPATH=build/lib sphinx-build-3 -b html doc build/html
rm -r build/html/.buildinfo build/html/.doctrees build/lib/sphinxcontrib/__pycache__

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
%{__python3} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_pkgdocdir}
cp -rv build/html %{buildroot}%{_pkgdocdir}/
ln -vsf %{_jsdir}/jquery/latest/jquery.min.js %{buildroot}%{_pkgdocdir}/html/_static/jquery.js

%check
export LC_CTYPE="en_US.utf8" # without this encoding tests break
PYTHONPATH=build/lib/ py.test-%{python2_version} tests/ -v
PYTHONPATH=build/lib/ py.test-%{python3_version} tests/ -v

%files
%license LICENSE
%doc CHANGES.rst README.rst
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license LICENSE
%doc %{_pkgdocdir}
%{python3_sitelib}/*

%changelog
* Fri Jul 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-2
- Remove stray __pycache__ dir
- Add web-assets-devel to BR and Provide python2-*

* Tue Jul 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-1
- Initial packaging
