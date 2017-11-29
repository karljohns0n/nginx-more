## Synopsis

Nginx-more is a rebuild of Nginx with additional open source modules such as PageSpeed, Brotli, More Headers, Cache Purge, VTS. It's compiled using GCC 5.3 with the latest OpenSSL stable sources. It also includes a lot of built-in configurations such as WordPress and Laravel php-fpm setup.

## BUILD

Here's the procedure to build nginx-more rpm for CentOS 6 and 7:

```bash
NGINXV=1.12.2-2
GKEY=$(cat /home/karl/.gnupg/pkey)
pushd /home/karl/pkg-nginx-more
rm -rf RPMS/*
rm -rf SRPMS/*

mock --old-chroot -r aeris-6-x86_64 --spec=/home/karl/pkg-nginx-more/SPECS/nginx-more.spec --sources=SOURCES --resultdir=SRPMS --buildsrpm && mock --old-chroot --clean -D 'dist .el6' -r aeris-6-x86_64 --resultdir=RPMS --rebuild SRPMS/nginx-more-$NGINXV.el6.src.rpm && echo $GKEY && rpm --addsign RPMS/nginx-more-$NGINXV.el6.x86_64.rpm

mock --old-chroot -r aeris-7-x86_64 --spec=/home/karl/pkg-nginx-more/SPECS/nginx-more.spec --sources=SOURCES --resultdir=SRPMS --buildsrpm && mv SRPMS/nginx-more-$NGINXV.el7.centos.src.rpm SRPMS/nginx-more-$NGINXV.el7.src.rpm && mock --old-chroot --clean -D 'dist .el7' -r aeris-7-x86_64 --resultdir=RPMS --rebuild SRPMS/nginx-more-$NGINXV.el7.src.rpm && echo $GKEY && rpm --addsign RPMS/nginx-more-$NGINXV.el7.x86_64.rpm

sudo \cp -uf /home/karl/pkg-nginx-more/RPMS/nginx-more-$NGINXV.el6.x86_64.rpm /var/www/html/repo/testing/centos/6/x86_64/
sudo \cp -uf /home/karl/pkg-nginx-more/RPMS/nginx-more-$NGINXV.el7.x86_64.rpm /var/www/html/repo/testing/centos/7/x86_64/

sudo createrepo_c /var/www/html/repo/testing/centos/7/x86_64/
sudo repoview /var/www/html/repo/testing/centos/7/x86_64/
sudo createrepo_c /var/www/html/repo/testing/centos/6/x86_64/
sudo repoview /var/www/html/repo/testing/centos/6/x86_64/
sudo chown -R apache:apache /var/www/html/repo

sudo mv /var/www/html/repo/testing/centos/6/x86_64/nginx-more-$NGINXV.el6.x86_64.rpm /var/www/html/repo/stable/centos/6/x86_64/
sudo mv /var/www/html/repo/testing/centos/7/x86_64/nginx-more-$NGINXV.el7.x86_64.rpm /var/www/html/repo/stable/centos/7/x86_64/
sudo createrepo_c /var/www/html/repo/stable/centos/7/x86_64/
sudo repoview /var/www/html/repo/stable/centos/7/x86_64/
sudo createrepo_c /var/www/html/repo/stable/centos/6/x86_64/
sudo repoview /var/www/html/repo/stable/centos/6/x86_64/
sudo createrepo_c /var/www/html/repo/testing/centos/7/x86_64/
sudo repoview /var/www/html/repo/testing/centos/7/x86_64/
sudo createrepo_c /var/www/html/repo/testing/centos/6/x86_64/
sudo repoview /var/www/html/repo/testing/centos/6/x86_64/
sudo chown -R apache:apache /var/www/html/repo
```
