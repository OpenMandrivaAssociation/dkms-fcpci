%define module fcpci
%define version 3.11.07
%define card "AVM Audiovisuelles|A1 ISDN Adapter [Fritz] CAPI"

Summary: dkms package for %{module} driver
Name: dkms-%{module}
Version: %{version}
Release: 11
Source0: ftp://ftp.avm.de/cardware/fritzcrd.pci/linux/suse.93/fcpci-suse93-3.11-07.tar.bz2
Source1: dkms-fcpci-use-autoconf-header.patch
Source2: dkms-fcpci-use-pci_register_driver.patch
Source3: dkms-fcpci-update-irq-flags.patch
Source4: dkms-fcpci-update-irq_handler-definition.patch
Source5: dkms-fcpci-2.6.31-buildfix.patch
Source6: dkms-fcpci-2.6.33-buildfix.patch
Source7: dkms-fcpci-2.6.34-buildfix.patch
Patch0: fritz-xchg.patch
Patch1: fritz-rename-driver-init-exit.patch
Patch2: fritz-use-lib_strncpy.patch
License: Commercial
Group: System/Kernel and hardware
URL: http://www.avm.de/
Requires(post): dkms
Requires(preun): dkms
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

%description
This package contains the %{module} driver for %{card}

%prep
%setup -n fritz/src -q
%patch0 -p2
%patch1 -p2
%patch2 -p2
# copy the lib in the source tree, do not use some obscure place like /var/lib/fritz
cp ../lib/*.o .
# do not try to copy the lib in LIBDIR
perl -pi -e 's!.*cp -f \.\./lib.*!!' Makefile
# fool Makefile by using a already existing LIBDIR
perl -pi -e 's!(LIBDIR.*):=.*!$1:= \$(SUBDIRS)!' Makefile
#- dkms pass KERNELRELEASE and confuse the Makefile, rely on KERNELVERSION instead
perl -pi -e 's!(ifneq.*)KERNELRELEASE!$1KERNELVERSION!' Makefile
#- build for kernel release dkms is asking for
perl -pi -e 's!shell uname -r!KERNELRELEASE!' Makefile

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/src/%module-%version-%release/patches
cat > $RPM_BUILD_ROOT/usr/src/%module-%version-%release/dkms.conf <<EOF
PACKAGE_NAME=%module
PACKAGE_VERSION=%version-%release

DEST_MODULE_LOCATION[0]=/kernel/drivers/isdn/capi
BUILT_MODULE_NAME[0]=%module
MAKE[0]="make"
CLEAN="make clean"
AUTOINSTALL="yes"
PATCH[0]="dkms-fcpci-use-autoconf-header.patch"
PATCH_MATCH[0]="^2\.6\.(19)|([2-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[1]="dkms-fcpci-use-pci_register_driver.patch"
PATCH_MATCH[1]="^2\.6\.(2[2-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[2]="dkms-fcpci-update-irq-flags.patch"
PATCH_MATCH[2]="^2\.6\.(2[4-9])|([3-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[3]="dkms-fcpci-update-irq_handler-definition.patch"
PATCH_MATCH[3]="^2\.6\.(19)|([2-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[4]="dkms-fcpci-2.6.31-buildfix.patch"
PATCH_MATCH[4]="^2\.6\.(3[1-9])|([4-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[5]="dkms-fcpci-2.6.33-buildfix.patch"
PATCH_MATCH[5]="^2\.6\.(3[3-9])|([4-9][0-9]+)|([1-9][0-9][0-9]+)"
PATCH[6]="dkms-fcpci-2.6.34-buildfix.patch"
PATCH_MATCH[6]="^2\.6\.(3[4-9])|([4-9][0-9]+)|([1-9][0-9][0-9]+)"
EOF

tar c . | tar x -C $RPM_BUILD_ROOT/usr/src/%module-%version-%release/

for p in %{_sourcedir}/dkms-fcpci-use-autoconf-header.patch \
         %{_sourcedir}/dkms-fcpci-use-pci_register_driver.patch \
         %{_sourcedir}/dkms-fcpci-update-irq-flags.patch \
         %{_sourcedir}/dkms-fcpci-update-irq_handler-definition.patch \
         %{_sourcedir}/dkms-fcpci-2.6.31-buildfix.patch \
         %{_sourcedir}/dkms-fcpci-2.6.33-buildfix.patch \
         %{_sourcedir}/dkms-fcpci-2.6.34-buildfix.patch ;
do
	cp $p $RPM_BUILD_ROOT/usr/src/%module-%version-%release/patches
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
/usr/src/%module-%version-%release/

%post
/usr/sbin/dkms --rpm_safe_upgrade add -m %module -v %version-%release
/usr/sbin/dkms --rpm_safe_upgrade build -m %module -v %version-%release
/usr/sbin/dkms --rpm_safe_upgrade install -m %module -v %version-%release
exit 0

%preun
/usr/sbin/dkms --rpm_safe_upgrade remove -m %module -v %version-%release --all
exit 0

