%define		major	1
%define		minor	0
%define		micro	%{nil}
%define		type	REC
%define		year	2000
%define		month	01
%define		day	26

%define		mver	%{major}
%define		ver	%{major}%{minor}%{micro}
%define		v_er	%{major}.%{minor}%{micro}
%define		v__er	%{major}\.%{minor}%{micro}
Summary:	XHTML %{v_er}
Summary(pl):	XHTML %{v_er}
Name:		xhtml-dtd%{ver}-xml
Version:	%{year}%{month}%{day}
Release:	2
Group:		Applications/Publishing/SGML
License:	W3C
Vendor:		W3C
Source0:	http://www.w3.org/TR/%{year}/%{type}-xhtml%{mver}-%{version}/xhtml%{mver}.tgz
# Source0-md5:	a9ab373670f55fd50ce1e6c75261b75d
URL:		http://www.w3.org/TR/xhtml%{mver}/
Requires:	sgml-common >= 0.6.3-5
Requires:	sgmlparser
Requires(post):	/usr/bin/xmlcatalog
Requires(post):	sgml-common >= 0.5
Requires(preun):/usr/bin/xmlcatalog
Requires(preun):sgml-common >= 0.5
Provides:	xhtml-dtd
AutoReqProv:	no
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		catalog		%{_datadir}/sgml/html/xml-dtd-%{v_er}/xmlcatalog-%{v_er}-%{version}-%{release}

%description
XHTML specification (with DTD, needed to parse XHTML code).

%description -l pl
Specyfikacja XHTML (wraz z DTD, potrzebnym do sprawdzania poprawno¶ci
kodu XHTML).

%prep
%setup -q -n xhtml%{mver}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/html/xml-dtd-%{v_er}

xmlcatalog --noout --create $RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout --add rewriteSystem \
	'http://www.w3.org/TR/xhtml1/DTD/' \
	'/usr/share/sgml/html/xml-dtd-%{v_er}/' \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//DTD XHTML 1.0 Strict//EN" \
	xhtml1-strict.dtd \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//DTD XHTML 1.0 Transitional//EN" \
	xhtml1-transitional.dtd \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//DTD XHTML 1.0 Frameset//EN" \
	xhtml1-frameset.dtd \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//ENTITIES Latin 1 for XHTML//EN" \
	"xhtml-lat1.ent" \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//ENTITIES Symbols for XHTML//EN" \
	"xhtml-symbol.ent" \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//ENTITIES Special for XHTML//EN" \
	"xhtml-special.ent" \
	$RPM_BUILD_ROOT%{catalog}

install DTD/* $RPM_BUILD_ROOT%{_datadir}/sgml/html/xml-dtd-%{v_er}

# make symlink for minimizing file duplication and make documentation working
rm -rf DTD
ln -s ../../sgml/html/xml-dtd-%{v_er}/ DTD

%post
/usr/bin/install-catalog --add /etc/sgml/xhtml-%{v_er}-%{version}-%{release}.cat /usr/share/sgml/html/xml-dtd-%{v_er}/xhtml.soc > /dev/null
/usr/bin/xmlcatalog --noout --add nextCatalog xhtml %{catalog} /etc/xml/catalog

%preun
/usr/bin/install-catalog --remove /etc/sgml/xhtml-%{v_er}-%{version}-%{release}.cat /usr/share/sgml/html/xml-dtd-%{v_er}/xhtml.soc > /dev/null
/usr/bin/xmlcatalog --noout --del %{catalog} /etc/xml/catalog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *
%{_datadir}/sgml/html/*
