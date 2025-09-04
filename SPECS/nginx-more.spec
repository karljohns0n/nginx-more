%global packagename			nginx
%global nginx_user			nginx
%global nginx_group			%{nginx_user}
%global nginx_home			%{_localstatedir}/lib/nginx
%global nginx_home_cache	%{nginx_home}/cache
%global nginx_logdir		%{_localstatedir}/log/nginx
%global nginx_confdir		%{_sysconfdir}/nginx
%global nginx_datadir		%{_datadir}/nginx
%global nginx_webroot		%{nginx_datadir}/html
%global gcc_version			8
%global pcre_version		pcre2
%global openssl_version		3.5.2
%global module_ps_version	1.13.35.2
%global module_ps_commit		13bee9d
%global module_psol		%{module_ps_version}-x64
%global module_headers_more	0.39
%global module_cache_purge	2.3
%global module_vts		0.2.4
%global module_brotli		1.0.0rc-2-g6e97
%global module_brotli_deps	1.0.9-35-gf4153a0
%global module_geoip2		3.4
%global module_echo		0.63
%global module_modsecurity	1.0.4

%global module_dir_openssl		openssl-%{openssl_version}
%global module_dir_pagespeed		ngx_pagespeed-%{module_ps_version}
%global module_dir_pagespeed_psol	%{module_dir_pagespeed}/psol
%global module_dir_headers_more		ngx_headers_more-%{module_headers_more}
%global module_dir_cache_purge		ngx_cache_purge-%{module_cache_purge}
%global module_dir_brotli		ngx_brotli-%{module_brotli}
%global module_dir_brotli_deps		ngx_brotli-%{module_brotli}/deps/brotli
%global module_dir_vts			ngx_module_vts-%{module_vts}
%global module_dir_http_geoip2 		ngx_http_geoip2_module-%{module_geoip2}
%global module_dir_echo			ngx_echo-%{module_echo}
%global module_dir_modsecurity		ngx_modsecurity-%{module_modsecurity}

%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%bcond_with					modsecurity
%bcond_with					pagespeed

Name:						nginx-more
Version:					1.29.1
Release:					1%{?dist}

Summary:					A high performance web server and reverse proxy server
Group:						System Environment/Daemons
License:					2-clause BSD-like license
URL:						http://nginx.org/
BuildRoot:					%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:					https://nginx.org/download/nginx-%{version}.tar.gz
Source1:					nginx.service
Source2:					nginx.init
Source3:					nginx.logrotate
Source4:					nginx.conf
Source5:					nginx.upgrade.sh
Source6:					nginx.check-reload.sh
Source7:					nginx.pagespeed.conf

Source10:					fpm-default.conf
Source11:					fpm-wordpress-cache.conf
Source12:					fpm-wordpress.conf
Source13:					fpm-wordpress-mu.conf
Source14:					fpm-laravel.conf
Source15:					restrictions.conf
Source16:					admin-ips.conf
Source17:					virtual.conf-example
Source18:					ssl.conf-example
Source19:					aerisnetwork-ips
Source20:					cloudflare.conf
Source21:					pagespeed.conf
Source22:					fpm-prestashop.conf
Source23:					fpm-opencart.conf
Source24:					fpm-drupal.conf
Source25:					blacklist.conf
Source26:					fpm-default-users.conf
Source27:					fpm-laravel-users.conf
Source28:					fpm-wordpress-users.conf
Source29:					fpm-sendy.conf
Source30:					fpm-sendy-users.conf
Source31:					restrictions-users.conf
Source32:					fpm-wordpress-mu-users.conf
Source33:					fpm-wordpress-cache-users.conf
Source34:					fpm-wordpress-mu-cache-users.conf
Source35:					fpm-wordpress-mu-cache.conf
Source36:					fpm-wordpress-sub.conf
Source37:					fpm-wordpress-sub-users.conf
Source38:					fpm-wordpress-sub-cache.conf
Source39:					fpm-wordpress-sub-cache-users.conf
Source40:					mailgun-tracking.conf


