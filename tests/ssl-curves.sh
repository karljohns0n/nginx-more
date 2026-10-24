#!/bin/bash
set -euo pipefail

runtime=$(mktemp -d)
trap 'rm -rf "$runtime"' EXIT
openssl req -x509 -newkey rsa:2048 -nodes -keyout "$runtime/key.pem" \
    -out "$runtime/cert.pem" -days 1 -subj /CN=localhost > "$runtime/cert.log" 2>&1

example_curves=$(awk '$1 == "ssl_ecdh_curve" { sub(/;$/, "", $2); print $2 }' \
    /etc/nginx/conf.d/custom/ssl.conf-example)
test -n "$example_curves"

# The legacy list reproduces an unchanged configuration from before OpenSSL 4.
for curves in X25519:P-256:P-384:P-224:P-521 "$example_curves" auto; do
    cat > "$runtime/nginx.conf" <<EOF
pid $runtime/nginx.pid;
error_log $runtime/error.log notice;
events { worker_connections 128; }
http {
    access_log off;
    client_body_temp_path $runtime/client;
    proxy_temp_path $runtime/proxy;
    fastcgi_temp_path $runtime/fastcgi;
    uwsgi_temp_path $runtime/uwsgi;
    scgi_temp_path $runtime/scgi;
    server {
        listen 127.0.0.1:18443 ssl;
        ssl_certificate $runtime/cert.pem;
        ssl_certificate_key $runtime/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ecdh_curve $curves;
        ssl_buffer_size 1400;
    }
}
EOF
    nginx -e "$runtime/error.log" -t -p "$runtime/" -c "$runtime/nginx.conf"
    printf 'TLS curve configuration accepted: %s\n' "$curves"
done

# Validate the complete installed example with a disposable certificate.
sed \
    -e "s|^ssl_certificate .*|ssl_certificate $runtime/cert.pem;|" \
    -e "s|^ssl_certificate_key .*|ssl_certificate_key $runtime/key.pem;|" \
    -e "s|^ssl_trusted_certificate .*|ssl_trusted_certificate $runtime/cert.pem;|" \
    /etc/nginx/conf.d/custom/ssl.conf-example > "$runtime/ssl-example.conf"
sed "s|ssl_protocols TLSv1.2 TLSv1.3;|include $runtime/ssl-example.conf;|" \
    "$runtime/nginx.conf" \
    | sed \
        -e '/^[[:space:]]*ssl_certificate /d' \
        -e '/^[[:space:]]*ssl_certificate_key /d' \
        -e '/^[[:space:]]*ssl_prefer_server_ciphers /d' \
        -e '/^[[:space:]]*ssl_ecdh_curve /d' \
        -e '/^[[:space:]]*ssl_buffer_size /d' \
    > "$runtime/full-example.conf"
nginx -e "$runtime/error.log" -t -p "$runtime/" -c "$runtime/full-example.conf"
printf 'Complete SSL example configuration accepted\n'
