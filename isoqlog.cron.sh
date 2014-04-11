#!/bin/sh

confdir=/etc/isoqlog

# Generate the domains file
ls /home/vpopmail/domains >$confdir/isoqlog.domains

# Execute the program
isoqlog -f $confdir/isoqlog.conf >/dev/null 2>&1

# Correct permissions
chown -R apache:apache /usr/share/isoqlog/htdocs
