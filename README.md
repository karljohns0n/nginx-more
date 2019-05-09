## Synopsis

Nginx-more is a build of Nginx with additional modules such as HTTP2, PageSpeed, Brotli, More Headers, Cache Purge, VTS, GeoIP2, Echo. It's compiled using recent GCC version and latest OpenSSL sources. It also includes some built-in configurations such as WordPress and Laravel php-fpm setup. More information can be found on this package [here](https://medium.com/@karljohnson/nginx-more-get-http-2-with-alpn-pagespeed-modsecurity-and-much-more-in-one-single-package-7d28a44d1854) however it can be a bit outdated at this time. Nginx-more package is supported since 2014.

## Easy installation for CentOS

There's packages available for CentOS 6 and 7. The easiest way to install it is using Aeris Network yum repository:

```bash
CentOS 6 > yum install https://repo.aerisnetwork.com/pub/aeris-release-6.rpm
CentOS 7 > yum install https://repo.aerisnetwork.com/pub/aeris-release-7.rpm
```

Once the repository is configured, you can proceed with installing nginx-more:

```bash
#> yum install nginx-more
```

All configurations will be installed in default directory which is `/etc/nginx/`. The package already includes a bunch of PHP-FPM configurations in `conf.d/custom/` for WordPress, Laravel, Drupal, OpenCart and PrestaShop, so you can get started in few seconds with your website hosting.

Clean vhost exemple for WordPress:

```text
server {
    listen 80;
    listen 127.0.0.1:443 ssl http2;
    server_name exemple.com;
    root /home/www/exemple.com/public_html;
    access_log /var/log/nginx/exemple.com-access_log main;
    error_log /var/log/nginx/exemple.com-access_log warn;

    if ($bad_bot) { return 444; }

    include conf.d/custom/ssl-exemple.com.conf;
    include conf.d/custom/restrictions.conf;
    include conf.d/custom/pagespeed.conf;
    include conf.d/custom/fpm-wordpress.conf;
}
```

All nginx-more builds are kept in the repository. If you upgrade to a newest version and it has any issues that you don't have time to troubleshoot by looking at the nginx `error_log`, you can downgrade to an older version with yum:

```bash
#> yum downgrade nginx-more
```

You can also switch back to nginx package from EPEL or Nginx repo with a simple yum command:

```bash
#> yum swap nginx-more nginx
```

Full output of nginx configure:

```bash
#> nginx -V
nginx version: nginx/1.16.0
custom build maintained on github.com/karljohns0n/nginx-more
built by gcc 7.3.1 20180303 (Red Hat 7.3.1-5) (GCC) 
built with OpenSSL 1.1.1b  26 Feb 2019
TLS SNI support enabled
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/cache/client_body --http-proxy-temp-path=/var/lib/nginx/cache/proxy --http-fastcgi-temp-path=/var/lib/nginx/cache/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/cache/uwsgi --http-scgi-temp-path=/var/lib/nginx/cache/scgi --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --user=nginx --group=nginx --with-compat --with-file-aio --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_image_filter_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_geoip_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_stub_status_module --with-http_auth_request_module --with-http_xslt_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-threads --with-stream --with-stream_ssl_module --with-stream_realip_module --with-http_slice_module --with-stream_ssl_preread_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -DTCP_FASTOPEN=23' --with-cc=/opt/rh/devtoolset-7/root/usr/bin/gcc --with-openssl=modules/openssl-1.1.1b --add-module=modules/ngx_headers_more-0.33 --add-module=modules/ngx_cache_purge-2.3 --add-module=modules/ngx_module_vts-0.1.18 --add-module=modules/ngx_pagespeed-1.13.35.2-stable --add-module=modules/ngx_brotli-snap20190307 --add-module=modules/ngx_http_geoip2_module-3.2 --add-module=modules/ngx_echo-0.61
```

## Modules

* [OpenSSL](https://github.com/openssl/openssl)
* [PageSpeed](https://github.com/apache/incubator-pagespeed-ngx)
* [Brotli](https://github.com/eustas/ngx_brotli)
* [Virtual host traffic status](https://github.com/vozlt/nginx-module-vts)
* [Headers more](https://github.com/openresty/headers-more-nginx-module)
* [Cache purge](https://github.com/FRiCKLE/ngx_cache_purge)
* [GeoIP2](https://github.com/leev/ngx_http_geoip2_module)
* [Echo](https://github.com/openresty/echo-nginx-module)

## Ansible playbook

A simple [Ansible role](https://galaxy.ansible.com/karljohns0n/nginx-more) is available to install nginx-more and keep it updated on CentOS.

Example of playbook:

    - hosts: servers
      roles:
         - { role: karljohns0n.nginx-more }

## Changelog

The changelog for all packages is available from the RepoView:

* [CentOS 6](https://repo.aerisnetwork.com/stable/centos/6/x86_64/repoview/nginx-more.html)
* [CentOS 7](https://repo.aerisnetwork.com/stable/centos/7/x86_64/repoview/nginx-more.html)

## Package dependencies

As of writing, only one package outside CentOS default repositories is required to build nginx-more RPM, which is [libmaxminddb-devel](https://github.com/karljohns0n/pkg-libmaxminddb) for module GeoIP2. It's available in EPEL however a newer version is available in Aeris repository so it's recommended to add Aeris repository in your mock configuration. We try to avoid packages that aren't available in CentOS but if it's the case we will build and include them in Aeris repository therefore no other third-party repository is required to build nginx-more.
