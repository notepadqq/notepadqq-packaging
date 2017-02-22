Name:			notepadqq
Version:		1.0.1
Release:		3%{?dist}
Summary:		A Linux clone of Notepad++

License:		GPLv3
URL:			https://github.com/notepadqq/notepadqq
Source0:		%{name}-%{version}.tar.gz
#CodeMirror submodule https://github.com/notepadqq/CodeMirror/archive/5.18.2-nqq.tar.gz
Source1:		CodeMirror-5.18.2-nqq.tar.gz
#Source1:       cobalt-fedora.css


BuildRequires:	git
BuildRequires:	qt5-qtsvg-devel
BuildRequires:	qt5-qtwebkit-devel
BuildRequires:	qt5-devel
BuildRequires:	qt-creator
BuildRequires:	qtchooser

Requires:		qt5-qtwebkit
Requires:		qt5-qtsvg


%description
An advanced basic text editor.
Features:
* Syntax Highlighting
* Color Themes
* Code-Collapse
* Macro-recorder


%prep
%setup -q
tar -xf %{_builddir}/../SOURCES/CodeMirror-5.18.2-nqq.tar.gz -C %{_builddir}/%{name}-%{version}/src/editor/libs/codemirror --strip 1


%build

%configure --qmake=qmake-qt5 --prefix %{buildroot}/usr --lrelease /usr/bin/lrelease-qt5
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/%{_datarootdir}/%{name} \
	 %{buildroot}/%{_datarootdir}/applications \
	 %{buildroot}/%{_bindir} %{buildroot}%{_docdir}/%{name} \
	 %{buildroot}%{_mandir}/man1

# Docs, Manpage
mv *md COPYING %{buildroot}%{_docdir}/%{name}
cp support_files/manpage/%{name}.1 %{buildroot}%{_mandir}/man1

# Icon
cp $(find | grep desktop$) %{buildroot}/%{_datarootdir}/applications

# App data
cd out/release
mv * %{buildroot}/%{_datarootdir}/%{name}
# Lib is for libs.. Move notepadqq to bin
mv %{buildroot}/%{_datarootdir}/%{name}/lib/notepadqq-bin %{buildroot}/%{_datarootdir}/%{name}/bin/notepadqq-bin
rm -r %{buildroot}/%{_datarootdir}/%{name}/lib/
cd %{buildroot}/%{_bindir}
ln -sf %{_datarootdir}/%{name}/bin/%{name} %{name}

# Delete some not neccesary tests
rm -r %{buildroot}/usr/share/notepadqq/appdata/extension_tools/node_modules/archiver/node_modules/glob/node_modules/minimatch/node_modules/brace-expansion/test

%files
%doc %{_mandir}/man1/%{name}.1.gz
%{_bindir}/%{name}
%{_datarootdir}/applications/%{name}.desktop
%{_datarootdir}/%{name}
%{_docdir}/%{name}


%changelog

* Wed Feb 22 2017 Kevin Puertas Ruiz <kevin01010@gmail.com> 1.0.1-3
- Fixed fedora (25) compilation
- Move files to better places
- No patch required

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
