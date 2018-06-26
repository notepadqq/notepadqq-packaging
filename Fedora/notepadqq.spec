Name:           notepadqq
Version:        1.4.8
Release:        2%{?dist}
Summary:        An advanced text editor for developers

License:        GPLv3 and MIT
                #Notepadqq is licensed under GPLv3
                #CodeMirror is licensed under MIT
URL:            https://github.com/notepadqq/notepadqq
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch1:         add-node.patch
Patch2:         appdata.patch

BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-devel
BuildRequires:  qt-creator
BuildRequires:  qtchooser
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       qt5-qtwebkit
Requires:       qt5-qtsvg
Requires:       nodejs
Requires:       nodejs-shelljs
Requires:       nodejs-archiver

Provides:       bundled(nodejs-codemirror) = 5.33.0 
Provides:       bundled(nodejs-adm-zip) 

%description
A qt text editor for developers, with advanced tools, but remaining simple.
It supports syntax highlighting, themes and more

%prep
%autosetup -p1

%build
rm -rf %{_builddir}/%{name}-%{version}/src/extension_tools/node_modules/archiver
rm -rf %{_builddir}/%{name}-%{version}/src/extension_tools/node_modules/shelljs
rm -f %{_builddir}/%{name}-%{version}/src/extension_tools/node_modules/.bin/shjs
ln -s /usr/bin/shjs %{_builddir}/%{name}-%{version}/src/extension_tools/node_modules/.bin/shjs 
%configure --qmake=qmake-qt5 --lrelease /usr/bin/lrelease-qt5
%make_build


%install
mkdir -p %{buildroot}/%{_datadir}/%{name} \
         %{buildroot}/%{_datadir}/applications \
         %{buildroot}/%{_bindir} %{buildroot}%{_docdir}/%{name} \
         %{buildroot}%{_mandir}/man1 \
         %{buildroot}/%{_libexecdir}/%{name}/bin/

# Docs, Manpage
mv *md %{buildroot}%{_docdir}/%{name}
cp support_files/manpage/%{name}.1 %{buildroot}%{_mandir}/man1

# Icon
desktop-file-install --dir=%{buildroot}/%{_datadir}/applications support_files/shortcuts/%{name}.desktop

# Appstream
mkdir %{buildroot}%{_metainfodir}
cp support_files/notepadqq.appdata.xml %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/notepadqq.appdata.xml

# App data
cd out/release
# Move files to comply better with FHS
mv bin/* %{buildroot}/%{_bindir}/
mv lib/* %{buildroot}/%{_libexecdir}/%{name}/
mv appdata/* ./
rm -r lib appdata
mv * %{buildroot}/%{_datadir}/%{name}

%files
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_docdir}/%{name}
%{_metainfodir}/notepadqq.appdata.xml
%license COPYING

%changelog
* Tue Jun 26 2018 Jan De Luyck <jan@kcore.org> - 1.4.8-2
- Updated to latest comments on Bugzilla

* Wed Jun 13 2018 Jan De Luyck <jan@kcore.org> 1.4.8-1
- Updated to 1.4.8

* Tue Jun 12 2018 Jan De Luyck <jan@kcore.org> 1.4.0-1
- Updated to 1.4.0
- Updated SPEC file based on further comments on Bugzilla

* Fri Apr 20 2018 Jan De Luyck <jan@kcore.org> 1.3.6-1
- Removed bundled nodejs-archiver and nodejs-shelljs
- Updated to 1.3.6

* Wed Apr 11 2018 Jan De Luyck <jan@kcore.org> 1.3.4-2
- Added Provides (comment on Fedora bugzilla)

* Wed Apr 11 2018 Jan De Luyck <jan@kcore.org> 1.3.4-1
- updated to 1.3.4

* Sun Feb 04 2018 Jan De Luyck <jan@kcore.org> 1.2.0-3
- updated to codemirror 5.33.0

* Sun Dec 10 2017 Jan De Luyck <jan@kcore.org> 1.2.0-2
- Fixed some issues from Fedora bugzilla 1519785, as remarked by Ben Rosser.

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

