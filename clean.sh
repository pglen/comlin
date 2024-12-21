#!/bin/sh

# This script is used to clean generated files
# Portions Copyright (C) by Peter Glen. See open source license for details.

HERE=`pwd`
PROJ=`basename $HERE`

# Do some cleaning
echo "Cleaning .."

rm -rf _work

echo Done.