# Module sources
# https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/#_git_tags
# https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/#_troublesome_urls
Source100:					https://github.com/openssl/openssl/releases/download/openssl-%{openssl_version}/openssl-%{openssl_version}.tar.gz
Source101:					https://github.com/apache/incubator-pagespeed-ngx/archive/%{module_ps_commit}/ngx_pagespeed-%{module_ps_version}.tar.gz
Source102:					https://dl.google.com/dl/page-speed/psol/%{module_psol}.tar.gz#/psol-%{module_psol}.tar.gz
Source103:					https://github.com/openresty/headers-more-nginx-module/archive/v%{module_headers_more}/ngx_headers_more-%{module_headers_more}.tar.gz
Source104:					https://github.com/FRiCKLE/ngx_cache_purge/archive/%{module_cache_purge}/ngx_cache_purge-%{module_cache_purge}.tar.gz
Source105:					https://github.com/google/ngx_brotli/archive/v%{module_brotli}/ngx_brotli-%{module_brotli}.tar.gz
Source106:					https://github.com/vozlt/nginx-module-vts/archive/v%{module_vts}/ngx_module_vts-%{module_vts}.tar.gz
Source107:					https://github.com/leev/ngx_http_geoip2_module/archive/%{module_geoip2}/ngx_http_geoip2_module-%{module_geoip2}.tar.gz
Source108:					https://github.com/openresty/echo-nginx-module/archive/v%{module_echo}/ngx_echo-%{module_echo}.tar.gz
Source109:					https://github.com/owasp-modsecurity/ModSecurity-nginx/archive/v%{module_modsecurity}/ngx_modsecurity-%{module_modsecurity}.tar.gz
Source110:					https://github.com/google/brotli/archive/v%{module_brotli_deps}/ngx_brotli_deps-%{module_brotli_deps}.tar.gz

Patch0:						nginx-version.patch
Patch1:						ngx_cache_purge-fix-compatibility-with-nginx-1.11.6.patch
Patch3:						ngx_dynamic-tls-records-1.27.5.patch
Patch4:						ngx_cache_purge-fix-compatibility-with-nginx-1.19.3.patch


BuildRequires:				libxslt-devel
BuildRequires:				%{pcre_version}
BuildRequires:				%{pcre_version}-devel
BuildRequires:				zlib-devel
BuildRequires:				gd-devel
BuildRequires:				httpd-devel
BuildRequires:				libuuid-devel
BuildRequires:				libmaxminddb-devel
BuildRequires:				perl-IPC-Cmd
BuildRequires:				perl-Data-Dumper
BuildRequires:				gcc
BuildRequires:				make

%if 0%{?rhel} == 6
BuildRequires:				devtoolset-%{gcc_version}-gcc-c++ devtoolset-%{gcc_version}-binutils
%endif

%if 0%{?rhel} == 7
BuildRequires:				devtoolset-%{gcc_version}-gcc-c++ devtoolset-%{gcc_version}-binutils
BuildRequires:				GeoIP-devel
%endif

%if 0%{?rhel} == 8
BuildRequires:				GeoIP-devel perl-Getopt-Long
%endif

%if 0%{?rhel} == 9
BuildRequires:				perl-File-Compare perl-File-Copy perl-FindBin perl-Getopt-Long perl-IPC-Cmd perl-lib
%endif

%if 0%{?rhel} == 10
BuildRequires:				perl-File-Compare perl-File-Copy perl-FindBin perl-Getopt-Long perl-IPC-Cmd perl-lib
%endif

Requires:					gd
Requires:					%{pcre_version}
Requires:					procps-ng
Requires(pre):				shadow-utils

%if %{use_systemd}
BuildRequires:				systemd
Requires(post):				systemd
Requires(preun):			systemd
Requires(postun):			systemd
%else
Requires(post):				chkconfig
Requires(preun):			chkconfig, initscripts
Requires(postun):			initscripts
%endif

%if %{with pagespeed}
BuildRequires:				gcc-c++
%endif

%if %{with modsecurity}
%package module-modsecurity
Summary:					Nginx ModSecurity module
BuildRequires:				libmodsecurity-devel
Requires:					nginx-more = %{version}-%{release}

%description module-modsecurity
%{summary}.
%endif

Conflicts:					nginx

Provides:					webserver
Provides:					nginx

