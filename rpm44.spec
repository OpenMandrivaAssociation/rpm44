# because i'm lazy
%define _default_patch_fuzz 2

# Do not change this spec directly but in the svn
# $Id: rpm.spec 134789 2007-03-27 15:13:43Z nanardon $

%define lib64arches	x86_64 ppc64 sparc64

%ifarch %lib64arches
    %define _lib lib64
%else
    %define _lib lib
%endif

# Define directory which holds rpm config files, and some binaries actually
# NOTE: it remains */lib even on lib64 platforms as only one version
#       of rpm is supported anyway, per architecture
%define rpmdir %{_prefix}/lib/rpm44

%if %{?pyver:0}%{?!pyver:1}
%define pyver %(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")
%endif

#%%define __find_requires %{rpmdir}/mandriva/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
#%%define __find_provides %{rpmdir}/mandriva/find-provides
%define __find_requires /usr/lib/rpm/mandriva/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
%define __find_provides /usr/lib/rpm/mandriva/find-provides

%define rpmversion	4.4.2.3
%define srcver		%rpmversion
%define libver		4.4

%define librpmname   %mklibname rpm44_  %{libver}
%define librpmnamedevel   %mklibname -d rpm44

%define buildpython 0

%define buildnptl 0

%if %{mdkversion} >= 200710
# MDV 2007.1 builds with --hash-style=gnu by default
%define rpmsetup_version 1.34
%endif

%define builddebug 0
%{?_with_debug:%define builddebug 1}

%{?_with_python:%define buildpython 1}
%{?_without_python:%define buildpython 0}

%{?_with_nptl:%define buildnptl 1}
%{?_without_nptl:%define buildnptl 0}

Summary:	The RPM package management system
Name:		rpm44
Version:	%{rpmversion}
%define subrel 1
Release:	%mkrel 0
Group:		System/Configuration/Packaging
URL:            http://rpm.org/
Source:		http://www.rpm.org/releases/rpm-%{libver}.x/rpm-%{srcver}.tar.gz

# Add some undocumented feature to gendiff
Patch17:	rpm-4.4.2.2-gendiff-improved.patch

# (gb) force generation of PIC code for static libs that can be built into a DSO (file)
Patch3:		rpm-4.4.2.2-pic.patch

# if %post of foo-2 fails,
# or if %preun of foo-1 fails,
# or if %postun of foo-1 fails,
# => foo-1 is not removed, so we end up with both packages in rpmdb
# this patch makes rpm ignore the error in those cases
# failing %pre must still make the rpm install fail (#23677)
#
# (nb: the exit code for pretrans/posttrans & trigger/triggerun/triggerpostun
#       scripts is ignored with or without this patch)
Patch22:        rpm-4.4.6-non-pre-scripts-dont-fail.patch

# (fredl) add loging facilities through syslog
Patch31:	rpm-4.4.2.2-syslog.patch

# Check amd64 vs x86_64, these arch are the same
Patch44:	rpm-4.4.1-amd64.patch

# part of Backport from 4.2.1 provides becoming obsoletes bug (fpons)
# (is it still needed?)
Patch49:	rpm-4.4.2.2-provides-obsoleted.patch

# Introduce new ppc32 arch. Fix ppc64 bi-arch builds. Fix ppc builds on newer CPUs.
Patch56:	rpm-4.4.2.2-ppc32.patch

# - force /usr/lib/rpm/manbo/rpmrc instead of /usr/lib/rpm/<vendor>/rpmrc
# - read /usr/lib/rpm/manbo/rpmpopt (not only /usr/lib/rpm/rpmpopt)
Patch64:    rpm-4.4.2.2-manbo-rpmrc-rpmpopt.patch

# In original rpm, -bb --short-circuit does not work and run all stage
# From popular request, we allow to do this
# http://qa.mandriva.com/show_bug.cgi?id=15896
Patch70:	rpm-4.4.1-bb-shortcircuit.patch

# http://www.redhat.com/archives/rpm-list/2005-April/msg00131.html
# http://www.redhat.com/archives/rpm-list/2005-April/msg00132.html
Patch71:    rpm-4.4.4-ordererase.patch

# don't conflict for doc files
# (to be able to install lib*-devel together with lib64*-devel even if they have conflicting manpages)
Patch83: rpm-4.4.2.2-no-doc-conflicts.patch

# Fix http://qa.mandriva.com/show_bug.cgi?id=19392
# (is this working??)
Patch84: rpm-4.4.2.2-rpmqv-ghost.patch

# (sqlite) Use temporary table for Depends DB (Olivier Thauvin upstream)
Patch86: rpm-4.4.2.2-depsdb.patch

# avoids taking into account duplicates in file list when checking
# for unpackaged files
Patch91: rpm-4.4.6-check-dupl-files.patch

# without this patch, when pkg rpm-build is not installed,
# using rpm -bs t.spec returns: "t.spec: No such file or directory"
Patch100: rpm-4.4.6-fix-error-message-rpmb-not-installed.patch

Patch109: rpm-build-expand-field-for-single-token.patch

# Fix diff issue when buildroot contains some "//"
Patch111: rpm-check-file-trim-double-slash-in-buildroot.patch

# Fix strange issue making %pre/post/... -f not working
# (only needed on 4.4.8?)
Patch112: rpm-4.4.2.2-dont-use-rpmio-to-read-file-for-script.patch

# patch only needed when rpmrc is not used (ie jbj's rpm), 
# otherwise macrofiles from rpmrc always overrides MACROFILES
Patch114: rpm-4.4.2.2-read-vendor-macros.patch

# remove unused skipDir functionality that conflicts with patch124 below
Patch1124: rpm-4.4.2.2-revert-unused-skipDir-functionality.patch

# [pixel] without this patch, "rpm -e" or "rpm -U" will need to stat(2) every dirnames of
# files from the package (eg COPYING) in the db. This is quite costly when not in cache 
# (eg on a test here: >300 stats, and so 3 seconds after a "echo 3 > /proc/sys/vm/drop_caches")
# this breaks urpmi test case test_rpm_i_fail('gd') in superuser--file-conflicts.t,
# but this is bad design anyway
Patch124: rpm-4.4.2.2-speedup-by-not-checking-same-files-with-different-paths-through-symlink.patch

# [from SuSE] patch132 needed by patch133
Patch132: rpm-4.4.2.2-extcond.patch
# [from SuSE] handle "Suggests" via RPMTAG_SUGGESTSNAME
Patch133: rpm-4.4.2.2-weakdeps.patch
# complement patch above: add "suggests" handling to rpmdsNew
# (wondering how it works without it?) (nanardon)
Patch1133: rpm-4.4.2.3-rc1-weakdeps--allow-rpmds.patch

# MDV2008.0 sets %buildroot globally, but default rule is %buildroot overrides BuildRoot
# this breaks (broken) .spec relying on a specified BuildRoot (#34705).
# Introducing a global %defaultbuildroot which is used when neither %buildroot nor BuildRoot is used
# So %buildroot/$RPM_BUILD_ROOT in .spec are set to %buildroot or BuildRoot or %defaultbuildroot (in that order)
Patch134: rpm-4.4.2.2-defaultbuildroot.patch

# (from Turbolinux) remove a wrong check in case %_topdir is /RPM (ie when it is short)
Patch135: rpm-4.4.2.3-rc1-fix-debugedit.patch

# convert data in the header to a specific encoding which used in the selected locale.
Patch137: rpm-4.4.2.3-rc1-headerIconv.patch

# on x86_64, file conflicts were allowed because of transaction coloring
Patch139: rpm-4.4.2.3-rc1-do-not-allow-fileconflict-between-non-colored-file.patch

Patch140: rpm-4.4.2.3-rc1-russian-translation.patch

Patch141: rpm-4.4.2.3-drop-skipping-ldconfig-hack.patch

Patch142: rpm-do-not-ignore-failing-chroot.patch

# (already fixed upstream)
Patch143: rpm-4.4.2.3-fix-debugedit-build.patch

Patch144: rpm-4.4.2.3-handle-posttrans-p--with-no-body.patch

# ensure readLine errors are fatal soon
# (useful for forbid-badly-commented-define-in-spec, 
#  but also for "%if %xxx" where %xxx is not defined)
# (already fixed in rpm.org with PART_ERROR which is < 0)
Patch1450: rpm-4.4.2.3-readLine-errors-are-errors.patch

# without this patch, "#%define foo bar" is surprisingly equivalent to "%define foo bar"
# with this patch, "#%define foo bar" is a fatal error
Patch145: rpm-4.4.2.3-forbid-badly-commented-define-in-spec.patch

# cf http://wiki.mandriva.com/en/Rpm_filetriggers
Patch146: rpm-4.4.2.3-filetriggers.patch

# add two fatal errors (during package build)
Patch147: rpm-4.4.2.3-rpmbuild-check-useless-tags-in-non-existant-binary-packages.patch

Patch148: rpm-4.4.2.3-do-not-ignore-failing-chroot2.patch

# upstream rpm.org has already got rid of internal db
Patch149: rpm-4.4.2.3-external-db.patch

# fixed upstream
Patch150: rpm-4.4.2.3-fix-broken-cpio-for-hardlink-on-softlink.patch

Patch151: rpm-4.4.2.3-protect-against-non-robust-futex.patch

# be compatible with >= 4.4.8 :
Patch1001: rpm-4.4.2.3-liblzma-payload.patch
Patch1002: rpm-4.4.2.2-default-topdir--usr-src-rpm.patch

# keep compatibility with "suggests" the way rpm >= 4.4.7 do it
# (backport from 4.4.7 + mandriva fix)
Patch1003: rpm-4.4.2.2-handle-suggests--ignore-requires-hint.patch

# keep libpopt.so versioning from 4.4.8 to avoid warning:
# xxx: /lib/libpopt.so.0: no version information available (required by xxx)
Patch1004: rpm-4.4.2.2-add-libpopt-vers.patch

# default behaviour in rpm >= 4.4.6
Patch1005: rpm-4.4.2.2-allow-conflicting-ghost-files.patch

# Turbolinux patches
Patch2000: rpm-4.4.2-serial-tag.patch
# re-enable "copyright" tag (Kiichiro, 2005)
Patch2001: rpm-4.4.2-copyright-tag.patch
# add writeHeaderListTofile function into rpm-python (needed by "buildman" build system) (Toshihiro, 2003)
Patch2002: rpm-4.2.2-python-writeHdlist.patch
# Crusoe CPUs say that their CPU family is "5" but they have enough features for i686.
Patch2003: rpm-4.4.2.3-rc1-transmeta-crusoe-is-686.patch
# add japanese popt translations
Patch2004: rpm-4.4.2.3-rc1-popt-ja-translations.patch

# The following patch is unneeded for Mandriva, but Turbolinux has it and it can't hurt much
#
# This patch fixes the problem when the post-scripts launched by rpm-build. 
# The post-scripts launched by rpm-build works in LANG environment. If LANG is
# other locale except C, then some commands launched by post-scripts will not
# display characters which you expected.
Patch2005: rpm-4.2.0-buildlang.patch

Patch2006: rpm-4.4.2.3-CVE-2010-2059.diff
# P2007: stolen from debian to handle lzma-5
Patch2007: rpm-4.4.2.3-debian.diff
Patch2008: rpm-4.4.2.3-no_docs.diff
Patch2009: rpm-4.4.2.3-fmtstr.diff

License:	GPL
BuildRequires:	autoconf >= 2.57
BuildRequires:	zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:	automake >= 1.8
BuildRequires:	elfutils-devel
BuildRequires:	sed >= 4.0.3
BuildRequires:	libbeecrypt-devel
BuildRequires:	ed, gettext-devel
BuildRequires:  libsqlite3-devel
BuildRequires:  db4.6-devel
BuildRequires:  neon-devel
BuildRequires:  rpm-mandriva-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}
BuildRequires:  readline-devel
BuildRequires:	ncurses-devel
BuildRequires:  openssl-devel >= 0.9.8
BuildRequires:  lua-devel
BuildRequires:  bison
# Need for doc
BuildRequires:	graphviz
BuildRequires:	tetex
%if %buildpython
BuildRequires:	python-devel
%endif
%if %buildnptl
# BuildRequires:	nptl-devel
%endif

