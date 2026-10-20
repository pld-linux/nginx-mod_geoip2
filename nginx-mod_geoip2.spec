#
# Conditional build:
%bcond_without	stream		# stream (TCP/UDP) geoip2 module

%define		modname	ngx_http_geoip2_module

Summary:	Nginx GeoIP2 modules - IP geolocation from MaxMind DB (mmdb) files
Summary(pl.UTF-8):	Moduły GeoIP2 dla nginksa - geolokalizacja IP z plików MaxMind DB (mmdb)
Name:		nginx-mod_geoip2
Version:	3.4
Release:	2
License:	BSD
Group:		Daemons
#Source0Download: https://github.com/leev/ngx_http_geoip2_module/releases
Source0:	https://github.com/leev/ngx_http_geoip2_module/archive/%{version}/%{modname}-%{version}.tar.gz
# Source0-md5:	82d4beef48c260c3568eb0ae56451c95
URL:		https://github.com/leev/ngx_http_geoip2_module
BuildRequires:	libmaxminddb-devel
BuildRequires:	nginx-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nginx

%description
GeoIP2 modules for nginx.

%description -l pl.UTF-8
Moduły GeoIP2 dla nginksa.

%package -n nginx-mod_http_geoip2
Summary:	Nginx HTTP geoip2 module
Summary(pl.UTF-8):	Moduł HTTP geoip2 dla nginksa
Group:		Daemons
Requires:	nginx(modules-api) = %{nginx_modules_api}

%description -n nginx-mod_http_geoip2
Nginx HTTP geoip2 module. It reads MaxMind DB (.mmdb) files - the
GeoIP2 and GeoLite2 databases from MaxMind, or the DB-IP Lite
databases - and exposes the looked up fields as nginx variables, which
can then drive map, rate limiting, access rules or the log format.

The stock ngx_http_geoip_module reads only the retired GeoIP Legacy
(.dat) format, which MaxMind stopped publishing in 2019.

%description -n nginx-mod_http_geoip2 -l pl.UTF-8
Moduł HTTP geoip2 dla nginksa. Czyta pliki MaxMind DB (.mmdb) - bazy
GeoIP2 i GeoLite2 firmy MaxMind albo bazy DB-IP Lite - i udostępnia
odczytane pola jako zmienne nginksa, na których można oprzeć dyrektywę
map, ograniczanie ruchu, reguły dostępu czy format logu.

Standardowy ngx_http_geoip_module czyta wyłącznie wycofany format
GeoIP Legacy (.dat), którego MaxMind przestał publikować w 2019 roku.

%if %{with stream}
%package -n nginx-mod_stream_geoip2
Summary:	Nginx stream geoip2 module
Summary(pl.UTF-8):	Moduł stream geoip2 dla nginksa
Group:		Daemons
Requires:	nginx(modules-api) = %{nginx_modules_api}
Requires:	nginx-mod_stream

%description -n nginx-mod_stream_geoip2
Nginx stream geoip2 module. It reads MaxMind DB (.mmdb) files and
exposes the looked up fields as nginx variables in stream context.

%description -n nginx-mod_stream_geoip2 -l pl.UTF-8
Moduł stream geoip2 dla nginksa. Czyta pliki MaxMind DB (.mmdb) i
udostępnia odczytane pola jako zmienne nginksa w kontekście stream.
%endif

Moduł stream geoip2 dla nginksa. Czyta pliki MaxMind DB (.mmdb) i
udostępnia odczytane pola jako zmienne nginksa w kontekście stream.
%prep
%setup -q -n %{modname}-%{version}

%build
addon=$(pwd)

%{__mkdir_p} nginx-src
cp -a %{nginx_srcdir}/. nginx-src
cd nginx-src

# --with-compat on both sides makes NGX_MODULE_SIGNATURE match nginx's own build
./configure \
	--with-compat \
	--with-cc="%{__cc}" \
	%{?with_stream:--with-stream} \
	--with-cc-opt="%{rpmcflags} %{rpmcppflags}" \
	--with-ld-opt="%{rpmldflags}" \
	--add-dynamic-module="$addon"

%{__make} modules

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{nginx_moduledir},%{_sysconfdir}/modules.d}

install -p nginx-src/objs/ngx_http_geoip2_module.so $RPM_BUILD_ROOT%{nginx_moduledir}
printf 'load_module "%{nginx_moduledir}/ngx_http_geoip2_module.so";' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/modules.d/mod_http_geoip2.conf

%if %{with stream}
install -p nginx-src/objs/ngx_stream_geoip2_module.so $RPM_BUILD_ROOT%{nginx_moduledir}
printf 'load_module "%{nginx_moduledir}/ngx_stream_geoip2_module.so";' \
	> $RPM_BUILD_ROOT%{_sysconfdir}/modules.d/mod_stream_geoip2.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%nginx_module_scripts nginx-mod_http_geoip2

%if %{with stream}
%nginx_module_scripts nginx-mod_stream_geoip2
%endif

%files -n nginx-mod_http_geoip2
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_http_geoip2.conf
%attr(755,root,root) %{nginx_moduledir}/ngx_http_geoip2_module.so

%if %{with stream}
%files -n nginx-mod_stream_geoip2
%defattr(644,root,root,755)
%doc LICENSE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules.d/mod_stream_geoip2.conf
%attr(755,root,root) %{nginx_moduledir}/ngx_stream_geoip2_module.so
%endif