%description
Nginx-more is a build of Nginx with additional open source modules
such as PageSpeed, More Headers, Cache Purge, virtual host traffic status,
GeoIP2. It's compiled using recent GCC version and latest OpenSSL sources.
It also includes built-in configurations such as WordPress/Laravel php-fpm
setup, bad user-agents blocking, TCP_FASTOPEN, Cloudflare IPs, and more.

Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.


%prep
%setup -q -n %{packagename}-%{version}

%define source_prepare() (mkdir -p %2 && tar -zxvf %1 --strip-components=1 --no-same-owner -C %2)

%source_prepare %{SOURCE100} modules/%{module_dir_openssl}

%if %{with pagespeed}
	%source_prepare %{SOURCE101} modules/%{module_dir_pagespeed}
	%source_prepare %{SOURCE102} modules/%{module_dir_pagespeed_psol}
%endif
%source_prepare %{SOURCE103} modules/%{module_dir_headers_more}
%source_prepare %{SOURCE104} modules/%{module_dir_cache_purge}
%source_prepare %{SOURCE105} modules/%{module_dir_brotli}
%source_prepare %{SOURCE110} modules/%{module_dir_brotli_deps}
%source_prepare %{SOURCE106} modules/%{module_dir_vts}
%source_prepare %{SOURCE107} modules/%{module_dir_http_geoip2}
%source_prepare %{SOURCE108} modules/%{module_dir_echo}

%if %{with modsecurity}
	%source_prepare %{SOURCE109} modules/%{module_dir_modsecurity}
%endif

%{__sed} -i 's_@CACHEPVER@_%{module_cache_purge}_' %{PATCH1}
%{__sed} -i 's_@CACHEPVER@_%{module_cache_purge}_' %{PATCH4}

%patch0 -p0
%patch1 -p0
%patch3 -p1
%patch4 -p0

%build
export DESTDIR=%{buildroot}

# As we're using PSOL binary, set PSOL_BUILDTYPE so that nginx build does not trigger the interactive prompt about debugging
# https://github.com/apache/incubator-pagespeed-ngx/issues/1377#issuecomment-549804871
export PSOL_BUILDTYPE=Release

./configure \
	--prefix=%{nginx_datadir} \
	--sbin-path=%{_sbindir}/nginx \
	--modules-path=%{_libdir}/nginx/modules \
	--conf-path=%{nginx_confdir}/nginx.conf \
	--error-log-path=%{nginx_logdir}/error.log \
	--http-log-path=%{nginx_logdir}/access.log \
	--http-client-body-temp-path=%{nginx_home_cache}/client_body \
	--http-proxy-temp-path=%{nginx_home_cache}/proxy \
	--http-fastcgi-temp-path=%{nginx_home_cache}/fastcgi \
	--http-uwsgi-temp-path=%{nginx_home_cache}/uwsgi \
	--http-scgi-temp-path=%{nginx_home_cache}/scgi \
	--pid-path=%{_localstatedir}/run/nginx.pid \
	--lock-path=%{_localstatedir}/run/nginx.lock \
	--user=%{nginx_user} \
	--group=%{nginx_group} \
	--with-compat \
	--with-file-aio \
	--with-http_ssl_module \
	--with-http_realip_module \
	--with-http_addition_module \
	--with-http_image_filter_module \
	--with-http_sub_module \
	--with-http_dav_module \
	--with-http_flv_module \
	--with-http_mp4_module \
	--with-http_gunzip_module \
	--with-http_gzip_static_module \
	%if 0%{?rhel} == 7 || 0%{?rhel} == 8
		--with-http_geoip_module \
	%endif
	--with-http_random_index_module \
	--with-http_secure_link_module \
	--with-http_degradation_module \
	--with-http_stub_status_module \
	--with-http_auth_request_module \
	--with-http_xslt_module \
	--with-http_v2_module \
	--with-http_v3_module \
	--with-mail \
	--with-mail_ssl_module \
	--with-threads \
	--with-stream \
	--with-stream_ssl_module \
	--with-stream_realip_module \
	--with-http_slice_module \
	--with-stream_ssl_preread_module \
	--with-debug \
	--with-cc-opt="%{optflags} $(%{pcre_version}-config --cflags) -DTCP_FASTOPEN=23" \
	%if 0%{?rhel} <= 7
		--with-cc="/opt/rh/devtoolset-%{gcc_version}/root/usr/bin/gcc" \
	%endif
	--with-openssl=modules/%{module_dir_openssl} \
	%if 0%{?rhel} >= 8
		--with-openssl-opt=enable-ktls \
	%endif
	%if %{with modsecurity}
		--add-dynamic-module=modules/%{module_dir_modsecurity} \
	%endif
	%if %{with pagespeed}
		--add-module=modules/%{module_dir_pagespeed} \
	%endif
	--add-module=modules/%{module_dir_headers_more} \
	--add-module=modules/%{module_dir_cache_purge} \
	--add-module=modules/%{module_dir_brotli} \
	--add-module=modules/%{module_dir_vts} \
	--add-module=modules/%{module_dir_http_geoip2} \
	--add-module=modules/%{module_dir_echo}

