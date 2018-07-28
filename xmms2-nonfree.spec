%global codename DrO_o

Name:			xmms2-nonfree
Summary:		Nonfree plugins for XMMS2
Version:		0.8
Release:		13%{?dist}
License:		LGPLv2+
URL:			http://wiki.xmms2.xmms.se/
Group:			Applications/Multimedia
# Fedora's xmms2 has to use a sanitized tarball, we don't.
Source0:		http://downloads.sourceforge.net/xmms2/xmms2-%{version}%{codename}.tar.bz2
# Use libdir properly for Fedora multilib
Patch0:			xmms2-0.8DrO_o-use-libdir.patch
# Don't add extra CFLAGS, we're smart enough, thanks.
Patch1:			xmms2-0.8DrO_o-no-O0.patch
Patch2:			fix_vorbis_dso.patch
Patch3:			mac_abi_change.patch

BuildRequires:	sqlite-devel
BuildRequires:	glib2-devel
BuildRequires:	python2-devel
# RPMFusion only BuildRequires
BuildRequires:	mac-devel

Requires:		xmms2-mac = %{version}-%{release}
Obsoletes:		xmms2-sid < %{version}-%{release}

%description
XMMS2 is an audio framework, but it is not a general multimedia player - it 
will not play videos. It has a modular framework and plugin architecture for 
audio processing, visualisation and output, but this framework has not been 
designed to support video. Also the client-server design of XMMS2 (and the 
daemon being independent of any graphics output) practically prevents direct 
video output being implemented. It has support for a wide range of audio 
formats, which is expandable via plugins. It includes a basic CLI interface 
to the XMMS2 framework, but most users will want to install a graphical XMMS2 
client (such as gxmms2 or esperanza).

%package -n xmms2-mac
Summary:	XMMS2 plugin for APE audio format
Group:		Applications/Multimedia
License:	LGPLv2+
Requires:	xmms2 = %{version}
Obsoletes:	xmms2-nonfree-mac < 0.6-4
Provides:	xmms2-nonfree-mac = %{version}-%{release}

%description -n xmms2-mac
This package contains an XMMS2 Plugin for listening to Monkey's Audio files.


%prep
%setup -q -n xmms2-%{version}%{codename}

%patch0 -p1 -b .plugins-use-libdir
%patch1 -p1 -b .noO0
%patch2 -p1 -b .fix_vorbis_dso
%patch3 -p1 -b .mac_abi_change

# For some reasons RPMFusion's sidplay libraries are moved to a
# non-standard location. xmms2 can't detect this unless:
sed -i 's|\[builders\]|\["%{_libdir}/sidplay/builders"\]|' src/plugins/sid/wscript

for i in doc/tutorial/python/tut1.py doc/tutorial/python/tut2.py doc/tutorial/python/tut3.py doc/tutorial/python/tut4.py doc/tutorial/python/tut5.py doc/tutorial/python/tut6.py utils/gen-tree-hashes.py utils/gen-wiki-release-bugs.py utils/gen-tarball.py utils/gen-wiki-release-authors.py waf waftools/podselect.py waftools/genipc.py waftools/genipc_server.py waftools/cython.py; do
	sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python2|g' $i
done


# add configure to export build flags
touch configure
chmod a+x configure

