%{?python_enable_dependency_generator}
%global srcname sphinxcontrib-programoutput
%global _docdir_fmt %{name}

Name:           python-sphinxcontrib-programoutput
Version:        0.14
Release:        2%{?dist}
Summary:        Extension to insert output of commands into documents

License:        BSD
URL:            https://pypi.python.org/pypi/sphinxcontrib-programoutput
Source0:        https://github.com/NextThought/sphinxcontrib-programoutput/archive/%{version}/%{srcname}-%{version}.tar.gz
Patch0:         0001-Fix-compat-with-sphinx-2.0.patch

BuildArch:      noarch
BuildRequires:  python3-sphinx

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3dist(sphinx) >= 1.3.5
BuildRequires:  python3-pytest
BuildRequires:  git
BuildRequires:  web-assets-devel

%description
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%package -n python3-%{srcname}
Summary:       %{summary}

Requires:       js-jquery
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Sphinx extension to literally insert the output of arbitrary
commands into documents, helping you to keep your command examples
up to date.

%prep
%autosetup -n %{srcname}-%{version} -p1
sed -r -i s/python/python3/ src/sphinxcontrib/programoutput/tests/{test_directive.py,test_command.py,test_cache.py}

%build
%py3_build
PYTHONPATH=build/lib sphinx-build -b html doc build/html
rm -r build/lib/sphinxcontrib/__pycache__
rm -r build/html/.buildinfo build/html/.doctrees

%install
%py3_install
mkdir -p %{buildroot}%{_pkgdocdir}
cp -rv build/html %{buildroot}%{_pkgdocdir}/
ln -vsf %{_jsdir}/jquery/latest/jquery.min.js %{buildroot}%{_pkgdocdir}/html/_static/jquery.js

# remove .pth file which is useless under python3 and breaks namespace modules
rm %{buildroot}%{python3_sitelib}/sphinxcontrib_programoutput-*-nspkg.pth

%check
PYTHONPATH=build/lib/ py.test-%{python3_version} -v build/lib/sphinxcontrib -k 'not test_standard_error_disabled'

%files -n python3-%{srcname}
%license LICENSE
%doc %{_pkgdocdir}
%{python3_sitelib}/*

%changelog
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun  3 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.14-1
- Fix compatibility with sphinx 2.0 (#1716531)

* Fri Apr 26 2019 Yatin Karel <ykarel@redhat.com> - 0.14-1
- Update to 0.14 (#1697058)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.11-6
- Enable python dependency generator

* Fri Dec 28 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-5
- Subpackage python2-sphinxcontrib-programoutput has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

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
