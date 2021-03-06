import numpy as np
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid, cm
import os


def ncdump(nc_fid, verb=True):
    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print "NetCDF Global Attributes:"
        for nc_attr in nc_attrs:
            print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print "NetCDF dimension information:"
        for dim in nc_dims:
            print "\tName:", dim 
            print "\t\tsize:", len(nc_fid.dimensions[dim])
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print "NetCDF variable information:"
        for var in nc_vars:
            if var not in nc_dims:
                print '\tName:', var
                print "\t\tdimensions:", nc_fid.variables[var].dimensions
                print "\t\tsize:", nc_fid.variables[var].size
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars


heat_flux = 'data/AN1-HF.grd'

# an_model is initial array, ny and nx resolution

nc_fid = Dataset(heat_flux, 'r')
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)
# Extract data from NetCDF file

lons = nc_fid.variables['lon'][:]
lats = nc_fid.variables['lat'][:]
flux = nc_fid.variables['z'][:]
	
ny, nx = flux.shape


#print 'lats', lats
#print 'lons', lons

min_f = np.nanmin(flux)
max_f = np.nanmax(flux) #Tweek for better color map range 

print 'Heat flow range from %s to %s ' %(min_f, max_f)

#print lats


fig = plt.figure(figsize=(14,14))
#fig.suptitle("Heat flux (An et al 2015)", fontsize=16)

map = Basemap(projection='spstere',boundinglat=-60,lon_0=180,resolution='f')
map.drawcoastlines(color='white', linewidth=2.0)
map.drawparallels(np.arange(-80.,81.,30.))
map.drawmeridians(np.arange(-180.,181.,30.))
	
lons = np.linspace(min(lons), max(lons), nx)
lats = np.linspace(min(lats), max(lats), ny)
plotdata = map.transform_scalar(flux, lons, lats, nx, ny)
im = map.imshow(plotdata, vmin = min_f, vmax = max_f, cmap = plt.cm.magma) #viridis
cb = fig.colorbar(im, orientation='horizontal',fraction=0.046, pad=0.04)
cb.ax.tick_params(labelsize=24)             
cb.ax.yaxis.set_tick_params(color='w')


plt.savefig('fig/An_HEAT.png', bbox_inches='tight',transparent=True)

#plt.tight_layout()
#plt.show()

