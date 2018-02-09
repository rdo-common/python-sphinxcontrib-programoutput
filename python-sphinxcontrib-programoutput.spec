%global srcname sphinxcontrib-programoutput
%global _docdir_fmt %{name}
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-sphinxcontrib-programoutput
Version:        0.8
Release:        12%{?dist}
Summary:        Extension to insert output of commands into documents

License:        BSD
URL:            https://pythonhosted.org/%{srcname}/
Source0:        https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
Patch1:         0001-Error-tolerant-output-decoding.patch
Patch2:         0002-conftest.py-Use-basic-theme-instead-of-deprecated-de.patch
Patch3:         0003-Use-modern-pytest.fixture-syntax.patch
Patch4:         0004-Add-work-around-for-duplicated-directive-warning.patch

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

# remove .pth file which is useless under python3 and breaks namespace modules
rm %{buildroot}%{python3_sitelib}/sphinxcontrib_programoutput-*-nspkg.pth

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
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 24 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-10
- Drop useless .pth files under python3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-8
- Fix build with new pytest and sphinx-1.5

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.8-7
- Rebuild for Python 3.6

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
