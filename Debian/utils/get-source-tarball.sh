#!/bin/sh
cd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
cd - > /dev/null

# Downloads the source tarball (from git)
#
# Usage:
# get-source-tarball.sh git_revision output_tar_file

REVISION=$1
OUTPUT=$(readlink -m "$2") # Convert to absolute path

# Get the source code
git clone https://github.com/notepadqq/notepadqq.git _tmp_source_tarball || exit
cd _tmp_source_tarball

git checkout "$REVISION" || exit # Needed for branches that are not tracked by default
git submodule init
git submodule update
# Can't use the following line because it doesn't copy submodules:
# git archive $REVISION | bzip2 > ../notepadqq_$PKG_VERSION.orig.tar.bz2
"$SCRIPTPATH"/git-archive-all.sh "$OUTPUT"

cd ..
rm -rf _tmp_source_tarball

# Extract and re-create archive to fix uncompatible file produced by git-archive-all.sh
mkdir _tmp_extract_orig_source_tarball
cd _tmp_extract_orig_source_tarball
tar -xpf "$OUTPUT"
tar -cpf "$OUTPUT" *
cd ..
rm -rf _tmp_extract_orig_source_tarball