Requires:	bzip2 >= 0.9.0c-2
Requires:	xz >= 5.0.0
BuildRequires:	lzma-devel >= 5.0.0
Requires:	cpio
Requires:	gawk
Requires:	glibc >= 2.1.92
Requires:	mktemp
Requires:	popt
BuildRequires:	popt-devel
Requires:	setup >= 2.2.0-8mdk
Requires:	rpm-manbo-setup
Requires:	rpm-mandriva-setup >= 1.85
Requires:	update-alternatives
Requires:	%librpmname >= %version-%release
Conflicts:	patch < 2.5
Conflicts:	menu < 2.1.5-29mdk
Conflicts:	locales < 2.3.1.1
Conflicts:	man-pages-fr < 0.9.7-16mdk
Conflicts:	man-pages-pl < 0.4-9mdk
Conflicts:	perl-URPM < 1.63-3mdv2008.0
Requires(pre): rpm-helper >= 0.8
Requires(pre): coreutils
Requires(postun): rpm-helper >= 0.8
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
Each software package consists of an archive of files along with information
about the package like its version, a description, etc.

%package -n	%librpmname
Summary:	Library used by rpm
Group:		System/Libraries

%description -n %librpmname
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
This package contains common files to all applications based on rpm.

%package -n	%librpmnamedevel
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	rpm44 >= %{version}-%{release}
Provides:   	rpm44-devel >= %{version}-%{release}

