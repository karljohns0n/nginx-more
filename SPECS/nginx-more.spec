%global packagename			nginx
%global nginx_user			nginx
%global nginx_group			%{nginx_user}
%global nginx_home			%{_localstatedir}/lib/nginx
%global nginx_home_cache	%{nginx_home}/cache
%global nginx_logdir		%{_localstatedir}/log/nginx
%global nginx_confdir		%{_sysconfdir}/nginx
%global nginx_datadir		%{_datadir}/nginx
%global nginx_webroot		%{nginx_datadir}/html
%global openssl_version		1.1.1b
%global module_ps			1.13.35.2-stable
%global module_headers_more	0.33
%global module_cache_purge	2.3
%global module_vts			0.1.18
%global module_brotli		snap20190307
%global module_geoip2		3.2
%global module_echo			0.61

%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Name:						nginx-more
Version:					1.16.0
Release:					2%{?dist}

Summary:					A high performance web server and reverse proxy server
Group:						System Environment/Daemons
License:					2-clause BSD-like license
URL:						http://nginx.org/
BuildRoot:					%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:					http://nginx.org/download/nginx-%{version}.tar.gz
Source1:					nginx.service
Source2:					nginx.init
Source3:					nginx.logrotate
Source4:					nginx.conf
Source5:					nginx-upgrade
Source6:					nginx-upgrade.8

Source10:					fpm-default.conf
Source11:					fpm-wordpress-cache.conf
Source12:					fpm-wordpress.conf
Source13:					fpm-wordpress-mu.conf
Source14:					fpm-laravel.conf
Source15:					restrictions.conf
Source16:					admin-ips.conf
Source17:					virtual.conf-exemple
Source18:					ssl.conf-exemple
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

Source100:					openssl-%{openssl_version}.tar.gz
Source101:					ngx_pagespeed-%{module_ps}.tar.gz
Source102:					psol-%{module_ps}.tar.gz
Source103:					ngx_headers_more-%{module_headers_more}.tar.gz
Source104:					ngx_cache_purge-%{module_cache_purge}.tar.gz
Source105:					ngx_brotli-%{module_brotli}.tar.gz
Source106:					ngx_module_vts-%{module_vts}.tar.gz
Source107:					ngx_http_geoip2_module-%{module_geoip2}.tar.gz
Source108:					ngx_echo-%{module_echo}.tar.gz

Patch0:						nginx-version.patch
Patch1:						ngx_cache_purge-fix-compatibility-with-nginx-1.11.6.patch

BuildRequires:				devtoolset-7-gcc-c++ devtoolset-7-binutils
BuildRequires:				libxslt-devel
BuildRequires:				openssl-devel
BuildRequires:				pcre-devel
BuildRequires:				zlib-devel
BuildRequires:				pcre
BuildRequires:				gd-devel
BuildRequires:				httpd-devel
BuildRequires:				libuuid-devel
BuildRequires:				libmaxminddb-devel

%if 0%{?rhel} == 7
BuildRequires:				GeoIP-devel
%endif

Requires:					gd
Requires:					pcre
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

mkdir modules
tar -zxvf %{SOURCE100} -C modules/
tar -zxvf %{SOURCE101} -C modules/
tar -zxvf %{SOURCE102} -C modules/ngx_pagespeed-%{module_ps}/
tar -zxvf %{SOURCE103} -C modules/
tar -zxvf %{SOURCE104} -C modules/
tar -zxvf %{SOURCE105} -C modules/
tar -zxvf %{SOURCE106} -C modules/
tar -zxvf %{SOURCE107} -C modules/
tar -zxvf %{SOURCE108} -C modules/

%{__sed} -i 's_@CACHEPVER@_%{module_cache_purge}_' %{PATCH1}

%patch0 -p0
%patch1 -p0

%build
export DESTDIR=%{buildroot}
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
	%if 0%{?rhel} == 7
		--with-http_geoip_module \
	%endif
	--with-http_random_index_module \
	--with-http_secure_link_module \
	--with-http_degradation_module \
	--with-http_stub_status_module \
	--with-http_auth_request_module \
	--with-http_xslt_module \
	--with-http_v2_module \
	--with-mail \
	--with-mail_ssl_module \
	--with-threads \
	--with-stream \
	--with-stream_ssl_module \
	--with-stream_realip_module \
	--with-http_slice_module \
	--with-stream_ssl_preread_module \
	--with-debug \
	--with-cc-opt="%{optflags} $(pcre-config --cflags) -DTCP_FASTOPEN=23" \
	--with-cc="/opt/rh/devtoolset-7/root/usr/bin/gcc" \
	--with-openssl=modules/openssl-%{openssl_version} \
	--add-module=modules/ngx_headers_more-%{module_headers_more} \
	--add-module=modules/ngx_cache_purge-%{module_cache_purge} \
	--add-module=modules/ngx_module_vts-%{module_vts} \
	--add-module=modules/ngx_pagespeed-%{module_ps} \
	--add-module=modules/ngx_brotli-%{module_brotli} \
	--add-module=modules/ngx_http_geoip2_module-%{module_geoip2} \
	--add-module=modules/ngx_echo-%{module_echo}

