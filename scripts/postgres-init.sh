#!/bin/bash

DBUSER=`whoami`

pushd /tmp > /dev/null     # stupid way to silence potential errors about postgres user being in cwd
sudo -u postgres createuser --createdb --no-password --no-superuser --no-createrole $DBUSER 
createdb --no-password --owner=$DBUSER s2g
popd > /dev/null