%description -n	%librpmnamedevel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs
which manipulate RPM packages and databases and are intended to make
it easier to create graphical package managers or any other tools
that need an intimate knowledge of RPM packages in order to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package	build
Summary:	Scripts and executable programs used to build packages
Group:		System/Configuration/Packaging
Requires:	autoconf
Requires:	automake
Requires:	file
Requires:	gcc-c++
# We need cputoolize & amd64-* alias to x86_64-* in config.sub
Requires:	libtool-base >= 1.4.3-5mdk
Requires:	patch
Requires:	make
Requires:	tar
Requires:	unzip
Requires:	elfutils
Requires:	xz >= 5.0.0
Requires:	rpm44 >= %{version}-%{release}
Requires:	rpm-mandriva-setup-build %{?rpmsetup_version:>= %{rpmsetup_version}}

%description	build
This package contains scripts and executable programs that are used to
build packages using RPM.

%if %buildpython
%package -n python-rpm
Summary:	Python bindings for apps which will manipulate RPM packages
Group:		Development/Python
Requires:	python >= %{pyver}
Requires:	rpm44 = %{version}-%{release}
Obsoletes:  rpm-python < %epoch:%version-%release
Provides:   rpm-python = %version-%release

%description -n python-rpm
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.
%endif

%prep