make

%install
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

%{__mkdir} -p %{buildroot}%{_libdir}/nginx/modules
cd %{buildroot}%{_sysconfdir}/nginx && %{__ln_s} ../..%{_libdir}/nginx/modules modules && cd -

%if %{use_systemd}
	install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/nginx.service
%else
	install -p -D -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/nginx
%endif


install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/nginx

install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d/custom
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d/vhosts
install -p -d -m 0700 %{buildroot}%{nginx_home}
install -p -d -m 0700 %{buildroot}%{nginx_home_cache}
%if %{with pagespeed}
	install -p -d -m 0700 %{buildroot}%{nginx_home_cache}/pagespeed
%endif
install -p -d -m 0700 %{buildroot}%{nginx_logdir}
install -p -d -m 0755 %{buildroot}%{nginx_webroot}
install -p -d -m 0755 %{buildroot}%{_datadir}/nginx/modules

%if %{with pagespeed}
	install -p -m 0644 %{SOURCE7} %{buildroot}%{nginx_confdir}/nginx.conf
%else
	install -p -m 0644 %{SOURCE4} %{buildroot}%{nginx_confdir}/nginx.conf
%endif

install -p -m 0644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} %{SOURCE36} %{SOURCE37} %{SOURCE38} %{SOURCE39} %{SOURCE40} %{buildroot}%{nginx_confdir}/conf.d/custom
%if %{with pagespeed}
	install -p -m 0644 %{SOURCE21} %{buildroot}%{nginx_confdir}/conf.d/custom
%endif
install -p -m 0644 %{SOURCE17} %{buildroot}%{nginx_confdir}/conf.d/vhosts

install -p -D -m 0644 %{_builddir}/nginx-%{version}/man/nginx.8 %{buildroot}%{_mandir}/man8/nginx.8

%if %{use_systemd}
	%{__mkdir} -p %{buildroot}%{_libexecdir}/initscripts/legacy-actions/nginx
	%{__install} -m755 %SOURCE5 %{buildroot}%{_libexecdir}/initscripts/legacy-actions/nginx/upgrade
	%{__install} -m755 %SOURCE6 %{buildroot}%{_libexecdir}/initscripts/legacy-actions/nginx/check-reload
%endif

%if %{with modsecurity}
	echo 'load_module "%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so";' > %{buildroot}%{_datadir}/nginx/modules/module-modsecurity.conf
%endif

%pre
getent group %{nginx_group} > /dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} > /dev/null || \
	useradd -r -d %{nginx_home} -g %{nginx_group} \
	-s /sbin/nologin -c "Nginx web server" %{nginx_user}
exit 0


%post
if [ $1 -eq 1 ]; then
%if %{use_systemd}
	/usr/bin/systemctl preset nginx.service >/dev/null 2>&1 || :
%else
	/sbin/chkconfig --add nginx
%endif
fi
if [ $1 -eq 2 ]; then
	chmod 700 %{nginx_home}
	chmod 700 %{nginx_home_cache}
	chmod 700 %{nginx_logdir}
fi
if [ $1 -eq 1 ]; then
	cat <<BANNER
----------------------------------------------------------------------

