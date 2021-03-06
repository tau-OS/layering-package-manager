%global modname lpm                                                         

Name:           layering-package-manager                                                  
Version:        0.0.1
Release:        1%{?dist}
Summary:        Layering Package Manager
License:        GPL3
URL:            https://tauos.co
# TODO add url
Source0:        %{modname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel                                                  
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros

%?python_enable_dependency_generator                                            

%description

Thing

%prep
%autosetup -n %{modname}-%{version}

%build
%py3_build                                                                      

%install
%py3_install

# %check
# %{__python3} setup.py test                                                      

%files
%doc README.md
%license LICENSE
%{_bindir}/%{modname}
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*

%changelog
* Sun Apr 17 2022 Jamie Murphy <jamie@fyralabs.com> - 0.0.1-1
- Initial Release