#!/bin/sh

VPOPMAIL=/home/vpopmail/domains
ISOQLOG=`which isoqlog`
ISODOMAINS=/etc/isoqlog/isoqlog.domains
ISOCONF=/etc/isoqlog/isoqlog.conf
RM=`which rm`
TOUCH=`which touch`
CHOWN=`which chown`
CHMOD=`which chmod`

# Remove old domains
[ -f $ISODOMAINS ] && $RM -rf $ISODOMAINS

# Regenerate the file
for i in `ls $VPOPMAIL`; do
  echo "$i" >> $ISODOMAINS;
done

# Execute the program
$ISOQLOG -f $ISOCONF 1>/dev/null 2>&1

# Correct permissions
$CHOWN -R %{apacheuser}:%{apachegroup} /usr/share/toaster/htdocs/isoqlog
