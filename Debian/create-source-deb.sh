#!/bin/sh
cd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
cd - > /dev/null

PKG_VERSION_DEB=$(head -n1 debian/changelog | sed 's/notepadqq (//' | cut -d- -f1)

read -p "Notepadqq version [$PKG_VERSION_DEB]: " PKG_VERSION
test -z $PKG_VERSION && PKG_VERSION=$PKG_VERSION_DEB || true

TMP_DIR="$SCRIPTPATH"/tmp

# Clean the build directory
rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"

cd "$TMP_DIR"

# Get the source code tarball
REVISION=v$PKG_VERSION
echo
read -p "What commit/branch/tag do you want to package? [$REVISION] " input
REVISION="${input:-$REVISION}"
../utils/get-source-tarball.sh "$REVISION" "notepadqq_$PKG_VERSION.orig.tar" || exit

# Compress tarball
bzip2 notepadqq_$PKG_VERSION.orig.tar

# Extract tarball and move to the source directory
mkdir notepadqq-$PKG_VERSION
cd notepadqq-$PKG_VERSION
tar -xpf ../notepadqq_$PKG_VERSION.orig.tar.bz2

# Copy debian directory
cp -r "$SCRIPTPATH"/debian "$TMP_DIR"/notepadqq-$PKG_VERSION/debian

# Generate debian/copyright
cd "$TMP_DIR"/notepadqq-$PKG_VERSION
cat debian/copyright.in > debian/copyright
for f in `find src/extension_tools -name LICEN?E`; do
  cat <<EOF >> debian/copyright



Files: `dirname $f`/*

EOF
  cat $f >> debian/copyright
done

echo
echo
echo "Upstream source code downloaded and ready in:"
echo "$TMP_DIR/notepadqq-$PKG_VERSION/"
echo "Open another shell to apply your changes (e.g. to run 'dch' and 'dch -r')."
read -p "When ready, press enter to continue..." dummy

# Create source package, exit if fails
debuild -S || exit

echo
echo "Package created in: $TMP_DIR/"
cd "$TMP_DIR"

# Copy the modified debian folder to the git repository
read -p "Do you want to update the debian folder with your latest changes? (Y/n) " updatedebian
if [ "${updatedebian:-y}" = "y" ] || [ "${updatedebian:-Y}" = "Y" ]
then
	rm -rf "$SCRIPTPATH"/debian
	cp -r "$TMP_DIR"/notepadqq-$PKG_VERSION/debian "$SCRIPTPATH"/debian
fi

# Remove source directory
rm -rf "$TMP_DIR"/notepadqq-$PKG_VERSION

echo
read -p "Do you want to upload the package on Launchpad (ppa:notepadqq-team/notepadqq)? (y/N) " wantupload
if [ "$wantupload" = "y" ] || [ "$wantupload" = "Y" ]
then
	cd "$TMP_DIR"
	dput ppa:notepadqq-team/notepadqq 'notepadqq_'$PKG_VERSION*'_source.changes'
fi
