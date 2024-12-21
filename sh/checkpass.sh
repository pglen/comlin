#!/bin/bash

. /sh/functions.sh

# Check for changed passwords, change messages based upon it, notify user

TTT=.tmppass
RRR=.orgpass

cmpPass() {
    if [ -f $1/$RRR ] ; then
        grep "$2:" /etc/shadow > ~/$TTT
        diff ~/$TTT $1/$RRR >/dev/null 2>&1

        # Pass changed, copy real messages
        if [ $? -ne 0 ] ; then
	        cp /etc/issue.new /etc/issue
            mv /etc/motd /etc/motd.old
			echo "Welcome to Community Linux" > /etc/motd
            # Only check once
            #rm /$1/$RRR
        else
            # Tell the user
            /apps/notify/notify -r -d $3 -t 6000 "Password Alert" \
			"'$2' password has not yet been changed from its original. Please change $2's password."  &
        fi

        # Clean up
        rm ~/$TTT
    fi
}

cmpPass /root root 15
cmpPass /home/user user 25