%build
%configure
./waf configure --prefix=%{_prefix} \
		--libdir=%{_libdir} \
		--with-pkgconfigdir=%{_libdir}/pkgconfig \
		--without-optionals=et \
		--without-optionals=launcher \
		--without-optionals=medialib-updater \
		--without-optionals=perl \
		--without-optionals=pixmaps \
		--without-optionals=python \
		--without-optionals=ruby \
		--without-optionals=xmmsclient-ecore \
		--without-optionals=xmmsclient++ \
		--without-optionals=xmmsclient++-glib \
		--without-plugins=airplay \
		--without-plugins=alsa \
		--without-plugins=ao \
		--without-plugins=apefile \
		--without-plugins=asf \
		--without-plugins=asx \
		--without-plugins=cdda \
		--without-plugins=cue \
		--without-plugins=curl \
		--without-plugins=daap \
		--without-plugins=diskwrite \
		--without-plugins=equalizer \
		--without-plugins=curl \
		--without-plugins=file \
		--without-plugins=flac \
		--without-plugins=flv \
		--without-plugins=gme \
		--without-plugins=gvfs \
		--without-plugins=html \
		--without-plugins=ices \
		--without-plugins=icymetaint \
		--without-plugins=id3v2 \
		--without-plugins=jack \
		--without-plugins=karaoke \
		--without-plugins=m3u \
		--without-plugins=modplug \
		--without-plugins=musepack \
		--without-plugins=normalize \
		--without-plugins=null \
		--without-plugins=nulstripper \
		--without-plugins=ofa \
		--without-plugins=oss \
		--without-plugins=pls \
		--without-plugins=pulse \
		--without-plugins=replaygain \
		--without-plugins=rss \
		--without-plugins=samba \
		--without-plugins=speex \
		--without-plugins=tta \
		--without-plugins=vocoder \
		--without-plugins=vorbis \
		--without-plugins=wave \
		--without-plugins=xml \
		--without-plugins=xspf \
		--without-plugins=avcodec \
		--without-plugins=faad \
		--without-plugins=mad \
		--without-plugins=mms \
		--without-plugins=mp4

./waf build -v %{?_smp_mflags}

%install
./waf install \
	--destdir=%{buildroot} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--with-pkgconfigdir=%{_libdir}/pkgconfig

# There are lots of things that get built that we don't need
# to package, because they're in the Fedora xmms2 package.
rm -rf %{buildroot}%{_bindir} \
	%{buildroot}%{_libdir}/libxmmsclient* \
	%{buildroot}%{_mandir} \
	%{buildroot}%{_datadir} \
	%{buildroot}%{_includedir} \
	%{buildroot}%{_libdir}/pkgconfig 

# exec flags for debuginfo
chmod +x %{buildroot}%{_libdir}/xmms2/*


%files

%files -n xmms2-mac
%license COPYING.GPL COPYING.LGPL
%{_libdir}/xmms2/libxmms_mac.so

%changelog
* Sat Jul 28 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 19 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.8-11
- Fix build flags so debug packages are generated

* Fri Sep 01 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.8-10
- Disable debuginfo

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.8-7
- fix mac ABI breakage

* Tue Jan 06 2015 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.8-6
- Drop sid support RFBZ#2764

* Mon Aug 25 2014 Leigh Scott <leigh123linux@googlemail.com> - 0.8-5
- Fix vorbis DSO build failure

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.8-4
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 John Doe <anonymous@american.us> 0.8-1
- Update to 0.8

* Thu Jul 01 2010 John Doe <anonymous@american.us> 0.7-1
- Update to 0.7

* Sun Oct 25 2009 John Doe <anonymous@american.us> 0.6-4
- Rename subpackages to fix broken deps (RFBZ#894)

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.6-3
- rebuild for new ffmpeg

* Tue Aug 25 2009 John Doe <anonymous@american.us> 0.6-2
- Include sid plugin
- Separate plugin subpackages. The main package is made a meta package.

* Wed Aug 12 2009 John Doe <anonymous@american.us> 0.6-1
- Update to 0.6

* Thu Apr 09 2009 John Doe <anonymous@american.us> 0.5-3
- License is LGPLv2+
- Some SPEC file cosmetics

* Wed Apr 08 2009 John Doe <anonymous@american.us> 0.5-2
- Kill the -mac subpackage

* Wed Apr 08 2009 John Doe <anonymous@american.us> 0.5-1
- Initial package for RPMFusion (SPEC file is a slightly 
  modified version of xmms2-freeworld)
