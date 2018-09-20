## Synopsis

Nginx-more is a build of Nginx with additional modules such as HTTP2, PageSpeed, Brotli, More Headers, Cache Purge, VTS. It's compiled using recent GCC version and latest OpenSSL sources. It also includes some built-in configurations such as WordPress and Laravel php-fpm setup. More information can be found on this package [here](https://medium.com/@karljohnson/nginx-more-get-http-2-with-alpn-pagespeed-modsecurity-and-much-more-in-one-single-package-7d28a44d1854) however it can be a bit outdated at this time.

## Easy installation for CentOS

There's currently packages available for CentOS 6 and 7. The easiest way to install it is to use Aeris Network yum repository

```bash
CentOS 6 > yum install https://repo.aerisnetwork.com/stable/centos/6/x86_64/aeris-release-1.0-4.el6.noarch.rpm
CentOS 7 > yum install https://repo.aerisnetwork.com/stable/centos/7/x86_64/aeris-release-1.0-4.el7.noarch.rpm
```
Once the repository is configured, you can proceed with installing nginx-more.

```bash
#> yum install nginx-more
```

All configurations will be installed in default directory which is /etc/nginx/. The package already includes a bunch of PHP-FPM configurations in conf.d/custom/ for WordPress, Laravel, Drupal, OpenCart and PrestaShop, so you can get started in few seconds with your website hosting.

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

All nginx-more builds are kept in the repository. If you upgrade to a newest version and it has any issues that you don't have time to troubleshoot by looking at the nginx error_log, you can downgrade to an older version with yum:

```bash
#> yum downgrade nginx-more
```

You can also switch back to nginx package from EPEL or Nginx repo with a simple yum command:

```bash
#> yum swap nginx-more nginx
```

## Modules

* [OpenSSL](https://github.com/openssl/openssl)
* [PageSpeed](https://github.com/apache/incubator-pagespeed-ngx)
* [Brotli](https://github.com/google/ngx_brotli)
* [Virtual host traffic status](https://github.com/vozlt/nginx-module-vts)
* [Headers more](https://github.com/openresty/headers-more-nginx-module)
* [Cache purge](https://github.com/FRiCKLE/ngx_cache_purge)
