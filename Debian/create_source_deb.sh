#!/bin/sh
cd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
cd - > /dev/null

# Read package version
PKG_VERSION=$(dpkg-parsechangelog -ldebian/changelog | sed -n 's/^Version: //p' | cut -d "-" -f 1)
echo Detected version: $PKG_VERSION
read -p "Continue? (Y/n) " wantupload
if [ "${wantupload:-y}" != "y" ] && [ "${wantupload:-Y}" != "Y" ]
then
	exit
fi

TMP_DIR=/tmp/pkg-notepadqq-$PKG_VERSION

# Clean the build directory
rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"

# Get the source code
git clone https://github.com/notepadqq/notepadqq.git "$TMP_DIR"/notepadqq-$PKG_VERSION
cd "$TMP_DIR"/notepadqq-$PKG_VERSION

# Create source "orig" tarball
REVISION=master
read -p "What commit/branch/tag do you want to package? [$REVISION] " input
REVISION="${input:-$REVISION}"
git checkout $REVISION || exit # Needed for branches that are not tracked by default
git archive $REVISION | bzip2 > ../notepadqq_$PKG_VERSION.orig.tar.bz2

# Copy debian directory
cp -r "$SCRIPTPATH"/debian "$TMP_DIR"/notepadqq-$PKG_VERSION/debian

# Create source package, exit if fails
debuild -S || exit

# Remove source directory
rm -rf "$TMP_DIR"/notepadqq-$PKG_VERSION

echo
echo "Package created in: $TMP_DIR/"

echo
read -p "Do you want to upload the package on Launchpad (ppa:notepadqq-team/notepadqq)? (y/N) " wantupload
if [ "$wantupload" = "y" ] || [ "$wantupload" = "Y" ]
then
	cd "$TMP_DIR"
	dput ppa:notepadqq-team/notepadqq 'notepadqq_'$PKG_VERSION*'_source.changes'
fi
