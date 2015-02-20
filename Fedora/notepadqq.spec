Name:           notepadqq
Version:        0.41.1
Release:        19%{?dist}
Summary:        A Linux clone of Notepad++

License:        GPLv3
URL:            https://github.com/notepadqq/notepadqq
Source0:        %{name}-%{version}.tar.gz
#Source1:        cobalt-fedora.css
Patch0:         configure.patch
#.fedora
#Patch1:         configure.patch1

#BuildArch: i686

BuildRequires:  git
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt-creator

Requires:       qt5-qtwebkit
Requires:       qt5-qtsvg


%description
An advanced basic text editor.
Features:
* Syntax Highlighting
* Color Themes
* Code-Collapse
* Macro-recorder


%prep
%setup -q -c %{name}-%{version}
cd %{name}
#cd %{name}
%patch0 -b configure


%build
cd %{name}
#cd %{name}
#sed s,"QMAKE_PATH=qmake","QMAKE_PATH=qmake-qt5",g -i configure
%configure --prefix %{buildroot}/usr
#cp -v ../../../SOURCES/cobalt-fedora.css src/editor/libs/codemirror/theme/
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_datarootdir}/%{name} \
	 %{buildroot}/%{_datarootdir}/applications \
	 %{buildroot}/%{_bindir} %{buildroot}%{_docdir}/%{name} \
	 %{buildroot}%{_mandir}/man1
cd %{name}
# Docs, Manpage
mv *md COPYING %{buildroot}%{_docdir}/%{name}
cp support_files/manpage/%{name}.1 %{buildroot}%{_mandir}/man1

# Icon
cp $(find | grep desktop$) %{buildroot}/%{_datarootdir}/applications

# App data
cd out/release
mv * %{buildroot}/%{_datarootdir}/%{name}
cd %{buildroot}/%{_bindir}
ln -sf %{_datarootdir}/%{name}/bin/%{name} %{name}


%files
%doc %{_mandir}/man1/%{name}.1.gz
%{_bindir}/%{name}
%{_datarootdir}/applications/%{name}.desktop
%{_datarootdir}/%{name}
%{_docdir}/%{name}


%changelog
* Sun Feb 15 2015 Simon Arjuna Erat <erat.simon@gmail.com> 0.41.1-21
- Fixed blank opterations 2

* Sat Feb 14 2015 Simon Arjuna Erat <erat.simon@gmail.com> 0.41.1-16
- Fixed blank opterations

* Thu Feb 05 2015 Simon Arjuna Erat <erat.simon@gmail.com> 0.41.1-13
- Search in files
- Print and Print Now

* Sun Jan 11 2015 Simon Arjuna Erat <erat.simon@gmail.com> 0.41.1-10
- Close tabs with middle click

* Mon Dec 29 2014 Simon Arjuna Erat <erat.simon@gmail.com> 0.41.1-2
- Added: Qt 5.4 to LD_LIBRARY_PATH
- Added: recognize more shells: ksh, csh, tcsh, zsh and fish 

* Tue Nov 18 2014 Simon Arjuna Erat <erat.simon@gmail.com> 0.40.1-20
- Binary knows more shebangs (sh/bash)
- Figured it has a manpage & desktop files, trying to package them

* Mon Nov 17 2014 Simon Arjuna Erat <erat.simon@gmail.com> 0.40.1-9
- Figured BuildRequires and Requires

* Mon Nov 17 2014 Simon Arjuna Erat <erat.simon@gmail.com> 0.40.1-8
- Added patch
- Clean up spec

* Sat Nov 15 2014 Simon Arjuna Erat <erat.simon@gmail.com> 0.40.1-1
- Initial build attempt
