%global codename DrMattDestruction

Name:			xmms2-nonfree
Summary:		Nonfree plugins for XMMS2
Version:		0.6
Release:		3%{?dist}
License:		LGPLv2+ and GPLv2+
Group:			Applications/Multimedia
# Fedora's xmms2 has to use a sanitized tarball, we don't.
Source0:		http://downloads.sourceforge.net/xmms2/xmms2-%{version}%{codename}.tar.bz2
# Use libdir properly for Fedora multilib
Patch1:			xmms2-0.6DrMattDestruction-use-libdir.patch

# Don't add extra CFLAGS, we're smart enough, thanks.
Patch4:			xmms2-0.5DrLecter-no-O0.patch
# More sane versioning
Patch5:			xmms2-0.6DrMattDestruction-moresaneversioning.patch

URL:			http://wiki.xmms2.xmms.se/
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:		sqlite-devel
BuildRequires:		glib2-devel
BuildRequires:		python-devel
# RPMFusion only BuildRequires
BuildRequires:		mac-devel
BuildRequires:		sidplay-libs-static

Requires:		xmms2-mac = %{version}-%{release}
Requires:		xmms2-sid = %{version}-%{release}


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

%package mac
Summary:	XMMS2 plugin for APE audio format
Group:		Applications/Multimedia
License:	LGPLv2+
Requires:	xmms2 = %{version}

%description mac
This package contains an XMMS2 Plugin for listening to Monkey's Audio files.

%package sid
Summary:	XMMS2 plugin for SID audio format
Group:		Applications/Multimedia
License:	GPLv2+
Requires:	xmms2 = %{version}

%description sid
This package contains an XMMS2 Plugin for listening to C64 mono and stereo file
formats.


%prep
%setup -q -n xmms2-%{version}%{codename}

%patch1 -p1 -b .plugins-use-libdir

%patch4 -p1 -b .noO0
%patch5 -p1 -b .versionsanity


# Clean up paths in wafadmin
WAFADMIN_FILES=`find wafadmin/ -type f`
for i in $WAFADMIN_FILES; do
	 sed -i 's|/usr/lib|%{_libdir}|g' $i
done

# For some reasons RPMFusion's sidplay libraries are moved to a
# non-standard location. xmms2 can't detect this unless:
sed -i 's|\[builders\]|\["%{_libdir}/sidplay/builders"\]|' src/plugins/sid/wscript

%build
export CFLAGS="%{optflags}"
./waf configure --prefix=%{_prefix} \
		--with-libdir=%{_libdir} \
		--with-pkgconfigdir=%{_libdir}/pkgconfig \
		--without-optionals=avahi \
		--without-optionals=cli \
		--without-optionals=dns_sd \
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
rm -rf %{buildroot}
./waf install \
	--destdir=%{buildroot} \
	--prefix=%{_prefix} \
	--with-libdir=%{_libdir} \
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING.GPL COPYING.LGPL

%files mac
%defattr(-,root,root,-)
%doc COPYING.LGPL
%{_libdir}/xmms2/libxmms_mac.so

%files sid
%defattr(-,root,root,-)
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_sid.so

%changelog
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
