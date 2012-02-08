%global codename DrO_o

Name:			xmms2-nonfree
Summary:		Nonfree plugins for XMMS2
Version:		0.8
Release:		2%{?dist}
License:		LGPLv2+ and GPLv2+
Group:			Applications/Multimedia
# Fedora's xmms2 has to use a sanitized tarball, we don't.
Source0:		http://downloads.sourceforge.net/xmms2/xmms2-%{version}%{codename}.tar.bz2
# Use libdir properly for Fedora multilib
Patch0:			xmms2-0.8DrO_o-use-libdir.patch
# Don't add extra CFLAGS, we're smart enough, thanks.
Patch1:			xmms2-0.8DrO_o-no-O0.patch

URL:			http://wiki.xmms2.xmms.se/
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:		sqlite-devel
BuildRequires:		glib2-devel
BuildRequires:		python-devel
# RPMFusion only BuildRequires
BuildRequires:		mac-devel
BuildRequires:		sidplay-libs-devel

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

%package -n xmms2-mac
Summary:	XMMS2 plugin for APE audio format
Group:		Applications/Multimedia
License:	LGPLv2+
Requires:	xmms2 = %{version}
Obsoletes:	xmms2-nonfree-mac < 0.6-4
Provides:	xmms2-nonfree-mac = %{version}-%{release}

%description -n xmms2-mac
This package contains an XMMS2 Plugin for listening to Monkey's Audio files.

%package -n xmms2-sid
Summary:	XMMS2 plugin for SID audio format
Group:		Applications/Multimedia
License:	GPLv2+
Requires:	xmms2 = %{version}
Obsoletes:	xmms2-nonfree-sid < 0.6-4
Provides:	xmms2-nonfree-sid = %{version}-%{release}

%description -n xmms2-sid
This package contains an XMMS2 Plugin for listening to C64 mono and stereo file
formats.


%prep
%setup -q -n xmms2-%{version}%{codename}

%patch0 -p1 -b .plugins-use-libdir
%patch1 -p1 -b .noO0

# For some reasons RPMFusion's sidplay libraries are moved to a
# non-standard location. xmms2 can't detect this unless:
sed -i 's|\[builders\]|\["%{_libdir}/sidplay/builders"\]|' src/plugins/sid/wscript

%build
export CFLAGS="%{optflags}"
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
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING.GPL COPYING.LGPL

%files -n xmms2-mac
%defattr(-,root,root,-)
%doc COPYING.LGPL
%{_libdir}/xmms2/libxmms_mac.so

%files -n xmms2-sid
%defattr(-,root,root,-)
%doc COPYING.GPL
%{_libdir}/xmms2/libxmms_sid.so

%changelog
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
