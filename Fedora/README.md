## Building rpm for Fedora

**Note: Items prefixed with \# means run the command as root (or use `sudo`). Items prefixed with $ should be run as your own/build user.**

Steps:

1. Download dependencies

  * \# `dnf install fedora-packager gcc gcc-c++ make qt5-qtsvg-devel qt5-qtwebkit-devel qt5-devel qt-creator qtchooser nodejs nodejs-archiver nodejs-shelljs`

2. Create structure

  * $ `rpmdev-setuptree`

3. Copy sources to folders (You can see it in [notepadqq.spec](https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/notepadqq.spec) file)

  * $ `wget https://github.com/notepadqq/notepadqq/archive/v1.4.0.tar.gz -O ~/rpmbuild/SOURCES/notepadqq-1.4.0.tar.gz`
  * $ `wget https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/add-node.patch -O ~/rpmbuild/SOURCES/add-node.patch`
  * $ `wget https://raw.githubusercontent.com/notepadqq/notepadqq-packaging/master/Fedora/appdata.patch -O ~/rpmbuild/SOURCES/appdata.patch`


4. Go to directory, and build it

  * $ `cd ~/rpmbuild/SPECS/`
  * $ `rpmbuild -ba notepadqq.spec`

5. Go to build directory, and install it

  * $ `cd ~/rpmbuild/RPMS/x86_64`  (Or i686)
  * \# `dnf install notepadqq-1......rpm`

_Note: Do not install debuginfo versions_
