#!/bin/bash
#
# Legacy action script for "service nginx upgrade"

if [ -f /etc/sysconfig/nginx ]; then
    . /etc/sysconfig/nginx
fi

prog=nginx
nginx=/usr/sbin/nginx
conffile=/etc/nginx/nginx.conf
pidfile=$(/usr/bin/systemctl show -p PIDFile nginx.service | sed 's/^PIDFile=//' | tr ' ' '\n')
SLEEPSEC=${SLEEPSEC:-1}
UPGRADEWAITLOOPS=${UPGRADEWAITLOOPS:-5}

oldbinpidfile=${pidfile}.oldbin
${nginx} -t -c ${conffile} -q || return 6
echo -n $"Starting new master $prog: "
pkill -F "${pidfile}" ${prog} --signal USR2
echo

for i in $(/usr/bin/seq "$UPGRADEWAITLOOPS"); do
    /bin/sleep "$SLEEPSEC"
    if [ -f "${oldbinpidfile}" ] && [ "${pidfile}" ]; then
        echo -n $"Graceful shutdown of old $prog: "
        pkill -F "${oldbinpidfile}" ${prog} --signal QUIT
        echo
        exit 0
    fi
done

echo $"Upgrade failed!"
exit 1
