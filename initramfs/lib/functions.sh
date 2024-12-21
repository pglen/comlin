# Functions for custom dracut
 
# ------------------------------------------------------------------------
# Iterate /dev/sd[a-f][1-4], if we can mount it, test for the 
# 'comboot' file.
# Revisions:
#             apr 4 2015:           Moved to dracut
#             apr 6 2015:           Added locals
#                                   Removed ret code test from mount

mountUSB() {
    local ii iii
    mkdir -p /mnt/guest >/dev/null 2>&1
    # Expand the strings in line
    for ii in /dev/sda /dev/sdb /dev/sdc /dev/sdd /dev/sde /dev/sdf /dev/sdg /dev/sdh ; do
        #echo "Drive" $ii
        sleep 0.1                                   # Needs to breathe
        for iii in "$ii"1 "$ii"2 "$ii"3 "$ii"4; do
            #echo -n "$iii "
            #if 
                mount -t $MYFST $iii /mnt/guest >/dev/null 2>&1 #; then
                #echo "Testing file on $iii"
                if test -f /mnt/guest/comboot; then
                    echo "Found COMLIN system at $iii"
                    umount $iii >/dev/null 2>&1
                    DEVICE=$iii
                    return 0
                else
                    umount $iii >/dev/null 2>&1
                fi
            #fi
            done
        done
    return 1
}
            
# ------------------------------------------------------------------------

dosh() 
{
    export PS1="Tmp Shell\${PWD}# "
    [ -e /.profile ] || echo "exec 0<>/dev/console 1<>/dev/console 2<>/dev/console" > /.profile
    sh -i -l
}
        
# ------------------------------------------------------------------------

wait_for_loginit()
{
    if getarg rdinitdebug; then
    set +x
    exec 0<>/dev/console 1<>/dev/console 2<>/dev/console
    # wait for loginit
    i=0
    while [ $i -lt 10 ]; do 
        j=$(jobs)
        [ -z "$j" ] && break
        [ -z "${j##*Running*}" ] || break
        sleep 0.1
        i=$(($i+1))
    done    
    [ $i -eq 10 ] && kill %1 >/dev/null 2>&1

        while pidof -x /sbin/loginit >/dev/null 2>&1; do
            for pid in $(pidof -x /sbin/loginit); do
                kill $HARD $pid >/dev/null 2>&1
            done
            HARD="-9"
        done
    set -x
    fi
}

# ------------------------------------------------------------------------

emergency_shell()
{
    set +e
    if [ "$1" = "-n" ]; then
        _rdshell_name=$2
        shift 2 
    else
        _rdshell_name=dracut
    fi
    wait_for_loginit
    echo ; echo
    warn $@
    source_all emergency
    echo
    
    [ -e /.die ] && sleep 3; exit 1
    
    if getarg rdshell || getarg rdbreak; then
        echo "Dropping to debug shell."
        echo
        export PS1="$_rdshell_name:\${PWD}# "
        [ -e /.profile ] || echo "exec 0<>/dev/console 1<>/dev/console 2<>/dev/console" > /.profile
        sh -i -l
    else
        warn "Boot has failed. To debug this issue add \"rdshell\" to the kernel command line."
        warn "Exiting this shell will return to the dracut script"
        export PS1="$_rdshell_name:\${PWD}# "
        [ -e /.profile ] || echo "exec 0<>/dev/console 1<>/dev/console 2<>/dev/console" > /.profile
        sh -i -l
        #exit 1
    fi
}



