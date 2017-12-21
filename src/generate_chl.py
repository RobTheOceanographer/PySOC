#!/usr/bin/env python

from netCDF4 import Dataset 
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import numpy

a_443_file = "/Users/rjohnson/Documents/4.CODE/so_chl/data/MODIS-Aqua/Mapped/Daily/4km/Rrs/2017/A2017317.L3m_DAY_RRS_Rrs_443_4km.nc"
a_490_file = "/Users/rjohnson/Documents/4.CODE/so_chl/data/MODIS-Aqua/Mapped/Daily/4km/Rrs/2017/A2017317.L3m_DAY_RRS_Rrs_488_4km.nc"
a_555_file = "/Users/rjohnson/Documents/4.CODE/so_chl/data/MODIS-Aqua/Mapped/Daily/4km/Rrs/2017/A2017317.L3m_DAY_RRS_Rrs_555_4km.nc"



def modis_parse_Rrs(filepath):
    """Pull out the Rrs data grid.
    Apply the scaling information on each Rrs data.
    
    Args:
        filepath (str) : Full path to the input file
    """
    print('Processing %s' % filepath)
    # Open it
    nc = Dataset(filepath, 'r')
    key = os.path.basename(filepath)[21:28]
    variable = nc.variables[key]
    print('Variable = %s' % key)
    variable.set_auto_maskandscale(False)
    print('Setting the netCDF4 auto_maskandscale to False.')
    # Get the attributes
    attributes = [str(a) for a in variable.ncattrs()]
    # Get the fill value
    if '_FillValue' in attributes:
        fill_value = variable._FillValue
    else:
        fill_value = False
    # Get the scale factors, or set them to defaults (which would do nothing)
    scale_factor = 1.0 if 'scale_factor' not in attributes else variable.scale_factor
    add_offset = 0.0 if 'add_offset' not in attributes else variable.add_offset
    # Ensure that the scale factor is not 0, otherwise we would blow away the data
    if scale_factor == 0.0:
        scale_factor = 1.0
    # Get the data
    data = variable[:]
    # Mask out the data, if there is a fill value
    print('Masking fill values')
    if fill_value is not False:
        fill_mask = data == fill_value
    # Apply the scaling information
    print('Applying scaling: (data * %s) + %s' % (scale_factor, add_offset))
    data = (data * scale_factor) + add_offset
    # Remask the data, if there is a fill value
    print('Re-applying fill values')
    if fill_value is not False:
        data[fill_mask] = fill_value
    print('Turning fill values into nans')
    data[numpy.where(data == fill_value)] = numpy.nan
    return data


data_443 = modis_parse_Rrs(a_443_file)
data_490 = modis_parse_Rrs(a_490_file)
data_555 = modis_parse_Rrs(a_555_file)


# Calculate the Southern Ocean Chlorophyll.
def calculate_southern_ocean_chlorophyll(data_443, data_490, data_555):
    """Calculate the modis aqua southern ocean Chl based on Johnson et al 2013.
    
    Args:
        data_443 (array) : an array that is scaled and had the fill values put in.
        data_490 (array) : an array that is scaled and had the fill values put in.
        data_555 (array) : an array that is scaled and had the fill values put in.
    """
    # Calculate the Rrr maximum band ratio log10(Rrs(443/555) > Rrs(490/555))
    MBR = numpy.log10(numpy.maximum((data_443/data_555),(data_490/data_555)))
    # Calculate SO Chl.
    SO_Chl = 10**(0.6994 - 2.0384 * MBR - 0.4656 * (MBR**2) + 0.4337 * (MBR**3))
    # SO_Chl = 10.^(0.6994 - 2.0384 * MBR - 0.4656 * (MBR.^2) + 0.4337 * (MBR.^3));
    return SO_Chl

SO_Chl = calculate_southern_ocean_chlorophyll(data_443, data_490, data_555)

nc_fid = Dataset(a_443_file, 'r')
lats = nc_fid.variables['lat'][:]  # extract/copy the data
lons = nc_fid.variables['lon'][:]

# Subset the arrays.
SO_Chl = SO_Chl[numpy.where(lats < -40),:]
lats = lats[numpy.where(lats < -40)]


# write out a CF compliant netcdf file.
#  - draw on the metadat from the xarray dataset object





















# Plot
from matplotlib import cm
fig = plt.figure(figsize=(12, 12))
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)
# Setup the map. See http://matplotlib.org/basemap/users/mapsetup.html
# for other projections.
# m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)
m = Basemap(projection='spstere',boundinglat=-30,lon_0=90,resolution='l')
m.drawcoastlines()
# Create 2D lat/lon arrays for Basemap
lon2d, lat2d = np.meshgrid(lons, lats)
# Transforms lat/lon into plotting coordinates for projection
x, y = m(lon2d, lat2d)
cs = m.contourf(x, y, SO_Chl[0,:,:], 11, cmap=plt.cm.Spectral_r, levels = [0, 0.5, 1,2,3,4,5])
cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5, cmap=cm.viridis)







