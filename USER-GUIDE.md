# Nginx-more User Guide

## OpenSSL

### TLS 1.3

Nginx-more has always been compiled with latest OpenSSL version for all CentOS (6,7,8), thus it supports all recent TLS protocols and ciphers such as TLS 1.3. OpenSSL can be used to confirm TLS 1.3:

```bash
> echo | openssl s_client -connect git.market:443 -tls1_3 2>/dev/null |grep -E "TLSv1.3.*Cipher"
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
```

### HTTP/2 ALPN

HTTP/2 has been supported for a long time now by nginx-more on CentOS 6 and up. To confirm HTTP/2 ALPN on a website:

```bash
> echo | openssl s_client -alpn h2 -connect git.market:443 -status 2>/dev/null |grep "ALPN protocol"
ALPN protocol: h2
```

## PageSpeed

Module PageSpeed for nginx is built-in in nginx-more. It's already configured and it uses Memcached if available. To enable Pagespeed on a vhost, simply add `;include conf.d/custom/pagespeed.conf`. Here's an example of a WordPress configuration with Pagespeed enabled:

```text
server {
    listen 80;
    listen 443 ssl http2;
    server_name wordpress.com;
    root /home/myuser/wordpress/public_html;

    include conf.d/custom/restrictions.conf;
    include conf.d/custom/pagespeed.conf;
    include conf.d/custom/fpm-wordpress.conf;
}
```

Once enabled on a vhost, let's say example.com, Pagespeed logs, statistics and configurations can be accessed by these URLs if your IP is whitelisted in `/etc/nginx/conf.d/custom/admin-ips.conf`:

*   <https://example.com/ngx_pagespeed_message>
*   <https://example.com/ngx_pagespeed_statistics>
*   <https://example.com/pagespeed_admin>

## ModSecurity

ModSecurity for nginx is built as dynamic module. It can quickly be installed using yum:

```bash
> yum install nginx-more-module-modsecurity
> nginx -t
> grep -i modsec /var/log/nginx/error.log
```

An update of nginx-more-module-modsecurity package will follow every new release of nginx-more. 

## Virtual Host Traffic Status

Module VTS for nginx is built-in in nginx-more and so useful. It can be accessed on any website followed by `/traffic_status` if your IP is whitelisted in `/etc/nginx/conf.d/custom/admin-ips.conf`. This module display a live dashboard of all connections on nginx, on every server zones and upstreams, with responses code, bandwidth, cache status (hit/miss/bypass/expired) and more.

<img src="https://nginx-more.s3.ca-central-1.amazonaws.com/Assets/nginx-module-vts-example.png" width="600">

## Brotli

Brotli is enabled by default on every vhosts. It can be confirmed by looking at the headers:

```bash
> curl -s -I -H 'Accept-Encoding: br' https://git.market |grep content-encoding
content-encoding: br
```

## GeoIP2

GeoLite Legacy databases are discontinued as of January 2, 2019, they are not updated nor any longer available for download. Therefore, GeoIP2 module has been added to nginx-more to easily migrate from GeoIP to GeoIP2. Here's an example to make it works:

*   Download latest GeoIP2 databases from sources or rpm package
```bash
mkdir /usr/share/GeoIP2
wget -P /usr/share/GeoIP2 https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz
wget -P /usr/share/GeoIP2 https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz
gunzip /usr/share/GeoIP2/*.mmdb.gz
```
*   Load GeoIP2 databases in nginx, preferably in the http section:
```text
geoip2 /usr/share/GeoIP2/GeoLite2-Country.mmdb {
    auto_reload 60m;
    $geoip2_metadata_country_build metadata build_epoch;
    $geoip2_data_country_code country iso_code;
    $geoip2_data_country_name country names en;
}
geoip2 /usr/share/GeoIP2/GeoLite2-City.mmdb {
    auto_reload 60m;
    $geoip2_metadata_city_build metadata build_epoch;
    $geoip2_data_city_name city names en;
}
```
*   Test GeoIP2 using headers:
```text
add_header X-GeoCountry $geoip2_data_country_name;
add_header X-GeoCode $geoip2_data_country_code;
add_header X-GeoCity $geoip2_data_city_name;
```
*   Allow only specific countries on a website:
```text
map $geoip2_data_country_code $allowed_country {
    default no;
    CA yes;
    US yes;
}

location / {
    if ($allowed_country = no) {
        return 403;
    }
}
```

## Built-in PHP-FPM configurations

As said in synopsis, nginx-more includes a lot of built-in PHP-FPM configurations for popular CMS / Frameworks / Webapps including WordPress and Laravel. These configurations get you started quickly with hosting your CMS and makes nginx vhosts look cleaner with short blocks. Here's a few example.

### WordPress multi-user (pools) environment

Default configuration assume that PHP-FPM is configured as default, therefore listening on TCP port 9000. If you want to host multiple vhosts on a server with multiple users for enchanced security, you can setup php-fpm pools with socket (username.sock), add `-users` to the php-fpm include file and pass the username as $fpmuser variable. Here's an example of a WordPress running under user `myuser` (myuser.sock):

```text
server {
    listen 80;
    listen 443 ssl http2;
    server_name wordpress.com;
    root /home/myuser/wordpress/public_html;
    access_log /var/log/nginx/wordpress-access_log main;
    error_log /var/log/nginx/wordpress-error_log warn;

    if ($bad_bot) { return 444; }

    set $fpmuser myuser;

    include conf.d/custom/ssl.global.conf;
    include conf.d/custom/restrictions.conf;
    include conf.d/custom/pagespeed.conf;
    include conf.d/custom/fpm-wordpress-users.conf;
}
```

### Speeding up WordPress with Nginx

Nginx FastCGI cache improves WordPress performance by a lot instead of using all kinds of heavy WP plugins. It can easily be implemented by adding `-cache` to the php-fpm include file. With this configuation, Nginx wont pass PHP requests to PHP-FPM if it's in cache (20 minutes), but only if the visitor isn't logged into the WordPress, or if there's a query string or a POST to avoid caching dynamic queries. X-Cache header is added to track if the cache is HIT/MISS/BYPASS/EXPIRED. Here's an example of a WordPress running under user `myuser` with FastCGI caching:

```text
server {
    listen 80;
    listen 443 ssl http2;
    server_name wordpress.com;
    root /home/myuser/wordpress/public_html;
    access_log /var/log/nginx/wordpress-access_log main;
    error_log /var/log/nginx/wordpress-error_log warn;

    if ($bad_bot) { return 444; }

    set $fpmuser myuser;

    include conf.d/custom/ssl.global.conf;
    include conf.d/custom/restrictions.conf;
    include conf.d/custom/pagespeed.conf;
    include conf.d/custom/fpm-wordpress-cache-users.conf;
}
```
