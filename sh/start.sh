#!/bin/sh

# Create a reasonable startup environment

cd /root
export PS1='[\u@\h \W]\$ '
export PS2='> '
export PS4='+ '
export TERM=linux
export colors=/etc/DIR_COLORS
exec /bin/bash