Thanks for using nginx-more! Feel free to send any feature request 
with an Issue or Pull Request on github.com/karljohns0n/nginx-more

----------------------------------------------------------------------
BANNER
fi

%if %{with modsecurity}
%post module-modsecurity
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi
%endif

%preun
if [ $1 -eq 0 ]; then
%if %use_systemd
	/usr/bin/systemctl --no-reload disable nginx.service >/dev/null 2>&1 || :
	/usr/bin/systemctl stop nginx.service >/dev/null 2>&1 || :
%else
	/sbin/service nginx stop > /dev/null 2>&1
	/sbin/chkconfig --del nginx
%endif
fi


%postun
%if %use_systemd
	/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
%endif
if [ $1 -ge 1 ]; then
	/sbin/service nginx status  >/dev/null 2>&1 || exit 0
	/sbin/service nginx upgrade >/dev/null 2>&1 || echo \
		"Binary upgrade failed, please check nginx's error.log"
fi


%files
%doc LICENSE
%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%{_datadir}/nginx/html/*
%{_sbindir}/nginx
%{_mandir}/man8/nginx.8*
%if %{use_systemd}
%{_unitdir}/nginx.service
%dir %{_libexecdir}/initscripts/legacy-actions/nginx
%{_libexecdir}/initscripts/legacy-actions/nginx/*
%else
%{_initrddir}/nginx
%endif
%dir %{nginx_confdir}
%dir %{nginx_confdir}/conf.d
%dir %{nginx_confdir}/conf.d/custom
%dir %{nginx_confdir}/conf.d/vhosts
%{_sysconfdir}/nginx/modules

%config(noreplace) %{nginx_confdir}/fastcgi.conf
%config(noreplace) %{nginx_confdir}/fastcgi.conf.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/nginx.conf
%config(noreplace) %{nginx_confdir}/nginx.conf.default
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/scgi_params.default
%config(noreplace) %{nginx_confdir}/uwsgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params.default
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{nginx_confdir}/conf.d/custom/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/nginx

%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home_cache}
%if %{with pagespeed}
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home_cache}/pagespeed
%endif
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}
%attr(0755,root,root) %dir %{_libdir}/nginx
%attr(0755,root,root) %dir %{_libdir}/nginx/modules
%attr(0755,root,root) %dir %{_datadir}/nginx/modules
/etc/nginx/conf.d/vhosts/*-example
/etc/nginx/conf.d/custom/*-example
/etc/nginx/conf.d/custom/aerisnetwork-ips

%if %{with modsecurity}
%files module-modsecurity
%{_datadir}/nginx/modules/module-modsecurity.conf
%{_libdir}/nginx/modules/ngx_http_modsecurity_module.so
%endif

%changelog
* Thu Sep 4 2025 Karl Johnson <karljohnson.it@gmail.com> 1.29.1-1
- Upgrade nginx to 1.29.1
- Refactor CI

* Tue Sep 2 2025 Karl Johnson <karljohnson.it@gmail.com> 1.28.0-2
- Add el10 support
- Bump OpenSSL to 3.5.2
- Bump Headers More to 0.39
- Bump ModSecurity connector to 1.0.4

* Thu Apr 24 2025 Karl Johnson <karljohnson.it@gmail.com> 1.28.0-1
- Upgrade nginx to 1.28.0
- Bump OpenSSL to 3.5.0
- Bump VTS to 0.2.4
- Upgrade Dynamic TLS patch from kn007 for compatibility
- Remove old CHANGES and README

* Wed Feb 12 2025 Karl Johnson <karljohnson.it@gmail.com> 1.26.3-1
- Upgrade nginx to 1.26.3
- Bump OpenSSL to 3.4.1
- Bump Headers More to 0.38
- Bump VTS to 0.2.3

* Tue Nov 5 2024 Karl Johnson <karljohnson.it@gmail.com> 1.26.2-2
- Bump OpenSSL to 3.4.0

* Thu Aug 22 2024 Karl Johnson <karljohnson.it@gmail.com> 1.26.2-1
- Upgrade nginx to 1.26.2

* Mon Jul 8 2024 Karl Johnson <karljohnson.it@gmail.com> 1.26.1-1
- Upgrade nginx to 1.26.1
- Bump OpenSSL to 3.3.1
- Enable HTTP/3
- Disable incompatible HPACK patch for now
- Always use realpath_root

* Wed Jan 31 2024 Karl Johnson <karljohnson.it@gmail.com> 1.24.0-5
- Bump OpenSSL to 3.2.1
- Bump Headers More to 0.37

* Tue Nov 7 2023 Karl Johnson <karljohnson.it@gmail.com> 1.24.0-4
- Bump OpenSSL to 3.1.4
- Bump Headers More to 0.35
- Refresh bad user-agents from nginx-ultimate-bad-bot-blocker

* Sun Oct 1 2023 Karl Johnson <karljohnson.it@gmail.com> 1.24.0-3
- Bump OpenSSL to 3.1.3

* Thu Aug 3 2023 Karl Johnson <karljohnson.it@gmail.com> 1.24.0-2
- Bump OpenSSL to 3.1.2
- Bump VTS to 0.2.2

* Tue May 9 2023 Karl Johnson <karljohnson.it@gmail.com> 1.24.0-1
- Upgrade nginx to 1.24.0
- Bump OpenSSL to 3.1.0
- Bump module Echo to 0.63
- Temporary bump PageSpeed to latest commit for 1.24.0 compatibility until PageSpeed support is dropped from nginx-more
- Don't rely on killproc for legacy scripts

* Tue Apr 4 2023 Bug Fest <bugfest.dev@pm.me> 1.22.1-4
- Source code dependencies loaded from their original repositories
- Add missing build deps: gcc, make
- Add missing build deps for pagespeed: gcc-c++
- Add ngx_brotli submodule source
- Add ngx_pagespeed dependencies: PSOL (pre-compiled)

* Wed Feb 8 2023 Karl Johnson <karljohnson.it@gmail.com> 1.22.1-3
- Bump OpenSSL to 3.0.8
- Roll in patch to fix cache purge compatibility with nginx 1.19.3+

* Tue Nov 1 2022 Karl Johnson <karljohnson.it@gmail.com> 1.22.1-2
- Bump OpenSSL to 3.0.7

* Wed Oct 19 2022 Karl Johnson <karljohnson.it@gmail.com> 1.22.1-1
- Upgrade nginx to 1.22.1
- Bump module VTS 0.2.1

* Wed Jul 20 2022 Karl Johnson <karljohnson.it@gmail.com> 1.22.0-4
- Enable kTLS starting with el8
- Bump module More Headers 0.34

* Wed Jul 6 2022 Karl Johnson <karljohnson.it@gmail.com> - 1.22.0-3
- Bump OpenSSL to 3.0.5
- Bump GeoIP2 to 3.4

* Tue Jun 21 2022 Karl Johnson <karljohnson.it@gmail.com> - 1.22.0-2
- Bump OpenSSL to 3.0.4

* Wed Jun 15 2022 Karl Johnson <karljohnson.it@gmail.com> - 1.22.0-1
- Rebase on nginx 1.22.0
- Use PCRE2
- Bump ModSecurity connector to 1.0.3

* Thu May 19 2022 Karl Johnson <karljohnson.it@gmail.com> - 1.20.2-4
- Bump OpenSSL to 1.1.1o
- Bump Brotli to dev-f4153a0

* Wed Mar 16 2022 Karl Johnson <karljohnson.it@gmail.com> - 1.20.2-3
- Bump OpenSSL to 1.1.1n

* Tue Dec 28 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.2-2
- Bump OpenSSL to 1.1.1m

* Wed Nov 17 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.2-1
- Bump nginx to 1.20.2

* Mon Nov 15 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.1-4
- Support AlmaLinux 8 and Rocky Linux 8
- Rebuild nginx-more on latest libs
- Bump modudle Echo to 0.62

* Sun Aug 29 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.1-3
- Bump OpenSSL to 1.1.1l

* Wed Jun 9 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.1-2
- Bump ModSecurity module to 1.0.2
- Enhance WordPress caching with Woocommerce

* Wed May 26 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.1-1
- Bump Nginx to 1.20.1

* Fri Apr 23 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.20.0-1
- Bump Nginx to 1.20.0
- Update Cloudflare IPs
- Fix Cloudflare dynamic tls patch with fuzz=0

* Thu Mar 25 2021 Karl Johnson <karljohnson.it@gmail.com> - 1.18.0-4
- Bump OpenSSL to 1.1.1k

* Wed Dec 9 2020 Karl Johnson <karljohnson.it@gmail.com> - 1.18.0-3
- Bump OpenSSL to 1.1.1i
- Bump Brotli to 1.0.9
- Add xmlrpc.php to brute force protection and relax r/m

* Mon Sep 28 2020 Karl Johnson <karljohnson.it@gmail.com> - 1.18.0-2
- Bump OpenSSL to 1.1.1h
- Skip cache on WooCommerce pages

* Wed May 6 2020 Karl Johnson <karljohnson.it@gmail.com> - 1.18.0-1
- Bump Nginx to 1.18.0
- Bump OpenSSL to 1.1.1g
- Bump Brotli to git snapshot 2020-05-06

* Thu Mar 5 2020 Karl Johnson <karljohnson.it@gmail.com> - 1.16.1-4
- Add CentOS 8 support
- Bump GCC version from 7 to 8
- Add dynamic module ModSecurity Nginx connector 1.0.1 (el7 and el8)
- Bump Brotli to git snapshot 20200305
- Roll in Cloudflare full HPACK patch
- Roll in Cloudflare dynamic tls records patch
- Add Mailgun link tracking proxypass

* Mon Nov 18 2019 Karl Johnson <karljohnson.it@gmail.com> - 1.16.1-2
- Bump OpenSSL to 1.1.1d
- Bump GeoIP2 to 3.3
- Bump Brotli to git snapshot 2019-11-18
- Set expire on woff2 files
- Add caching php-fpm option (20 minutes) for all WordPress configs

* Tue Aug 13 2019 Karl Johnson <karljohnson.it@gmail.com> - 1.16.1-1
- Bump Nginx to 1.16.1
- Bump OpenSSL to 1.1.1c
- Bump Brotli to 1.0.7

* Wed May 15 2019 Karl Johnson <karljohnson.it@gmail.com> - 1.16.0-2
- Bump to Nginx 1.16.0
- Remove obsolete "--with-ipv6" and "ssl on"
- Refresh bad user-agents list
- Add 1.1.1.1 as resolver
- Make restrictions.conf compatible with multiple fpm users

* Thu Mar 7 2019 Karl Johnson <karljohnson.it@gmail.com> - 1.14.2-3
- Bump OpenSSL 1.1.1b, Brotli 1.0.4
- Add new module ngx_echo
- Add patch1 to fix module ngx_cache_purge on recent nginx

* Fri Dec 14 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.14.2-2
- Add module geoip2 3.2 with latest libmaxminddb 1.3.2

* Wed Dec 12 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.14.2-1
- Bump to Nginx 1.14.2, OpenSSL 1.1.1a
- Increase ciphers strength per default, disable TLS 1.0 and 1.1
- Switch RapidSSL to Lets Encrypt in SSL example configuration

* Tue Nov 6 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.14.1-1
- Bump to Nginx 1.14.1, module VTS 0.1.18

* Mon Oct 22 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.14.0-2
- Restrictions cleanup and more FCGI params added by default

* Thu Sep 20 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.14.0-1
- Bump to Nginx 1.14.0, OpenSSL 1.1.1
- Rolled in TLS 1.3 configuration

* Tue May 22 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.12.2-5
- Bump OpenSSL 1.1.0h, module VTS 0.1.16, module More Headers 0.33
- Allow .well-known access

* Fri Mar 2 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.12.2-4
- Move nginx-more version in ngx_show_configure
- Enable TCP_FASTOPEN
- Bump GCC to 7.2

* Fri Feb 23 2018 Karl Johnson <karljohnson.it@gmail.com> - 1.12.2-3
- Bump Pagespeed to 1.13.35.2, Brotli snapshot 20180222

* Fri Nov 17 2017 Karl Johnson <karljohnson.it@gmail.com> - 1.12.2-2
- Add module ngx_brotli from Github master snapshot, bump Pagespeed to 1.12.34.3

* Thu Nov 2 2017 Karl Johnson <karljohnson.it@gmail.com> - 1.12.2-1
- Bump to Nginx 1.12.2, OpenSSL 1.1.0g, Cloudflare IPs added

* Thu Jul 13 2017 Karl Johnson <karljohnson.it@gmail.com> - 1.12.1-1
- Bump to Nginx 1.12.1, OpenSSL 1.1.0f, PageSpeed 1.12.34.2, nginx vts 0.1.15

* Tue Apr 18 2017 Karl Johnson <karljohnson.it@gmail.com> - 1.12.0-1
- Bump to Nginx 1.12.0, OpenSSL 1.1.0e, nginx vts 0.1.14, user agents blacklist updated
- Important: Removal of old ModSecurity nginx add-on, might be replaced later by ModSecurity-nginx

* Wed Mar 1 2017 Karl Johnson <karljohnson.it@gmail.com> - 1.10.3-1
- Bump to Nginx 1.10.3, OpenSSL 1.0.2k, nginx vts 0.1.12
- Add user agents blacklist

* Mon Nov 7 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.10.2-1
- Bump to Nginx 1.10.2, More Headers 0.32

* Mon Sep 26 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.10.1-2
- Bump to OpenSSL 1.0.2j, PageSpeed 1.11.33.4, More Headers 0.30, nginx vts 0.1.10

* Tue May 31 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.10.1-1
- Bump to Nginx 1.10.1 (CVE-2016-4450)

* Fri May 20 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.10.0-1
- Bump to Nginx 1.10.0 with threads pools
- Important: SPDY replaced by HTTP2

* Tue May 17 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.8.1-6
- Switch to GCC 5.2.1
- Remove EPEL dep
- Bump PageSpeed 1.11.33.2, More Headers 0.30

* Fri Apr 29 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.8.1-5
- Bump OpenSSL 1.0.2h, PageSpeed 1.11.33.1, ModSecurity 2.9.1
- Add nginx vts 0.1.9

* Mon Mar 7 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.8.1-4
- Bump PageSpeed 1.10.33.6, OpenSSL 1.0.2g

* Thu Feb 18 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.8.1-3
- Build with GCC 4.8 on el6
- Bump PageSpeed 1.10.33.5

* Fri Jan 29 2016 Karl Johnson <karljohnson.it@gmail.com> - 1.8.1-1
- Bump Nginx 1.8.1, PageSpeed 1.9.32.10, OpenSSL 1.0.2f, More-Headers 0.29

* Fri Aug 14 2015 Karl Johnson <karljohnson.it@gmail.com> - 1.8.0-4
- Bump PageSpeed to 1.9.32.6
- Increase fcgi buffer for php-fpm

* Fri Jul 17 2015 Karl Johnson <karljohnson.it@gmail.com> - 1.8.0-3
- Changes in rpm upgrade process 
- Add install banner

* Wed Jul 15 2015 Karl Johnson <karljohnson.it@gmail.com> - 1.8.0-2
- Bump module OpenSSL 1.0.2d and PageSpeed 1.9.32.4
- Few configurations updates

* Tue May 12 2015 Karl Johnson <kjohnson@aerisnetwork.com> - 1.8.0-1
- Bump Nginx to 1.8.0 and module More Headers 0.26

* Wed Apr 8 2015 Karl Johnson <kjohnson@aerisnetwork.com> - 1.6.3-1
- Bump Nginx to 1.6.3 and module OpenSSL 1.0.2a

* Fri Mar 6 2015 Karl Johnson <kjohnson@aerisnetwork.com> - 1.6.2-3
- El7 support added

* Tue Feb 17 2015 Karl Johnson <kjohnson@aerisnetwork.com> - 1.6.2-2
- Bump modules ModSecurity 2.9.0, PageSpeed 1.9.32.3, Cache Purge 2.3, OpenSSL 1.0.1l

* Wed Nov 12 2014 Karl Johnson <kjohnson@aerisnetwork.com> - 1.6.2-1
- First build based on Nginx 1.6.2, OpenSSL 1.0.1j, Pagespeed 1.9.32.2, Cache Purge 2.1, More Headers 0.25
