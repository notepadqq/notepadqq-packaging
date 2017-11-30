Name:			notepadqq
Version:		1.2.0
Release:		1%{?dist}
Summary:		An advanced text editor for developers

License:		GPLv3
URL:			https://github.com/notepadqq/notepadqq
Source0:		%{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Codemirror download
Source1:		https://github.com/codemirror/CodeMirror/archive/5.32.0.tar.gz

Patch0: nodepath.patch
Patch1: sas.patch

BuildRequires:	qt5-qtsvg-devel
BuildRequires:	qt5-qtwebkit-devel
BuildRequires:	qt5-devel
BuildRequires:	qt-creator
BuildRequires:	qtchooser

Requires:		qt5-qtwebkit
Requires:		qt5-qtsvg
Requires:               nodejs

%description
A qt text editor for developers, with advanced tools, but remaining simple.
It supports syntax highlighting, themes and more

%prep
%setup -q
tar -xf %SOURCE1 -C %{_builddir}/%{name}-%{version}/src/editor/libs/codemirror --strip 1

# Patch source
%patch0 -p1 
%patch1 -p1

# Delete some not neccesary tests (Causes warnings of shebangs, not useful)
#rm -r %{_builddir}/%{name}-%{version}/src/extension_tools/node_modules/archiver/node_modules/glob/node_modules/minimatch/node_modules/brace-expansion/test
#rm -r %{_builddir}/%{name}-%{version}/src/extension_tools/node_modules/archiver/node_modules/tar-stream/node_modules/bl/test


%build
%configure --qmake=qmake-qt5 --prefix %{buildroot}/usr --lrelease /usr/bin/lrelease-qt5
%make_build


%install
mkdir -p %{buildroot}/%{_datarootdir}/%{name} \
	 %{buildroot}/%{_datarootdir}/applications \
	 %{buildroot}/%{_bindir} %{buildroot}%{_docdir}/%{name} \
	 %{buildroot}%{_mandir}/man1 \
	 %{buildroot}/%{_libexecdir}/%{name}/bin/
	 

# Docs, Manpage
mv *md COPYING %{buildroot}%{_docdir}/%{name}
cp support_files/manpage/%{name}.1 %{buildroot}%{_mandir}/man1

# Icon
cp $(find | grep desktop$) %{buildroot}/%{_datarootdir}/applications

# App data
cd out/release
# Move files to comply better with FHS
mv bin/* %{buildroot}/%{_bindir}/
mv lib/* %{buildroot}/%{_libexecdir}/%{name}/
mv appdata/* ./
rm -r lib appdata
mv * %{buildroot}/%{_datarootdir}/%{name}

%files
%doc %{_mandir}/man1/%{name}.1.gz
%{_bindir}/%{name}
%{_libexecdir}/%{name}/%{name}-bin
%{_datarootdir}/applications/%{name}.desktop
%{_datarootdir}/%{name}
%{_docdir}/%{name}


%changelog

* Thu Nov 30 2017 Jan De Luyck <jan@kcore.org> 1.2.0-1
- Updated to 1.2.0
- Updated to CodeMirror 5.32.0
- Moved patching to .patch files

* Sun Feb 26 2017 Kevin Puertas Ruiz <kevin01010@gmail.com> 1.0.1-5
- Fix some issues from fedora bugzilla 1426844 (Nemanja Milosevic)

* Sat Feb 25 2017 Kevin Puertas Ruiz <kevin01010@gmail.com> 1.0.1-4
- Some files change path
- Delete some tests
- Fixes to rpmlint changing shebangs of codemirror
- Patch for notepadqq start (Till notepadqq accepts patch in release)

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

