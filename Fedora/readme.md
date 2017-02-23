**Building rpm for Fedora**

Steps:

1- Download dependencies

\# dnf install fedora-packager gcc gcc-c++ make qt5-qtsvg-devel qt5-qtwebkit-devel qt5-devel qt-creator qtchooser

2- Create structure

$ rpmdev-setuptree

3- Copy sources to folders

$ wget https://github.com/notepadqq/notepadqq/archive/v1.0.1.tar.gz -O ~/rpmbuild/SOURCES/notepadqq-1.0.1.tar.gz

$ wget https://github.com/notepadqq/CodeMirror/archive/5.18.2-nqq.tar.gz -O ~/rpmbuild/SOURCES/CodeMirror-5.18.2-nqq.tar.gz

$ wget https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/notepadqq.spec -O ~/rpmbuild/SOURCES/notepadqq.spec

4- Go to directory, and build it

$ cd ~/rpmbuild/SOURCES/

$ rpmbuild -ba notepadqq.spec

5- Go to build directory, and install it

$ cd ~/rpmbuild/RPMS/x86_64  (Or i686)

\# dnf install notepadqq-1......rpm

Note: Do not install debuginfo version

Additional notes: \# is run as root, $ is normal user
