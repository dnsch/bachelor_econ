#Imports

#standard modules
import pandas as pd
import numpy as np
import os
import re
#plots:
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cartopy
import cartopy.feature as cf
import cartopy.crs as ccrs
import seaborn as sns
import folium
from folium.plugins import HeatMap, HeatMapWithTime
#data
from netCDF4 import Dataset
from datetime import datetime
#IO
import openpyxl
#speedup
from numba import jit
#animations
from celluloid import Camera # getting the camera
from IPython.display import HTML # to show the animation in Jupyter


######################################################################
# Global Variables
######################################################################

# get parent working dir
parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


######################################################################
# Functions
######################################################################


"--------------------------------------------------------------------"
'Data Processing Functions'
"--------------------------------------------------------------------"



def process_merra_data(data_directory, seasonal = True, variables = [], two_vars = True, hourly = False, time_steps = 0, y_steps = 91, x_steps = 0, datatype = 'float32'):
    """
    process_merra_data() returns the mean numpy array of the MERRA2 lists for given variables (max 2 variables per MERRA2 netCDF4 file) 
    and a given frequency and optionally also the mean numpy arrays for the dry and wet seasons.
    It can also save the values of the MERRA2 lists to a numpy array and return it.
    It can also optionally return a list of indices that indicate which entries of the numpy array belong to the dry and which to the wet season.
    
    Parameters:
        data_directory(string):     a string of a directory relative to the parent directory in which this code is stored that points to the folder
                                    that contains the MERRA2 netCDF4 files list
        seasonal(boolean):          a boolean that indicates whether the data for the wet and dry season shall be returned. This is set to 'True' by default.
        variables(list):            a list containing the strings of variable names in the MERRA2 netCDF4 file. A maximum of 2 variables per netCDF4 can be processed.
        two_vars(boolean):          a boolean indicating whether the MERRA2 netCDF4 file contains 2 variables of interest. This is set to 'True' by default.
        hourly(boolean):            a boolean indicating wether the MERRA2 netCDF4 file has a hourly frequency. This is set to 'False' by default.
        time_steps(int):            an int for the number of total time steps (the 0 axis) in the optionally returned numpy array.
                                    For example, the number of time steps for a file that provides hourly data from 1980-01-01 to 2016-12-31 is 24x13515=324360.
                                    This is set to 0 by default.
        y_steps(int):               an int for the number of y steps (the 1 axis) in the returned numpy array.
                                    For example, the number of y steps for the latitudes from 15°S to 30°N in the y size of a MERRA2 grid is 91.
                                    This is set to 91 by default.
        x_steps(int):               an int for the number of x steps (the 2 axis) in the returned numpy array.
                                    For example, the number of y steps for the latitudes from 30°W to 35°E in the x size of a MERRA2 grid is 105.
                                    This is set to 105 by default.
        datatype(string):           a string for the datatype being used in the returned numpy array. This is set to 'float32' by default.

    Returns:
        longitudes(list):           a list containing the longitudes of the input variables.
        latitudes(list):            a list containing the latiitudes of the input variables.
        time(list):                 a list containing the time steps of the input variables.
        junsep_indices(list):       a list of indices for the values of the returned numpy array that belong to the wet season.
        novapr_indices(list):       a list of indices for the values of the returned numpy array that belong to the dry season.
        data_junsep(ndarray):       a numpy array containing the mean values for the wet seasons.
        data_novapr(ndarray):       a numpy array containing the mean values for the dry seasons.
        data_total(ndarray):        a numpy array containing the mean values for the entire time.
        
        If hourly:
        longitudes(list):           a list containing the longitudes of the input variables.
        latitudes(list):            a list containing the latiitudes of the input variables.
        time(list):                 a list containing the time steps of the input variables.
        data_total_time_0(ndarray): a numpy array containing the MERRA2 values for the given variable for the entire given time.
        data_junsep_0(ndarray):     a numpy array containing the mean values for the wet seasons.
        data_novapr_0(ndarray):     a numpy array containing the mean values for the dry seasons.
        data_total_0(ndarray):      a numpy array containing the mean values for the entire time.

        If hourly & two_vars:
        longitudes(list):           a list containing the longitudes of the input variables.
        latitudes(list):            a list containing the latiitudes of the input variables.
        time(list):                 a list containing the time steps of the input variables.
        data_total_time_0(ndarray): a numpy array containing the MERRA2 values for the first variable for the entire given time.
        data_total_time_1(ndarray): a numpy array containing the MERRA2 values for the second variable for the entire given time.
        junsep_indices(list):       a list of indices for the values of the returned numpy array that belong to the wet season.
        novapr_indices(list):       a list of indices for the values of the returned numpy array that belong to the dry season.
        data_junsep_0(ndarray):     a numpy array containing the mean values for the wet seasons of the first variable.
        data_novapr_0(ndarray):     a numpy array containing the mean values for the dry seasons of the first variable.
        data_total_0(ndarray):      a numpy array containing the mean values for the entire time of the first variable.
        data_junsep_1(ndarray):     a numpy array containing the mean values for the wet seasons of the second variable.
        data_novapr_1(ndarray):     a numpy array containing the mean values for the dry seasons of the second variable.
        data_total_1(ndarray):      a numpy array containing the mean values for the entire time of the second variable.
    """

    
    # add path to data folder of interest
    directory = parent_directory + data_directory

    #aod MERRA2 files have a different naming structure and hence the need of adjustment
    aod = False

    if (directory[-5:] == 's_Nx\\'):
        aod = True

    # boolean to for later initialization of all variables and arrays
    first = True

    file_list = os.listdir(directory)
    # counter variables for mean calculation and indication of wet and dry seasons
    # (daily/monthly depending on input)
    counter_total = 0
    if seasonal:
        counter_junsep = 0
        counter_novapr = 0
        junsep_indices = []
        novapr_indices = []

    # build array for dates to later check if the time range of the files analyzed
    # is continuous and that there are no missing values
    continuity_check = []

    # loop over all files in data folder of interest
    for filename in sorted(file_list):
        with open(os.path.join(directory, filename), 'r') as file: #open in readonly mode
            data = Dataset(directory + filename, more="r")

            #init data array
            if (first):
                #longitudes, latitudes and time for the netCDF4 file.
                # This doesn't change, so can be set at initialization
                longitudes = data.variables['lon'][:]
                latitudes = data.variables['lat'][:]
                time = data.variables['time'][:]

                if hourly:
                    
                    if two_vars:

                        if seasonal:
                            #init by always taking daily mean
                            data_junsep_0 = data.variables[variables[0]][:,:,:]
                            data_junsep_0 = np.sum(data_junsep_0, axis = 0); data_junsep_0 /= 24

                            data_junsep_1 = data.variables[variables[1]][:,:,:]
                            data_junsep_1 = np.sum(data_junsep_1, axis = 0); data_junsep_1 /= 24

                            data_novapr_0 = data.variables[variables[0]][:,:,:]
                            data_novapr_0 = np.sum(data_novapr_0, axis = 0); data_novapr_0 /= 24

                            data_novapr_1 = data.variables[variables[0]][:,:,:]
                            data_novapr_1 = np.sum(data_novapr_1, axis = 0); data_novapr_1 /= 24

                            for i in range(24*counter_total, 24*counter_total + 24) : novapr_indices.append(i) 
                        #create data ndarray with initialized time steps
                        data_total_0 = data.variables[variables[0]][:,:,:]
                        data_total_time_0 = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                        data_total_time_0[0:24,:,:] = data_total_0
                        data_total_0 = np.sum(data_total_0, axis = 0); data_total_0 /= 24

                        data_total_1 = data.variables[variables[1]][:,:,:]
                        data_total_time_1 = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                        data_total_time_1[0:24,:,:] = data_total_1
                        data_total_1 = np.sum(data_total_1, axis = 0); data_total_1 /= 24

                    else:

                        if seasonal:

                            data_junsep_0 = data.variables[variables[0]][:,:,:]
                            data_junsep_0 = np.sum(data_junsep_0, axis = 0); data_junsep_0 /= 24

                            data_novapr_0 = data.variables[variables[0]][:,:,:]
                            data_novapr_0 = np.sum(data_novapr_0, axis = 0); data_novapr_0 /= 24

                            for i in range(24*counter_total, 24*counter_total + 24) : novapr_indices.append(i) 

                        data_total_0 = data.variables[variables[0]][:,:,:]
                        data_total_time_0 = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                        data_total_time_0[0:24,:,:] = data_total_0
                        data_total_0 = np.sum(data_total_0, axis = 0); data_total_0 /= 24

                else:
                    if seasonal:
                        data_junsep = data.variables[variables[0]][:,:,:]; data_junsep = data_junsep[0,:,:]
                        data_novapr = data.variables[variables[0]][:,:,:]; data_novapr = data_novapr[0,:,:]
                    data_total = data.variables[variables[0]][:,:,:]; data_total = data_total[0,:,:]

                if seasonal:
                    counter_novapr += 1
                counter_total += 1
                # continuity check to see if we got all dates covered
                # since aod files have another naming convention, we control for that
                if aod:
                    continuity_check.append(datetime.strptime(filename[27:33], '%Y%m').strftime('%Y-%m'))
                else:
                    continuity_check.append(datetime.strptime(filename[27:35], '%Y%m%d').strftime('%Y-%m-%d'))
                
                first = False
                continue

            if seasonal:
                # calculate mean for jun-sep period using regex
                if (re.search(r'(.*)-(06|07|08|09)-(.*)', data.RangeBeginningDate)):
                    # calculate current data to add to overall data

                    if hourly:
                    
                        data_current_0 = data.variables[variables[0]][:,:,:]
                        data_current_time_0 = data_current_0
                        data_current_0 = np.sum(data_current_0, axis = 0); data_current_0 /= 24
                        data_junsep_0 += data_current_0

                        if two_vars:

                            data_current_1 = data.variables[variables[1]][:,:,:]
                            data_current_time_1 = data_current_1
                            data_current_1 = np.sum(data_current_1, axis = 0); data_current_1 /= 24
                            data_junsep_1 += data_current_1

                        for i in range(24*counter_total, 24*counter_total + 24) : junsep_indices.append(i) 

                    else:

                        data_current = data.variables[variables[0]][:,:,:]; data_current = data_current[0,:,:]
                        data_junsep += data_current

                    counter_junsep += 1

                # calculate mean for nov-apr period using regex
                if (re.search(r'(.*)-(11|12|01|02|03|04)-(.*)', data.RangeBeginningDate)):
                    # calculate current data to add to overall data

                    if hourly:
                    
                        data_current_0 = data.variables[variables[0]][:,:,:]
                        data_current_time_0 = data_current_0
                        data_current_0 = np.sum(data_current_0, axis = 0); data_current_0 /= 24
                        data_novapr_0 += data_current_0

                        if two_vars:

                            data_current_1 = data.variables[variables[1]][:,:,:]
                            data_current_time_1 = data_current_1
                            data_current_1 = np.sum(data_current_1, axis = 0); data_current_1 /= 24
                            data_novapr_1 += data_current_1

                        for i in range(24*counter_total, 24*counter_total + 24) : novapr_indices.append(i) 

                    else:

                        data_current = data.variables[variables[0]][:,:,:]; data_current = data_current[0,:,:]
                        data_novapr += data_current
                        
                    counter_novapr += 1

            # calculate total data independent of season

            if hourly:
                    
                data_current_0 = data.variables[variables[0]][:,:,:]
                data_current_time_0 = data_current_0
                data_current_0 = np.sum(data_current_0, axis = 0); data_current_0 /= 24
                data_total_0 += data_current_0
                data_total_time_0[24*counter_total: 24*counter_total+24,:,:] = data_current_time_0

                if two_vars:

                    data_current_1 = data.variables[variables[1]][:,:,:]
                    data_current_time_1 = data_current_1
                    data_current_1 = np.sum(data_current_1, axis = 0); data_current_1 /= 24
                    data_total_1 += data_current_1
                    data_total_time_1[24*counter_total:24*counter_total+24,:,:] = data_current_time_1

            else:

                data_current = data.variables[variables[0]][:,:,:]; data_current = data_current[0,:,:]
                data_total += data_current

            counter_total += 1

            # add to dates array

            if aod:
                continuity_check.append(datetime.strptime(filename[27:33], '%Y%m').strftime('%Y-%m'))
            else:
                continuity_check.append(datetime.strptime(filename[27:35], '%Y%m%d').strftime('%Y-%m-%d'))

    # divide for mean

    if hourly:

        data_junsep_0 /= counter_junsep
        data_novapr_0 /= counter_novapr
        data_total_0 /= counter_total

        if two_vars:

            data_junsep_1 /= counter_junsep
            data_novapr_1 /= counter_novapr
            data_total_1 /= counter_total
    else:
        data_junsep /= counter_junsep
        data_novapr /= counter_novapr
        data_total /= counter_total


    # continuity check:
    if hourly:
        # given time range:
        test_ts = pd.Series(pd.to_datetime(continuity_check))
        # continuous time range from 1980-01-01 to 2016-12-31
        continuous_ts = pd.date_range(start='1980-01-01', end='2016-12-31')
        assert (continuous_ts.difference(test_ts).size == 0)
        if two_vars:
            return [longitudes, latitudes, time, data_total_time_0, data_total_time_1,junsep_indices, novapr_indices,data_junsep_0, data_novapr_0, data_total_0, data_junsep_1, data_novapr_1, data_total_1]
        else:
            return [longitudes, latitudes, time, data_total_time_0,junsep_indices, novapr_indices,data_junsep_0, data_novapr_0, data_total_0]
    else:
        #given time range:
        test_ts = pd.Series(pd.to_datetime(continuity_check).strftime('%Y-%m'))
        #continuous time range from 1980-01 to 2016-12
        continuous_ts = pd.date_range(start='1980-01', end='2016-12', freq='M').strftime('%Y-%m')
        assert (continuous_ts.difference(test_ts).size == 0)
        return [longitudes, latitudes, time, junsep_indices, novapr_indices,data_junsep, data_novapr, data_total]


