#!/usr/bin/env bash

########################################################################
#                                                            Configs
########################################################################
export DATADIR="/rd/private/ocd/MODIS-Aqua/Mapped/Daily/4km/Rrs"

########################################################################
#                                                           wget
########################################################################
cd $DATADIR

wget -q --post-data="sensor=aqua&sdate=2002-01-01&edate=2017-12-01&dtype=L3m&addurl=1&results_as_file=1&search=A*DAY_RRS_Rrs*4km*" -O - https://oceandata.sci.gsfc.nasa.gov/api/file_search | wget -nc --continue -i -

echo "Finished downloading."
