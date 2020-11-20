import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cftime
import cartopy.crs as ccrs

### -------------------------- Data cleaning functions -------------------------- ###

def convert_time(yyyymmdd):
    '''Converts a string of form YYYYMMDD to a cftime datetime object.'''
    year = int(yyyymmdd[0:4])
    month = int(yyyymmdd[4:6])
    day = int(yyyymmdd[6:8])
    return cftime.datetime(year, month, day)

def convert_coords(coord):
    if coord[-1] == 'N' or coord[-1] == 'E':
        return float(coord[0:-1])
    else:
        return -float(coord[0:-1])

def get_hurricane_attributes(dataframe, ID):
    '''For a given hurricane ID, returns key attributes of that hurricane in a dictionary.
    Attributes:
    * Duration: number of 6 hour periods that the storm is active.
    * Make_landfall: Boolean indicating whether the hurricane ever makes landfall.
    * Initial_latitude
    * Initial_longitude
    '''
    hurricane_data = dataframe[dataframe['ID']==ID]
    duration = len(hurricane_data)
    make_landfall = np.any(hurricane_data['Record'].str.contains('L'))
    initial_latitude = hurricane_data['Latitude'].iloc[0]
    initial_longitude = hurricane_data['Longitude'].iloc[0]
    if make_landfall:
        record = hurricane_data.loc[hurricane_data['Record'].str.contains('L')].iloc[0]
        landfall_latitude = record['Latitude']
        landfall_longitude = record['Longitude']
    else:
        landfall_latitude = np.nan
        landfall_longitude = np.nan

    attrs = {
        'Duration': duration,
        'Initial latitude': initial_latitude,
        'Initial longitude': initial_longitude,
        'Makes Landfall': make_landfall,
        'Landfall latitude': landfall_latitude,
        'Landfall longitude': landfall_longitude
    }
    return attrs


### -------------------------- Plotting functions -------------------------- ###

def create_geoaxes(projection=ccrs.Orthographic(-70, 30), extent=(-100, -40, 10, 50)):
    '''Creates a set of geoaxes to be passed for plotting functions.'''
    ax = plt.axes(projection=projection)
    ax.set_extent(extent)
    ax.coastlines()
    ax.gridlines()
    return ax

def plot_hurricane_trajectory(dataframe, ID, ax=create_geoaxes()):
    hurricane = dataframe[dataframe['ID']==ID]
    lats = hurricane['Latitude']
    lons = hurricane['Longitude']
    ax.plot(lons, lats, 'r-x', transform=ccrs.PlateCarree())


