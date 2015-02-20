#!/usr/bin/env bash
# Build NotepadQQ package for and on a Fedora or RedHat based system
# (c) SA, 2014-2015 by Simon Arjuna Erat (sea), erat DOT simon AT gmail D0T (0M
# --------------------------------------------------
#
# 	Are you root or what?
#
	#[ ! 0 -eq $UID ] && printf '%s\n' "$ME: Requires root access!" && exit 1
	
#	
#	Variables
#
	# Environment
	APP=notepadqq
	URL="https://github.com/notepadqq/notepadqq.git"
	ME="${0##*/}"		# Get Scripts name
	ME=${ME/.sh/}		# Remove shell extension
	cd "$(dirname $0)"	# Change to script location, where the SPEC and PATCH are located as well
	ME_DIR="$(pwd)"		# This is the current dir
	OUTPUT_DIR="$HOME/$APP" # There the packages will be saved when successfull
	SOURCES_DIR="$HOME/rpmbuild/SOURCES"	# Where to place the tarball and patchfile
	SPECS_DIR="${SOURCES_DIR/SOURCES/SPECS}" # Where to place the specfile
	SPEC=$ME_DIR/$APP.spec			# The specfile
	PATCH=$ME_DIR/configure.patch		# The patchfile, to use qmake(-qt5)
	LIST_APPS_REQUIRED="git rpmbuild avr-gcc-c++ mingw32-qt5-qmake  qt5-qtsvg-devel qt5-qtwebkit-devel"
	to_install=""				# Which of these is still required?
	OPT=""					# What kind of package to build? -- Will be asked!
	
	# Check for existing temp dir
	for td in "$HOME/.cache" "$HOME/.local/cache" /var/cache /var/tmp;do [ -d "$td" ] && break;done
	APP_DIR="$td/$APP"
	
	# Retrieve the versionnumber from the specfile
	VER=$(grep -i "version:" "$SPEC"|awk '{print $2}')
	[ -z "$VER" ] && exit 1		# Exit with failure if VER is empty
	TARBALL="$SOURCES_DIR/$APP-$VER.tar.gz"	# Location of the tarball
#
#	Environment
#
	# Verify applications are intalled
	echo "Installing required packages to build the package"
	for req in $LIST_APPS_REQUIRED;do printf "\rChecking: $req..." ; which $req 2>/dev/zero 1>/dev/zero && printf "good.\n"|| to_install+=" $req";done
	echo "Missing: $to_install"
	[ -z "$to_install" ] || sudo yum install -y $to_install 2>/dev/zero 1>/dev/zero
#
#	Display & Action
#
	echo "Creating a RPM package for $APP."
	rpmdev-setuptree
	
	# Clean previous data
	[ -d "$APP_DIR" ] 	&& rm -fr "$APP_DIR"
	[ -d "$OUTPUT_DIR" ] 	&& rm -fr "$OUTPUT_DIR"
	mkdir -p "$OUTPUT_DIR"
	
	# Retrieve raw code
	git clone "$URL" "$APP_DIR" 2>/dev/zero
	
	# Prepare sources for build
	cd "$APP_DIR/.."
	tar -acf "$TARBALL" "$APP" && rm -fr "$APP_DIR"
	cd "$ME_DIR"
	cp "$PATCH" "$SOURCES_DIR"
	cp "$SPEC" "$SPECS_DIR"
	
	# Which packages to build?
	echo "Please select which packages to build:"
	MENU=( "All available" "Binary only" "Sources only" )
	select menu in "${MENU[@]}";do
		case "$menu" in
		"${MENU[0]}")	OPT=ba	;;
		"${MENU[0]}")	OPT=bb	;;
		"${MENU[0]}")	OPT=bs	;;
		esac
		break
	done
	
	# Build it
	cd "$SPECS_DIR/.."
	#cd "$OUTPUT_DIR"
	echo "Start building $menu...."
	export LC_ALL=C	# Make sure the output to parse is english
	#list=$(rpmbuild -$OPT "$SPEC" 2>/dev/zero |grep "Wrote:"|awk '{print $2}')
	rpmbuild -$OPT "$SPEC"  #|grep "Wrote:"|awk '{print $2}' | while read tFile;do list+=" $tFile";done
	cd ~/rpmbuild
	list=$(find|grep  \\.rpm$)
	
	# Collect data to output dir
	
	list+=" $SPEC"
	list+=" $TARBALL"
	for L in $list;do
		if [[ -f "$L" ]]
		then	echo "Moving: $L"
			cp "$L" "$OUTPUT_DIR"
		fi
	done
	
	# Present the output
	cd "$OUTPUT_DIR"
	echo
	echo
	echo "These files were created:"
	pwd
	ls -l
	echo
	echo "Thank you for using $ME by sea"
	echo