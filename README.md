Distribution Packages
---------------------

#### Ubuntu (official packages)
Notepadqq is available from an [official PPA](https://launchpad.net/~notepadqq-team/+archive/ubuntu/notepadqq):

    sudo add-apt-repository ppa:notepadqq-team/notepadqq
    sudo apt-get update
    sudo apt-get install notepadqq

#### Debian (official packages)
Download a deb package from the Ubuntu PPA: [download](https://launchpad.net/~notepadqq-team/+archive/ubuntu/notepadqq/+packages)

#### Arch Linux
You can install different versions of the package from AUR:

 * Stable (pre-built Debian package): [notepadqq-bin](https://aur4.archlinux.org/packages/notepadqq-bin/)
 * Development (git version): [notepadqq-git](https://aur4.archlinux.org/packages/notepadqq-git/)

#### Fedora / RHEL
Notepadqq is available from a [testing-repositry](http://sea.fedorapeople.org/sea-devel.repo)

	su
	cd /etc/yum.repos.d
	wget http://sea.fedorapeople.org/sea-devel.repo
	yum install notepadqq

If you would like to compile/package yourself, get this git code and run:

	su
	cd Fedora
	create-fedora-package.sh
	cd ~/notepadqq
	yum install ./notepadqq*[46].rpm
    
#### Solus
Notepaddqq is available in the `shannon` (stable) repository [here](https://dev.solus-project.com/source/notepadqq/)

You can install it via `eopkg`:

    sudo eopkg install notepadqq

#### Others
Use a package for a compatible distribution, or build from [source](https://github.com/notepadqq/notepadqq.git).
If you want to submit a package: https://github.com/notepadqq/notepadqq-packaging
