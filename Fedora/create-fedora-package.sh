#!/usr/bin/env bash
# Build NotepadQQ package for and on a Fedora or RedHat based system
# (c) CCSA, 2014-2015 by Simon Arjuna Erat (sea), erat DOT simon AT gmail D0T (0M
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
	[ -z "$VER" ] && exit 1			# Exit with failure if VER is empty
	TARBALL="$SOURCES_DIR/$APP-$VER.tar.gz"	# Location of the tarball
#
#	Environment
#
	# Verify applications are intalled
	echo "Installing required packages to build the package"
	for req in $LIST_APPS_REQUIRED;do 
		printf "\rChecking: $req..."
		if rpm -qa $req 2>/dev/zero 1>/dev/zero
		then 	printf "good.\n"
		else	printf "missing.\n"
			to_install+=" $req"
		fi
	done
	[ -z "$to_install" ] || echo "Missing: $to_install"
	[ -z "$to_install" ] || sudo yum install -y $to_install 2>/dev/zero 1>/dev/zero
#
#	Display & Action
#
	echo
	echo "Creating a RPM package for $APP."
	rpmdev-setuptree
	
	# Clean previous data
	[ -d "$APP_DIR" ] 	&& rm -fr "$APP_DIR"
	[ -d "$OUTPUT_DIR" ] 	&& rm -fr "$OUTPUT_DIR"
	mkdir -p "$OUTPUT_DIR"
	
	# Retrieve raw code
	echo "Downloading code"
	git clone "$URL" "$APP_DIR" #2>/dev/zero
	
	# Prepare sources for build
	echo
	echo "Prepare files to build package..."
	cd "$APP_DIR/.."
	tar -acf "$TARBALL" "$APP" && rm -fr "$APP_DIR"
	cd "$ME_DIR"
	cp "$PATCH" "$SOURCES_DIR"
	cp "$SPEC" "$SPECS_DIR"
	
	# Which packages to build?
	echo
	echo "Please select which packages to build:"
	MENU=( "All available" "Binary only" "Sources only" )
	select menu in "${MENU[@]}";do
		case "$menu" in
		"${MENU[0]}")	OPT=ba	;;
		"${MENU[1]}")	OPT=bb	;;
		"${MENU[2]}")	OPT=bs	;;
		esac
		break
	done
	
	# Build it
	cd "$SPECS_DIR/.."
	echo
	echo "Start building $menu...."
	rpmbuild -$OPT "$SPEC"
	if [ $? -eq 0 ]
	then	# Update relase upon successfull build
		rel=$(grep -i "release:" "$SPEC"|awk '{print $2}')
		num=${rel/\%*/}
		other=${rel/*\%/}
		num=$((num+1))
		sed s,"$rel","$num%$other",g -i "$SPEC"
	fi
	
	# Collect data to output dir
	cd ~/rpmbuild
	echo
	echo "Moving files to $OUTPUT_DIR"
	list=$(find|grep  \\.rpm$)
	list+=" $SPEC"
	list+=" $TARBALL"
	printf "Copying files: "
	for L in $list;do
		if [ -f "$L" ]
		then	printf "."
			cp "$L" "$OUTPUT_DIR"
		fi
	done
	printf "\n"
	
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