make

%install
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules
cd $RPM_BUILD_ROOT%{_sysconfdir}/nginx && \
	%{__ln_s} ../..%{_libdir}/nginx/modules modules && cd -

%if %{use_systemd}
	install -p -D -m 0644 %{SOURCE1} \
		%{buildroot}%{_unitdir}/nginx.service
%else
	install -p -D -m 0755 %{SOURCE2} \
		%{buildroot}%{_initrddir}/nginx
%endif


install -p -D -m 0644 %{SOURCE3} \
	%{buildroot}%{_sysconfdir}/logrotate.d/nginx

install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d/custom
install -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d/vhosts
install -p -d -m 0700 %{buildroot}%{nginx_home}
install -p -d -m 0700 %{buildroot}%{nginx_home_cache}
install -p -d -m 0700 %{buildroot}%{nginx_home_cache}/pagespeed
install -p -d -m 0700 %{buildroot}%{nginx_logdir}
install -p -d -m 0755 %{buildroot}%{nginx_webroot}

install -p -m 0644 %{SOURCE4} %{buildroot}%{nginx_confdir}

install -p -m 0644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} %{SOURCE30} %{SOURCE31} \
	%{buildroot}%{nginx_confdir}/conf.d/custom
install -p -m 0644 %{SOURCE17} \
	%{buildroot}%{nginx_confdir}/conf.d/vhosts

install -p -D -m 0644 %{_builddir}/nginx-%{version}/man/nginx.8 \
	%{buildroot}%{_mandir}/man8/nginx.8

%if %{use_systemd}
	install -p -D -m 0755 %{SOURCE5} %{buildroot}%{_bindir}/nginx-upgrade
	install -p -D -m 0644 %{SOURCE6} %{buildroot}%{_mandir}/man8/nginx-upgrade.8
%endif


%pre
getent group %{nginx_group} > /dev/null || groupadd -r %{nginx_group}
getent passwd %{nginx_user} > /dev/null || \
	useradd -r -d %{nginx_home} -g %{nginx_group} \
	-s /sbin/nologin -c "Nginx web server" %{nginx_user}
exit 0


%post
%if %{use_systemd}
%systemd_post %{packagename}.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add %{packagename}
fi
%endif
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

Installing memcached is highly recommended to let PageSpeed cache in 
memory instead of disk.

----------------------------------------------------------------------
BANNER
fi


%preun
%if %use_systemd
%systemd_preun %{packagename}.service
%else
if [ $1 -eq 0 ] ; then
	/sbin/service %{packagename} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{packagename} > /dev/null 2>&1
fi
%endif


%postun
%if %use_systemd
%systemd_postun_with_restart %{packagename}.service
%else
if [ "$1" -ge "1" ] ; then
	/sbin/service %{packagename} status  >/dev/null 2>&1 || exit 0
	/sbin/service %{packagename} upgrade >/dev/null 2>&1 || echo \
		"Binary upgrade failed, please check nginx's error.log"
fi
%endif


%files
%doc LICENSE CHANGES README
%{nginx_datadir}/
%if %{use_systemd}
%{_bindir}/nginx-upgrade
%endif
%{_sbindir}/nginx
%{_mandir}/man8/nginx.8*
%if %{use_systemd}
%{_mandir}/man8/nginx-upgrade.8*
%{_unitdir}/nginx.service
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
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_home_cache}/pagespeed
%attr(700,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}
%attr(0755,root,root) %dir %{_libdir}/nginx
%attr(0755,root,root) %dir %{_libdir}/nginx/modules
/etc/nginx/conf.d/vhosts/*-exemple
/etc/nginx/conf.d/custom/*-exemple
/etc/nginx/conf.d/custom/aerisnetwork-ips


%changelog
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
- Switch RapidSSL to Lets Encrypt in SSL exemple configuration

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
