#!/bin/sh
cd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
cd - > /dev/null

# Read *upstream* package version from debian/changelog. Format: https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-Version
read -p "Notepadqq version (e.g. 0.13.9): " PKG_VERSION

TMP_DIR="$SCRIPTPATH"/tmp

# Clean the build directory
rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"

# Get the source code
git clone https://github.com/notepadqq/notepadqq.git "$TMP_DIR"/notepadqq-$PKG_VERSION
cd "$TMP_DIR"/notepadqq-$PKG_VERSION

# Create source "orig" tarball
REVISION=master
echo
read -p "What commit/branch/tag do you want to package? [$REVISION] " input
REVISION="${input:-$REVISION}"
git checkout $REVISION || exit # Needed for branches that are not tracked by default
git archive $REVISION | bzip2 > ../notepadqq_$PKG_VERSION.orig.tar.bz2

# Copy debian directory
cp -r "$SCRIPTPATH"/debian "$TMP_DIR"/notepadqq-$PKG_VERSION/debian

echo
echo
echo "Upstream source code downloaded and ready in:"
echo "$TMP_DIR/notepadqq-$PKG_VERSION/"
echo "Open another shell to apply your changes (e.g. to run dch)."
read -p "When ready, press enter to continue..." dummy

# Create source package, exit if fails
debuild -S || exit

echo
echo "Package created in: $TMP_DIR/"

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
