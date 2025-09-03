# Nginx-more

[![Release](https://img.shields.io/badge/release-1.28.0--2-success.svg)](#)
[![Build](https://img.shields.io/github/actions/workflow/status/karljohns0n/nginx-more/build.yml?branch=master)](#)
[![Installs](https://img.shields.io/badge/dynamic/yaml?color=brightgreen&label=installs&query=installs&url=https%3A%2F%2Frepo.aerisnetwork.com%2Farchive%2Fnginx-more-stats.yaml)](#)
[![Downloads](https://img.shields.io/badge/dynamic/yaml?color=brightgreen&label=downloads&query=downloads&url=https%3A%2F%2Frepo.aerisnetwork.com%2Farchive%2Fnginx-more-stats.yaml)](#)

## Synopsis

Nginx-more is a build of Nginx with additional modules such as HTTP/2, HTTP/3, PageSpeed, Brotli, More Headers, Cache Purge, VTS, GeoIP2, Echo and ModSecurity. It's compiled using recent GCC version and latest OpenSSL sources. It also includes some built-in configurations such as WordPress and Laravel php-fpm setup. More information about this package can be found [here](https://medium.com/@karljohnson/nginx-more-get-http-2-with-alpn-pagespeed-modsecurity-and-much-more-in-one-single-package-7d28a44d1854) however this post is be a bit outdated at this time. Nginx-more is supported since 2014 and used on a thousand of servers.

## Easy installation for RHEL / CentOS / AlmaLinux / Rocky Linux

There's packages available for Enterprise Linux 6, 7, 8, 9 and 10. The easiest way to install nginx-more is by using Aeris yum repository:

```bash
EL6 > yum install -y https://repo.aerisnetwork.com/pub/aeris-release-6.rpm
EL7 > yum install -y https://repo.aerisnetwork.com/pub/aeris-release-7.rpm
EL8 > dnf install -y https://repo.aerisnetwork.com/pub/aeris-release-8.rpm
EL9 > dnf install -y https://repo.aerisnetwork.com/pub/aeris-release-9.rpm
EL10 > dnf install -y https://repo.aerisnetwork.com/pub/aeris-release-10.rpm
```

Once the repository is configured, you can proceed with installing nginx-more:

```bash
> yum install nginx-more
```

All configurations will be installed in default directory which is `/etc/nginx/`. The package already includes a bunch of PHP-FPM configurations in `conf.d/custom/` for WordPress, Laravel, Drupal, OpenCart, PrestaShop and Sendy, so you can get started in few seconds with your website hosting.

Clean vhost example for WordPress:

```text
server {
    listen 80;
    listen 443 ssl;
    http2 on;
    server_name example.com;
    root /home/www/example.com/public_html;
    access_log /var/log/nginx/example.com-access_log main;
    error_log /var/log/nginx/example.com-error_log warn;

    if ($bad_bot) { return 444; }

    include conf.d/custom/ssl.global.conf;
    include conf.d/custom/restrictions.conf;
    include conf.d/custom/fpm-wordpress.conf;
}
```

All nginx-more builds are kept in the repository. If you upgrade to a newest version and it has any issues that you don't have time to troubleshoot by looking at the nginx `error_log`, you can downgrade to an older version with yum:

```bash
> yum downgrade nginx-more
```

Note that you cannot install nginx-more if nginx package is already installed on your system because both packages provide nginx binary and configurations. You need to choose between nginx-more OR nginx from CentOS / EPEL / Nginx repository. Nginx-more is compiled using a more recent GCC version than the others and it provides lots of ready-to-go WordPress / Laravel configurations. If nginx is already installed, it's possible to swap from nginx to nginx-more with a simple yum command, although be careful with your inplace configurations. A new install is recommended.

```bash
> yum swap nginx nginx-more
```

Full output of nginx configure:

```bash
> nginx -V
nginx version: nginx/1.28.0
custom build maintained on github.com/karljohns0n/nginx-more
built by gcc 11.5.0 20240719 (Red Hat 11.5.0-5) (GCC) 
built with OpenSSL 3.5.2 5 Aug 2025
TLS SNI support enabled
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/cache/client_body --http-proxy-temp-path=/var/lib/nginx/cache/proxy --http-fastcgi-temp-path=/var/lib/nginx/cache/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/cache/uwsgi --http-scgi-temp-path=/var/lib/nginx/cache/scgi --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --user=nginx --group=nginx --with-compat --with-file-aio --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_image_filter_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_stub_status_module --with-http_auth_request_module --with-http_xslt_module --with-http_v2_module --with-http_v3_module --with-mail --with-mail_ssl_module --with-threads --with-stream --with-stream_ssl_module --with-stream_realip_module --with-http_slice_module --with-stream_ssl_preread_module --with-debug --with-cc-opt='-O2 -flto=auto -ffat-lto-objects -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -fstack-protector-strong -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -march=x86-64-v2 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection -DTCP_FASTOPEN=23' --with-openssl=modules/openssl-3.5.2 --with-openssl-opt=enable-ktls --add-dynamic-module=modules/ngx_modsecurity-1.0.4 --add-module=modules/ngx_headers_more-0.39 --add-module=modules/ngx_cache_purge-2.3 --add-module=modules/ngx_brotli-1.0.0rc-2-g6e97 --add-module=modules/ngx_module_vts-0.2.4 --add-module=modules/ngx_http_geoip2_module-3.4 --add-module=modules/ngx_echo-0.63
```

## Packages

*   EL6 [[x86_64]](https://repo.aerisnetwork.com/stable/el/6/x86_64/)
*   EL7 [[x86_64]](https://repo.aerisnetwork.com/stable/el/7/x86_64/)
*   EL8 [[x86_64]](https://repo.aerisnetwork.com/stable/el/8/x86_64/)
*   EL9 [[x86_64]](https://repo.aerisnetwork.com/stable/el/9/x86_64/) [[aarch64]](https://repo.aerisnetwork.com/stable/el/9/aarch64/)
*   EL10 [[x86_64]](https://repo.aerisnetwork.com/stable/el/10/x86_64/) [[aarch64]](https://repo.aerisnetwork.com/stable/el/10/aarch64/)

## Modules

*   [OpenSSL](https://github.com/openssl/openssl)
*   [PageSpeed](https://github.com/apache/incubator-pagespeed-ngx) (removed ≥ el9)
*   [Brotli](https://github.com/google/ngx_brotli)
*   [Virtual host traffic status](https://github.com/vozlt/nginx-module-vts)
*   [Headers more](https://github.com/openresty/headers-more-nginx-module)
*   [Cache purge](https://github.com/FRiCKLE/ngx_cache_purge)
*   [GeoIP2](https://github.com/leev/ngx_http_geoip2_module)
*   [Echo](https://github.com/openresty/echo-nginx-module)
*   [ModSecurity](https://github.com/owasp-modsecurity/ModSecurity-nginx) (dynamic)

## Patches

*   [Cloudflare TLS Dynamic Record](https://blog.cloudflare.com/optimizing-tls-over-tcp-to-reduce-latency/)
*   [Cloudflare full HPACK implementation](https://blog.cloudflare.com/hpack-the-silent-killer-feature-of-http-2/) (removed ≥ nginx 1.26.0)

## SELinux

Third-party modules such as PageSpeed will cause trouble while SELinux enforced. To get nginx-more works with SELinux, you need at least to turn on `httpd_execmem` policy:

```bash
> yum -y install policycoreutils && setsebool -P httpd_execmem 1
> systemctl start nginx
```

It's possible to temporarily disable SELinux for Nginx to get started quickly:

```bash
> semanage permissive -a httpd_t
```

Here's two nice external blogs to help you troubleshoot SELinux with Nginx:

*   [selinux-making-it-a-little-easier-for-web](https://medium.com/@ChristopherShaffer/selinux-making-it-a-little-easier-for-web-b8fad76e2d97)
*   [using-nginx-plus-with-selinux](https://www.nginx.com/blog/using-nginx-plus-with-selinux/)

## Ansible playbook

A simple [Ansible role](https://galaxy.ansible.com/karljohns0n/nginx-more) is available to install nginx-more and keep it updated.

Example of playbook:

```yaml
- hosts: servers
    roles:
      - { role: karljohns0n.nginx-more }
```

## Package dependencies

As of writing, only one package outside EL default repositories is required to build nginx-more RPM, which is [libmaxminddb-devel](https://github.com/karljohns0n/pkg-libmaxminddb) for module GeoIP2. It's available in EPEL however a newer version is available in Aeris repository so it's recommended to add Aeris repository in your mock configuration. We try to avoid packages that aren't available in EL but if it's the case we will build and include them in Aeris repository therefore no other third-party repository is required to build nginx-more.
