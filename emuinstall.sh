#!/bin/sh

BASE_PATH=`pwd`

echo "Welcome to the EmuWebmail installation script!"
echo "This script will install and configure EMUWebmail for basic usage."
echo "It is strongly recommended that you review the default settings after"
echo "installation. A good place to start is the 'site.emu' file in the"
echo "'webmail/data/' directory of your new installation."
echo

echo "This script need some basic information before it can begin. For any of"
echo "these questions, you can simply press 'enter' to accept the default value."
echo
echo "Where would you like EmuWebmail installed? [Default: /home/EMU]"
echo -n "Path: "
read INST_PATH
if [ ! $INST_PATH ] ; then 
   INST_PATH=/home/EMU
   echo "Using '$INST_PATH'"
fi

echo "What user should the new installation be owned by? [Default: nobody]"
echo -n "Owner: "
read INST_OWNER
if [ ! $INST_OWNER ] ; then 
   INST_OWNER='nobody'
   echo "Using '$INST_OWNER'"
fi

echo "What group should the new installation be assigned to? [Default: nobody]"
echo -n "Group: "
read INST_GROUP
if [ ! $INST_GROUP ] ; then 
   INST_GROUP='nobody'
   echo "Using '$INST_GROUP'"
fi

# Set up emuwebmail

mkdir -p $INST_PATH
cd $INST_PATH
echo "Un-packing EmuWebmail.tar.gz to $INST_PATH"
gzip -dc $BASE_PATH/EmuWebmail.tar.gz | tar -xf -
cd $BASE_PATH
echo "Setting ownership..."
chown -R $INST_OWNER $INST_PATH
chgrp -R $INST_GROUP $INST_PATH

echo "page_root=$INST_PATH/webmail/data" > $INST_PATH/webmail/html/init.emu

# Build modules
if [ -f modules.tar.gz ] ; then
   echo "Installing Perl modules!"
   gzip -dc modules.tar.gz | tar -xf -
   cd modules
   ./modules-build.pl
   cd ..
   cp -R modules/built_modules/* $INST_PATH/lib
fi

echo "All Done!"
echo "Add, in access.conf or httpd.conf (which are probably in /etc/httpd/conf/):"
echo " "
echo "<VirtualHost webmail>"
echo "DirectoryIndex emumail.cgi index.html"
echo "AddHandler cgi-script .cgi"
echo "DocumentRoot /home/EMU/webmail/html"
echo "<Directory /home/EMU/webmail/html>"
echo "   Options FollowSymlinks ExecCGI"
echo "</Directory>"
echo "Alias /webmail /home/EMU/webmail/html"
echo "RewriteEngine on"
echo "RewriteRule ^/$ /webmail/ [R,L]"
echo "</VirtualHost>"
echo
