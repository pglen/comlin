#!/bin/sh

echo "Testing dracut lib"

. ./dracut-lib.sh
. ./functions.sh

getarg "root" && echo "got"
echo ret=$?
dosh

