%global srcname sphinxcontrib-programoutput
%global _docdir_fmt %{name}
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-sphinxcontrib-programoutput
Version:        0.8
Release:        6%{?dist}
Summary:        Extension to insert output of commands into documents

License:        BSD
URL:            https://pythonhosted.org/%{srcname}/
# https://github.com/lunaryorn/sphinxcontrib-programoutput
Source0:        https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0:         https://github.com/lunaryorn/%{srcname}/commit/592078e0386c2a36d50a6528b6e49d91707138bf.patch
Patch1:         https://github.com/lunaryorn/%{srcname}/commit/83502056efa0aaed2a5edbd1f44a28d9d5d4815d.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  pytest

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  python3-pytest
%endif
BuildRequires:  git
BuildRequires:  web-assets-devel

%description
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python-sphinx
Requires:       js-jquery
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%if %{with python3}
%package -n python3-%{srcname}
Summary:       %{summary}

Requires:       python3-sphinx
Requires:       js-jquery
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.
%endif

%prep
%autosetup -n %{srcname}-%{version} -S git

# ^ additional newline to work around #1225118
# can be removed once you are on rpm-4.11.3-17.el7
rm -r *.egg-info

%build
%py2_build
%if %{with python3}
%py3_build
PYTHONPATH=build/lib sphinx-build-3 -b html doc build/html
rm -r build/lib/sphinxcontrib/__pycache__
%else
PYTHONPATH=build/lib sphinx-build -b html doc build/html
%endif
rm -r build/html/.buildinfo build/html/.doctrees

%install
%py2_install
%if %{with python3}
%py3_install
%endif
mkdir -p %{buildroot}%{_pkgdocdir}
cp -rv build/html %{buildroot}%{_pkgdocdir}/
ln -vsf %{_jsdir}/jquery/latest/jquery.min.js %{buildroot}%{_pkgdocdir}/html/_static/jquery.js

%check
export LC_CTYPE="en_US.utf8" # without this encoding tests break
PYTHONPATH=build/lib/ py.test-%{python2_version} tests/ -v
%if %{with python3}
PYTHONPATH=build/lib/ py.test-%{python3_version} tests/ -v
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc CHANGES.rst README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{srcname}
%license LICENSE
%doc %{_pkgdocdir}
%{python3_sitelib}/*
%endif

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 03 2015 Robert Buchholz <rbu@goodpoint.de> - 0.8-5
- epel7: Only build python2 package

* Mon Nov 16 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-4
- Update to latest packaging guidelines

* Mon Jul 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-3
- Make provides versioned

* Fri Jul 24 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-2
- Remove stray __pycache__ dir
- Add web-assets-devel to BR and Provide python2-*

* Tue Jul 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-1
- Initial packaging