def process_outcome_data():
    """
    process_outcome_data() returns dataframes of the economic input data of interest.

    Returns:
        df_pwt_resid_log(dataframe):    a dataframe of the residualized logarithmic gdp of the Penn World Tables for 1980-2016 and countries of interest
        df_wbdi_resid_log(dataframe):   a dataframe of the residualized logarithmic gdp of the World Bank Development Indicators for 1980-2016 and countries of interest
        df_mpd_resid_log(dataframe):    a dataframe of the residualized logarithmic gdp of the Maddison Project Database for 1980-2016 and countries of interest
    """

    #create times and countries of interest
    columns_years =  list(range(1980, 2017))
    countries = ['Benin', 'Burkina Faso', 'Gambia', 'Ghana', 'Guinea', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Sierra Leone', 'Senegal', 'Togo']

    #Penn World Tables:
    file_pwt = parent_directory + '\\raw_data\\2.2_outcome_data\\penn_world_tables\\FebPwtExport2232022.csv'

    #country codes in pwt dataset
    country_codes = ['BEN', 'BFA', 'GMB', 'GHA', 'GIN', 'LBR', 'MLI', 'NER', 'NGA', 'SLE', 'SEN', 'TGO']

    #create pwt data frame that will be plotted later
    df_pwt = pd.DataFrame(columns = columns_years)
    df_pwt.insert (0, "country", countries)

    pwt = pd.read_csv(file_pwt)

    #create dataframe from csv file
    for country,country_code in enumerate(country_codes):
        for year in range(1980, 2017):
            df_pwt.at[country,year] = pwt['AggValue'].loc[(pwt['RegionCode'] == country_code) & (pwt['YearCode'] == year)].values[0]

    #create residualized log dataframe        
    df_pwt_resid_log = pd.DataFrame(columns = columns_years)
    df_pwt_resid_log.insert (0, "country", countries)

    for index, country in enumerate(df_pwt['country']):
        for year in range(1980, 2016):
            df_pwt_resid_log.at[index,year] = (np.log(df_pwt.loc[(df_pwt['country'] == country)][year].values[0]) - np.log(df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0]))
            #df_pwt_resid_log.at[index,year] = np.log(df_pwt.loc[(df_pwt['country'] == country)][year].values[0])
            #df_pwt_resid_log.at[index,year] = np.log((df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0] - df_pwt.loc[(df_pwt['country'] == country)][year].values[0]))

    ######################################################################        
            
    #World Bank Development Indicators:
    file_wbdi = parent_directory + '\\raw_data\\2.2_outcome_data\\world_bank_development_indicators\\gdp_constant_2015_usd\\6da13646-0ee3-46fc-99e6-de3592d3f6ac_Data.csv'

    #create wbdi data frame that will be plotted later
    df_wbdi = pd.read_csv(file_wbdi)
    #drop unnecessary columns
    df_wbdi = df_wbdi.drop(['Country Code', 'Series Name', 'Series Code'], axis=1)
    #drop unnecessary rows
    df_wbdi = df_wbdi[:-5]
    #rename year columns
    df_wbdi = pd.concat([df_wbdi.iloc[: ,0:1], df_wbdi.iloc[: ,1:].rename(columns = lambda x : str(x)[:-9])], axis=1)

    #create residualized log dataframe
    df_wbdi_resid_log = pd.DataFrame(columns = columns_years)
    df_wbdi_resid_log.insert (0, "country", countries)

    for index, country in enumerate(df_wbdi['Country Name']):
        for year in range(1980, 2016):
            if (df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0] == '..'):
                #assign 'None' to missing values
                df_wbdi_resid_log.at[index,year] = None
            else:
                df_wbdi_resid_log.at[index,year] = (np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0])) - np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])))
                #df_wbdi_resid_log.at[index,year] = np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0]))
                #df_wbdi_resid_log.at[index,year] = np.log((float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0]) - float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])))

    ######################################################################        
            
    #Maddison Project Database:

    file_mpd = parent_directory + '\\raw_data\\2.2_outcome_data\\maddison_project_database\\mpd2020.xlsx'

    mpd = pd.read_excel(file_mpd, sheet_name = 'Full data')

    #create mpd data frame that will be plotted later
    df_mpd = pd.DataFrame(columns = columns_years)
    df_mpd.insert (0, "country", countries)

    mpd = pd.read_excel(file_mpd, sheet_name = 'Full data')

    #create dataframe from csv file
    for country,country_name in enumerate(countries):
        for year in range(1980, 2017):
            df_mpd.at[country,year] = mpd['gdppc'].loc[(mpd['country'] == country_name) & (mpd['year'] == year)].values[0]

    #create residualized log dataframe        
    df_mpd_resid_log = pd.DataFrame(columns = columns_years)
    df_mpd_resid_log.insert (0, "country", countries)

    for index, country in enumerate(df_pwt['country']):
        for year in range(1980, 2016):
            df_mpd_resid_log.at[index,year] = (np.log(df_mpd.loc[(df_mpd['country'] == country)][year].values[0]) - np.log(df_mpd.loc[(df_mpd['country'] == country)][year+1].values[0]))
            #df_mpd_resid_log.at[index,year] = np.log(df_mpd.loc[(df_mpd['country'] == country)][year].values[0])
            #df_mpd_resid_log.at[index,year] = np.log((df_mpd.loc[(df_mpd['country'] == country)][year+1].values[0] - df_mpd.loc[(df_mpd['country'] == country)][year].values[0]))

    return [df_pwt_resid_log, df_wbdi_resid_log, df_mpd_resid_log]


######################################################################



"--------------------------------------------------------------------"
'Plotting Functions'
"--------------------------------------------------------------------"

def add_pixel(ax,lat_from, lat_to, lon_from, lon_to):
    # ax.add_patch(Rectangle((lon_from,lat_from), (lon_to-lon_from), (lat_to-lat_from),color = 'black',fill=False, lw=.5, linestyle='--', alpha = .3))
    ax.add_patch(Rectangle((lon_from,lat_from), (lon_to-lon_from), (lat_to-lat_from),color = 'black',fill=True))

#function to plot merra data

