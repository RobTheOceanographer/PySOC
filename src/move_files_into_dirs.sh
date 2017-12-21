#!/usr/bin/env bash

# This moves the data that was downloaded into the Rrs directory into the appropriate year dir.

########################################################################
#                                                            Configs
########################################################################
export ROOTDIR="/Users/rjohnson/Documents/4.CODE/so_chl"
export INCOMINGDIR="$ROOTDIR/data/MODIS-Aqua/Mapped/Daily/4km/Rrs"

########################################################################
#                                                           mkdirs
########################################################################
cd $INCOMINGDIR
mkdir -p {2002..2018}

########################################################################
#                                                           move files
########################################################################
for f in $( ls *.nc ); do
  echo moving: $f
  year=`echo $f | cut -c2-5`
  echo into: $year
  mv $f $year
done
