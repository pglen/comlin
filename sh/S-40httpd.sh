#!/bin/bash

echo -n "Starting Web Server ... "
mkdir -p /var/www/html
/usr/sbin/httpd >/dev/null 2>&1
echo OK

