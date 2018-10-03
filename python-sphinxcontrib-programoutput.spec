%global srcname sphinxcontrib-programoutput
%global _docdir_fmt %{name}
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-sphinxcontrib-programoutput
Version:        0.11
Release:        5%{?dist}
Summary:        Extension to insert output of commands into documents

License:        BSD
URL:            https://pypi.python.org/pypi/sphinxcontrib-programoutput
Source0:        https://github.com/NextThought/sphinxcontrib-programoutput/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx
BuildRequires:  python2-pytest

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
Requires:       python2-sphinx
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%if %{with python3}
%package -n python3-%{srcname}
Summary:       %{summary}

Requires:       python3-sphinx
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.
%endif

%prep
%autosetup -n %{srcname}-%{version}
%if %{with python3}
sed -r -i s/python/python3/ src/sphinxcontrib/programoutput/tests/{test_directive.py,test_command.py,test_cache.py}
%endif

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

%if %{with python3}
# remove .pth file which is useless under python3 and breaks namespace modules
rm %{buildroot}%{python3_sitelib}/sphinxcontrib_programoutput-*-nspkg.pth
%endif

%check
export LC_CTYPE="en_US.UTF-8"        # without this encoding tests break

# test_standard_error_disabled assumes that the called python has the
# same version as the calling python, which doesn't hold.
PYTHONPATH=build/lib/ py.test-%{python2_version} -v build/lib/sphinxcontrib -k 'not test_standard_error_disabled'
%if %{with python3}
PYTHONPATH=build/lib/ py.test-%{python3_version} -v build/lib/sphinxcontrib -k 'not test_standard_error_disabled'
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc CHANGES.rst README.rst
%doc %{_pkgdocdir}
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{srcname}
%license LICENSE
%doc %{_pkgdocdir}
%{python3_sitelib}/*
%endif

%changelog
* Wed Oct 3 2018 Alfredo Moralejo <amoralej@redhat.com> - 0.11-5
- Removed js-jquery as requirement. It bundles a js-jquery which is used instead.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11-3
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.11-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Feb 24 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-1
- Switch upstream, update to latest version

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
