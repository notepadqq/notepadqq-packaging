**Building rpm for Fedora**

Steps:

1- Download dependencies

\# dnf install fedora-packager gcc gcc-c++ make qt5-qtsvg-devel qt5-qtwebkit-devel qt5-devel qt-creator qtchooser nodejs

2- Create structure

$ rpmdev-setuptree

3- Copy sources to folders (You can see it in Source0 and Source1 in the .spec file)

$ wget https://github.com/notepadqq/notepadqq/archive/v1.2.0.tar.gz -O ~/rpmbuild/SOURCES/notepadqq-1.2.0.tar.gz

$ wget https://github.com/codemirror/CodeMirror/archive/5.32.0.tar.gz -O ~/rpmbuild/SOURCES/5.32.0.tar.gz

$ wget https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/notepadqq.spec -O ~/rpmbuild/SPECS/notepadqq.spec

$ wget https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/nodepath.patch -O ~/rpmbuild/SOURCES/nodepath.patch

$ wget https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/sas.patch -O ~/rpmbuild/SOURCES/sas.patch

4- Go to directory, and build it

$ cd ~/rpmbuild/SPECS/

$ rpmbuild -ba notepadqq.spec

5- Go to build directory, and install it

$ cd ~/rpmbuild/RPMS/x86_64  (Or i686)

\# dnf install notepadqq-1......rpm

Note: Do not install debuginfo version

Additional notes: \# is run as root, $ is normal user
