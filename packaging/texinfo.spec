#
# Please submit bugfixes or comments via http://bugs.meego.com/
#

%define tex_texinfo %{_datadir}/texmf/tex/texinfo

Name:           texinfo
Version:        4.13a
Release:        7
License:        GPLv3+
Summary:        Tools needed to create Texinfo format documentation files
Url:            http://www.gnu.org/software/texinfo/
Group:          Applications/Publishing
Source0:        ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz
Source1:        info-dir
Source2:        texi2pdf.man
Patch0:         texinfo-4.12-zlib.patch
Patch1:         texinfo-4.13a-data_types.patch
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(zlib),
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary:        A stand-alone TTY-based reader for GNU texinfo documentation
Group:          System/Base

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

%package tex
Summary:        Tools for formatting Texinfo documentation files using TeX
Group:          Applications/Publishing
#Requires:       tetex
Requires:       texinfo = %{version}
Requires(post): %{_bindir}/texconfig-sys
Requires(postun): %{_bindir}/texconfig-sys

%description tex
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

The texinfo-tex package provides tools to format Texinfo documents
for printing using TeX.

%prep
%setup -q -n %{name}-4.13
%patch0 -p1 -b .zlib
%patch1 -p1 -b .data_types

%build
%configure
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/sbin

make install DESTDIR=%{buildroot} INSTALL='install -p'

mkdir -p %{buildroot}%{tex_texinfo}
install -p -m644 doc/texinfo.tex doc/txi-??.tex %{buildroot}%{tex_texinfo}

install -p -m644 %{SOURCE2} %{buildroot}%{_mandir}/man1/texi2pdf.1
install -p -m644 %{SOURCE1} %{buildroot}%{_infodir}/dir
mv %{buildroot}%{_bindir}/install-info %{buildroot}/sbin

# Convert ChangeLog to UTF-8
/usr/bin/iconv -f iso-8859-2 -t utf-8 < ChangeLog > ChangeLog_utf8
touch -r ChangeLog ChangeLog_utf8
mv ChangeLog_utf8 ChangeLog

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
if [ -f %{_infodir}/texinfo ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/texinfo %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/texinfo ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/texinfo %{_infodir}/dir || :
    fi
fi

%post -n info
if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/info-stnd.info %{_infodir}/dir
fi
if [ -x /bin/sed ]; then
    /bin/sed -i '/^This is.*produced by makeinfo.*from/d' %{_infodir}/dir || :
fi

%preun -n info
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/info-stnd.info %{_infodir}/dir \
        || :
    fi
fi

%post tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :


%docs_package

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/makeinfo
%{_datadir}/texinfo
%{_infodir}/texinfo*

%files -n info
%defattr(-,root,root,-)
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
%doc COPYING
%{_bindir}/info
%{_bindir}/infokey
/sbin/install-info

%files tex
%defattr(-,root,root)
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{tex_texinfo}/*

