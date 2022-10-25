#!/bin/bash
#
# Fetch nginx-more srpm SOURCES from spectool if URL is provided else from the CDN

spectool -C /tmp/nginx-more/SOURCES/ -g <(rpmspec -P /tmp/nginx-more/SPECS/nginx-more.spec)

for SOURCES in $(spectool -l -S <(rpmspec -P /tmp/nginx-more/SPECS/nginx-more.spec)|grep ".tar.gz" | grep -vi 'http:\|https:\|ftp' |awk '{print $2}')
do
	wget -q -P /tmp/nginx-more/SOURCES/ "$1""$SOURCES" && echo "$SOURCES downloaded." || echo "Error downloading $SOURCES."
done