%setup -q -n rpm-%srcver
%patch3 -p1 -b .pic
%patch17 -p1 -b .improved
%patch22 -p1 -b .fail
%patch31 -p1 -b .syslog
%patch44 -p1 -b .amd64
%patch49 -p1 -b .provides
%patch56 -p1 -b .ppc32
%patch64 -p1 -b .morepopt
%patch70 -p0 -b .shortcircuit
%patch71 -p0  -b .ordererase
%patch83 -p1 -b .no-doc-conflicts
%patch84 -p1 -b .poptQVghost
%patch86 -p1 -b .depsdb
%patch91 -p0 -b .check-dupl-files
%patch100 -p1 -b .rpmb-missing
# Fix diff issue when buildroot contains some "//"
%patch111 -p0 -b .trim-slash
# Fix strange issue making %pre/post/... -f not working
%patch112 -p1 -b .build-no-rpmio
%patch114 -p1 -b .read-our-macros
%patch1124 -p1 -b .skipDir
%patch124 -p1 -b .speedup
%patch1001 -p1 -b .liblzma
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch132 -p0
%patch133 -p1
%patch1133 -p1
%patch134 -p1 -b .defaultbuildroot
%patch135 -p1 -b .debugedit
%patch137 -p1 -b .iconv
%patch139 -p1 -b .fileconflict
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch1450 -p1
%patch145 -p1
%patch146 -p1 -b .filetriggers
%patch147 -p1
%patch148 -p1
%patch149 -p1 -b .external-db
%patch150 -p1 -b .hardlink-symlink
%patch151 -p1 -b .lock__db001
rm -rf db db3 rpmdb/db.h
%patch2000 -p1 -b .serial-tag
%patch2001 -p0 -b .copyright-tag
%patch2002 -p0 -b .python_writeHD
%patch2003 -p1 -b .crusoe-arch
%patch2004 -p1 -b .popt-ja
%patch2005 -p1 -b .buildlang
%patch2006 -p0 -b .CVE-2010-2059
# stolen from debian to handle lzma-5
%patch2007 -p1 -b .lzma-5
%patch2008 -p0 -b .no_docs
%patch2009 -p0 -b .fmtstr

