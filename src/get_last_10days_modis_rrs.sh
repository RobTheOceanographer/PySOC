#!/usr/bin/env bash

# This downloads the data into the Rrs dir but not into year directories.

########################################################################
#                                                            Configs
########################################################################
export ROOTDIR="/Users/rjohnson/Documents/4.CODE/so_chl"
export INCOMINGDIR="$ROOTDIR/data/MODIS-Aqua/Mapped/Daily/4km/Rrs"
export ENDDATE=`date +%Y-%m-%d`
export STARTDATE=`date -v-10d +%Y-%m-%d`

########################################################################
#                                                           wget
########################################################################
cd $INCOMINGDIR

wget -q --post-data="sensor=aqua&sdate=$STARTDATE&edate=$ENDDATE&dtype=L3m&addurl=1&results_as_file=1&search=A*DAY_RRS_Rrs*4km*" -O - https://oceandata.sci.gsfc.nasa.gov/api/file_search | wget -nc --continue -i -

echo "Finished downloading."