#taken in parts from: https://www.kaggle.com/gpreda/how-to-read-and-plot-earthdata-merra2-data-files
def plot_merra_data(data, lons, lats, title='', date='', data_value='', extent=[-150, 150, -90, 90], borders = False, bodele = False, plot_grids = False, add_source_region = False, cbar_min = 0, cbar_max = 7, unit = 1):
    #size, extent and cartopy projection
    fig = plt.figure(figsize=(16,8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    #draw bodélé depression?
    if bodele:
        #bodélé coords: 16°05'-17°38'N/15°50'-18°50'E
        #source: https://web.archive.org/web/20120924181446/http://ramsar.wetlands.org/Portals/15/CHAD.pdf
        ax.add_patch(Rectangle((15.5,16.05), (18.05-15.5), (17.38-16.05),edgecolor = 'black',fill=False,lw=2, linestyle='--'))

    #additional geographical information
    ax.coastlines(resolution="50m",linewidth=1)
    if(borders):
        ax.add_feature(cf.BORDERS)
    #gridlines
    gl = ax.gridlines(linestyle='--',color='black', draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    #axis labeling
    ax.text(-0.05, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax.transAxes, size=14)
    ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax.transAxes, size=14)
    #plot+info
    if plot_grids:
        plt.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')

    if add_source_region:
        
        add_pixel(ax,(48*0.5),(47*0.5),-(2.1*0.625),(0.8*0.625))
        add_pixel(ax,(47*0.5),(46*0.5),-(1.1*0.625),(1.8*0.625))
        add_pixel(ax,(46*0.5),(45*0.5),(0.9*0.625),(1.8*0.625))
        add_pixel(ax,(45*0.5),(44*0.5),-(1.1*0.625),(0.8*0.625))
        add_pixel(ax,(44*0.5),(43*0.5),-(2.1*0.625),(-.2*0.625))
        add_pixel(ax,(44*0.5),(43*0.5),-(2.1*0.625),(.8*0.625))
        add_pixel(ax,(43*0.5),(42*0.5),-(2.1*0.625),(-.2*0.625))
        add_pixel(ax,(42*0.5),(41*0.5),-(6.1*0.625),(-1.2*0.625))
        add_pixel(ax,(41*0.5),(40*0.5),-(6.1*0.625),(-2.2*0.625))
        add_pixel(ax,(40*0.5),(39*0.5),-(7.1*0.625),(-3.2*0.625))
        add_pixel(ax,(39*0.5),(38*0.5),-(6.1*0.625),(-4.2*0.625))
        add_pixel(ax,(38*0.5),(37*0.5),-(6.1*0.625),(-5.2*0.625))

        #right:
        add_pixel(ax,(40*0.5),(39*0.5),(22.9*0.625),(25.8*0.625))
        add_pixel(ax,(39*0.5),(38*0.5),(20.9*0.625),(25.8*0.625))
        add_pixel(ax,(38*0.5),(37*0.5),(20.9*0.625),(29.8*0.625))
        add_pixel(ax,(37*0.5),(36*0.5),(20.9*0.625),(32.8*0.625))
        add_pixel(ax,(36*0.5),(35*0.5),(19.9*0.625),(32.8*0.625))
        add_pixel(ax,(35*0.5),(34*0.5),(18.9*0.625),(32.8*0.625))
        add_pixel(ax,(34*0.5),(33*0.5),(19.9*0.625),(32.8*0.625))
        add_pixel(ax,(33*0.5),(32*0.5),(21.9*0.625),(32.8*0.625))
        add_pixel(ax,(32*0.5),(31*0.5),(21.9*0.625),(32.8*0.625))
        add_pixel(ax,(31*0.5),(30*0.5),(23.9*0.625),(25.8*0.625))
        add_pixel(ax,(31*0.5),(30*0.5),(28.9*0.625),(31.8*0.625))

        #upper right:
        add_pixel(ax,(53*0.5),(52*0.5),(33.9*0.625),(36.9*0.625))
        add_pixel(ax,(52*0.5),(51*0.5),(33.9*0.625),(36.9*0.625))

        #upper right corner:
        add_pixel(ax,(58*0.5),(57*0.5),(38.9*0.625),(44.8*0.625))
        add_pixel(ax,(57*0.5),(56*0.5),(38.9*0.625),(41.8*0.625))
        add_pixel(ax,(57*0.5),(56*0.5),(43.9*0.625),(44.8*0.625))

    if plot_grids:
        quadmesh = ax.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')
        quadmesh.set_clim(vmin=cbar_min, vmax=cbar_max * unit)
    else:
        plt.contourf(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')
    plt.title(f'MERRA-2 {title}, {date}', size=14, pad=15)
    plt.xlabel('Latitude')
    #colorbar
    if plot_grids:
        cb = plt.colorbar(quadmesh, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
    else:
        cb = plt.colorbar(ax=ax, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
    cb.set_label(data_value,size=12,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=10)
    plt.show()



def plot_grid(lats, lons, title='', extent=[-150, 150, -90, 90], borders = False, add_source_region = False):

    fig = plt.figure(figsize=(16,8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    if add_source_region:
        # #34
        # #∼ 21°N, 16°W
        # add_pixel(ax,21,22,-16,-17)
        # #∼26°–27°N, 6° –7°W
        # add_pixel(ax,26,27,-6,-7)
        # #35
        # #∼17°– 18°N, 8°–10°W
        # add_pixel(ax,17,18,-8,-10)
        # #∼ 16°N, 3°–4°W
        # add_pixel(ax,16,17,-3,-4)
        # #18° and 20°N and 3° and 8°W
        # add_pixel(ax,18,20,-3,-8)
        # #36
        # #26°N, 1°E
        # add_pixel(ax,26,27,1,2)
        # #37
        # #lies between 18° and 23°N, 3° and 6°E
        # add_pixel(ax,18,23,3,6)
        # #39
        # #lies between 16° and 18°N and extends from 15° to 19°E
        # add_pixel(ax,16,18,15,19)
        # #centered at ∼17.5°N between 12° and 14°E
        # add_pixel(ax,17.5, 18.5, 12,14)
        # #ax.add_patch(Rectangle((15.5,16.05), (18.05-15.5), (17.38-16.05),color = 'black',fill=True))


        #merra spatial resolution: 0.5 ° x 0.5 °

        #fig10:
        #left:
        add_pixel(ax,(48*0.5),(47*0.5),-(1*0.625),(2*0.625))
        add_pixel(ax,(47*0.5),(46*0.5),-(0*0.625),(3*0.625))
        add_pixel(ax,(46*0.5),(45*0.5),(1*0.625),(3*0.625))
        add_pixel(ax,(45*0.5),(44*0.5),-(0*0.625),(2*0.625))
        add_pixel(ax,(44*0.5),(43*0.5),-(1*0.625),(1*0.625))
        add_pixel(ax,(44*0.5),(43*0.5),-(1*0.625),(2*0.625))
        add_pixel(ax,(43*0.5),(42*0.5),-(1*0.625),(1*0.625))
        add_pixel(ax,(42*0.5),(41*0.5),-(5*0.625),(0*0.625))
        add_pixel(ax,(41*0.5),(40*0.5),-(5*0.625),(-1*0.625))
        add_pixel(ax,(40*0.5),(39*0.5),-(6*0.625),(-2*0.625))
        add_pixel(ax,(39*0.5),(38*0.5),-(5*0.625),(-3*0.625))
        add_pixel(ax,(38*0.5),(37*0.5),-(5*0.625),(-4*0.625))
        
        #right:
        add_pixel(ax,(40*0.5),(39*0.5),(22*0.625),(25*0.625))
        add_pixel(ax,(39*0.5),(38*0.5),(20*0.625),(25*0.625))
        add_pixel(ax,(38*0.5),(37*0.5),(20*0.625),(29*0.625))
        add_pixel(ax,(37*0.5),(36*0.5),(20*0.625),(32*0.625))
        add_pixel(ax,(36*0.5),(35*0.5),(19*0.625),(32*0.625))
        add_pixel(ax,(35*0.5),(34*0.5),(18*0.625),(32*0.625))
        add_pixel(ax,(34*0.5),(33*0.5),(19*0.625),(32*0.625))
        add_pixel(ax,(33*0.5),(32*0.5),(21*0.625),(32*0.625))
        add_pixel(ax,(32*0.5),(31*0.5),(21*0.625),(32*0.625))
        add_pixel(ax,(31*0.5),(30*0.5),(23*0.625),(25*0.625))
        add_pixel(ax,(31*0.5),(30*0.5),(28*0.625),(31*0.625))

        #upper right:
        add_pixel(ax,(53*0.5),(52*0.5),(33*0.625),(36*0.625))
        add_pixel(ax,(52*0.5),(51*0.5),(33*0.625),(36*0.625))

        #upper right corner:
        add_pixel(ax,(58*0.5),(57*0.5),(38*0.625),(44*0.625))
        add_pixel(ax,(57*0.5),(56*0.5),(38*0.625),(41*0.625))
        add_pixel(ax,(57*0.5),(56*0.5),(43*0.625),(44*0.625))

    for lat in lats:

        ax.hlines(y=lat, xmin = -30, xmax = 29, linewidth=.5, color='r')
    
    for lon in lons:
        ax.vlines(x=lon, ymin =-15, ymax = 29, linewidth=.5, color='r')
    
    #additional geographical information
    ax.coastlines(resolution="50m",linewidth=1)
    if(borders):
        ax.add_feature(cf.BORDERS)
    #gridlines
    gl = ax.gridlines(linestyle='--',color='black', draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    #axis labeling
    ax.text(-0.05, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax.transAxes, size=14)
    ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax.transAxes, size=14)
    #plot+info
    #plt.contourf(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')
    plt.title(f'MERRA-2 {title}', size=14, pad=15)
    plt.xlabel('Latitude')
    plt.show()


def plot_outcome_data(pwt_data, mpd_data, wbdi_data):

    fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(10,6),gridspec_kw={'wspace':0.3,'hspace':0.3})
    #index variable for countries in loop
    idx = 0
    for row in ax:
        for col in row:
            #plotting variables
            col.plot(list(range(1980,2016)), pwt_data.loc[pwt_data['country'] == pwt_data['country'][idx]].values[0][1:-1], color = "black", linewidth=.8)
            col.plot(list(range(1980,2016)), mpd_data.loc[mpd_data['country'] == mpd_data['country'][idx]].values[0][1:-1], color = "lightseagreen", linewidth=.8)
            col.plot(list(range(1980,2016)), wbdi_data.loc[wbdi_data['country'] == wbdi_data['country'][idx]].values[0][1:-1], color = "violet", linewidth=.8)
            #set limits
            col.set_ylim([-2,1])
            col.set_xlim([1980, 2020])
            #set x,y ticks
            col.set_yticks([-2,-1,0,1])
            col.set_xticks([1980,1990,2000,2010,2020])
            #set x and y axis aspect ratio
            col.set_aspect(8)
            #set titles and labels
            col.set_title(pwt_data['country'][idx], fontsize=5)
            col.set_xlabel('Year', fontsize=5)
            col.set_ylabel('Log differences (GDP)', fontsize=5)
            #set tick label sizes
            col.tick_params(axis='both', which='minor', labelsize=5)
            col.tick_params(axis='both', which='major', labelsize=5)
            #set grid
            col.grid(linestyle=':', linewidth='0.5')
            #remove upper and right bounding lines
            col.spines['right'].set_visible(False)
            col.spines['top'].set_visible(False)
            #increment country index
            idx += 1
            #handles, labels = ax.get_legend_handles_labels()

    fig.set_dpi(500)
    #fig.legend(handles, ['PWT','WDI','MPD'], loc='upper center')
    fig.legend(['PWT','Maddison','WDI'], loc = "lower center", ncol=5 )
    #plt.legend(['PWT','WDI','MPD'], loc="lower center")
    plt.show()

def plot_wind_vectorfield(x_winds, y_winds, lons_wind, lats_wind, fig_size = (16,8),title='', date='', data_value='', extent=[-150, 150, -90, 90], borders = False, bodele = False, interpolation = "None"):

    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if bodele:
        #bodélé coords: 16°05'-17°38'N/15°50'-18°50'E
        #source: https://web.archive.org/web/20120924181446/http://ramsar.wetlands.org/Portals/15/CHAD.pdf
        ax.add_patch(Rectangle((15.5,16.05), (18.05-15.5), (17.38-16.05),edgecolor = 'black',fill=False,lw=2, linestyle='--'))

    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.coastlines(resolution="110m",linewidth=1)
    if borders:
        ax.add_feature(cf.BORDERS)
    gl = ax.gridlines(linestyle='--',color='black', draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    ax.text(-0.05, 0.55, 'Latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax.transAxes, size=14)
    ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, size=14)
    plt.title(f'MERRA-2 {title}, {date}', size=14, pad=15)
    plt.xlabel('Latitude')
    color = np.sqrt(np.power(x_winds, 2) + np.power(y_winds, 2))
    #color2 = np.arctan2(x_winds, y_winds)

    color_background = ax.imshow(color,interpolation=interpolation,extent = extent,aspect = 'auto')
    cb = plt.colorbar(color_background,pad=0.02, aspect=16, shrink=0.8)
    cb.set_label(data_value,size=12,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=10)
    ax.quiver(lons_wind, lats_wind, x_winds, y_winds, transform=ccrs.PlateCarree(),color='indianred', width=.0016)

    plt.show()



"--------------------------------------------------------------------"
'Animation Functions'
"--------------------------------------------------------------------"



def simulation_comparison_animation(simulation_data_array, real_data_array, lats, lons, extent=[-30,29,-15,29], add_source_region = False, borders = True, cbar_min = 0, cbar_max = 7, unit = 1, min_time = 0, max_time = 1, fpers = 10):

    from matplotlib import animation
    from matplotlib.animation import FuncAnimation, PillowWriter

    fig, axes = plt.subplots(1,2, figsize=(25,11), subplot_kw={"projection": ccrs.PlateCarree()})

    axes[0].set_extent(extent, crs=ccrs.PlateCarree())
    gl1 = axes[0].gridlines(linestyle='--',color='black', draw_labels=True)
    gl1.top_labels = False
    gl1.right_labels = False

    axes[0].coastlines(resolution="50m",linewidth=1)
    if borders:
        axes[0].add_feature(cf.BORDERS)
    #axis labeling
    axes[0].text(-0.1, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[0].transAxes, size=14)
    axes[0].text(0.5, -0.11, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=axes[0].transAxes, size=14)
    axes[0].title.set_text('Simulated Dust Movement')  

    if add_source_region:
        #fig10:
        #left:
        add_pixel(axes[0],(48*0.5),(47*0.5),-(2.1*0.625),(0.8*0.625))
        add_pixel(axes[0],(47*0.5),(46*0.5),-(1.1*0.625),(1.8*0.625))
        add_pixel(axes[0],(46*0.5),(45*0.5),(0.9*0.625),(1.8*0.625))
        add_pixel(axes[0],(45*0.5),(44*0.5),-(1.1*0.625),(0.8*0.625))
        add_pixel(axes[0],(44*0.5),(43*0.5),-(2.1*0.625),(-.2*0.625))
        add_pixel(axes[0],(44*0.5),(43*0.5),-(2.1*0.625),(.8*0.625))
        add_pixel(axes[0],(43*0.5),(42*0.5),-(2.1*0.625),(-.2*0.625))
        add_pixel(axes[0],(42*0.5),(41*0.5),-(6.1*0.625),(-1.2*0.625))
        add_pixel(axes[0],(41*0.5),(40*0.5),-(6.1*0.625),(-2.2*0.625))
        add_pixel(axes[0],(40*0.5),(39*0.5),-(7.1*0.625),(-3.2*0.625))
        add_pixel(axes[0],(39*0.5),(38*0.5),-(6.1*0.625),(-4.2*0.625))
        add_pixel(axes[0],(38*0.5),(37*0.5),-(6.1*0.625),(-5.2*0.625))

        #right:
        add_pixel(axes[0],(40*0.5),(39*0.5),(22.9*0.625),(25.8*0.625))
        add_pixel(axes[0],(39*0.5),(38*0.5),(20.9*0.625),(25.8*0.625))
        add_pixel(axes[0],(38*0.5),(37*0.5),(20.9*0.625),(29.8*0.625))
        add_pixel(axes[0],(37*0.5),(36*0.5),(20.9*0.625),(32.8*0.625))
        add_pixel(axes[0],(36*0.5),(35*0.5),(19.9*0.625),(32.8*0.625))
        add_pixel(axes[0],(35*0.5),(34*0.5),(18.9*0.625),(32.8*0.625))
        add_pixel(axes[0],(34*0.5),(33*0.5),(19.9*0.625),(32.8*0.625))
        add_pixel(axes[0],(33*0.5),(32*0.5),(21.9*0.625),(32.8*0.625))
        add_pixel(axes[0],(32*0.5),(31*0.5),(21.9*0.625),(32.8*0.625))
        add_pixel(axes[0],(31*0.5),(30*0.5),(23.9*0.625),(25.8*0.625))
        add_pixel(axes[0],(31*0.5),(30*0.5),(28.9*0.625),(31.8*0.625))

        #upper right:
        add_pixel(axes[0],(53*0.5),(52*0.5),(33.9*0.625),(36.9*0.625))
        add_pixel(axes[0],(52*0.5),(51*0.5),(33.9*0.625),(36.9*0.625))

        #upper right corner:
        add_pixel(axes[0],(58*0.5),(57*0.5),(38.9*0.625),(44.8*0.625))
        add_pixel(axes[0],(57*0.5),(56*0.5),(38.9*0.625),(41.8*0.625))
        add_pixel(axes[0],(57*0.5),(56*0.5),(43.9*0.625),(44.8*0.625))

    quadmesh1 = axes[0].pcolormesh(lons, lats, simulation_data_array[0], transform=ccrs.PlateCarree(),cmap='YlOrRd',shading='flat')
    quadmesh1.set_clim(vmin=cbar_min, vmax=cbar_max * unit)
        

    axes[1].set_extent(extent, crs=ccrs.PlateCarree())
    gl2 = axes[1].gridlines(linestyle='--',color='black', draw_labels=True)
    gl2.top_labels = False
    gl2.right_labels = False

    axes[1].coastlines(resolution="50m",linewidth=1)
    if borders:
        axes[1].add_feature(cf.BORDERS)
    #axis labeling
    axes[1].text(-0.1, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[1].transAxes, size=14)
    axes[1].text(0.5, -0.11, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=axes[1].transAxes, size=14)
    axes[1].title.set_text('Real Dust Movement')   

    quadmesh2 = axes[1].pcolormesh(lons, lats, real_data_array[0], transform=ccrs.PlateCarree(),cmap='YlOrRd',shading='flat')
    quadmesh2.set_clim(vmin=cbar_min, vmax=cbar_max * unit)

    cb = fig.colorbar(quadmesh2, orientation="vertical", pad=0.02, aspect=12, shrink=0.65, ax=axes.ravel().tolist())
    cb.set_label('dust surface mass concentration-PM 2.5 \n \n kg/m^3',size=12,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=10)
    def init():
        quadmesh1.set_array(simulation_data_array[0].ravel())
        quadmesh2.set_array(real_data_array[0].ravel())
        return quadmesh1, quadmesh2

    def animate(i):
        input1 = simulation_data_array[i+min_time+1][:-1, :-1]
        quadmesh1.set_array(input1.ravel())
        input2 = real_data_array[i+min_time][:-1, :-1]
        quadmesh2.set_array(input2.ravel())
        return quadmesh1, quadmesh2

    anim = animation.FuncAnimation(fig, animate, frames=max_time, interval=20, blit=True)
    anim.save("anim_0_1.mp4", dpi=100, writer=animation.FFMpegWriter(fps=fpers))



"--------------------------------------------------------------------"
'Advection Diffusion Simulation Functions'
"--------------------------------------------------------------------"



@jit
def build_source_array(input_array, longitudes, latitudes):

    source_array = np.zeros((input_array.shape[0], longitudes, latitudes), dtype='float32')

    source_array[:,77,46] = input_array[:,77,46]
    source_array[:,77,47] = input_array[:,77,47]
    source_array[:,77,48] = input_array[:,77,48]
    source_array[:,76,47] = input_array[:,76,47]
    source_array[:,76,48] = input_array[:,76,48]
    source_array[:,76,49] = input_array[:,76,49]
    source_array[:,75,48] = input_array[:,75,48]
    source_array[:,75,49] = input_array[:,75,49]
    source_array[:,74,47] = input_array[:,74,47]
    source_array[:,74,48] = input_array[:,74,48]
    source_array[:,73,46] = input_array[:,73,46]
    source_array[:,73,47] = input_array[:,73,47]
    source_array[:,73,48] = input_array[:,73,48]
    source_array[:,72,46] = input_array[:,72,46]
    source_array[:,72,47] = input_array[:,72,47]
    source_array[:,71,42] = input_array[:,71,42]
    source_array[:,71,43] = input_array[:,71,43]
    source_array[:,71,44] = input_array[:,71,44]
    source_array[:,71,45] = input_array[:,71,45]
    source_array[:,71,46] = input_array[:,71,46]
    source_array[:,70,42] = input_array[:,70,42]
    source_array[:,70,43] = input_array[:,70,43]
    source_array[:,70,44] = input_array[:,70,44]
    source_array[:,70,45] = input_array[:,70,45]
    source_array[:,69,41] = input_array[:,69,41]
    source_array[:,69,42] = input_array[:,69,42]
    source_array[:,69,43] = input_array[:,69,43]
    source_array[:,69,44] = input_array[:,69,44]
    source_array[:,68,42] = input_array[:,68,42]
    source_array[:,68,43] = input_array[:,68,43]
    source_array[:,67,42] = input_array[:,67,42]

    #right:
    source_array[:,69,71] = input_array[:,69,71]
    source_array[:,69,72] = input_array[:,69,72]
    source_array[:,69,73] = input_array[:,69,73]
    source_array[:,68,68] = input_array[:,68,68]
    source_array[:,68,69] = input_array[:,68,69]
    source_array[:,68,70] = input_array[:,68,70]
    source_array[:,68,71] = input_array[:,68,71]
    source_array[:,68,72] = input_array[:,68,72]
    source_array[:,68,73] = input_array[:,68,73]
    source_array[:,67,68] = input_array[:,67,68]
    source_array[:,67,69] = input_array[:,67,69]
    source_array[:,67,70] = input_array[:,67,70]
    source_array[:,67,71] = input_array[:,67,71]
    source_array[:,67,72] = input_array[:,67,72]
    source_array[:,67,73] = input_array[:,67,73]
    source_array[:,67,74] = input_array[:,67,74]
    source_array[:,67,75] = input_array[:,67,75]
    source_array[:,67,76] = input_array[:,67,76]
    source_array[:,67,77] = input_array[:,67,77]
    source_array[:,66,68] = input_array[:,66,68]
    source_array[:,66,69] = input_array[:,66,69]
    source_array[:,66,70] = input_array[:,66,70]
    source_array[:,66,71] = input_array[:,66,71]
    source_array[:,66,72] = input_array[:,66,72]
    source_array[:,66,73] = input_array[:,66,73]
    source_array[:,66,74] = input_array[:,66,74]
    source_array[:,66,75] = input_array[:,66,75]
    source_array[:,66,76] = input_array[:,66,76]
    source_array[:,66,77] = input_array[:,66,77]
    source_array[:,66,78] = input_array[:,66,78]
    source_array[:,66,79] = input_array[:,66,79]
    source_array[:,66,80] = input_array[:,66,80]
    source_array[:,65,67] = input_array[:,65,67]
    source_array[:,65,68] = input_array[:,65,68]
    source_array[:,65,69] = input_array[:,65,69]
    source_array[:,65,70] = input_array[:,65,70]
    source_array[:,65,71] = input_array[:,65,71]
    source_array[:,65,72] = input_array[:,65,72]
    source_array[:,65,73] = input_array[:,65,73]
    source_array[:,65,74] = input_array[:,65,74]
    source_array[:,65,75] = input_array[:,65,75]
    source_array[:,65,76] = input_array[:,65,76]
    source_array[:,65,77] = input_array[:,65,77]
    source_array[:,65,78] = input_array[:,65,78]
    source_array[:,65,79] = input_array[:,65,79]
    source_array[:,65,80] = input_array[:,65,80]
    source_array[:,64,66] = input_array[:,64,66]
    source_array[:,64,67] = input_array[:,64,67]
    source_array[:,64,68] = input_array[:,64,68]
    source_array[:,64,69] = input_array[:,64,69]
    source_array[:,64,70] = input_array[:,64,70]
    source_array[:,64,71] = input_array[:,64,71]
    source_array[:,64,72] = input_array[:,64,72]
    source_array[:,64,73] = input_array[:,64,73]
    source_array[:,64,74] = input_array[:,64,74]
    source_array[:,64,75] = input_array[:,64,75]
    source_array[:,64,76] = input_array[:,64,76]
    source_array[:,64,77] = input_array[:,64,77]
    source_array[:,64,78] = input_array[:,64,78]
    source_array[:,64,79] = input_array[:,64,79]
    source_array[:,64,80] = input_array[:,64,80]
    source_array[:,63,67] = input_array[:,64,67]
    source_array[:,63,68] = input_array[:,63,68]
    source_array[:,63,69] = input_array[:,63,69]
    source_array[:,63,70] = input_array[:,63,70]
    source_array[:,63,71] = input_array[:,63,71]
    source_array[:,63,72] = input_array[:,63,72]
    source_array[:,63,73] = input_array[:,63,73]
    source_array[:,63,74] = input_array[:,63,74]
    source_array[:,63,75] = input_array[:,63,75]
    source_array[:,63,76] = input_array[:,63,76]
    source_array[:,63,77] = input_array[:,63,77]
    source_array[:,63,78] = input_array[:,63,78]
    source_array[:,63,79] = input_array[:,63,79]
    source_array[:,63,80] = input_array[:,63,80]
    source_array[:,62,69] = input_array[:,62,69]
    source_array[:,62,70] = input_array[:,62,70]
    source_array[:,62,71] = input_array[:,62,71]
    source_array[:,62,72] = input_array[:,62,72]
    source_array[:,62,73] = input_array[:,62,73]
    source_array[:,62,74] = input_array[:,62,74]
    source_array[:,62,75] = input_array[:,62,75]
    source_array[:,62,76] = input_array[:,62,76]
    source_array[:,62,77] = input_array[:,62,77]
    source_array[:,62,78] = input_array[:,62,78]
    source_array[:,62,79] = input_array[:,62,79]
    source_array[:,62,80] = input_array[:,62,80]
    source_array[:,61,69] = input_array[:,61,69]
    source_array[:,61,70] = input_array[:,61,70]
    source_array[:,61,71] = input_array[:,61,71]
    source_array[:,61,72] = input_array[:,61,72]
    source_array[:,61,73] = input_array[:,61,73]
    source_array[:,61,74] = input_array[:,61,74]
    source_array[:,61,75] = input_array[:,61,75]
    source_array[:,61,76] = input_array[:,61,76]
    source_array[:,61,77] = input_array[:,61,77]
    source_array[:,61,78] = input_array[:,61,78]
    source_array[:,61,79] = input_array[:,61,79]
    source_array[:,61,80] = input_array[:,61,80]
    source_array[:,60,71] = input_array[:,60,71]
    source_array[:,60,72] = input_array[:,60,72]
    source_array[:,60,77] = input_array[:,60,77]
    source_array[:,60,78] = input_array[:,60,78]
    source_array[:,60,79] = input_array[:,60,79]

    #upper right:
    source_array[:,82,82] = input_array[:,82,82]
    source_array[:,82,83] = input_array[:,82,83]
    source_array[:,82,84] = input_array[:,82,84]
    source_array[:,81,82] = input_array[:,81,82]
    source_array[:,81,83] = input_array[:,81,83]
    source_array[:,81,84] = input_array[:,81,84]

    #upper right corner:
    source_array[:,87,87] = input_array[:,87,87]
    source_array[:,87,88] = input_array[:,87,88]
    source_array[:,87,89] = input_array[:,87,89]
    source_array[:,87,90] = input_array[:,87,90]
    source_array[:,87,91] = input_array[:,87,91]
    source_array[:,86,87] = input_array[:,86,87]
    source_array[:,86,88] = input_array[:,86,88]
    source_array[:,86,89] = input_array[:,86,89]
    source_array[:,86,91] = input_array[:,86,91]

    return source_array


@jit
def fill_with_source(uninitialized_array, source_array):
    uninitialized_array[77,46] = source_array[77,46]
    uninitialized_array[77,47] = source_array[77,47]
    uninitialized_array[77,48] = source_array[77,48]
    uninitialized_array[76,47] = source_array[76,47]
    uninitialized_array[76,48] = source_array[76,48]
    uninitialized_array[76,49] = source_array[76,49]
    uninitialized_array[75,48] = source_array[75,48]
    uninitialized_array[75,49] = source_array[75,49]
    uninitialized_array[74,47] = source_array[74,47]
    uninitialized_array[74,48] = source_array[74,48]
    uninitialized_array[73,46] = source_array[73,46]
    uninitialized_array[73,47] = source_array[73,47]
    uninitialized_array[73,48] = source_array[73,48]
    uninitialized_array[72,46] = source_array[72,46]
    uninitialized_array[72,47] = source_array[72,47]
    uninitialized_array[71,42] = source_array[71,42]
    uninitialized_array[71,43] = source_array[71,43]
    uninitialized_array[71,44] = source_array[71,44]
    uninitialized_array[71,45] = source_array[71,45]
    uninitialized_array[71,46] = source_array[71,46]
    uninitialized_array[70,42] = source_array[70,42]
    uninitialized_array[70,43] = source_array[70,43]
    uninitialized_array[70,44] = source_array[70,44]
    uninitialized_array[70,45] = source_array[70,45]
    uninitialized_array[69,41] = source_array[69,41]
    uninitialized_array[69,42] = source_array[69,42]
    uninitialized_array[69,43] = source_array[69,43]
    uninitialized_array[69,44] = source_array[69,44]
    uninitialized_array[68,42] = source_array[68,42]
    uninitialized_array[68,43] = source_array[68,43]
    uninitialized_array[67,42] = source_array[67,42]

    #right:
    uninitialized_array[69,71] = source_array[69,71]
    uninitialized_array[69,72] = source_array[69,72]
    uninitialized_array[69,73] = source_array[69,73]
    uninitialized_array[68,68] = source_array[68,68]
    uninitialized_array[68,69] = source_array[68,69]
    uninitialized_array[68,70] = source_array[68,70]
    uninitialized_array[68,71] = source_array[68,71]
    uninitialized_array[68,72] = source_array[68,72]
    uninitialized_array[68,73] = source_array[68,73]
    uninitialized_array[67,68] = source_array[67,68]
    uninitialized_array[67,69] = source_array[67,69]
    uninitialized_array[67,70] = source_array[67,70]
    uninitialized_array[67,71] = source_array[67,71]
    uninitialized_array[67,72] = source_array[67,72]
    uninitialized_array[67,73] = source_array[67,73]
    uninitialized_array[67,74] = source_array[67,74]
    uninitialized_array[67,75] = source_array[67,75]
    uninitialized_array[67,76] = source_array[67,76]
    uninitialized_array[67,77] = source_array[67,77]
    uninitialized_array[66,68] = source_array[66,68]
    uninitialized_array[66,69] = source_array[66,69]
    uninitialized_array[66,70] = source_array[66,70]
    uninitialized_array[66,71] = source_array[66,71]
    uninitialized_array[66,72] = source_array[66,72]
    uninitialized_array[66,73] = source_array[66,73]
    uninitialized_array[66,74] = source_array[66,74]
    uninitialized_array[66,75] = source_array[66,75]
    uninitialized_array[66,76] = source_array[66,76]
    uninitialized_array[66,77] = source_array[66,77]
    uninitialized_array[66,78] = source_array[66,78]
    uninitialized_array[66,79] = source_array[66,79]
    uninitialized_array[66,80] = source_array[66,80]
    uninitialized_array[65,67] = source_array[65,67]
    uninitialized_array[65,68] = source_array[65,68]
    uninitialized_array[65,69] = source_array[65,69]
    uninitialized_array[65,70] = source_array[65,70]
    uninitialized_array[65,71] = source_array[65,71]
    uninitialized_array[65,72] = source_array[65,72]
    uninitialized_array[65,73] = source_array[65,73]
    uninitialized_array[65,74] = source_array[65,74]
    uninitialized_array[65,75] = source_array[65,75]
    uninitialized_array[65,76] = source_array[65,76]
    uninitialized_array[65,77] = source_array[65,77]
    uninitialized_array[65,78] = source_array[65,78]
    uninitialized_array[65,79] = source_array[65,79]
    uninitialized_array[65,80] = source_array[65,80]
    uninitialized_array[64,66] = source_array[64,66]
    uninitialized_array[64,67] = source_array[64,67]
    uninitialized_array[64,68] = source_array[64,68]
    uninitialized_array[64,69] = source_array[64,69]
    uninitialized_array[64,70] = source_array[64,70]
    uninitialized_array[64,71] = source_array[64,71]
    uninitialized_array[64,72] = source_array[64,72]
    uninitialized_array[64,73] = source_array[64,73]
    uninitialized_array[64,74] = source_array[64,74]
    uninitialized_array[64,75] = source_array[64,75]
    uninitialized_array[64,76] = source_array[64,76]
    uninitialized_array[64,77] = source_array[64,77]
    uninitialized_array[64,78] = source_array[64,78]
    uninitialized_array[64,79] = source_array[64,79]
    uninitialized_array[64,80] = source_array[64,80]
    uninitialized_array[63,67] = source_array[64,67]
    uninitialized_array[63,68] = source_array[63,68]
    uninitialized_array[63,69] = source_array[63,69]
    uninitialized_array[63,70] = source_array[63,70]
    uninitialized_array[63,71] = source_array[63,71]
    uninitialized_array[63,72] = source_array[63,72]
    uninitialized_array[63,73] = source_array[63,73]
    uninitialized_array[63,74] = source_array[63,74]
    uninitialized_array[63,75] = source_array[63,75]
    uninitialized_array[63,76] = source_array[63,76]
    uninitialized_array[63,77] = source_array[63,77]
    uninitialized_array[63,78] = source_array[63,78]
    uninitialized_array[63,79] = source_array[63,79]
    uninitialized_array[63,80] = source_array[63,80]
    uninitialized_array[62,69] = source_array[62,69]
    uninitialized_array[62,70] = source_array[62,70]
    uninitialized_array[62,71] = source_array[62,71]
    uninitialized_array[62,72] = source_array[62,72]
    uninitialized_array[62,73] = source_array[62,73]
    uninitialized_array[62,74] = source_array[62,74]
    uninitialized_array[62,75] = source_array[62,75]
    uninitialized_array[62,76] = source_array[62,76]
    uninitialized_array[62,77] = source_array[62,77]
    uninitialized_array[62,78] = source_array[62,78]
    uninitialized_array[62,79] = source_array[62,79]
    uninitialized_array[62,80] = source_array[62,80]
    uninitialized_array[61,69] = source_array[61,69]
    uninitialized_array[61,70] = source_array[61,70]
    uninitialized_array[61,71] = source_array[61,71]
    uninitialized_array[61,72] = source_array[61,72]
    uninitialized_array[61,73] = source_array[61,73]
    uninitialized_array[61,74] = source_array[61,74]
    uninitialized_array[61,75] = source_array[61,75]
    uninitialized_array[61,76] = source_array[61,76]
    uninitialized_array[61,77] = source_array[61,77]
    uninitialized_array[61,78] = source_array[61,78]
    uninitialized_array[61,79] = source_array[61,79]
    uninitialized_array[61,80] = source_array[61,80]
    uninitialized_array[60,71] = source_array[60,71]
    uninitialized_array[60,72] = source_array[60,72]
    uninitialized_array[60,77] = source_array[60,77]
    uninitialized_array[60,78] = source_array[60,78]
    uninitialized_array[60,79] = source_array[60,79]

    #upper right:
    uninitialized_array[82,82] = source_array[82,82]
    uninitialized_array[82,83] = source_array[82,83]
    uninitialized_array[82,84] = source_array[82,84]
    uninitialized_array[81,82] = source_array[81,82]
    uninitialized_array[81,83] = source_array[81,83]
    uninitialized_array[81,84] = source_array[81,84]

    #upper right corner:
    uninitialized_array[87,87] = source_array[87,87]
    uninitialized_array[87,88] = source_array[87,88]
    uninitialized_array[87,89] = source_array[87,89]
    uninitialized_array[87,90] = source_array[87,90]
    uninitialized_array[87,91] = source_array[87,91]
    uninitialized_array[86,87] = source_array[86,87]
    uninitialized_array[86,88] = source_array[86,88]
    uninitialized_array[86,89] = source_array[86,89]
    uninitialized_array[86,91] = source_array[86,91]

    return uninitialized_array



@jit
def advection_diffusion_fd(num_time_steps, num_x_steps, num_y_steps, min_time, max_time,
                           source_input_latitudes, source_input_longitudes, diff,
                           source_input_array, wx,  wy, datatype = 'float32'):
    """
    Returns dust field for 2D advection-diffusion and given input array
    """
    dt = np.float32(0.5)
    dx = 1
    dy = 1



    f_sol = np.zeros((num_time_steps, num_y_steps, num_x_steps), dtype=datatype)

    source_array = build_source_array(source_input_array, 91, 105)
   
    # ywind mulitplier: *3600 (für h) / 55597.46332227382 =  0.06475115562615506 = 0.06475
    # xwind mulitplier: *3600 (für h) / 65305.56055924967 =  0.05512547429607979 = 0.05513

    # fast
    ywind_mtpl = np.float(0.06475115562615506)
    xwind_mtpl = np.float(0.05512547429607979)

    # slow
    # ywind_mtpl = np.float32(0.03237557781307753)
    # xwind_mtpl = np.float32(0.027562737148039897)

    f_sol_current = np.zeros((num_y_steps, num_x_steps), dtype=datatype)

    #wiki loop
    for n in range(min_time,max_time-1):
        # if first:
        f_sol_current = fill_with_source(f_sol_current, source_array[n,:,:])
        f_sol_first = np.zeros((num_y_steps, num_x_steps), dtype=datatype)
        for j in range(1,num_y_steps-1):
            for i in range(1,num_x_steps-1):
                
                # if ( (f_sol[n,j,i+1] == 0) and ( f_sol[n,j,i-1] == 0) and (f_sol[n,j+1,i] == 0) and (f_sol[n,j-1,i] == 0) ):
                #     continue

                wx0 = ((wx[n,j,i] * xwind_mtpl))
                wy0 = ((wy[n,j,i] * ywind_mtpl))

                #solution for time n
                f_sol_first[j,i] = ((dt * diff*(((f_sol_current[j,i+1]-2*f_sol_current[j,i]+f_sol_current[j,i-1])/(dx**2))
                + ((f_sol_current[j+1,i]-2*f_sol_current[j,i]+f_sol_current[j-1,i])/(dy**2)))
                - ((wx0) * (dt/(2*dx)) * (f_sol_current[j,i+1]-f_sol_current[j,i-1]))
                - ((wy0) * (dt/(2*dy)) * (f_sol_current[j+1,i]-f_sol_current[j-1,i]))
                + f_sol_current[j,i]))

                #set erratic values to 0
                if (f_sol_first[j,i] < 0):
                    f_sol_first[j,i] = 0

        f_sol_current = f_sol_first

        #now we have a solution field for n+.5 (that is the next half hour)
        #we now take this solution as the input for our artificial next half hour time step
        #it's artificial, because we don't have 'real' data for it and hence create it by using an interpolation (mean)
        #between n and n+1
        f_sol_n = f_sol_current
        #fill with interpolation data
        f_sol_current = fill_with_source(f_sol_current, ((source_array[n,:,:] + source_array[(n+1),:,:])/2))
        f_sol_second = np.zeros((num_y_steps, num_x_steps), dtype=datatype)

        for j in range(1,num_y_steps-1):
            for i in range(1,num_x_steps-1):

                #wind:
                # to calculate half hour value from hourly data, we take the mean of the wind data from half hour before and half hour after 
                
                wx_mean = ((wx[n,j,i] + wx[(n+1),j,i]) / 2) * xwind_mtpl

                wy_mean = ((wy[n,j,i] + wy[(n+1),j,i]) / 2) * ywind_mtpl

                f_sol_second[j,i] = ((dt * diff*(((f_sol_current[j,i+1]-2*f_sol_current[j,i]+f_sol_current[j,i-1])/(dx**2))
                + ((f_sol_current[j+1,i]-2*f_sol_current[j,i]+f_sol_current[j-1,i])/(dy**2)))
                - ((wx_mean) * (dt/(2*dx)) * (f_sol_current[j,i+1]-f_sol_current[j,i-1]))
                - ((wy_mean) * (dt/(2*dy)) * (f_sol_current[j+1,i]-f_sol_current[j-1,i]))
                + f_sol_current[j,i]))

                if (f_sol_second[j,i] < 0):
                    f_sol_second[j,i] = 0

        f_sol_current = f_sol_second

        f_sol[n+1] = ((f_sol_second + f_sol_first) / 2)
        

        # f_sol[n+1,:,:] = fill_with_source(f_sol[n+1,:,:], source_array[(n+1),:,:])

    return f_sol


"--------------------------------------------------------------------"
'Regional Pixel Mapping Functions'
"--------------------------------------------------------------------"

def return_region_pixel_array(region_name = ''):

    # regions:

    # bodele region:
    if (region_name == 'bodele'):
        bodele_depression_pixels = np.array([[60,71],[60,72],[60,77],[60,78],[60,79],
                                            [61,69],[61,70],[61,71],[61,72],[61,73],[61,74],[61,75],[61,76],[61,77],[61,78],[61,79],[61,80],
                                            [62,69],[62,70],[62,71],[62,72],[62,73],[62,74],[62,75],[62,76],[62,77],[62,78],[62,79],[62,80],
                                            [63,68],[63,69],[63,70],[63,71],[63,72],[63,73],[63,74],[63,75],[63,76],[63,77],[63,78],[63,79],[63,80],
                                            [64,66],[64,67],[64,68],[64,69],[64,70],[64,71],[64,72],[64,73],[64,74],[64,75],[64,76],[64,77],[64,78],[64,79],[64,80],[64,67],
                                            [65,67],[65,68],[65,69],[65,70],[65,71],[65,72],[65,73],[65,74],[65,75],[65,76],[65,77],[65,78],[65,79],[65,80],
                                            [66,68],[66,69],[66,70],[66,71],[66,72],[66,73],[66,74],[66,75],[66,76],[66,77],[66,78],[66,79],[66,80],
                                            [67,68],[67,69],[67,70],[67,71],[67,72],[67,73],[67,74],[67,75],[67,76],[67,77],
                                            [68,68],[68,69],[68,70],[68,71],[68,72],[68,73],
                                            [69,71],[69,72],[69,73]], dtype = 'float32')
        return bodele_depression_pixels

    # togo coastline spot:
    elif (region_name == 'togo_coast'):
        togo_coast_pixel = np.array([[42,50]], dtype = 'float32')
        return togo_coast_pixel

    # countries:

    # Benin:
    elif (region_name == 'benin'):
        benin_pixels = np.array([[42,51],[42,52],
                                [43,50],[43,51],[43,52],[44,50],
                                [44,51],[44,52],
                                [45,50],[45,51],[45,52],
                                [46,50],[46,51],[46,52],
                                [47,50],[47,51],[47,52],
                                [48,50],[48,51],[48,52],
                                [49,50],[49,51],[49,52],[49,53],
                                [50,49],[50,50],[50,51],[50,52],[50,53],
                                [51,49],[51,50],[51,51],[51,52],[51,53],
                                [52,50],[52,51],[52,52],[52,53],
                                [53,51],[53,52],[53,53],
                                [54,52]], dtype = 'float32')
        return benin_pixels

    # Burkina Faso:
    elif (region_name == 'burkina_faso'):
        burkina_faso_pixels = np.array([[49,40],[49,41],[49,43],
                                        [50,40],[50,41],[50,42],[50,43],
                                        [51,39],[51,40],[51,41],[51,42],[51,43],
                                        [52,39],[52,40],[52,41],[52,42],[52,43],[52,44],[52,45],[52,46],[52,47],[52,48],[52,49],
                                        [53,39],[53,40],[53,41],[53,42],[53,43],[53,44],[53,45],[53,46],[53,47],[53,48],[53,49],[53,50],[53,51],
                                        [54,40],[54,41],[54,42],[54,43],[54,44],[54,45],[54,46],[54,47],[54,48],[54,49],[54,50],[54,51],
                                        [55,40],[55,41],[55,42],[55,43],[55,44],[55,45],[55,46],[55,47],[55,48],[55,49],[55,50],[55,51],
                                        [56,41],[56,42],[56,43],[56,44],[56,45],[56,46],[56,47],[56,48],[56,49],
                                        [57,43],[57,44],[57,45],[57,46],[57,47],[57,48],[57,49],
                                        [58,43],[58,44],[58,45],[58,46],[58,47],[58,48],
                                        [59,45],[59,46],[59,47],[59,48]], dtype = 'float32')
        return burkina_faso_pixels

    # Gambia:
    elif (region_name == 'gambia'):
        gambia_pixels = np.array([[56,21],[56,22],[56,24],[56,25], 
                                [57,23],[57,24]], dtype = 'float32')
        return gambia_pixels

    # Ghana
    elif (region_name == 'ghana'):
        ghana_pixels = np.array([[39,44],
                                [40,43],[40,44],[40,45],[40,46],[40,47],
                                [41,43],[41,44],[41,45],[41,46],[41,47],[41,48],[41,49],
                                [42,43],[42,44],[42,45],[42,46],[42,47],[42,48],[42,49],
                                [43,43],[43,44],[43,45],[43,46],[43,47],[43,48],
                                [44,43],[44,44],[44,45],[44,46],[44,47],[44,48],
                                [45,43],[45,44],[45,45],[45,46],[45,47],[45,48],
                                [46,44],[46,45],[46,46],[46,47],[46,48],
                                [47,44],[47,45],[47,46],[47,47],[47,48],
                                [48,43],[48,44],[48,45],[48,46],[48,47],[48,48],
                                [49,43],[49,44],[49,45],[49,46],[49,47],[49,48],
                                [50,43],[50,44],[50,45],[50,46],[50,47],[50,48],
                                [51,43],[51,44],[51,45],[51,46],[51,47],
                                [52,47]], dtype = 'float32')
        return ghana_pixels

    # Guinea:
    elif (region_name == 'guinea'):
        guinea_pixels = np.array([[44,33],
                                [45,33],[45,34],
                                [46,33],[46,34],
                                [47,31],[47,32],[47,33],[47,34],[47,35],
                                [48,26],[48,27],[48,31],[48,32],[48,33],[48,34],[48,35],
                                [49,26],[49,27],[49,30],[49,31],[49,32],[49,33],[49,34],
                                [50,25],[50,26],[50,27],[50,28],[50,29],[50,30],[50,31],[50,32],[50,33],[50,34],[50,35],
                                [51,24],[51,25],[51,26],[51,27],[51,28],[51,29],[51,30],[51,31],[51,32],[51,33],[51,34],
                                [52,24],[52,25],[52,26],[52,27],[52,28],[52,29],[52,30],[52,31],[52,32],[52,33],[52,34],
                                [53,25],[53,26],[53,27],[53,28],[53,29],[53,30],[53,31],[53,32],[53,33],
                                [54,26],[54,27],[54,28],[54,29],[54,30],[54,31],[54,32],[54,33],
                                [55,26]], dtype = 'float32')
        return guinea_pixels

    # Liberia:
    elif (region_name == 'liberia'):
        liberia_pixels = np.array([[39,34],[39,35],
                                [40,33],[40,34],[40,35],
                                [41,31],[41,32],[41,33],[41,34],[41,35],
                                [42,31],[42,32],[42,33],[42,34],[42,34],[42,35],
                                [43,30],[43,31],[43,32],[43,33],[43,34],[43,34],
                                [44,30],[44,31],[44,32],[44,33],[44,34],[44,34],
                                [45,31],[45,32],
                                [46,31],[46,32]], dtype = 'float32')
        return liberia_pixels

    # Mali:
    elif (region_name == 'mali'):
        mali_pixels = np.array([[50,35],[50,37],[50,38],
                                [51,35],[51,36],[51,37],[51,38],
                                [52,34],[52,35],[52,36],[52,37],[52,38],[52,39],
                                [53,34],[53,35],[53,36],[53,37],[53,38],[53,39],
                                [54,30],[54,31],[54,32],[54,33],[54,34],[54,35],[54,36],[54,37],[54,38],[54,39],[54,40],
                                [55,30],[55,31],[55,32],[55,33],[55,34],[55,35],[55,36],[55,37],[55,38],[55,39],[55,40],
                                [56,29],[56,30],[56,31],[56,32],[56,33],[56,34],[56,35],[56,36],[56,37],[56,38],[56,39],[56,40],[56,41],[56,42],
                                [57,29],[57,30],[57,31],[57,32],[57,33],[57,34],[57,35],[57,36],[57,37],[57,38],[57,39],[57,40],[57,41],[57,42],[57,43],
                                [58,29],[58,30],[58,31],[58,32],[58,33],[58,34],[58,35],[58,36],[58,37],[58,38],[58,39],[58,40],[58,41],[58,42],[58,43],[58,43],
                                [59,29],[59,29],[59,30],[59,31],[59,32],[59,33],[59,34],[59,35],[59,36],[59,37],[59,38],[59,39],[59,40],[59,41],[59,42],[59,43],[59,43],[59,44],[59,45],[59,46],
                                [60,29],[60,29],[60,30],[60,31],[60,32],[60,33],[60,34],[60,35],[60,36],[60,37],[60,38],[60,39],[60,40],[60,41],[60,42],[60,43],[60,43],[60,44],[60,45],[60,46],[60,47],[60,48],[60,49],[60,50],[60,51],
                                [61,39],[61,40],[61,41],[61,42],[61,43],[61,43],[61,44],[61,45],[61,46],[61,47],[61,48],[61,49],[61,50],[61,51],[61,52],[61,53],[61,54],
                                [62,39],[62,40],[62,41],[62,42],[62,43],[62,43],[62,44],[62,45],[62,46],[62,47],[62,48],[62,49],[62,50],[62,51],[62,52],[62,53],[62,54],
                                [63,39],[63,40],[63,41],[63,42],[63,43],[63,43],[63,44],[63,45],[63,46],[63,47],[63,48],[63,49],[63,50],[63,51],[63,52],[63,53],[63,54],
                                [64,39],[64,40],[64,41],[64,42],[64,43],[64,43],[64,44],[64,45],[64,46],[64,47],[64,48],[64,49],[64,50],[64,51],[64,52],[64,53],[64,54],
                                [65,39],[65,40],[65,41],[65,42],[65,43],[65,43],[65,44],[65,45],[65,46],[65,47],[65,48],[65,49],[65,50],[65,51],[65,52],[65,53],[65,54],
                                [66,39],[66,40],[66,41],[66,42],[66,43],[66,43],[66,44],[66,45],[66,46],[66,47],[66,48],[66,49],[66,50],[66,51],[66,52],[66,53],[66,54],
                                [67,38],[67,39],[67,40],[67,41],[67,42],[67,43],[67,43],[67,44],[67,45],[67,46],[67,47],[67,48],[67,49],[67,50],[67,51],[67,52],[67,53],[67,54],
                                [68,38],[68,39],[68,40],[68,41],[68,42],[68,43],[68,43],[68,44],[68,45],[68,46],[68,47],[68,48],[68,49],[68,50],[68,51],[68,52],
                                [69,38],[69,39],[69,40],[69,41],[69,42],[69,43],[69,43],[69,44],[69,45],[69,46],[69,47],[69,48],[69,49],[69,50],[69,51],[69,52],
                                [70,38],[70,39],[70,40],[70,41],[70,42],[70,43],[70,43],[70,44],[70,45],[70,46],[70,47],[70,48],[70,49],[70,50],[70,51],
                                [71,38],[71,39],[71,40],[71,41],[71,42],[71,43],[71,43],[71,44],[71,45],[71,46],[71,47],[71,48],[71,49],[71,50],
                                [72,38],[72,39],[72,40],[72,41],[72,42],[72,43],[72,43],[72,44],[72,45],[72,46],[72,47],[72,48],[72,49],
                                [73,38],[73,39],[73,40],[73,41],[73,42],[73,43],[73,43],[73,44],[73,45],[73,46],[73,47],[73,48],
                                [74,38],[74,39],[74,40],[74,41],[74,42],[74,43],[74,43],[74,44],[74,45],[74,46],[74,47],
                                [75,38],[75,39],[75,40],[75,41],[75,42],[75,43],[75,43],[75,44],[75,45],[75,46],[75,47],
                                [76,38],[76,39],[76,40],[76,41],[76,42],[76,43],[76,43],[76,44],
                                [77,37],[77,38],[77,39],[77,40],[77,41],[77,42],[77,43],[77,43],[77,44],
                                [78,37],[78,38],[78,39],[78,40],[78,41],[78,42],[78,42],
                                [79,37],[79,38],[79,39],[79,40]], dtype = 'float32')
        return mali_pixels

    # Niger:
    elif (region_name == 'niger'):
        niger_pixels = np.array([[54,51],[54,52],[54,53],
                                [55,50],[55,51],[55,52],[55,53],[55,54],[55,62],[55,63],
                                [56,49],[56,50],[56,51],[56,52],[56,53],[56,54],[56,59],[56,60],[56,61],[56,62],[56,63],[56,64],[56,66],[56,67],[56,68],
                                [57,49],[57,50],[57,51],[57,52],[57,53],[57,54],[57,55],[57,56],[57,57],[57,58],[57,59],[57,60],[57,61],[57,62],[57,63],[57,64],[57,65],[57,66],[57,67],[57,68],[57,69],
                                [57,49],[57,50],[57,51],[57,52],[57,53],[57,54],[57,55],[57,56],[57,57],[57,58],[57,59],[57,60],[57,61],[57,62],[57,63],[57,64],[57,65],[57,66],[57,67],[57,68],[57,69],
                                [58,48],[58,49],[58,50],[58,51],[58,52],[58,53],[58,54],[58,55],[58,56],[58,57],[58,58],[58,59],[58,60],[58,61],[58,62],[58,63],[58,64],[58,65],[58,66],[58,67],[58,68],[58,69],
                                [59,48],[59,49],[59,50],[59,51],[59,52],[59,53],[59,54],[59,55],[59,56],[59,57],[59,58],[59,59],[59,60],[59,61],[59,62],[59,63],[59,64],[59,65],[59,66],[59,67],[59,68],[59,69],
                                [60,50],[60,51],[60,52],[60,53],[60,54],[60,55],[60,56],[60,57],[60,58],[60,59],[60,60],[60,61],[60,62],[60,63],[60,64],[60,65],[60,66],[60,67],[60,68],[60,69],[60,70],
                                [61,54],[61,55],[61,56],[61,57],[61,58],[61,59],[61,60],[61,61],[61,62],[61,63],[61,64],[61,65],[61,66],[61,67],[61,68],[61,69],[61,70],[61,71],
                                [62,54],[62,55],[62,56],[62,57],[62,58],[62,59],[62,60],[62,61],[62,62],[62,63],[62,64],[62,65],[62,66],[62,67],[62,68],[62,69],[62,70],[62,71],
                                [63,54],[63,55],[63,56],[63,57],[63,58],[63,59],[63,60],[63,61],[63,62],[63,63],[63,64],[63,65],[63,66],[63,67],[63,68],[63,69],[63,70],[63,71],[63,72],
                                [64,54],[64,55],[64,56],[64,57],[64,58],[64,59],[64,60],[64,61],[64,62],[64,63],[64,64],[64,65],[64,66],[64,67],[64,68],[64,69],[64,70],[64,71],[64,72],
                                [65,55],[65,56],[65,57],[65,58],[65,59],[65,60],[65,61],[65,62],[65,63],[65,64],[65,65],[65,66],[65,67],[65,68],[65,69],[65,70],[65,71],[65,72],
                                [66,55],[66,56],[66,57],[66,58],[66,59],[66,60],[66,61],[66,62],[66,63],[66,64],[66,65],[66,66],[66,67],[66,68],[66,69],[66,70],[66,71],[66,72],
                                [67,55],[67,56],[67,57],[67,58],[67,59],[67,60],[67,61],[67,62],[67,63],[67,64],[67,65],[67,66],[67,67],[67,68],[67,69],[67,70],[67,71],[67,72],
                                [68,55],[68,56],[68,57],[68,58],[68,59],[68,60],[68,61],[68,62],[68,63],[68,64],[68,65],[68,66],[68,67],[68,68],[68,69],[68,70],[68,71],[68,72],
                                [69,57],[69,58],[69,59],[69,60],[69,61],[69,62],[69,63],[69,64],[69,65],[69,66],[69,67],[69,68],[69,69],[69,70],[69,71],[69,72],
                                [70,58],[70,59],[70,60],[70,61],[70,62],[70,63],[70,64],[70,65],[70,66],[70,67],[70,68],[70,69],[70,70],[70,71],[70,72],[70,73],
                                [71,59],[71,60],[71,61],[71,62],[71,63],[71,64],[71,65],[71,66],[71,67],[71,68],[71,69],[71,70],[71,71],[71,72],
                                [72,60],[72,61],[72,62],[72,63],[72,64],[72,65],[72,66],[72,67],[72,68],[72,69],[72,70],[72,71],[72,72],
                                [73,62],[73,63],[73,64],[73,65],[73,66],[73,67],[73,68],[73,69],[73,70],[73,71],[73,72],
                                [73,62],[73,63],[73,64],[73,65],[73,66],[73,67],[73,68],[73,69],[73,70],[73,71],[73,72],
                                [74,63],[74,64],[74,65],[74,66],[74,67],[74,68],[74,69],[74,70],[74,71],
                                [75,65],[75,66],[75,67],[75,68],[75,69],[75,70],[75,71],
                                [76,66],[76,67],[76,68],[76,69]], dtype = 'float32')
        return niger_pixels

    # Nigeria:
    elif (region_name == 'nigeria'):
        nigeria_pixels = np.array([[38,57],[38,58],
                                [39,57],[39,58],[39,59],[39,60],[39,61],
                                [40,56],[40,57],[40,58],[40,59],[40,60],[40,61],
                                [41,56],[41,57],[41,58],[41,59],[41,60],[41,61],[41,62],
                                [42,55],[42,56],[42,57],[42,58],[42,59],[42,60],[42,61],[42,62],[42,63],
                                [43,52],[43,53],[43,54],[43,55],[43,56],[43,57],[43,58],[43,59],[43,60],[43,61],[43,62],[43,63],[43,65],[43,66],
                                [44,52],[44,53],[44,54],[44,55],[44,56],[44,57],[44,58],[44,59],[44,60],[44,61],[44,62],[44,63],[44,64],[44,65],[44,66],
                                [45,52],[45,53],[45,54],[45,55],[45,56],[45,57],[45,58],[45,59],[45,60],[45,61],[45,62],[45,63],[45,64],[45,65],[45,66],[45,67],
                                [46,52],[46,53],[46,54],[46,55],[46,56],[46,57],[46,58],[46,59],[46,60],[46,61],[46,62],[46,63],[46,64],[46,65],[46,66],[46,67],
                                [47,52],[47,53],[47,54],[47,55],[47,56],[47,57],[47,58],[47,59],[47,60],[47,61],[47,62],[47,63],[47,64],[47,65],[47,66],[47,67],[47,68],
                                [48,53],[48,54],[48,55],[48,56],[48,57],[48,58],[48,59],[48,60],[48,61],[48,62],[48,63],[48,64],[48,65],[48,66],[48,67],[48,68],
                                [48,53],[48,54],[48,55],[48,56],[48,57],[48,58],[48,59],[48,60],[48,61],[48,62],[48,63],[48,64],[48,65],[48,66],[48,67],[48,68],[48,69],
                                [49,53],[49,54],[49,55],[49,56],[49,57],[49,58],[49,59],[49,60],[49,61],[49,62],[49,63],[49,64],[49,65],[49,66],[49,67],[49,68],[49,69],
                                [50,54],[50,55],[50,56],[50,57],[50,58],[50,59],[50,60],[50,61],[50,62],[50,63],[50,64],[50,65],[50,66],[50,67],[50,68],[50,69],
                                [51,54],[51,55],[51,56],[51,57],[51,58],[51,59],[51,60],[51,61],[51,62],[51,63],[51,64],[51,65],[51,66],[51,67],[51,68],[51,69],
                                [52,54],[52,55],[52,56],[52,57],[52,58],[52,59],[52,60],[52,61],[52,62],[52,63],[52,64],[52,65],[52,66],[52,67],[52,68],[52,69],[52,70],
                                [53,54],[53,55],[53,56],[53,57],[53,58],[53,59],[53,60],[53,61],[53,62],[53,63],[53,64],[53,65],[53,66],[53,67],[53,68],[53,69],[53,70],[53,71],
                                [54,54],[54,55],[54,56],[54,57],[54,58],[54,59],[54,60],[54,61],[54,62],[54,63],[54,64],[54,65],[54,66],[54,67],[54,68],[54,69],[54,70],[54,71],
                                [55,54],[55,55],[55,56],[55,57],[55,58],[55,59],[55,60],[55,61],[55,62],[55,63],[55,64],[55,65],[55,66],[55,67],[55,68],[55,69],[55,70],
                                [56,54],[56,55],[56,56],[56,57],[56,58],[56,60],[56,61],[56,64],[56,65],[56,66],[56,67],[56,68],[56,69],[56,70],
                                [57,54],[57,55],[57,56],[57,57],[57,58],[57,69]], dtype = 'float32')
        return nigeria_pixels

    # Sierra Leone:
    elif (region_name == 'sierra_leone'):
        sierra_leone_pixels = np.array([[44,28],[44,29],
                                        [45,27],[45,28],[45,29],[45,30],
                                        [46,27],[46,28],[46,29],[46,30],[46,31],
                                        [47,27],[47,28],[47,29],[47,30],
                                        [48,27],[48,28],[48,29],[48,30],
                                        [49,28],[49,29],[49,30]], dtype = 'float32')
        return sierra_leone_pixels

    # Senegal:
    elif (region_name == 'senegal'):
        senegal_pixels = np.array([[55,21],[55,22],[55,23],[55,24],[55,25],[55,26],[55,27],[55,28],[55,29],
                                [56,23],[56,24],[56,26],[56,27],[56,28],[56,29],
                                [57,21],[57,22],[57,25],[57,26],[57,27],[57,28],
                                [58,21],[58,22],[58,23],[58,24],[58,25],[58,26],[58,27],[58,28],
                                [59,20],[59,21],[59,22],[59,23],[59,24],[59,25],[59,26],[59,27],[59,28],
                                [60,21],[60,22],[60,23],[60,24],[60,25],[60,26],[60,27],
                                [61,21],[61,22],[61,23],[61,24],[61,25],[61,26],
                                [62,21],[62,22],[62,23],[62,24],[62,25],
                                [62,24]], dtype = 'float32')
        return senegal_pixels

    # Togo:
    elif (region_name == 'togo'):
        togo_pixels = np.array([[42,49],[42,50],
                                [43,49],[43,50],
                                [44,49],[44,50],
                                [45,49],[45,50],
                                [46,49],[46,50],
                                [47,49],[47,50],
                                [48,49],[48,50],
                                [49,48],[49,49],
                                [50,48],[50,49],
                                [51,48],[51,49]], dtype = 'float32')
        return togo_pixels
    
    else:
        return None



"--------------------------------------------------------------------"
'Regression Preparation Functions'
"--------------------------------------------------------------------"


@jit
def get_pixels_data_one_dim(data, pixels_list):
    pixel_data = np.zeros((pixels_list.shape[0]), dtype = 'float32')
    idx = 0
    for pixel in range(pixels_list.shape[0]):
        pixel_data[idx] = data[int(pixels_list[pixel][0])][int(pixels_list[pixel][1])]
        idx += 1
    return pixel_data

@jit
def get_pixels_data_two_dim(data, pixels_list, pixels_data_x_shape = 105, pixels_data_y_shape = 91):
    pixel_data = np.zeros((pixels_data_x_shape, pixels_data_y_shape), dtype = 'float32')
    for pixel in pixels_list:
        pixel_data[pixel[0]][pixel[1]] = data[pixel[0]][pixel[1]]
    return pixel_data

@jit
def get_hourly_region_data(data, region):
    hourly_region_data = np.zeros((data.shape[0], region.shape[0]), dtype = 'float32')
    idx = 0

    for hourly_data in data:
        hourly_region_data[idx] = get_pixels_data_one_dim(hourly_data, region)
        idx += 1
    
    return hourly_region_data

@jit
def get_regional_mean_data(regional_data):

    regional_mean_data = np.zeros((regional_data.shape[0], 1), dtype = 'float32')
    regional_mean_data = np.sum(regional_data, axis=1)/regional_data.shape[1]
    
    return regional_mean_data

@jit
def hourly_regional_data_to_daily_mean(data):
    daily_mean_data = np.zeros((round(data.shape[0]/24), data.shape[1]), dtype = 'float32')
    day_counter = 0
    daily_data = np.zeros((data.shape[1]), dtype = 'float32')

    idx = 0

    for hourly_data in data:
        daily_data += hourly_data
        if ((idx != 0) and (idx%24 == 0)):
            daily_mean_data[day_counter] = daily_data / 24
            daily_data = np.zeros((data.shape[1]), dtype = 'float32')
            day_counter += 1
        idx += 1
    return daily_mean_data

@jit
def extract_hourly_jun_sep_data(data,hourly_junsep_indices_np,hourly_novapr_indices_np):

    hourly_junsep_counter = 0
    hourly_novapr_counter = 0
    idx = 0

    hourly_junsep_data = np.zeros((hourly_junsep_indices_np.shape[1], data.shape[1]), dtype = 'float32')
    hourly_novapr_data = np.zeros((hourly_novapr_indices_np.shape[1], data.shape[1]), dtype = 'float32')
    
    for hourly_data in data:
        if idx in hourly_junsep_indices_np:
            hourly_junsep_data[hourly_junsep_counter] = hourly_data
            hourly_junsep_counter += 1 
        elif idx in hourly_novapr_indices_np:
            hourly_novapr_data[hourly_novapr_counter] = hourly_data
            hourly_novapr_counter += 1
        idx += 1
        
    return (hourly_junsep_data, hourly_novapr_data)


"--------------------------------------------------------------------"
'Regression Functions'
"--------------------------------------------------------------------"






"--------------------------------------------------------------------"
'Miscellaneous Functions'
"--------------------------------------------------------------------"



#taken from: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula

from math import cos, asin, sqrt, pi

def distance(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...