# hardcoded crap!
for i in `find . -type f -name "*"`; do
    perl -pi -e "s|/etc/rpm/|/etc/%{name}/|g" $i
    perl -pi -e "s|/etc/rpm\b|/etc/%{name}|g" $i
    perl -pi -e "s|\\$\\(prefix\\)/src/rpm|\\$\\(prefix\\)/src/%{name}|g" $i
    perl -pi -e "s|\\$\\(libdir\\)/rpm/|\\$\\(libdir\\)/%{name}/|g" $i
    perl -pi -e "s|\\$\\(libdir\\)/rpm\b|\\$\\(libdir\\)/%{name}|g" $i
    perl -pi -e "s|\\$\\(includedir\\)/rpm\b|\\$\\(includedir\\)/%{name}|g" $i
    perl -pi -e "s|/etc/rpm/|/etc/%{name}/|g" $i
    perl -pi -e "s|/var/lock/rpm/|/var/lock/%{name}/|g" $i
    perl -pi -e "s|/lib/rpm/|/lib/%{name}/|g" $i
    perl -pi -e "s|/lib/rpm\b|/lib/%{name}|g" $i
done

# more crap...
perl -pi -e "s|bin2c|/bin/true|g" lua/*

for i in `find . -type f -name "Makefile*"`; do
    # rename the libs
    for lib in librpm librpmbuild librpmdb librpmio; do
        perl -pi -e "s|${lib}\.la|${lib}44\.la|g" $i
        perl -pi -e "s|${lib}\.a|${lib}44\.a|g" $i
	perl -pi -e "s|${lib}_la_|${lib}44_la_|g" $i
    done
done

# grr...
perl -pi -e "s|\\$\\(includedir\\)/\@PACKAGE\@|\\$\\(includedir\\)/%{name}|g" Makefile*

# hmm...
mkdir -p zlib

# try to use system popt
rm -rf popt

for dir in . file; do
    pushd $dir
#    autoreconf
    libtoolize --copy --force
    aclocal
    autoheader
    automake -a -c
    autoconf
    popd
done

%build
# rpm takes care of --libdir but explicitelly setting --libdir on
# configure breaks make install, but this does not matter.
# --build, we explictly set 'mandriva' as our config subdir and 
# _host_vendor are 'mandriva'
%if %builddebug
RPM_OPT_FLAGS=-g
%endif
CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" \
./configure \
    --build=%{_target_cpu}-%{_host_vendor}-%{_target_os}%{?_gnu} \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_localstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --disable-nls \
    --without-javaglue \
%if %builddebug
    --enable-debug \
%endif
%if %buildnptl
    --enable-posixmutexes \
%else
    --with-mutex=UNIX/fcntl \
%endif
%if %buildpython
    --with-python=%{pyver} \
%else
    --without-python \
%endif
    --with-lua \
    --with-glob \
    --without-selinux --with-selinux=no \
    --without-apidocs --with-apidocs=no

%make

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

# [pixel - March 2008] this is deprecated afaik, but keeping it for now
ln -sf rpm44/rpmpopt-%{srcver} %{buildroot}%{_prefix}/lib/rpmpopt44

%ifarch ppc powerpc
    ln -sf ppc-mandriva-linux %{buildroot}%{rpmdir}/powerpc-mandriva-linux
%endif

mkdir -p %{buildroot}/var/lib/%{name}
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Providename \
    Provideversion Removetid Requirename Requireversion Triggername \
    Packages __db.001 __db.002 __db.003 __db.004
do
    touch %{buildroot}/var/lib/%{name}/$dbi
done

test -d doc-copy || mkdir doc-copy
rm -rf doc-copy/*
ln -f doc/manual/* doc-copy/
rm -f doc-copy/Makefile*

mkdir -p %{buildroot}%_sysconfdir/%{name}/macros.d
cat > %{buildroot}%_sysconfdir/%{name}/macros <<EOF
# Put your own system macros here
# usually contains 

# Set this one according your locales
# %%_install_langs

EOF

# Get rid of unpackaged files
(cd %{buildroot};
  rm -rf .%{_includedir}/beecrypt/
  rm -f  .%{_libdir}/libbeecrypt.{a,la,so*}
  rm -f  .%{_libdir}/python*/site-packages/poptmodule.{a,la}
  rm -f  .%{_libdir}/python*/site-packages/rpmmodule.{a,la}
  rm -f  .%{rpmdir}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req}
  rm -f  .%{rpmdir}/{config.site,cross-build,rpmdiff.cgi}
  rm -f  .%{rpmdir}/trpm
  rm -f  .%{_bindir}/rpmdiff
  rm -rf .%{_mandir}
  rm -f  .%{_libdir}/*.a
)

#%%if %_vendor == Mandriva
#%{rpmdir}/%{_host_vendor}/find-lang.pl %{buildroot} %{name}
#%{rpmdir}/%{_host_vendor}/find-lang.pl %{buildroot} popt
#/usr/lib/rpm/%{_host_vendor}/find-lang.pl %{buildroot} %{name}
#/usr/lib/rpm/%{_host_vendor}/find-lang.pl %{buildroot} popt
#%%else
#%%find_lang %{name}
#%%find_lang popt
#%%endif

# renaming voodoo magic...
mv %{buildroot}/bin/rpm %{buildroot}/bin/%{name}

pushd %{buildroot}%{_bindir}
    mv gendiff gendiff44
    mv rpm2cpio rpm2cpio44
    mv rpmgraph rpmgraph44
    ln -snf ../lib/rpm44/rpmb rpmbuild44
    ln -snf ../lib/rpm44/rpmd rpmdb44
    ln -snf ../lib/rpm44/rpme rpme44
    ln -snf ../lib/rpm44/rpmi rpmi44
    ln -snf ../lib/rpm44/rpmq rpmquery44
    ln -snf ../lib/rpm44/rpmk rpmsign44
    ln -snf ../lib/rpm44/rpmu rpmu44
    ln -snf ../lib/rpm44/rpmv rpmverify44
    rm -f rpmbuild rpmdb rpme rpmi rpmquery rpmsign rpmu rpmverify
popd

# plan b
mv %{buildroot}%{_includedir}/rpm %{buildroot}%{_includedir}/rpm44

%clean
rm -rf %{buildroot}

%pre
if [ -f /var/lib/%{name}/Packages -a -f /var/lib/%{name}/packages.rpm ]; then
    echo "
You have both
	/var/lib/%{name}/packages.rpm	db1 format installed package headers
	/var/lib/%{name}/Packages		db3 format installed package headers
Please remove (or at least rename) one of those files, and re-install.
"
    exit 1
fi

/usr/share/rpm-helper/add-user %{name} $1 %{name} /var/lib/%{name} /bin/false

rm -rf /usr/lib/%{name}/*-mandrake-*

%post
## nuke __db.00? when updating to this rpm
#
#if [ ! -e /etc/%{name}/macros -a -e /etc/rpmrc -a -f %{rpmdir}/convertrpmrc.sh ] 
#then
#	sh %{rpmdir}/convertrpmrc.sh 2>&1 > /dev/null
#fi
#
#if [ -f /var/lib/%{name}/packages.rpm ]; then
#    /bin/chown %{name}:%{name} /var/lib/%{name}/*.rpm
#elif [ ! -f /var/lib/%{name}/Packages ]; then
#    /bin/%{name} --initdb
#fi

/bin/rm -f /var/lib/%{name}/__db.00?
/bin/chown -R %{name}:%{name} /var/lib/%{name}

%postun
/usr/share/rpm-helper/del-user %{name} $1 %{name}

%define	rpmattr %attr(0755,%{name},%{name})

%files
%defattr(-,root,root)
%doc GROUPS CHANGES doc/manual/[a-z]*
%attr(0755,%{name},%{name}) /bin/%{name}
%attr(0755,%{name},%{name}) %{_bindir}/gendiff44
%attr(0755,%{name},%{name}) %{_bindir}/rpm2cpio44
%attr(0755,%{name},%{name}) %{_bindir}/rpmdb44
%attr(0755,%{name},%{name}) %{_bindir}/rpme44
%attr(0755,%{name},%{name}) %{_bindir}/rpmgraph44
%attr(0755,%{name},%{name}) %{_bindir}/rpmi44
%attr(0755,%{name},%{name}) %{_bindir}/rpmquery44
%attr(0755,%{name},%{name}) %{_bindir}/rpmsign44
%attr(0755,%{name},%{name}) %{_bindir}/rpmu44
%attr(0755,%{name},%{name}) %{_bindir}/rpmverify44

%dir %{rpmdir}
%dir /etc/%{name}
%config(noreplace) /etc/%{name}/macros
%dir /etc/%{name}/macros.d
%attr(0755,%{name},%{name}) %{rpmdir}/config.guess
%attr(0755,%{name},%{name}) %{rpmdir}/config.sub
%attr(0755,%{name},%{name}) %{rpmdir}/rpmdb_*
%attr(0644,%{name},%{name}) %{rpmdir}/macros
%attr(0755,%{name},%{name}) %{rpmdir}/mkinstalldirs
%attr(0755,%{name},%{name}) %{rpmdir}/rpm.*
%attr(0755,%{name},%{name}) %{rpmdir}/rpm[deiukqv]
%attr(0644,%{name},%{name}) %{rpmdir}/rpmpopt*
%attr(0644,%{name},%{name}) %{rpmdir}/rpmrc

%{_prefix}/lib/rpmpopt44
%rpmattr %{rpmdir}/rpm2cpio.sh
%rpmattr %{rpmdir}/tgpg

%ifarch %{ix86} x86_64
%attr(-,%{name},%{name}) %{rpmdir}/i*86-*
%attr(-,%{name},%{name}) %{rpmdir}/athlon-*
%attr(-,%{name},%{name}) %{rpmdir}/pentium*-*
%attr(-,%{name},%{name}) %{rpmdir}/geode-*
%endif
%ifarch alpha
%attr(-,%{name},%{name}) %{rpmdir}/alpha*
%endif
%ifarch %{sunsparc}
%attr(-,%{name},%{name}) %{rpmdir}/sparc*
%endif
%ifarch ppc powerpc
%attr(-,%{name},%{name}) %{rpmdir}/ppc-*
%attr(-,%{name},%{name}) %{rpmdir}/ppc32-*
%attr(-,%{name},%{name}) %{rpmdir}/ppc64-*
%attr(-,%{name},%{name}) %{rpmdir}/powerpc-*
%endif
%ifarch ppc powerpc ppc64
%attr(-,%{name},%{name}) %{rpmdir}/ppc*series-*
%endif
%ifarch ppc64
%attr(-,%{name},%{name}) %{rpmdir}/ppc-*
%attr(-,%{name},%{name}) %{rpmdir}/ppc32-*
%attr(-,%{name},%{name}) %{rpmdir}/ppc64-*
%endif
%ifarch ia64
%attr(-,%{name},%{name}) %{rpmdir}/ia64-*
%endif
%ifarch x86_64
%attr(-,%{name},%{name}) %{rpmdir}/amd64-*
%attr(-,%{name},%{name}) %{rpmdir}/x86_64-*
%attr(-,%{name},%{name}) %{rpmdir}/ia32e-*
%endif
%attr(-,%{name},%{name}) %{rpmdir}/noarch*

%attr(0755,%{name},%{name})	%dir %_localstatedir/lib/%{name}

%define	rpmdbattr %attr(0644,%{name},%{name}) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)

%rpmdbattr /var/lib/%{name}/Basenames
%rpmdbattr /var/lib/%{name}/Conflictname
%rpmdbattr /var/lib/%{name}/__db.0*
%rpmdbattr /var/lib/%{name}/Dirnames
%rpmdbattr /var/lib/%{name}/Group
%rpmdbattr /var/lib/%{name}/Installtid
%rpmdbattr /var/lib/%{name}/Name
%rpmdbattr /var/lib/%{name}/Packages
%rpmdbattr /var/lib/%{name}/Providename
%rpmdbattr /var/lib/%{name}/Provideversion
%rpmdbattr /var/lib/%{name}/Removetid
%rpmdbattr /var/lib/%{name}/Requirename
%rpmdbattr /var/lib/%{name}/Requireversion
%rpmdbattr /var/lib/%{name}/Triggername

%files build
%defattr(-,root,root)
%doc CHANGES
%doc doc-copy/*
%{_prefix}/src/%{name}
%rpmattr %{_bindir}/rpmbuild44

%rpmattr %{_prefix}/lib/%{name}/brp-*
%rpmattr %{_prefix}/lib/%{name}/check-files
%rpmattr %{_prefix}/lib/%{name}/debugedit
%rpmattr %{_prefix}/lib/%{name}/find-debuginfo.sh
%rpmattr %{_prefix}/lib/%{name}/find-lang.sh
%rpmattr %{_prefix}/lib/%{name}/find-prov.pl
%rpmattr %{_prefix}/lib/%{name}/find-provides
%rpmattr %{_prefix}/lib/%{name}/find-provides.perl
%rpmattr %{_prefix}/lib/%{name}/find-req.pl
%rpmattr %{_prefix}/lib/%{name}/find-requires
%rpmattr %{_prefix}/lib/%{name}/find-requires.perl
%rpmattr %{_prefix}/lib/%{name}/getpo.sh
%rpmattr %{_prefix}/lib/%{name}/http.req
%rpmattr %{_prefix}/lib/%{name}/magic
%rpmattr %{_prefix}/lib/%{name}/magic.mgc
%rpmattr %{_prefix}/lib/%{name}/magic.mime
%rpmattr %{_prefix}/lib/%{name}/magic.mime.mgc
%rpmattr %{_prefix}/lib/%{name}/perldeps.pl
%rpmattr %{_prefix}/lib/%{name}/perl.prov
%rpmattr %{_prefix}/lib/%{name}/perl.req
%rpmattr %{_prefix}/lib/%{name}/check-buildroot
%rpmattr %{_prefix}/lib/%{name}/check-prereqs
%rpmattr %{_prefix}/lib/%{name}/check-rpaths
%rpmattr %{_prefix}/lib/%{name}/check-rpaths-worker
%rpmattr %{_prefix}/lib/%{name}/convertrpmrc.sh
%rpmattr %{_prefix}/lib/%{name}/freshen.sh
%rpmattr %{_prefix}/lib/%{name}/get_magic.pl
%rpmattr %{_prefix}/lib/%{name}/javadeps
%rpmattr %{_prefix}/lib/%{name}/magic.prov
%rpmattr %{_prefix}/lib/%{name}/magic.req
%rpmattr %{_prefix}/lib/%{name}/mono-find-provides
%rpmattr %{_prefix}/lib/%{name}/mono-find-requires
%rpmattr %{_prefix}/lib/%{name}/osgideps.pl
%rpmattr %{_prefix}/lib/%{name}/rpmcache
%rpmattr %{_prefix}/lib/%{name}/rpmdiff
%rpmattr %{_prefix}/lib/%{name}/rpmfile
%rpmattr %{_prefix}/lib/%{name}/rpm[bt]
%rpmattr %{_prefix}/lib/%{name}/rpmdeps
%rpmattr %{_prefix}/lib/%{name}/u_pkg.sh
%rpmattr %{_prefix}/lib/%{name}/vpkg-provides.sh
%rpmattr %{_prefix}/lib/%{name}/vpkg-provides2.sh
%rpmattr %{_prefix}/lib/%{name}/pythondeps.sh

%if %buildpython
%files -n python-rpm
%defattr(-,root,root)
%{_libdir}/python*/site-packages/rpm
%endif

%files -n %librpmname
%defattr(-,root,root)
%{_libdir}/librpm44-%{libver}.so
%{_libdir}/librpmdb44-%{libver}.so
%{_libdir}/librpmio44-%{libver}.so
%{_libdir}/librpmbuild44-%{libver}.so

%files -n %librpmnamedevel
%defattr(-,root,root)
%{_includedir}/rpm44
%{_libdir}/librpm44.la
%{_libdir}/librpm44.so
%{_libdir}/librpmdb44.la
%{_libdir}/librpmdb44.so
%{_libdir}/librpmio44.la
%{_libdir}/librpmio44.so
%{_libdir}/librpmbuild44.la
%{_libdir}/librpmbuild44.so
