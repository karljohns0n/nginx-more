# Nginx-more User Guide

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
