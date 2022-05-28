#Imports

#standard modules
import pandas as pd
import numpy as np
import os
import re
#plots:
import matplotlib.pyplot as plt
from matplotlib.patches import Patch,Rectangle
import cartopy
import cartopy.feature as cf
import cartopy.crs as ccrs
import seaborn as sns
import folium
from folium.plugins import HeatMap, HeatMapWithTime
import cmocean
import cmocean.cm as cmo
import math
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
#regression
import statsmodels.api as sm


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



def process_merra_data(data_directory, seasonal_indices = True, variables = [], two_vars = True, timing='', time_steps = 0, y_steps = 91, x_steps = 0, datatype = 'float32'):
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

    # boolean to for later initialization of all variables and arrays
    first = True

    file_list = os.listdir(directory)
    # (daily/monthly depending on input)
    counter_total = 0
    if seasonal_indices:
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

                if timing == 'hourly':
                    if two_vars:
                        if seasonal_indices:
                            hourly_novapr_indices = []
                            hourly_junsep_indices = []
                            for i in range(24*counter_total, 24*counter_total + 24) : hourly_novapr_indices.append(i)
                            novapr_indices.append(counter_total)

                        #create data ndarray with initialized time steps
                        data_total_time_0 = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                        data_total_time_0[0:24,:,:] = data.variables[variables[0]][:,:,:]

                        data_total_time_1 = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                        data_total_time_1[0:24,:,:] = data.variables[variables[1]][:,:,:]
                    else:
                        if seasonal_indices:
                            hourly_novapr_indices = []
                            hourly_junsep_indices = []
                            for i in range(24*counter_total, 24*counter_total + 24) : hourly_novapr_indices.append(i)
                            novapr_indices.append(counter_total)

                        #create data ndarray with initialized time steps
                        data_total_time_0 = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                        data_total_time_0[0:24,:,:] = data.variables[variables[0]][:,:,:]

                elif timing == 'three_hourly':
                    if seasonal_indices:
                        three_hourly_novapr_indices = []
                        three_hourly_junsep_indices = []
                        for i in range(8*counter_total, 8*counter_total + 8) : three_hourly_novapr_indices.append(i)
                        novapr_indices.append(counter_total) 

                    data_total_time = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                    data_total_time[0:8,:,:] = data.variables[variables[0]][:,:,:]

                elif timing == 'monthly':
                    if seasonal_indices:
                        novapr_indices.append(counter_total)

                    data_total_time = np.zeros((time_steps, y_steps, x_steps), dtype=datatype)
                    data_total_time[0,:,:] = data.variables[variables[0]][:,:,:]

                counter_total += 1
                # continuity check to see if we got all dates covered
                # since aod files have another naming convention, we control for that
                if timing == 'monthly':
                    continuity_check.append(datetime.strptime(filename[27:33], '%Y%m').strftime('%Y-%m'))
                else:
                    continuity_check.append(datetime.strptime(filename[27:35], '%Y%m%d').strftime('%Y-%m-%d'))
                
                first = False
                continue

            if seasonal_indices:
                # calculate mean for jun-sep period using regex
                if (re.search(r'(.*)-(06|07|08|09)-(.*)', data.RangeBeginningDate)):
                    # calculate current data to add to overall data
                    if timing == 'hourly':
                        for i in range(24*counter_total, 24*counter_total + 24) : hourly_junsep_indices.append(i) 
                        junsep_indices.append(counter_total)
                    elif timing == 'three_hourly':
                        for i in range(8*counter_total, 8*counter_total + 8) : three_hourly_junsep_indices.append(i) 
                        junsep_indices.append(counter_total)
                    elif timing == 'monthly':
                        junsep_indices.append(counter_total)

                # calculate mean for nov-apr period using regex
                if (re.search(r'(.*)-(11|12|01|02|03|04)-(.*)', data.RangeBeginningDate)):
                    # calculate current data to add to overall data
                    if timing == 'hourly':
                        for i in range(24*counter_total, 24*counter_total + 24) : hourly_novapr_indices.append(i) 
                        novapr_indices.append(counter_total)
                    elif timing == 'three_hourly':
                        for i in range(8*counter_total, 8*counter_total + 8) : three_hourly_novapr_indices.append(i) 
                        novapr_indices.append(counter_total)
                    elif timing == 'monthly':
                        novapr_indices.append(counter_total)
    
            # calculate total data independent of season
            if timing == 'hourly':
                data_current_time_0 = data.variables[variables[0]][:,:,:]
                data_total_time_0[24*counter_total: 24*counter_total+24,:,:] = data_current_time_0
                if two_vars:
                    data_current_time_1 = data.variables[variables[1]][:,:,:]
                    data_total_time_1[24*counter_total:24*counter_total+24,:,:] = data_current_time_1
            elif timing == 'three_hourly':
                data_current_time = data.variables[variables[0]][:,:,:]
                data_total_time[8*counter_total: 8*counter_total+8,:,:] = data_current_time
            elif timing == 'monthly':
                data_current_time = data.variables[variables[0]][:,:,:]
                data_total_time[counter_total,:,:] = data_current_time

            counter_total += 1
            # add to dates array
            if timing == 'monthly':
                continuity_check.append(datetime.strptime(filename[27:33], '%Y%m').strftime('%Y-%m'))
            else:
                continuity_check.append(datetime.strptime(filename[27:35], '%Y%m%d').strftime('%Y-%m-%d'))

    # continuity check:
    if timing == 'hourly':
        # given time range:
        test_ts = pd.Series(pd.to_datetime(continuity_check))
        # continuous time range from 1980-01-01 to 2016-12-31
        continuous_ts = pd.date_range(start='1980-01-01', end='2016-12-31')
        assert (continuous_ts.difference(test_ts).size == 0)
        if seasonal_indices:
            if two_vars:
                return [longitudes, latitudes, time, data_total_time_0, data_total_time_1, hourly_junsep_indices, junsep_indices, hourly_novapr_indices, novapr_indices]
            else:
                return [longitudes, latitudes, time, data_total_time_0, hourly_junsep_indices, junsep_indices, hourly_novapr_indices, hourly_novapr_indices]
        else:
            if two_vars:
                return [longitudes, latitudes, time, data_total_time_0, data_total_time_1]
            else:
                return [longitudes, latitudes, time, data_total_time_0]

    elif timing == 'three_hourly':
        # given time range:
        test_ts = pd.Series(pd.to_datetime(continuity_check))
        # continuous time range from 1980-01-01 to 2016-12-31
        continuous_ts = pd.date_range(start='1980-01-01', end='2016-12-31')
        assert (continuous_ts.difference(test_ts).size == 0)
        if seasonal_indices:
            return [longitudes, latitudes, time, data_total_time, three_hourly_junsep_indices, junsep_indices, three_hourly_novapr_indices, novapr_indices]
        else:
            return [longitudes, latitudes, time, data_total_time]
    
    elif timing == 'monthly':
        #given time range:
        test_ts = pd.Series(pd.to_datetime(continuity_check).strftime('%Y-%m'))
        #continuous time range from 1980-01 to 2016-12
        continuous_ts = pd.date_range(start='1980-01', end='2016-12', freq='M').strftime('%Y-%m')
        assert (continuous_ts.difference(test_ts).size == 0)
        if seasonal_indices:
            return [longitudes, latitudes, time, data_total_time, junsep_indices, novapr_indices]
        else:
            return [longitudes, latitudes, time, data_total_time]


@jit
def extract_seasonal_data(total_data, novapr_indices, junsep_indices):
    novapr_data = np.zeros((np.array([novapr_indices], dtype='float32').shape[1], total_data.shape[1], total_data.shape[2]), dtype = 'float32')
    junsep_data = np.zeros((np.array([junsep_indices], dtype='float32').shape[1], total_data.shape[1], total_data.shape[2]), dtype = 'float32')

    idx = 0
    counter_novapr = 0
    counter_junsep = 0
    for entry in total_data:
        if idx in novapr_indices:
            novapr_data[counter_novapr] = entry
            counter_novapr += 1
        elif idx in junsep_indices:
            junsep_data[counter_junsep] = entry
            counter_junsep += 1
        idx += 1

    return novapr_data, junsep_data

@jit
def hourly_data_to_daily_mean(data):
    daily_mean_data = np.zeros((round(data.shape[0]/24), data.shape[1], data.shape[2]), dtype = 'float32')
    day_counter = 0
    daily_data = np.zeros((data.shape[1], data.shape[2]), dtype = 'float32')

    idx = 0

    for hourly_data in data:
        daily_data += hourly_data
        if ((idx != 0) and (idx%24 == 0)):
            daily_mean_data[day_counter] = daily_data / 24
            daily_data = np.zeros((data.shape[1], data.shape[2]), dtype = 'float32')
            day_counter += 1
        idx += 1
    return daily_mean_data

@jit
def three_hourly_data_to_daily_mean(data):
    daily_mean_data = np.zeros((round(data.shape[0]/8), data.shape[1], data.shape[2]), dtype = 'float32')
    day_counter = 0
    daily_data = np.zeros((data.shape[1], data.shape[2]), dtype = 'float32')

    idx = 0

    for hourly_data in data:
        daily_data += hourly_data
        if ((idx != 0) and (idx%8 == 0)):
            daily_mean_data[day_counter] = daily_data / 8
            daily_data = np.zeros((data.shape[1], data.shape[2]), dtype = 'float32')
            day_counter += 1
        idx += 1
    return daily_mean_data


def process_outcome_data():
    """
    process_outcome_data() returns dataframes of the economic input data of interest.

    Returns:
        df_pwt_resid_log(dataframe):    a dataframe of the residualized logarithmic gdp of the Penn World Tables for 1980-2016 and countries of interest
        df_wbdi_resid_log(dataframe):   a dataframe of the residualized logarithmic gdp of the World Bank Development Indicators for 1980-2016 and countries of interest
        df_mpd_resid_log(dataframe):    a dataframe of the residualized logarithmic gdp of the Maddison Project Database for 1980-2016 and countries of interest
    """

    #create times and countries of interest
    columns_years =  list(range(1979, 2018))
    countries = ['Benin', 'Burkina Faso', 'Gambia', 'Ghana', 'Guinea', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Sierra Leone', 'Senegal', 'Togo']


    #Maddison Project Database(in constant 2011 USD):
    # 2011(Dec) USD to 2017(Dec) USD: $1.09 #https://www.bls.gov/data/inflation_calculator.htm

    file_mpd = parent_directory + '\\raw_data\\2.2_outcome_data\\maddison_project_database\\mpd2020.xlsx'

    mpd = pd.read_excel(file_mpd, sheet_name = 'Full data', engine='openpyxl')

    #create mpd data frame that will be plotted later
    df_mpd = pd.DataFrame(columns = columns_years)
    df_mpd.insert(0, "country", countries)

    mpd_pop = pd.read_excel(file_mpd, sheet_name = 'Full data', engine='openpyxl')

    df_mpd_pop = pd.DataFrame(columns = columns_years)
    df_mpd_pop.insert(0, "country", countries)

    df_mpd_per_cap = pd.DataFrame(columns = columns_years)
    df_mpd_per_cap.insert(0, "country", countries)

    #create dataframe from csv file
    for country,country_name in enumerate(countries):
        for year in range(1979, 2018):
            df_mpd.at[country,year] = (mpd['gdppc'].loc[(mpd['country'] == country_name) & (mpd['year'] == year)].values[0]*
                                      mpd['pop'].loc[(mpd['country'] == country_name) & (mpd['year'] == year)].values[0]*1000)*1.09
            df_mpd_pop.at[country,year] = mpd['pop'].loc[(mpd['country'] == country_name) & (mpd['year'] == year)].values[0]*1000 #pop given in 1000s
            df_mpd_per_cap.at[country,year] = (mpd['gdppc'].loc[(mpd['country'] == country_name) & (mpd['year'] == year)].values[0])*1.09


    #create residualized log dataframe        
    df_mpd_resid_log = pd.DataFrame(columns = columns_years)
    df_mpd_resid_log.insert (0, "country", countries)

    df_mpd_growth = pd.DataFrame(columns = columns_years)
    df_mpd_growth.insert (0, "country", countries)

    df_mpd_per_cap_growth = pd.DataFrame(columns = columns_years)
    df_mpd_per_cap_growth.insert (0, "country", countries)


    for index, country in enumerate(df_mpd['country']):
        for year in range(1979, 2016):
            df_mpd_resid_log.at[index,year+1] = (np.log(df_mpd.loc[(df_mpd['country'] == country)][year].values[0]) - np.log(df_mpd.loc[(df_mpd['country'] == country)][year+1].values[0]))
            #df_mpd_resid_log.at[index,year] = np.log(df_mpd.loc[(df_mpd['country'] == country)][year].values[0])
            #df_mpd_resid_log.at[index,year] = np.log((df_mpd.loc[(df_mpd['country'] == country)][year+1].values[0] - df_mpd.loc[(df_mpd['country'] == country)][year].values[0]))
            # df_mpd_growth.at[index,year] = (df_mpd.loc[(df_mpd['country'] == country)][year+1].values[0] / df_mpd.loc[(df_mpd['country'] == country)][year].values[0]) - 1
            df_mpd_growth.at[index,year+1] = ((df_mpd.loc[(df_mpd['country'] == country)][year+1].values[0] - df_mpd.loc[(df_mpd['country'] == country)][year].values[0]) /
                                            df_mpd.loc[(df_mpd['country'] == country)][year].values[0])
            # df_mpd_per_cap_growth.at[index,year] = ((df_mpd_per_cap.loc[(df_mpd_per_cap['country'] == country)][year+1].values[0]/
            #                                          df_mpd_per_cap.loc[(df_mpd_per_cap['country'] == country)][year].values[0]) - 1)
            df_mpd_per_cap_growth.at[index,year+1] = ((df_mpd_per_cap.loc[(df_mpd_per_cap['country'] == country)][year+1].values[0]-
                                                     df_mpd_per_cap.loc[(df_mpd_per_cap['country'] == country)][year].values[0]) /
                                                     df_mpd_per_cap.loc[(df_mpd_per_cap['country'] == country)][year].values[0])

    ######################################################################

    #Penn World Tables(in constant 2017 USD):
    file_pwt = parent_directory + '\\raw_data\\2.2_outcome_data\\penn_world_tables\\FebPwtExport2232022.csv'

    #country codes in pwt dataset
    country_codes = ['BEN', 'BFA', 'GMB', 'GHA', 'GIN', 'LBR', 'MLI', 'NER', 'NGA', 'SLE', 'SEN', 'TGO']

    #create pwt data frame that will be plotted later
    df_pwt = pd.DataFrame(columns = columns_years)
    df_pwt.insert (0, "country", countries)

    df_pwt_per_cap = pd.DataFrame(columns = columns_years)
    df_pwt_per_cap.insert (0, "country", countries)

    pwt = pd.read_csv(file_pwt)

    #create dataframe from csv file
    for country,country_code in enumerate(country_codes):
        for year in range(1979, 2018):
            df_pwt.at[country,year] = pwt['AggValue'].loc[(pwt['RegionCode'] == country_code) & (pwt['YearCode'] == year)].values[0]*(10**6)
            df_pwt_per_cap.at[country,year] = ((pwt['AggValue'].loc[(pwt['RegionCode'] == country_code) & (pwt['YearCode'] == year)].values[0])/
                                                df_mpd_pop.at[country,year])

    #create residualized log dataframe        
    df_pwt_resid_log = pd.DataFrame(columns = columns_years)
    df_pwt_resid_log.insert (0, "country", countries)

    df_pwt_growth = pd.DataFrame(columns = columns_years[:-1])
    df_pwt_growth.insert (0, "country", countries)

    df_pwt_growth_per_cap = pd.DataFrame(columns = columns_years[:-1])
    df_pwt_growth_per_cap.insert (0, "country", countries)

    for index, country in enumerate(df_pwt['country']):
        for year in range(1979, 2016):
            df_pwt_resid_log.at[index,year+1] = (np.log(df_pwt.loc[(df_pwt['country'] == country)][year].values[0]) - np.log(df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0]))
            #df_pwt_resid_log.at[index,year] = np.log(df_pwt.loc[(df_pwt['country'] == country)][year].values[0])
            #df_pwt_resid_log.at[index,year] = np.log((df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0] - df_pwt.loc[(df_pwt['country'] == country)][year].values[0]))
            #df_pwt_growth.at[index,year] = (df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0]) / np.log(df_pwt.loc[(df_pwt['country'] == country)][year].values[0]) - 1
            # df_pwt_growth.at[index,year] = (float(df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0]) / float(df_pwt.loc[(df_pwt['country'] == country)][year].values[0])) - 1
            df_pwt_growth.at[index,year+1] = ((float(df_pwt.loc[(df_pwt['country'] == country)][year+1].values[0]) - float(df_pwt.loc[(df_pwt['country'] == country)][year].values[0])) /
                                           float(df_pwt.loc[(df_pwt['country'] == country)][year].values[0]))
            # df_pwt_growth_per_cap.at[index,year] = ((float(df_pwt_per_cap.loc[(df_pwt_per_cap['country'] == country)][year+1].values[0])/
            #                                          float(df_pwt_per_cap.loc[(df_pwt_per_cap['country'] == country)][year].values[0])) - 1)
            df_pwt_growth_per_cap.at[index,year+1] = ((float(df_pwt_per_cap.loc[(df_pwt_per_cap['country'] == country)][year+1].values[0])-
                                                     float(df_pwt_per_cap.loc[(df_pwt_per_cap['country'] == country)][year].values[0])) /
                                                     float(df_pwt_per_cap.loc[(df_pwt_per_cap['country'] == country)][year].values[0]))


    ######################################################################        
            
    #World Bank Development Indicators (in constant 2015 USD):
    # 2015(Dec) USD to 2017(Dec) USD: $1.04 #https://www.bls.gov/data/inflation_calculator.htm

    # file_wbdi = parent_directory + '\\raw_data\\2.2_outcome_data\\world_bank_development_indicators\\gdp_constant_2015_usd\\babf19e0-2ef9-49ac-96ed-f9405ca35164_Data.csv'
    file_wbdi = parent_directory + '\\raw_data\\2.2_outcome_data\\world_bank_development_indicators\\gdp_constant_2015_usd\\d2e26fc5-507f-429d-84b1-5494db626098_Data.csv'
    # file_wbdi_per_capita = parent_directory + '\\raw_data\\2.2_outcome_data\\world_bank_development_indicators\\gdp_per_capita_constant_2015_usd\\57ab2b5a-425e-46cb-8590-4670aa232348_Data.csv'
    file_wbdi_per_capita = parent_directory + '\\raw_data\\2.2_outcome_data\\world_bank_development_indicators\\gdp_per_capita_constant_2015_usd\\4b995b1c-f7d6-4b0a-86c8-6cb53000472c_Data.csv'
    #create wbdi data frame that will be plotted later
    df_wbdi = pd.read_csv(file_wbdi)
    #drop unnecessary columns
    df_wbdi = df_wbdi.drop(['Country Code', 'Series Name', 'Series Code'], axis=1)
    #drop unnecessary rows
    df_wbdi = df_wbdi[:-5]
    #rename year columns
    df_wbdi = pd.concat([df_wbdi.iloc[: ,0:1], df_wbdi.iloc[: ,1:].rename(columns = lambda x : str(x)[:-9])], axis=1)

    # replace .. values with NaN
    df_wbdi = df_wbdi.replace('..', np.nan)

    # change dtypes to numeric
    df_wbdi[["1980","1981","1982","1983","1984","1985","1986","1987","1988","1989",
         "1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",]] = df_wbdi[["1980","1981","1982","1983","1984","1985","1986","1987","1988","1989",
                                                                                        "1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",]].apply(pd.to_numeric)

    #multiply by inflator to 2017 USD
    df_wbdi[df_wbdi.select_dtypes(include=['float64']).columns] *= 1.04

    #create residualized log dataframe
    df_wbdi_resid_log = pd.DataFrame(columns = columns_years)
    df_wbdi_resid_log.insert (0, "country", countries)

    df_wbdi_growth = pd.DataFrame(columns = columns_years)
    df_wbdi_growth.insert (0, "country", countries)

    for index, country in enumerate(df_wbdi['Country Name']):
        for year in range(1979, 2017):
            df_wbdi_resid_log.at[index,year] = (np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0])) - np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])))
            #df_wbdi_resid_log.at[index,year] = np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0]))
            #df_wbdi_resid_log.at[index,year] = np.log((float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0]) - float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])))
            # df_wbdi_growth.at[index,year] = (float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0]) /
            #                                  float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])) - 1
            df_wbdi_growth.at[index,year+1] = ((float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0]) -
                                             float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])) /
                                             float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0]))

    df_wbdi_per_cap = pd.read_csv(file_wbdi_per_capita)
    #drop unnecessary columns
    df_wbdi_per_cap = df_wbdi_per_cap.drop(['Country Code', 'Series Name', 'Series Code'], axis=1)
    #drop unnecessary rows
    df_wbdi_per_cap = df_wbdi_per_cap[:-5]
    #rename year columns
    df_wbdi_per_cap = pd.concat([df_wbdi_per_cap.iloc[: ,0:1], df_wbdi_per_cap.iloc[: ,1:].rename(columns = lambda x : str(x)[:-9])], axis=1)

    # replace .. values with NaN
    df_wbdi_per_cap = df_wbdi_per_cap.replace('..', np.nan)

    # change dtypes to numeric
    df_wbdi_per_cap[["1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989",
                     "1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",]] = df_wbdi_per_cap[["1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989",
                                                                                                            "1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",]].apply(pd.to_numeric)

    #multiply by inflator to 2017 USD
    df_wbdi[df_wbdi.select_dtypes(include=['float64']).columns] *= 1.04

    df_wbdi_pop = pd.DataFrame(columns = columns_years)
    df_wbdi_pop.insert (0, "country", countries)

    #create residualized log dataframe
    df_wbdi_per_cap_resid_log = pd.DataFrame(columns = columns_years)
    df_wbdi_per_cap_resid_log.insert (0, "country", countries)

    df_wbdi_per_cap_growth = pd.DataFrame(columns = columns_years)
    df_wbdi_per_cap_growth.insert (0, "country", countries)

    for index, country in enumerate(df_wbdi_per_cap['Country Name']):
        for year in range(1979, 2017):
            df_wbdi_per_cap_resid_log.at[index,year] = (np.log(float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year+1)].values[0])) - np.log(float(df_wbdi_per_cap.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])))
            #df_wbdi_resid_log.at[index,year] = np.log(float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0]))
            #df_wbdi_resid_log.at[index,year] = np.log((float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year+1)].values[0]) - float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0])))
            # df_wbdi_per_cap_growth.at[index,year] = (float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year+1)].values[0])/
            #                                          float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year)].values[0])) - 1
            df_wbdi_per_cap_growth.at[index,year+1] = ((float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year+1)].values[0]) -
                                                     float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year)].values[0])) /
                                                     float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year)].values[0]))
            df_wbdi_pop.at[index,year] = float(df_wbdi.loc[(df_wbdi['Country Name'] == country)][str(year)].values[0]) / float(df_wbdi_per_cap.loc[(df_wbdi_per_cap['Country Name'] == country)][str(year)].values[0])


    ######################################################################        
            
    df_pwt = df_pwt.drop(1979, 1)
    df_pwt_growth = df_pwt_growth.drop(1979, 1)
    df_pwt_per_cap = df_pwt_per_cap.drop(1979, 1)
    df_pwt_growth_per_cap = df_pwt_growth_per_cap.drop(1979, 1)
    df_wbdi = df_wbdi.drop('1979', 1)
    df_wbdi_per_cap = df_wbdi_per_cap.drop('1979', 1)
    df_wbdi_pop = df_wbdi_pop.drop(1979, 1)
    df_wbdi_growth = df_wbdi_growth.drop(1979, 1)
    df_wbdi_per_cap_growth = df_wbdi_per_cap_growth.drop(1979, 1)
    df_mpd = df_mpd.drop(1979, 1)
    df_mpd_growth = df_mpd_growth.drop(1979, 1)
    df_mpd_pop = df_mpd_pop.drop(1979, 1)
    df_mpd_per_cap = df_mpd_per_cap.drop(1979, 1)
    df_mpd_per_cap_growth = df_mpd_per_cap_growth.drop(1979, 1)

    return [df_pwt, df_pwt_growth, df_pwt_per_cap, df_pwt_growth_per_cap, df_wbdi, df_wbdi_per_cap, df_wbdi_pop, df_wbdi_growth, df_wbdi_per_cap_growth, df_mpd, df_mpd_growth, df_mpd_pop, df_mpd_per_cap, df_mpd_per_cap_growth]


######################################################################



"--------------------------------------------------------------------"
'Plotting Functions'
"--------------------------------------------------------------------"

def add_pixel(ax,lat_from, lat_to, lon_from, lon_to, alpha=1):
    # ax.add_patch(Rectangle((lon_from,lat_from), (lon_to-lon_from), (lat_to-lat_from),color = 'black',fill=False, lw=.5, linestyle='--', alpha = .3))
    ax.add_patch(Rectangle((lon_from,lat_from), (lon_to-lon_from), (lat_to-lat_from),color = 'black',fill=True, alpha = alpha))

def add_pixel2(ax,lat, lon, alpha=1, color='black', lw=1, linestyle='-', fill=True):
    ax.add_patch(Rectangle([(lat-.313),(lon-.25)], (.56), (.45),color = color,fill=fill, alpha = alpha, lw=lw, linestyle=linestyle))

#function to plot merra data

#taken in parts from: https://www.kaggle.com/gpreda/how-to-read-and-plot-earthdata-merra2-data-files
def plot_merra_data(data, lons, lats, title='', date='', data_value='', extent=[-150, 150, -90, 90],
                    borders = False, bodele = False, plot_grids = False, add_source_region = False,
                    add_bodele_source_exclusive = False, add_bodele_source_exclusive_alpha = 1, source_region_alpha = 1, source_region_lw = 0.2, source_region_fill = False,
                    cbar_color = 'YlOrRd', cbar_min = 0, cbar_max = 7, unit = 1, shrink=0.8, ax_text_left = -0.05, ax_text_bottom=-0.1):
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
    ax.text(ax_text_left, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax.transAxes, size=14)
    ax.text(0.5, ax_text_bottom, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax.transAxes, size=14)
    #plot+info
    if plot_grids:
        plt.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree(),cmap=cbar_color)

    if add_source_region:
        
        for pixel in return_region_pixel_array(region_name = 'upper_left'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)

        #right
        for pixel in return_region_pixel_array(region_name = 'bodele'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)

        for pixel in return_region_pixel_array(region_name = 'upper_right'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)
        
        for pixel in return_region_pixel_array(region_name = 'upper_right_corner'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)

    if add_bodele_source_exclusive:
            for pixel in return_region_pixel_array(region_name = 'bodele'):
                add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=add_bodele_source_exclusive_alpha, lw=.2, linestyle='solid', fill=False)

    if plot_grids:
        quadmesh = ax.pcolormesh(lons, lats, data, transform=ccrs.PlateCarree(),cmap=cbar_color)
        quadmesh.set_clim(vmin=cbar_min, vmax=cbar_max * unit)
    else:
        plt.contourf(lons, lats, data, transform=ccrs.PlateCarree(),cmap=cbar_color)
    plt.title(f'{title}{date}', size=14, pad=15, weight='bold')
    plt.xlabel('Latitude')
    #colorbar
    if plot_grids:
        cb = plt.colorbar(quadmesh, orientation="vertical", pad=0.02, aspect=16, shrink=shrink)
    else:
        cb = plt.colorbar(ax=ax, orientation="vertical", pad=0.02, aspect=16, shrink=shrink)
    cb.set_label(data_value,size=14,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=12)
    cb.ax.yaxis.offsetText.set_fontsize(12)
    plt.show()

#for subplots with >1 col
def plot_merra_data2(data, lons, lats, titles='', date='', data_values='', extent=[-150, 150, -90, 90],
                    borders = False, bodele = False, plot_grids = False, add_source_region = False,
                    add_bodele_source_exclusive = False, add_bodele_source_exclusive_alpha = 1, source_region_alpha = 1, source_region_lw = 0.2, source_region_fill = False,
                    cbar_color = 'YlOrRd', cbar_min = 0, cbar_max = 7, unit = 1, figsize = (16,8),
                    rows = 1, columns = 1, shrink=1, labelsize=12, lat_space = -0.07, unit_text='l'):
    #size, extent and cartopy projection
    # fig = plt.figure(figsize=(16,8))
    # ax = plt.axes(projection=ccrs.PlateCarree())
    # ax.set_extent(extent, crs=ccrs.PlateCarree())

    fig, axes = plt.subplots(rows,columns, figsize=figsize, subplot_kw={"projection": ccrs.PlateCarree()})

    qaudmesh = dict()
    cb = dict()
    contourf = dict()

    for i in range(len(data)):

        axes[i].set_extent(extent, crs=ccrs.PlateCarree())

        #draw bodélé depression?
        if bodele:
            #bodélé coords: 16°05'-17°38'N/15°50'-18°50'E
            #source: https://web.archive.org/web/20120924181446/http://ramsar.wetlands.org/Portals/15/CHAD.pdf
            axes[i].add_patch(Rectangle((15.5,16.05), (18.05-15.5), (17.38-16.05),edgecolor = 'black',fill=False,lw=2, linestyle='--'))

        #additional geographical information
        axes[i].coastlines(resolution="50m",linewidth=1)
        if(borders):
            axes[i].add_feature(cf.BORDERS)
        #gridlines
        gl = axes[i].gridlines(linestyle='--',color='black', draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 12}
        gl.ylabel_style = {'size': 12}
        #axis labeling
        axes[i].text(-0.06, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[i].transAxes, size=14)
        axes[i].text(0.5, lat_space, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=axes[i].transAxes, size=14)
        #plot+info

        if add_source_region:
        
            for pixel in return_region_pixel_array(region_name = 'upper_left'):
                add_pixel2(axes[i],lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)

            #right
            for pixel in return_region_pixel_array(region_name = 'bodele'):
                add_pixel2(axes[i],lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)

            for pixel in return_region_pixel_array(region_name = 'upper_right'):
                add_pixel2(axes[i],lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)
            
            for pixel in return_region_pixel_array(region_name = 'upper_right_corner'):
                add_pixel2(axes[i],lons[pixel[1]], lats[pixel[0]], alpha=source_region_alpha, lw=source_region_lw, linestyle='solid', fill=source_region_fill)

        if add_bodele_source_exclusive:
                for pixel in return_region_pixel_array(region_name = 'bodele'):
                    add_pixel2(axes[i],lons[pixel[1]], lats[pixel[0]], alpha=add_bodele_source_exclusive_alpha, lw=.2, linestyle='solid', fill=False)

        if plot_grids:
            qaudmesh[i] = axes[i].pcolormesh(lons, lats, data[i], transform=ccrs.PlateCarree(),cmap=cbar_color[i])
            qaudmesh[i].set_clim(vmin=cbar_min[i], vmax=cbar_max[i] * unit[i])
        else:
            contourf[i] = axes[i].contourf(lons, lats, data[i], transform=ccrs.PlateCarree(),cmap=cbar_color[i])
        # plt.title(f'{title}{date}', size=14, pad=15, weight='bold')
        axes[i].set_title(f'{titles[i]}{date[i]}', size=14, pad=15, weight='bold')
        plt.xlabel('Latitude')

        #colorbar
        if plot_grids:
            cb[i] = fig.colorbar(qaudmesh[i], orientation="vertical", pad=0.02, aspect=16, shrink=shrink, ax=axes[i])
        else:
            cb[i] = fig.colorbar(contourf[i], orientation="vertical", pad=0.02, aspect=16, shrink=shrink, ax=axes[i])
        cb[i].set_label(data_values[i],size=labelsize,rotation=90,labelpad=15)
        cb[i].ax.tick_params(labelsize=12)
        cb[i].ax.yaxis.offsetText.set_fontsize(12)

        plt.subplots_adjust(wspace=0.08)



def plot_grid(lats, lons, title='', extent=[-150, 150, -90, 90], borders = False, add_source_region = False,
              plot_lines = True, plot_grid_lines = True, add_countries = False, country_list = '', color_list = '', country_alpha = 1, country_names = ''):

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
        
        #upper left:
        for pixel in return_region_pixel_array(region_name = 'upper_left'):
            # print('pixel1: ' , pixel[1] , 'actual lon: ' , lons[pixel[1]])
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=1,fill=True)
        #bodele:
        for pixel in return_region_pixel_array(region_name = 'bodele'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=1)
        #upper right:
        for pixel in return_region_pixel_array(region_name = 'upper_right'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=1)
        #upper right corner:
        for pixel in return_region_pixel_array(region_name = 'upper_right_corner'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=1)

    if add_countries:
        for idx,country in enumerate(country_list):
            #draw them afterwards
            if (country == 'benin' or country == 'gambia'):
                continue
            else:
                for pixel in return_region_pixel_array(region_name = country):
                    add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color=color_list[idx])
        for pixel in return_region_pixel_array(region_name = 'benin'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color='black')
        for pixel in return_region_pixel_array(region_name = 'gambia'):
            add_pixel2(ax,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color='deepskyblue')

    if plot_lines:

        for lat in lats:
            ax.hlines(y=lat+.25, xmin = -30, xmax = 35, linewidth=.5, color='r')
        
        for lon in lons:
            ax.vlines(x=lon+.25, ymin =-15, ymax = 30, linewidth=.5, color='r')
    
    #additional geographical information
    ax.coastlines(resolution="50m",linewidth=1)
    if(borders):
        ax.add_feature(cf.BORDERS)
    #gridlines

    if plot_grid_lines:
        gl = ax.gridlines(linestyle='--',color='black', draw_labels=True)
    else:
        gl = ax.gridlines(linestyle='--',color='black', draw_labels=True, alpha=0)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    #axis labeling
    ax.text(-0.06, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax.transAxes, size=14)
    ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax.transAxes, size=14)

    handles = [
        Patch(facecolor=color, label=label) 
        for label, color in zip(country_names, color_list)
    ]

    ax.legend(handles=handles)

    #plot+info
    #plt.contourf(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')
    plt.title(f'{title}', size=14, pad=15, weight='bold')
    plt.xlabel('Latitude')
    plt.show()

def plot_grid2(lats, lons, title='', extent=[-150, 150, -90, 90], figsize = (32,16), rows = 1, columns = 2, first=[True, False],
              borders = False, add_source_region = False, latspace = [-0.07,-0.07],
              plot_lines = True, plot_grid_lines = True, add_countries = False, country_list = '', color_list = '', country_alpha = 1, country_names = ''):

    fig, (ax1,ax2) = plt.subplots(rows,columns, figsize=figsize, subplot_kw={"projection": ccrs.PlateCarree()})

    ax1 = plt.subplot(1,2,1, projection=ccrs.PlateCarree())
    ax1.set_extent(extent, crs=ccrs.PlateCarree())

    if add_source_region[0]:
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
        
        #upper left:
        for pixel in return_region_pixel_array(region_name = 'upper_left'):
            # print('pixel1: ' , pixel[1] , 'actual lon: ' , lons[pixel[1]])
            add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=1,fill=True)
        #bodele:
        for pixel in return_region_pixel_array(region_name = 'bodele'):
            add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=1)
        #upper right:
        for pixel in return_region_pixel_array(region_name = 'upper_right'):
            add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=1)
        #upper right corner:
        for pixel in return_region_pixel_array(region_name = 'upper_right_corner'):
            add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=1)

    if add_countries[0]:
        for idx,country in enumerate(country_list):
            #draw them afterwards
            if (country == 'benin' or country == 'gambia'):
                continue
            else:
                for pixel in return_region_pixel_array(region_name = country):
                    add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color=color_list[idx])
        for pixel in return_region_pixel_array(region_name = 'benin'):
            add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color='black')
        for pixel in return_region_pixel_array(region_name = 'gambia'):
            add_pixel2(ax1,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color='deepskyblue')

    if plot_lines[0]:

        for lat in lats:
            ax1.hlines(y=lat+.25, xmin = -30, xmax = 35, linewidth=.5, color='r')
        
        for lon in lons:
            ax1.vlines(x=lon+.25, ymin =-15, ymax = 30, linewidth=.5, color='r')
    
    #additional geographical information
    ax1.coastlines(resolution="50m",linewidth=1)
    if(borders):
        ax1.add_feature(cf.BORDERS)
    #gridlines

    if plot_grid_lines[0]:
        gl = ax1.gridlines(linestyle='--',color='black', draw_labels=True)
    else:
        gl = ax1.gridlines(linestyle='--',color='black', draw_labels=True, alpha=0)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    #axis labeling
    ax1.text(-0.06, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax1.transAxes, size=14)
    ax1.text(0.5, latspace[0], 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax1.transAxes, size=14)

    

    #plot+info
    #plt.contourf(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')
    ax1.set_title(f'{title[0]}', size=14, pad=15, weight='bold')   
    plt.xlabel('Latitude')

    ax2 = plt.subplot(1,2,2, projection=ccrs.PlateCarree())
    ax2.set_extent(extent, crs=ccrs.PlateCarree())

    if add_source_region[1]:
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
        
        #upper left:
        for pixel in return_region_pixel_array(region_name = 'upper_left'):
            # print('pixel1: ' , pixel[1] , 'actual lon: ' , lons[pixel[1]])
            add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=1,fill=True)
        #bodele:
        for pixel in return_region_pixel_array(region_name = 'bodele'):
            add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=1)
        #upper right:
        for pixel in return_region_pixel_array(region_name = 'upper_right'):
            add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=1)
        #upper right corner:
        for pixel in return_region_pixel_array(region_name = 'upper_right_corner'):
            add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=1)

    if add_countries[1]:
        for idx,country in enumerate(country_list):
            #draw them afterwards
            if (country == 'benin' or country == 'gambia'):
                continue
            else:
                for pixel in return_region_pixel_array(region_name = country):
                    add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color=color_list[idx])
        for pixel in return_region_pixel_array(region_name = 'benin'):
            add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color='black')
        for pixel in return_region_pixel_array(region_name = 'gambia'):
            add_pixel2(ax2,lons[pixel[1]], lats[pixel[0]], alpha=country_alpha, color='deepskyblue')

    if plot_lines[1]:

        for lat in lats:
            ax2.hlines(y=lat+.25, xmin = -30, xmax = 35, linewidth=.5, color='r')
        
        for lon in lons:
            ax2.vlines(x=lon+.25, ymin =-15, ymax = 30, linewidth=.5, color='r')
    
    #additional geographical information
    ax2.coastlines(resolution="50m",linewidth=1)
    if(borders):
        ax2.add_feature(cf.BORDERS)
    #gridlines

    if plot_grid_lines[1]:
        gl = ax2.gridlines(linestyle='--',color='black', draw_labels=True)
    else:
        gl = ax2.gridlines(linestyle='--',color='black', draw_labels=True, alpha=0)
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    #axis labeling
    ax2.text(-0.06, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax2.transAxes, size=14)
    ax2.text(0.5, latspace[1], 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax2.transAxes, size=14)

    ax2.set_title(f'{title[1]}', size=14, pad=15, weight='bold')

    handles = [
        Patch(facecolor=color, label=label) 
        for label, color in zip(country_names, color_list)
    ]

    ax2.legend(handles=handles, prop={'size': 12})
    plt.show()

def barplot(data, columns, titles = '', xlabels='', ylabels='', bar_colors = ['#76d7c3', '#f0b27a', '#84929e', '#f7dc6f', '#85c1e9'], figsize = (16,9)):
  fig, ax = plt.subplots(1, ncols=columns, figsize = figsize)

  baro = dict()
  # plt.figure(dpi=1200)

  # Save the chart so we can loop through the bars below.

  for idx in range(len(data)):

    baro[idx] = ax[idx].bar(
        x=np.arange(data[idx].size),
        height=data[idx]['value'],
        tick_label=data[idx].index, 
        color = bar_colors
    )

    # Axis formatting.
    ax[idx].spines['top'].set_visible(False)
    ax[idx].spines['right'].set_visible(False)
    ax[idx].spines['left'].set_visible(False)
    ax[idx].spines['bottom'].set_color('#DDDDDD')
    ax[idx].tick_params(bottom=False, left=False)
    ax[idx].set_axisbelow(True)
    ax[idx].yaxis.grid(True, color='#EEEEEE')
    ax[idx].xaxis.grid(False)

    # Add text annotations to the top of the bars.
    # bar_color = bar_colors[idx]
    for bar_idx, bar in enumerate(baro[idx]):
      ax[idx].text(
          bar.get_x() + bar.get_width() / 2,
          bar.get_height() + 0.3,
          str(round(bar.get_height(), 1))+'%',
          horizontalalignment='center',
          color=bar_colors[bar_idx],
          weight='bold'
      )

    ax[idx].set_ylim([0,100])

    # Add labels and a title.
    if(idx is 0):
      ax[idx].set_ylabel(ylabels[idx], labelpad=15, color='#333333', fontsize=10, weight='bold')
    # ax[idx].set_xlabel(xlabels[idx], labelpad=15, color='#333333')
    ax[idx].set_title(titles[idx], pad=15, color='#333333',
                weight='bold')

  fig.tight_layout()


def plot_outcome_data(pwt_data, mpd_data, wbdi_data,
                      xlim = [1980, 2020], xticks = [1980,1990,2000,2010,2020],
                      xlabel = 'Year', ylabel = 'Log differences (GDP)', title = '', figsize = (16,8)):

    pwt_data[pwt_data.select_dtypes(include=['float64']).columns]*=100
    mpd_data[mpd_data.select_dtypes(include=['float64']).columns]*=100
    wbdi_data[wbdi_data.select_dtypes(include=['float64']).columns]*=100

    fig, ax = plt.subplots(nrows=3, ncols=4, figsize=figsize,gridspec_kw={'wspace':0.3,'hspace':0.5})
    #index variable for countries in loop
    idx = 0
    for row in ax:
        for col in row:
            #plotting variables
            col.plot(list(range(1980,2017)), pwt_data.loc[pwt_data['country'] == pwt_data['country'][idx]].values[0][2:], color = "black", linewidth=1.5, linestyle = 'solid')
            col.plot(list(range(1980,2017)), mpd_data.loc[mpd_data['country'] == mpd_data['country'][idx]].values[0][2:-1], color = "lightseagreen", linewidth=1.5, linestyle = 'dashdot')
            col.plot(list(range(1980,2017)), wbdi_data.loc[wbdi_data['country'] == wbdi_data['country'][idx]].values[0][2:-1], color = "violet", linewidth=1.5, linestyle = 'dashed')

            min_value = math.floor(min([pwt_data.loc[pwt_data['country'] == pwt_data['country'][idx]].values[0][2:].min(),
                         mpd_data.loc[mpd_data['country'] == mpd_data['country'][idx]].values[0][2:-1].min(),
                         wbdi_data.loc[wbdi_data['country'] == wbdi_data['country'][idx]].values[0][2:-1].min()])/10)*10
            
            max_value = math.ceil(max([pwt_data.loc[pwt_data['country'] == pwt_data['country'][idx]].values[0][2:].max(),
                         mpd_data.loc[mpd_data['country'] == mpd_data['country'][idx]].values[0][2:-1].max(),
                         wbdi_data.loc[wbdi_data['country'] == wbdi_data['country'][idx]].values[0][2:-1].max()])/10)*10

            #set limits
            col.set_ylim(ymin = min_value, ymax=max_value)
            col.set_xlim(xlim)
            #set x,y ticks
            col.set_yticks([min_value,0,max_value])
            col.set_xticks(xticks)
            #set x and y axis aspect ratio
            col.set_aspect('auto')
            #set titles and labels
            col.set_title(pwt_data['country'][idx], fontsize=9)
            col.set_xlabel(xlabel, fontsize=8)
            col.set_ylabel(ylabel, fontsize=8)
            #set tick label sizes
            col.tick_params(axis='both', which='minor', labelsize=7)
            col.tick_params(axis='both', which='major', labelsize=7)
            #set grid
            col.grid(linestyle=':', linewidth='0.5')
            #remove upper and right bounding lines
            col.spines['right'].set_visible(False)
            col.spines['top'].set_visible(False)
            #increment country index
            idx += 1
            #handles, labels = ax.get_legend_handles_labels()
    #fig.legend(handles, ['PWT','WDI','MPD'], loc='upper center')
    fig.legend(['PWT','Maddison','WDI'], loc = "lower center", ncol=5 )
    # plt.title(f'{title}', size=14, pad=15, weight='bold')
    fig.suptitle(f'{title}', size=14, weight='bold')
    #plt.legend(['PWT','WDI','MPD'], loc="lower center")
    plt.show()
    

def plot_wind_vectorfield(x_winds, y_winds, lons_wind, lats_wind, fig_size = (16,8),
                          title='', date='', data_value='', extent=[-150, 150, -90, 90],
                          borders = False, bodele = False, interpolation = "None"):

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
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    ax.text(-0.06, 0.5, 'Latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax.transAxes, size=14)
    ax.text(0.5, -0.075, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, size=14)
    plt.title(f'{title}{date}', size=14, pad=15, weight='bold')
    plt.xlabel('Latitude')
    color = np.sqrt(np.power(x_winds, 2) + np.power(y_winds, 2))
    #color2 = np.arctan2(x_winds, y_winds)

    color_background = ax.imshow(color,interpolation=interpolation,extent = extent,aspect = 'auto')
    cb = plt.colorbar(color_background,pad=0.02, aspect=16, shrink=1)
    cb.set_label(data_value,size=14,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=12)
    ax.quiver(lons_wind, lats_wind, x_winds, y_winds, transform=ccrs.PlateCarree(),color='indianred', width=.0016)

    plt.show()

#for subplot with 2 cols
def plot_wind_vectorfield2(x_winds, y_winds, lons_wind, lats_wind, fig_size = (16,8),
                          title='', date='', data_value='', extent=[-150, 150, -90, 90],
                          borders = False, bodele = False, interpolation = "None", x_winds2=0, y_winds2=0, shrink=1):

    # fig = plt.figure(figsize=fig_size)
    fig, (ax, ax2) = plt.subplots(1,2, figsize=fig_size, subplot_kw={"projection": ccrs.PlateCarree()})
    # ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
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
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}
    ax.text(-0.06, 0.5, 'Latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax.transAxes, size=14)
    ax.text(0.5, -0.075, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, size=14)
    ax.set_title(f'{title[0]}{date[0]}', size=14, pad=15, weight='bold')
    plt.xlabel('Latitude')
    color = np.sqrt(np.power(x_winds, 2) + np.power(y_winds, 2))
    #color2 = np.arctan2(x_winds, y_winds)

    color_background = ax.imshow(color,interpolation=interpolation,extent = extent,aspect = 'equal')
    cb = plt.colorbar(color_background,pad=0.02, aspect=16, shrink=shrink, ax=ax)
    cb.set_label(data_value,size=14,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=12)
    ax.quiver(lons_wind, lats_wind, x_winds, y_winds, transform=ccrs.PlateCarree(),color='indianred', width=.0016)

    # ax2 = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    if bodele:
        #bodélé coords: 16°05'-17°38'N/15°50'-18°50'E
        #source: https://web.archive.org/web/20120924181446/http://ramsar.wetlands.org/Portals/15/CHAD.pdf
        ax2.add_patch(Rectangle((15.5,16.05), (18.05-15.5), (17.38-16.05),edgecolor = 'black',fill=False,lw=2, linestyle='--'))

    ax2.set_extent(extent, crs=ccrs.PlateCarree())
    ax2.coastlines(resolution="110m",linewidth=1)
    if borders:
        ax2.add_feature(cf.BORDERS)
    gl2 = ax2.gridlines(linestyle='--',color='black', draw_labels=True)
    gl2.top_labels = False
    gl2.right_labels = False
    gl2.xlabel_style = {'size': 12}
    gl2.ylabel_style = {'size': 12}
    ax2.text(-0.06, 0.5, 'Latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax2.transAxes, size=14)
    ax2.text(0.5, -0.075, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax2.transAxes, size=14)
    ax2.set_title(f'{title[1]}{date[1]}', size=14, pad=15, weight='bold')
    plt.xlabel('Latitude')
    color2 = np.sqrt(np.power(x_winds2, 2) + np.power(y_winds2, 2))
    #color2 = np.arctan2(x_winds, y_winds)

    color_background2 = ax2.imshow(color2,interpolation=interpolation,extent = extent,aspect = 'equal')
    cb2 = plt.colorbar(color_background2,pad=0.02, aspect=16, shrink=shrink, ax=ax2)
    cb2.set_label(data_value,size=14,rotation=90,labelpad=15)
    cb2.ax.tick_params(labelsize=12)
    ax2.quiver(lons_wind, lats_wind, x_winds2, y_winds2, transform=ccrs.PlateCarree(),color='indianred', width=.0016)

    plt.subplots_adjust(wspace=0.08)

    plt.show()

def plot_gpw_data(population_array, lats, lons, extent=[-30,29,-15,29], borders = True, cbar_min = 0, cbar_max = 1000000, unit = 1,
                  population_data =[], title='', figsize = (16,8), shrink=1, labelsize=12, lat_space = -0.07, cmap = cmocean.tools.lighten(cmo.matter, 0.85)):

    fig, axes = plt.subplots(1,2, figsize=figsize, subplot_kw={"projection": ccrs.PlateCarree()})

    axes[0].set_extent(extent, crs=ccrs.PlateCarree())
    gl1 = axes[0].gridlines(linestyle='--',color='black', draw_labels=True)
    gl1.top_labels = False
    gl1.right_labels = False
    gl1.xlabel_style = {'size': 12}
    gl1.ylabel_style = {'size': 12}

    axes[0].coastlines(resolution="50m",linewidth=1)
    if borders:
        axes[0].add_feature(cf.BORDERS)
    #axis labeling
    axes[0].text(-0.06, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[0].transAxes, size=14)
    axes[0].text(0.5, lat_space, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=axes[0].transAxes, size=14)
    axes[0].set_title('GPW Data Centroids for Selected Countries', size=14, pad=15, weight='bold')  
        
    for pop_file in population_data:
        for idx, x_coord in enumerate(pop_file['CENTROID_X']):
            axes[0].add_patch(plt.Circle((x_coord, pop_file['CENTROID_Y'][idx]), .1, color='indianred', alpha = 0.5))
        
    axes[1].set_extent(extent, crs=ccrs.PlateCarree())
    gl2 = axes[1].gridlines(linestyle='--',color='black', draw_labels=True)
    gl2.top_labels = False
    gl2.right_labels = False
    gl2.xlabel_style = {'size': 12}
    gl2.ylabel_style = {'size': 12}

    axes[1].coastlines(resolution="50m",linewidth=1)
    if borders:
        axes[1].add_feature(cf.BORDERS)
    #axis labeling
    axes[1].text(-0.06, 0.5, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[1].transAxes, size=14)
    axes[1].text(0.5, lat_space, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=axes[1].transAxes, size=14)
    axes[1].set_title('GPW Data Mapped to MERRA-2 Grid', size=14, pad=15, weight='bold')   

    quadmesh2 = axes[1].pcolormesh(lons, lats, population_array, transform=ccrs.PlateCarree(),cmap=cmap)
    quadmesh2.set_clim(vmin=cbar_min, vmax=cbar_max * unit)

    

    cb = fig.colorbar(quadmesh2, orientation="vertical", pad=0.02, aspect=16, shrink=shrink, ax=axes.ravel().tolist())
    cb.set_label('$\\it{Population\ in\ Millions}$',size=labelsize,rotation=90,labelpad=15)
    cb.ax.set_yticklabels(['no data', '0.2', '0.4', '0.6', '0.8',r'$\geq 1$']) 
    cb.ax.tick_params(labelsize=12)
    #plt.title(f'{title}', size=14, pad=15, weight='bold') 


def plot_ols_data(real_data, predicted_values, y_name= '', x_name = '', title=f'', fig_size=(16,8)):

    fig, ax = plt.subplots()

    ax.plot(range(real_data.shape[0]), real_data.iloc[: ,0],"--", label="Real Values")
    ax.plot(range(real_data.shape[0]), predicted_values,"--", label="OLS Predicted Values")
    fig.set_size_inches(fig_size)

    # ax.plot(x1, aod_reg_predictions, "o", label="Data")
    # ax.plot(x1, y_true, "b-", label="True")
    # ax.plot(np.hstack((x1, x1n)), np.hstack((ypred, ynewpred)), "r", label="OLS prediction")
    ax.legend(loc="best")
    ax.text(-0.03, 0.55, y_name, va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=ax.transAxes, size=14)
    ax.text(0.5, -0.1, x_name, va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=ax.transAxes, size=14)
    #plot+info
    #plt.contourf(lons, lats, data, transform=ccrs.PlateCarree(),cmap='YlOrRd')
    plt.title(title, size=14, pad=15, weight='bold')


"--------------------------------------------------------------------"
'Animation Functions'
"--------------------------------------------------------------------"



def simulation_comparison_animation(simulation_data_array, real_data_array, lats, lons, extent=[-30,29,-15,29],
                                    add_source_region = False, borders = True, cbar_min = 0, cbar_max = 7,
                                    unit = 1, min_time = 0, max_frames = 1, fpers = 10, save_as = "anim_0_1.mp4", title=''):

    from matplotlib import animation
    from matplotlib.animation import FuncAnimation, PillowWriter

    fig, axes = plt.subplots(1,2, figsize=(25,11), subplot_kw={"projection": ccrs.PlateCarree()})

    axes[0].set_extent(extent, crs=ccrs.PlateCarree())
    gl1 = axes[0].gridlines(linestyle='--',color='black', draw_labels=True)
    gl1.top_labels = False
    gl1.right_labels = False
    gl1.xlabel_style = {'size': 12}
    gl1.ylabel_style = {'size': 12}

    axes[0].coastlines(resolution="50m",linewidth=1)
    if borders:
        axes[0].add_feature(cf.BORDERS)
    #axis labeling
    axes[0].text(-0.06, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[0].transAxes, size=14)
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
    axes[1].text(-0.06, 0.55, 'Latitude', va='bottom', ha='center', rotation='vertical', rotation_mode='anchor', transform=axes[1].transAxes, size=14)
    axes[1].text(0.5, -0.11, 'Longitude', va='bottom', ha='center', rotation='horizontal', rotation_mode='anchor', transform=axes[1].transAxes, size=14)
    axes[1].title.set_text('Real Dust Movement')   

    quadmesh2 = axes[1].pcolormesh(lons, lats, real_data_array[0], transform=ccrs.PlateCarree(),cmap='YlOrRd',shading='flat')
    quadmesh2.set_clim(vmin=cbar_min, vmax=cbar_max * unit)

    cb = fig.colorbar(quadmesh2, orientation="vertical", pad=0.02, aspect=12, shrink=0.65, ax=axes.ravel().tolist())
    cb.set_label('dust surface mass concentration-PM 2.5 \n \n kg/m^3',size=12,rotation=90,labelpad=15)
    cb.ax.tick_params(labelsize=12)
    plt.title(title, size=14, pad=15, weight='bold')
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

    anim = animation.FuncAnimation(fig, animate, frames=max_frames, interval=20, blit=True)
    anim.save(save_as, dpi=100, writer=animation.FFMpegWriter(fps=fpers))



"--------------------------------------------------------------------"
'Advection Diffusion Simulation Functions'
"--------------------------------------------------------------------"



@jit
def build_source_array(input_array, longitudes, latitudes):
    #ToDO:
    #modify so it uses return_region_pixel_array

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
    #ToDO:
    #modify so it uses return_region_pixel_array
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


#to be deleted?
@jit
def advection_diffusion_fd_old(num_time_steps, num_x_steps, num_y_steps, min_time, max_time,
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


from functions import build_source_array,fill_with_source

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
    # ywind_mtpl = np.float(0.06475115562615506)
    # xwind_mtpl = np.float(0.05512547429607979)

    # slow
    ywind_mtpl = np.float32(0.03237557781307753)
    xwind_mtpl = np.float32(0.027562737148039897)

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

                #taking 1800 for half hour as we are using half hour time steps
                xwind_mtpl = np.float32(1800/(distance2(source_input_latitudes[j], source_input_longitudes[i], source_input_latitudes[j], source_input_longitudes[i+1])*1000))

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
    
    #upper left source
    if (region_name == 'upper_left'):
        upper_left_source_pixels = np.array([[67,43],
                                             [68,43],[68,44],
                                             [69,42],[69,43],[69,44],[69,45],
                                             [70,43],[70,44],[70,45],[70,46],
                                             [71,43],[71,44],[71,45],[71,46],[71,47],
                                             [72,47],[72,48],
                                             [73,47],[73,48],[73,49],
                                             [74,48],[74,49],
                                             [75,49],[75,50],
                                             [76,48],[76,49],[76,50],
                                             [77,47],[77,48],[77,49]], dtype = 'int')
        return upper_left_source_pixels

    #upper right source
    if (region_name == 'upper_right'):
        upper_right_source_pixels = np.array([[81,82],[81,83],[81,84],
                                              [82,82],[82,83],[82,84]], dtype = 'int')
        return upper_right_source_pixels

    #upper right corner source
    if (region_name == 'upper_right_corner'):
        upper_right_corner_source_pixels = np.array([[86,87],[86,88],[86,89],[86,91],
                                                     [87,87],[87,88],[87,89],[87,90],[87,91]], dtype = 'int')
        return upper_right_corner_source_pixels
    
    # bodele region:
    if (region_name == 'bodele'):
        bodele_depression_pixels = np.array([[60,71],[60,72],[60,77],[60,78],[60,79],
                                            [61,69],[61,70],[61,71],[61,72],[61,73],[61,74],[61,75],[61,76],[61,77],[61,78],[61,79],[61,80],
                                            [62,69],[62,70],[62,71],[62,72],[62,73],[62,74],[62,75],[62,76],[62,77],[62,78],[62,79],[62,80],
                                            [63,67],[63,68],[63,69],[63,70],[63,71],[63,72],[63,73],[63,74],[63,75],[63,76],[63,77],[63,78],[63,79],[63,80],
                                            [64,66],[64,67],[64,68],[64,69],[64,70],[64,71],[64,72],[64,73],[64,74],[64,75],[64,76],[64,77],[64,78],[64,79],[64,80],[64,67],
                                            [65,67],[65,68],[65,69],[65,70],[65,71],[65,72],[65,73],[65,74],[65,75],[65,76],[65,77],[65,78],[65,79],[65,80],
                                            [66,68],[66,69],[66,70],[66,71],[66,72],[66,73],[66,74],[66,75],[66,76],[66,77],[66,78],[66,79],[66,80],
                                            [67,68],[67,69],[67,70],[67,71],[67,72],[67,73],[67,74],[67,75],[67,76],[67,77],
                                            [68,68],[68,69],[68,70],[68,71],[68,72],[68,73],
                                            [69,71],[69,72],[69,73]], dtype = 'int')
        return bodele_depression_pixels

    # togo coastline spot:
    elif (region_name == 'togo_coast'):
        togo_coast_pixel = np.array([[43,50]], dtype = 'int')
        return togo_coast_pixel

    # countries:

    # Benin:
    elif (region_name == 'benin'):
        benin_pixels = np.array([[43,51],[43,52],
                                 [44,51],[44,52],
                                 [45,51],[45,52],
                                 [46,51],[46,52],
                                 [47,51],[47,52],
                                 [48,51],[48,52],
                                 [49,50],[49,51],[49,52],[49,53],
                                 [50,50],[50,51],[50,52],[50,53],
                                 [51,49],[51,50],[51,51],[51,52],[51,53],[51,54],
                                 [52,50],[52,51],[52,52],[52,53],[52,54],
                                 [53,51],[53,52],[53,53],
                                 [54,52],[54,53]], dtype = 'int')
        return benin_pixels

    # Burkina Faso:
    elif (region_name == 'burkina_faso'):
        burkina_faso_pixels = np.array([[49,43],
                                        [50,40],[50,41],[50,42],[50,43],
                                        [51,39],[51,40],[51,41],[51,42],[51,43],
                                        [52,39],[52,40],[52,41],[52,42],[52,43],[52,44],[52,45],[52,46],[52,47],[52,48],[52,49],
                                        [53,40],[53,41],[53,42],[53,43],[53,44],[53,45],[53,46],[53,47],[53,48],[53,49],[53,50],[53,51],
                                        [54,40],[54,41],[54,42],[54,43],[54,44],[54,45],[54,46],[54,47],[54,48],[54,49],[54,50],[54,51],
                                        [55,41],[55,42],[55,43],[55,44],[55,45],[55,46],[55,47],[55,48],[55,49],[55,50],[55,51],
                                        [56,41],[56,42],[56,43],[56,44],[56,45],[56,46],[56,47],[56,48],[56,49],[56,50],
                                        [57,42],[57,43],[57,44],[57,45],[57,46],[57,47],[57,48],[57,49],[57,50],
                                        [58,44],[58,45],[58,46],[58,47],[58,48],[58,49],
                                        [59,45],[59,46],[59,47],[59,48],
                                        [60,47]], dtype = 'int')
        return burkina_faso_pixels

    # Gambia:
    elif (region_name == 'gambia'):
        gambia_pixels = np.array([[56,21],[56,22],[56,23],
                                  [57,21],[57,22],[57,23],[57,24],[57,25],[57,26]], dtype = 'int')
        return gambia_pixels

    # Ghana
    elif (region_name == 'ghana'):
        ghana_pixels = np.array([[40,44],[40,45],[40,46],
                                 [41,44],[41,45],[41,46],[41,47],[41,48],
                                 [42,44],[42,45],[42,46],[42,47],[42,48],[42,49],[42,50],
                                 [43,43],[43,44],[43,45],[43,46],[43,47],[43,48],[43,49],
                                 [44,43],[44,44],[44,45],[44,46],[44,47],[44,48],[44,49],
                                 [45,44],[45,45],[45,46],[45,47],[45,48],[45,49],
                                 [46,44],[46,45],[46,46],[46,47],[46,48],[46,49],
                                 [47,44],[47,45],[47,46],[47,47],[47,48],[47,49],
                                 [48,44],[48,45],[48,46],[48,47],[48,48],[48,49],
                                 [49,44],[49,45],[49,46],[49,47],[49,48],[49,48],
                                 [50,44],[50,45],[50,46],[50,47],[50,48],
                                 [51,43],[51,44],[51,45],[51,46],[51,47],[51,48],
                                 [52,44],[52,45],[52,46],[52,47],[52,48]], dtype = 'int')
        return ghana_pixels

    # Guinea:
    elif (region_name == 'guinea'):
        guinea_pixels = np.array([[45,33],[45,34],[45,35],
                                  [46,33],[46,34],[46,35],
                                  [47,32],[47,31],[47,33],[47,34],[47,35],
                                  [48,27],[48,31],[48,32],[48,33],[48,34],[48,35],
                                  [49,26],[49,27],[49,28],[49,31],[49,32],[49,33],[49,34],[49,35],[48,35],
                                  [50,25],[50,26],[50,27],[50,28],[50,29],[50,30],[50,31],[50,32],[50,33],[50,34],[50,35],
                                  [51,25],[51,26],[51,27],[51,28],[51,29],[51,30],[51,31],[51,32],[51,33],[51,34],[51,35],
                                  [52,24],[52,25],[52,26],[52,27],[52,28],[52,29],[52,30],[52,31],[52,32],[52,33],[52,34],
                                  [53,25],[53,26],[53,27],[53,28],[53,29],[53,30],[53,31],[53,32],[53,33],[53,34],
                                  [54,26],[54,27],[54,28],[54,29],[54,30],[54,31],[54,32],[54,33],[54,34],
                                  [55,26],[55,27],[55,28]], dtype = 'int')
        return guinea_pixels

    # Liberia:
    elif (region_name == 'liberia'):
        liberia_pixels = np.array([[39,35],[39,36],
                                   [40,33],[40,34],[40,35],[40,36],
                                   [41,33],[41,34],[41,35],[41,36],
                                   [42,32],[42,33],[42,34],[42,35],
                                   [43,30],[43,31],[43,32],[43,33],[43,34],
                                   [44,30],[44,31],[44,32],[44,33],[44,34],[44,35],
                                   [45,30],[45,31],[45,32],[45,33],[45,34],
                                   [46,31],[46,32],[46,33],
                                   [47,32],[47,33]], dtype = 'int')
        return liberia_pixels

    # Mali:
    elif (region_name == 'mali'):
        mali_pixels = np.array([[51,35],[51,36],[51,37],[51,38],[51,39],
                                [52,34],[52,35],[52,36],[52,37],[52,38],[52,39],
                                [53,34],[53,35],[53,36],[53,37],[53,38],[53,39],
                                [54,31],[54,32],[54,34],[54,35],[54,36],[54,37],[54,38],[54,39],[54,40],[54,41],
                                [55,30],[55,31],[55,32],[55,33],[55,34],[55,35],[55,36],[55,37],[55,38],[55,39],[55,40],[55,41],
                                [56,30],[56,31],[56,32],[56,33],[56,34],[56,35],[56,36],[56,37],[56,38],[56,39],[56,40],[56,41],
                                [57,29],[57,30],[57,31],[57,32],[57,33],[57,34],[57,35],[57,36],[57,37],[57,38],[57,39],[57,40],[57,41],[57,42],[57,43],
                                [58,29],[58,30],[58,31],[58,32],[58,33],[58,34],[58,35],[58,36],[58,37],[58,38],[58,39],[58,40],[58,41],[58,42],[58,43],
                                [59,29],[59,30],[59,31],[59,32],[59,33],[59,34],[59,35],[59,36],[59,37],[59,38],[59,39],[59,40],[59,41],[59,42],[59,43],[59,44],[59,45],
                                [60,29],[60,29],[60,30],[60,31],[60,32],[60,33],[60,34],[60,35],[60,36],[60,37],[60,38],[60,39],[60,40],[60,41],[60,42],[60,43],[60,44],[60,45],[60,46],[60,47],[60,48],[60,49],
                                [61,30],[61,31],[61,32],[61,33],[61,34],[61,35],[61,36],[61,37],[61,38],[61,39],[61,40],[61,41],[61,42],[61,43],[61,44],[61,45],[61,46],[61,47],[61,48],[61,49],[61,50],[61,51],[61,52],[61,53],[61,54],
                                [62,40],[62,41],[62,42],[62,43],[62,44],[62,45],[62,46],[62,47],[62,48],[62,49],[62,50],[62,51],[62,52],[62,53],[62,54],
                                [63,40],[63,41],[63,42],[63,43],[63,44],[63,45],[63,46],[63,47],[63,48],[63,49],[63,50],[63,51],[63,52],[63,53],[63,54],
                                [64,39],[64,40],[64,41],[64,42],[64,43],[64,44],[64,45],[64,46],[64,47],[64,48],[64,49],[64,50],[64,51],[64,52],[64,53],[64,54],[64,55],
                                [65,39],[65,40],[65,41],[65,42],[65,43],[65,44],[65,45],[65,46],[65,47],[65,48],[65,49],[65,50],[65,51],[65,52],[65,53],[65,54],[65,55],
                                [66,39],[66,40],[66,41],[66,42],[66,43],[66,44],[66,45],[66,46],[66,47],[66,48],[66,49],[66,50],[66,51],[66,52],[66,53],[66,54],[66,55],
                                [67,39],[67,40],[67,41],[67,42],[67,43],[67,44],[67,45],[67,46],[67,47],[67,48],[67,49],[67,50],[67,51],[67,52],[67,53],[67,54],[67,55],
                                [68,39],[68,40],[68,41],[68,42],[68,43],[68,44],[68,45],[68,46],[68,47],[68,48],[68,49],[68,50],[68,51],[68,52],[68,53],[68,54],[68,55],
                                [69,39],[69,40],[69,41],[69,42],[69,43],[69,44],[69,45],[69,46],[69,47],[69,48],[69,49],[69,50],[69,51],[69,52],[69,53],
                                [70,39],[70,40],[70,41],[70,42],[70,43],[70,44],[70,45],[70,46],[70,47],[70,48],[70,49],[70,50],[70,51],[70,52],[70,53],
                                [71,39],[71,40],[71,41],[71,42],[71,43],[71,44],[71,45],[71,46],[71,47],[71,48],[71,49],[71,50],
                                [72,38],[72,39],[72,40],[72,41],[72,42],[72,43],[72,44],[72,45],[72,46],[72,47],[72,48],[72,49],[72,50],
                                [73,38],[73,39],[73,40],[73,41],[73,42],[73,43],[73,44],[73,45],[73,46],[73,47],[73,48],[73,49],
                                [74,38],[74,39],[74,40],[74,41],[74,42],[74,43],[74,44],[74,45],[74,46],[74,47],[74,48],
                                [75,38],[75,39],[75,40],[75,41],[75,42],[75,43],[75,44],[75,45],[75,46],
                                [76,38],[76,39],[76,40],[76,41],[76,42],[76,43],[76,44],[76,45],
                                [77,38],[77,39],[77,40],[77,41],[77,42],[77,43],[77,44],
                                [78,38],[78,39],[78,40],[78,41],[78,42],[78,43],
                                [79,38],[79,39],[79,40],[79,41],
                                [80,38],[80,39],[80,40],], dtype = 'int')
        return mali_pixels

    # Niger:
    elif (region_name == 'niger'):
        niger_pixels = np.array([[54,54],
                                 [55,52],[55,53],[55,54],
                                 [56,50],[56,51],[56,52],[56,53],[56,54],[56,62],[56,63],[56,64],
                                 [57,50],[57,51],[57,52],[57,53],[57,54],[57,59],[57,60],[57,61],[57,62],[57,63],[57,64],[57,65],[57,66],[57,67],[57,68],[57,69],
                                 [58,49],[58,50],[58,51],[58,52],[58,53],[58,54],[58,55],[58,56],[58,57],[58,58],[58,59],[58,60],[58,61],[58,62],[58,63],[58,64],[58,65],[58,66],[58,67],[58,68],[58,69],
                                 [59,49],[59,50],[59,51],[59,52],[59,53],[59,54],[59,55],[59,56],[59,57],[59,58],[59,59],[59,60],[59,61],[59,62],[59,63],[59,64],[59,65],[59,66],[59,67],[59,68],[59,69],
                                 [60,49],[60,50],[60,51],[60,52],[60,53],[60,54],[60,55],[60,56],[60,57],[60,58],[60,59],[60,60],[60,61],[60,62],[60,63],[60,64],[60,65],[60,66],[60,67],[60,68],[60,69],[60,70],
                                 [61,54],[61,55],[61,56],[61,57],[61,58],[61,59],[61,60],[61,61],[61,62],[61,63],[61,64],[61,65],[61,66],[61,67],[61,68],[61,69],[61,70],
                                 [62,55],[62,56],[62,57],[62,58],[62,59],[62,60],[62,61],[62,62],[62,63],[62,64],[62,65],[62,66],[62,67],[62,68],[62,69],[62,70],[62,71],
                                 [63,55],[63,56],[63,57],[63,58],[63,59],[63,60],[63,61],[63,62],[63,63],[63,64],[63,65],[63,66],[63,67],[63,68],[63,69],[63,70],[63,71],[63,72],
                                 [64,55],[64,56],[64,57],[64,58],[64,59],[64,60],[64,61],[64,62],[64,63],[64,64],[64,65],[64,66],[64,67],[64,68],[64,69],[64,70],[64,71],[64,72],
                                 [65,55],[65,56],[65,57],[65,58],[65,59],[65,60],[65,61],[65,62],[65,63],[65,64],[65,65],[65,66],[65,67],[65,68],[65,69],[65,70],[65,71],[65,72],[65,73],
                                 [66,55],[66,56],[66,57],[66,58],[66,59],[66,60],[66,61],[66,62],[66,63],[66,64],[66,65],[66,66],[66,67],[66,68],[66,69],[66,70],[66,71],[66,72],[66,73],
                                 [67,55],[67,56],[67,57],[67,58],[67,59],[67,60],[67,61],[67,62],[67,63],[67,64],[67,65],[67,66],[67,67],[67,68],[67,69],[67,70],[67,71],[67,72],[67,73],
                                 [68,55],[68,56],[68,57],[68,58],[68,59],[68,60],[68,61],[68,62],[68,63],[68,64],[68,65],[68,66],[68,67],[68,68],[68,69],[68,70],[68,71],[68,72],[68,73],
                                 [69,57],[69,58],[69,59],[69,60],[69,61],[69,62],[69,63],[69,64],[69,65],[69,66],[69,67],[69,68],[69,69],[69,70],[69,71],[69,72],[69,73],
                                 [70,59],[70,60],[70,61],[70,62],[70,63],[70,64],[70,65],[70,66],[70,67],[70,68],[70,69],[70,70],[70,71],[70,72],[70,73],
                                 [71,60],[71,61],[71,62],[71,63],[71,64],[71,65],[71,66],[71,67],[71,68],[71,69],[71,70],[71,71],[71,72],[71,73],
                                 [72,61],[72,62],[72,63],[72,64],[72,65],[72,66],[72,67],[72,68],[72,69],[72,70],[72,71],[72,72],[72,73],
                                 [73,62],[73,63],[73,64],[73,65],[73,66],[73,67],[73,68],[73,69],[73,70],[73,71],[73,72],
                                 [74,63],[74,64],[74,65],[74,66],[74,67],[74,68],[74,69],[74,70],[74,71],[74,72],
                                 [75,64],[75,65],[75,66],[75,67],[75,68],[75,69],[75,70],[75,71],[75,72],
                                 [76,66],[76,67],[76,68],[76,69],[76,70],[76,72],
                                 [77,67],[77,68]], dtype = 'int')
        return niger_pixels

    # Nigeria:
    elif (region_name == 'nigeria'):
        nigeria_pixels = np.array([[39,57],[39,58],[39,59],[39,60],[39,61],
                                   [40,57],[40,58],[40,59],[40,60],[40,61],[40,62],
                                   [41,57],[41,58],[41,59],[41,60],[41,61],[41,62],
                                   [42,56],[42,56],[42,57],[42,58],[42,59],[42,60],[42,61],[42,62],
                                   [43,52],[43,53],[43,54],[43,55],[43,56],[43,57],[43,58],[43,59],[43,60],[43,61],[43,62],[43,63],
                                   [44,53],[44,54],[44,55],[44,56],[44,57],[44,58],[44,59],[44,60],[44,61],[44,62],[44,63],[44,64],[44,65],[44,66],
                                   [45,53],[45,54],[45,55],[45,56],[45,57],[45,58],[45,59],[45,60],[45,61],[45,62],[45,63],[45,64],[45,65],[45,66],[45,67],
                                   [46,53],[46,54],[46,55],[46,56],[46,57],[46,58],[46,59],[46,60],[46,61],[46,62],[46,63],[46,64],[46,65],[46,66],[46,67],
                                   [47,53],[47,54],[47,55],[47,56],[47,57],[47,58],[47,59],[47,60],[47,61],[47,62],[47,63],[47,64],[47,65],[47,66],[47,67],[47,68],
                                   [48,53],[48,54],[48,55],[48,56],[48,57],[48,58],[48,59],[48,60],[48,61],[48,62],[48,63],[48,64],[48,65],[48,66],[48,67],[48,68],
                                   [49,53],[49,54],[49,55],[49,56],[49,57],[49,58],[49,59],[49,60],[49,61],[49,62],[49,63],[49,64],[49,65],[49,66],[49,67],[49,68],
                                   [50,54],[50,55],[50,56],[50,57],[50,58],[50,59],[50,60],[50,61],[50,62],[50,63],[50,64],[50,65],[50,66],[50,67],[50,68],[50,69],
                                   [51,54],[51,55],[51,56],[51,57],[51,58],[51,59],[51,60],[51,61],[51,62],[51,63],[51,64],[51,65],[51,66],[51,67],[51,68],[51,69],[51,70],
                                   [52,54],[52,55],[52,56],[52,57],[52,58],[52,59],[52,60],[52,61],[52,62],[52,63],[52,64],[52,65],[52,66],[52,67],[52,68],[52,69],[52,70],
                                   [53,54],[53,55],[53,56],[53,57],[53,58],[53,59],[53,60],[53,61],[53,62],[53,63],[53,64],[53,65],[53,66],[53,67],[53,68],[53,69],[53,70],[53,71],
                                   [54,54],[54,55],[54,56],[54,57],[54,58],[54,59],[54,60],[54,61],[54,62],[54,63],[54,64],[54,65],[54,66],[54,67],[54,68],[54,69],[54,70],[54,71],
                                   [55,54],[55,55],[55,56],[55,57],[55,58],[55,59],[55,60],[55,61],[55,62],[55,63],[55,64],[55,65],[55,66],[55,67],[55,68],[55,69],[55,70],
                                   [56,55],[56,56],[56,57],[56,58],[56,59],[56,60],[56,61],[56,62],[56,64],[56,65],[56,66],[56,67],[56,68],[56,69],[56,70],
                                   [57,55],[57,56],[57,57],[57,58],[57,69],[57,70]], dtype = 'int')
        return nigeria_pixels

    # Sierra Leone:
    elif (region_name == 'sierra_leone'):
        sierra_leone_pixels = np.array([[44,29],[44,30],
                                        [45,27],[45,28],[45,29],[45,30],[45,31],
                                        [46,28],[46,29],[46,30],[46,31],
                                        [47,27],[47,28],[47,29],[47,30],[47,31],
                                        [48,27],[48,28],[48,29],[48,30],[48,31],
                                        [49,28],[49,29],[49,30],[49,31],
                                        [50,29],[50,30]], dtype = 'int')
        return sierra_leone_pixels

    # Senegal:
    elif (region_name == 'senegal'):
        senegal_pixels = np.array([[55,21],[55,22],[55,23],[55,28],[55,29],
                                   [56,22],[56,23],[56,24],[56,25],[56,26],[56,27],[56,28],[56,29],
                                   [57,23],[57,26],[57,27],[57,28],[57,29],
                                   [58,22],[58,23],[58,24],[58,25],[58,26],[58,27],[58,28],[58,29],
                                   [59,20],[59,21],[59,22],[59,23],[59,24],[59,25],[59,26],[59,27],[59,28],
                                   [60,20],[60,21],[60,22],[60,23],[60,24],[60,25],[60,26],[60,27],[60,28],
                                   [61,22],[61,23],[61,24],[61,25],[61,26],[61,27],
                                   [62,22],[62,23],[62,24],[62,25],[62,26],
                                   [63,22],[63,23],[63,24],[63,25]], dtype = 'int')
        return senegal_pixels

    # Togo:
    elif (region_name == 'togo'):
        togo_pixels = np.array([[42,50],
                                [43,49],[43,50],[43,51],
                                [44,49],[44,50],[44,51],
                                [45,49],[45,50],
                                [46,49],[46,50],
                                [47,49],[47,50],
                                [48,49],[48,50],
                                [49,49],[49,50],
                                [50,49],[50,50],
                                [51,48],[51,49],
                                [52,48],[52,49]], dtype = 'int')
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
def get_time_span_region_data(data, region):
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

# @jit
# def hourly_regional_data_to_daily_mean(data):
#     daily_mean_data = np.zeros((round(data.shape[0]/24), data.shape[1]), dtype = 'float32')
#     day_counter = 0
#     daily_data = np.zeros((data.shape[1]), dtype = 'float32')

#     idx = 0

#     for hourly_data in data:
#         daily_data += hourly_data
#         if ((idx != 0) and (idx%24 == 0)):
#             daily_mean_data[day_counter] = daily_data / 24
#             daily_data = np.zeros((data.shape[1]), dtype = 'float32')
#             day_counter += 1
#         idx += 1
#     return daily_mean_data

# @jit
# def extract_hourly_jun_sep_data(data,hourly_junsep_indices_np,hourly_novapr_indices_np):

#     hourly_junsep_counter = 0
#     hourly_novapr_counter = 0
#     idx = 0

#     hourly_junsep_data = np.zeros((hourly_junsep_indices_np.shape[1], data.shape[1]), dtype = 'float32')
#     hourly_novapr_data = np.zeros((hourly_novapr_indices_np.shape[1], data.shape[1]), dtype = 'float32')
    
#     for hourly_data in data:
#         if idx in hourly_junsep_indices_np:
#             hourly_junsep_data[hourly_junsep_counter] = hourly_data
#             hourly_junsep_counter += 1 
#         elif idx in hourly_novapr_indices_np:
#             hourly_novapr_data[hourly_novapr_counter] = hourly_data
#             hourly_novapr_counter += 1
#         idx += 1
        
#     return (hourly_junsep_data, hourly_novapr_data)

@jit
def create_lag_array(data, lag_num = 10):
    lag_array = np.zeros((data.shape[0], lag_num+1))
    
    for i in range(lag_num, lag_array.shape[0]):
        for lag in range(lag_num+1):
            lag_array[i][lag] = data[i-lag]
    
    return lag_array

@jit
def create_regression_rhs(exogenous_variables, junsep_indices, novapr_indices):
    reg_rhs = np.zeros((exogenous_variables.shape[0], exogenous_variables.shape[1] + 2))
    
    idx = 0
    for row in reg_rhs:
        if idx in junsep_indices:
            row[0] = 1
        elif idx in novapr_indices:
            row[1] = 1
        idx += 1
    row_idx = 0
    for variable_row in exogenous_variables:
        idx = 0
        for variable in variable_row:
            reg_rhs[row_idx][idx+2] = variable
            idx += 1
        row_idx += 1
    return reg_rhs

def create_lag_regression_data(lag_data, lag_num, other_ex_data, y_vector, junsep_indices, novapr_indices,
                               dataframe = True, variable_names = [], y_name = ''):

    reg_array = create_lag_array(lag_data, lag_num = lag_num)

    for data in other_ex_data:
        reg_array = np.concatenate((reg_array, data), axis=1)
    reg_array = create_regression_rhs(reg_array, np.array([junsep_indices], dtype='float32'), np.array([novapr_indices], dtype='float32'))

    if dataframe:
        reg_array_df = pd.DataFrame(reg_array, columns = variable_names)
        reg_array_df.insert(0, y_name, y_vector, True)

        return reg_array_df[10:-1]
    else:
        return reg_array

def lag(x, n):
    if n == 0:
        return x
    if isinstance(x, pd.Series):
        return x.shift(n) 
    else:
        x = pd.Series(x)
        return x.shift(n) 

    x = x.copy()
    x[n:] = x[0:-n]
    x[:n] = np.nan
    return x

def create_lag_array_from_df(data, lag_num):
    lag_array = np.zeros((lag_num+1, data.shape[0]), dtype='float32')
    for lags in range(lag_num+1):
        lag_array[lags] = lag(data,lags)
    return lag_array

def create_multiple_lag_array_from_df(data_list, lag_num):
    total_lag_array = np.zeros((len(data_list), lag_num+1, data_list[0].shape[0]), dtype='float32')

    for idx,data in enumerate(data_list):
        total_lag_array[idx] = create_lag_array_from_df(data, lag_num)
    
    return total_lag_array

# Population Weights:

# taken from unutbu's answer: https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def map_population_to_pixel(population_array, longitudes, latitudes, x_coords, y_coords, pop_values):
    pop_array = population_array
    for idx, x_coord in enumerate(x_coords):
        x_pixel = find_nearest(longitudes, x_coord)
        y_pixel = find_nearest(latitudes, y_coords[idx])
        pop_array[y_pixel][x_pixel] += pop_values[idx]
    return pop_array

def create_population_array(population_data, longitudes, latitudes):
    pop_array = np.zeros((latitudes.shape[0],longitudes.shape[0]))

    for pop_file in population_data:
        pop_array = map_population_to_pixel(pop_array, longitudes, latitudes, pop_file['CENTROID_X'], pop_file['CENTROID_Y'], pop_file['UN_2000_E'])
    
    return pop_array

def create_population_weight_array_old(population_array):
    pop_array = population_array
    max_value = pop_array.max()

    pop_array /= max_value
    pop_array += 1

    return pop_array

#still unclear under what measure to create the weights
def create_population_weight_array(pop_array, countries_list):

    pixel_visited = np.zeros((pop_array.shape[0], pop_array.shape[1]))

    for country in countries_list:
        country_pixels = return_region_pixel_array(country)
        total_country_pop = 0

        for pixel in country_pixels:
            total_country_pop += pop_array[pixel[0]][pixel[1]]
        
        for pixel in country_pixels:
            if ((pixel_visited[pixel[0]][pixel[1]] != 1) or (pop_array[pixel[0]][pixel[1]] > 0)):
                pop_array[pixel[0]][pixel[1]] = (pop_array[pixel[0]][pixel[1]] / total_country_pop)
                pixel_visited[pixel[0]][pixel[1]] = 1

    return pop_array

"--------------------------------------------------------------------"
'Regression Functions'
"--------------------------------------------------------------------"

def daily_dust_country_regression(aod_daily_data, daily_bodele_aod_data, precipitation_daily_data, temperature_daily_data, daily_junsep_indices, daily_novapr_indices, countries_list):

    predicted_daily_aod_data = np.zeros((13515, 91,105), dtype='float32')
    r_squared_map = np.zeros((91,105), dtype='float32')
    

    for country in countries_list:

        country_pixels = return_region_pixel_array(country)

        for pixel in country_pixels:

            y_vector = aod_daily_data[:,pixel[0], pixel[1]][:, np.newaxis]
            current_regression_data = create_lag_regression_data(daily_bodele_aod_data, 10, [precipitation_daily_data[:,pixel[0], pixel[1]][:, np.newaxis],
                                                                 temperature_daily_data[:,pixel[0], pixel[1]][:, np.newaxis]],
                                                                 y_vector, daily_junsep_indices, daily_novapr_indices, dataframe=False)

            current_regression_model = sm.OLS(y_vector[10:-1],sm.add_constant(current_regression_data[10:-1])).fit(cov_type='HC1')
            current_predictions = current_regression_model.predict(sm.add_constant(current_regression_data))
            predicted_daily_aod_data[:,pixel[0], pixel[1]] = current_predictions

            r_squared_map[pixel[0], pixel[1]] = float(current_regression_model.summary2().tables[0][1][6])


    return predicted_daily_aod_data, r_squared_map

def daily_dust_regression(aod_daily_data, daily_bodele_aod_data, precipitation_daily_data, temperature_daily_data, daily_junsep_indices, daily_novapr_indices):

    predicted_daily_aod_data = np.zeros((13515, 91,105), dtype='float32')
    r_squared_map = np.zeros((91,105), dtype='float32')
    
    total_list = [[0,0] for y in range(91*105)]
    idx = 0
    for x in range(91):
        for y in range(105):
            total_list[idx][0] = x
            total_list[idx][1] = y
            idx += 1

    for pixel in total_list:

        y_vector = aod_daily_data[:,pixel[0], pixel[1]][:, np.newaxis]
        current_regression_data = create_lag_regression_data(daily_bodele_aod_data, 10, [precipitation_daily_data[:,pixel[0], pixel[1]][:, np.newaxis],
                                                                temperature_daily_data[:,pixel[0], pixel[1]][:, np.newaxis]],
                                                                y_vector, daily_junsep_indices, daily_novapr_indices, dataframe=False)

        current_regression_model = sm.OLS(y_vector[10:-1],sm.add_constant(current_regression_data[10:-1])).fit(cov_type='HC1')
        current_predictions = current_regression_model.predict(sm.add_constant(current_regression_data))
        predicted_daily_aod_data[:,pixel[0], pixel[1]] = current_predictions

        r_squared_map[pixel[0], pixel[1]] = float(current_regression_model.summary2().tables[0][1][6])


    return predicted_daily_aod_data, r_squared_map

#ehemals get_mse_data:
def get_country_mse_data(daily_data, daily_predicted_data, countries_list):

    mse_array = np.zeros((13515, 91, 105), dtype='float32')
    
    for country in countries_list:
        country_pixels = return_region_pixel_array(country)
        for pixel in country_pixels:
            mse_array[:,pixel[0],pixel[1]] = daily_data[:,pixel[0],pixel[1]]
    
    mse_array = np.abs(mse_array-daily_predicted_data)**2
    np.sum(mse_array, axis=0)/mse_array.shape[0]

    return mse_array

def get_mse_data(daily_data, daily_predicted_data):

    mse_array = np.zeros((13515, 91, 105), dtype='float32')

    total_list = [[0,0] for y in range(91*105)]
    idx = 0
    for x in range(91):
        for y in range(105):
            total_list[idx][0] = x
            total_list[idx][1] = y
            idx += 1

    for pixel in total_list:
        mse_array[:,pixel[0],pixel[1]] = daily_data[:,pixel[0],pixel[1]]
    
    mse_array = np.abs(mse_array-daily_predicted_data)**2
    np.sum(mse_array, axis=0)/mse_array.shape[0]

    return mse_array

def extract_yearly_indices(years,daily_seasonal_indices):
    yearly_seasonal_indices_list = [[]] * years
    year = 0
    previous_idx = 0
    current_indices = []
    for idx in daily_seasonal_indices:
        if (idx > 1):
            if (idx-1 != previous_idx):
                yearly_seasonal_indices_list[year] = current_indices
                year += 1
                current_indices = []
        previous_idx = idx
        current_indices.append(idx)
    return yearly_seasonal_indices_list


def create_dust_exposure_df(predicted_values, predicted_values_weighted,country_list, years, daily_seasonal_indices):
    yearly_countries_predicted_values = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')
    yearly_countries_predicted_values_weighted = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')

    yearly_countries_predicted_values_seasonal = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')
    yearly_countries_predicted_values_weighted_seasonal = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')

    seasonal_indices_by_year = extract_yearly_indices(years, daily_seasonal_indices)

    for idx, country in enumerate(country_list):
        daily_country_predicted_values = np.zeros((predicted_values.shape[0], return_region_pixel_array(country).shape[0]), dtype='float32')
        daily_country_predicted_values_weighted = np.zeros((predicted_values_weighted.shape[0], return_region_pixel_array(country).shape[0]), dtype='float32')
        for day in range(predicted_values.shape[0]):
            daily_country_predicted_values[day] = get_pixels_data_one_dim(predicted_values[day], return_region_pixel_array(country))
            daily_country_predicted_values_weighted[day] = get_pixels_data_one_dim(predicted_values_weighted[day], return_region_pixel_array(country))
        yearly_country_predicted_values = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')
        yearly_country_predicted_values_weighted = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')

        yearly_country_predicted_values_seasonal = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')
        yearly_country_predicted_values_weighted_seasonal = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')

        current_days = 0
        for year_idx in range((2016-1980)+1):
            if(year_idx%4 == 0):
                yearly_country_predicted_values[year_idx] = np.sum(daily_country_predicted_values[current_days:current_days+366], axis = 0)/366
                yearly_country_predicted_values_weighted[year_idx] = np.sum(daily_country_predicted_values_weighted[current_days:current_days+366], axis = 0)/366
                current_days += 366
            else:
                yearly_country_predicted_values[year_idx] = np.sum(daily_country_predicted_values[current_days:current_days+365], axis = 0)/365
                yearly_country_predicted_values_weighted[year_idx] = np.sum(daily_country_predicted_values_weighted[current_days:current_days+365], axis = 0)/365
                current_days += 365
            
            daily_seasonal_data = np.zeros((return_region_pixel_array(country).shape[0]), dtype='float32')
            daily_seasonal_data_weighted = np.zeros((return_region_pixel_array(country).shape[0]), dtype='float32')

            for day in seasonal_indices_by_year[year_idx]:
                daily_seasonal_data += daily_country_predicted_values[day]
                daily_seasonal_data_weighted += daily_country_predicted_values_weighted[day]
            
            yearly_country_predicted_values_seasonal[year_idx] = daily_seasonal_data/len(seasonal_indices_by_year[year_idx])
            yearly_country_predicted_values_weighted_seasonal[year_idx] = daily_seasonal_data_weighted/len(seasonal_indices_by_year[year_idx])

        yearly_countries_predicted_values[idx] = np.sum(yearly_country_predicted_values, axis = 1)/yearly_country_predicted_values.shape[1]
        yearly_countries_predicted_values_weighted[idx] = np.sum(yearly_country_predicted_values_weighted, axis = 1)/yearly_country_predicted_values_weighted.shape[1]

        yearly_countries_predicted_values_seasonal[idx] = np.sum(yearly_country_predicted_values_seasonal, axis = 1)/yearly_country_predicted_values_seasonal.shape[1]
        yearly_countries_predicted_values_weighted_seasonal[idx] = np.sum(yearly_country_predicted_values_weighted_seasonal, axis = 1)/yearly_country_predicted_values_weighted_seasonal.shape[1]


    dust_exposure_predicted_df = pd.DataFrame(yearly_countries_predicted_values, index = country_list, columns = range(1980,2016+1))
    dust_exposure_predicted_weighted_df = pd.DataFrame(yearly_countries_predicted_values_weighted, index = country_list, columns = range(1980,2016+1))

    dust_exposure_predicted_seasonal_df = pd.DataFrame(yearly_countries_predicted_values_seasonal, index = country_list, columns = range(1980,2016+1))
    dust_exposure_predicted_weighted_seasonal_df = pd.DataFrame(yearly_countries_predicted_values_weighted_seasonal, index = country_list, columns = range(1980,2016+1))

    return dust_exposure_predicted_df, dust_exposure_predicted_weighted_df, dust_exposure_predicted_seasonal_df, dust_exposure_predicted_weighted_seasonal_df

# to be deleted?
def create_dust_exposure_df_weighted(predicted_values, predicted_values_weighted,country_list, years, daily_seasonal_indices):
    yearly_countries_predicted_values = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')
    yearly_countries_predicted_values_weighted = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')

    yearly_countries_predicted_values_seasonal = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')
    yearly_countries_predicted_values_weighted_seasonal = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')

    seasonal_indices_by_year = extract_yearly_indices(years, daily_seasonal_indices)

    for idx, country in enumerate(country_list):
        daily_country_predicted_values = np.zeros((predicted_values.shape[0], return_region_pixel_array(country).shape[0]), dtype='float32')
        #get shape of populated pixels array
        temp_shape = get_pixels_data_one_dim(predicted_values_weighted[0], return_region_pixel_array(country))
        shape_population_array = temp_shape[temp_shape >= 0]
        daily_country_predicted_values_weighted = np.zeros((predicted_values_weighted.shape[0], shape_population_array.shape[0]), dtype='float32')
        for day in range(predicted_values.shape[0]):
            daily_country_predicted_values[day] = get_pixels_data_one_dim(predicted_values[day], return_region_pixel_array(country))
            #use temporal data 
            temp_daily_weighted_data = get_pixels_data_one_dim(predicted_values_weighted[day], return_region_pixel_array(country))
            #only take values above zero (pixels with no population were set to -1 in the predicted_values_weighted array)
            temp_data = temp_daily_weighted_data[~np.isnan(temp_daily_weighted_data)]
            daily_country_predicted_values_weighted[day] = temp_data
        yearly_country_predicted_values = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')
        yearly_country_predicted_values_weighted = np.zeros(((2016-1980)+1, shape_population_array.shape[0]), dtype='float32')

        yearly_country_predicted_values_seasonal = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')
        yearly_country_predicted_values_weighted_seasonal = np.zeros(((2016-1980)+1, shape_population_array.shape[0]), dtype='float32')

        current_days = 0
        for year_idx in range((2016-1980)+1):
            if(year_idx%4 == 0):
                yearly_country_predicted_values[year_idx] = np.sum(daily_country_predicted_values[current_days:current_days+366], axis = 0)/366
                yearly_country_predicted_values_weighted[year_idx] = np.sum(daily_country_predicted_values_weighted[current_days:current_days+366], axis = 0)/366
                current_days += 366
            else:
                yearly_country_predicted_values[year_idx] = np.sum(daily_country_predicted_values[current_days:current_days+365], axis = 0)/365
                yearly_country_predicted_values_weighted[year_idx] = np.sum(daily_country_predicted_values_weighted[current_days:current_days+365], axis = 0)/365
                current_days += 365
            
            daily_seasonal_data = np.zeros((return_region_pixel_array(country).shape[0]), dtype='float32')
            daily_seasonal_data_weighted = np.zeros((shape_population_array.shape[0]), dtype='float32')

            for day in seasonal_indices_by_year[year_idx]:
                daily_seasonal_data += daily_country_predicted_values[day]
                daily_seasonal_data_weighted += daily_country_predicted_values_weighted[day]
            
            yearly_country_predicted_values_seasonal[year_idx] = daily_seasonal_data/len(seasonal_indices_by_year[year_idx])
            yearly_country_predicted_values_weighted_seasonal[year_idx] = daily_seasonal_data_weighted/len(seasonal_indices_by_year[year_idx])

        yearly_countries_predicted_values[idx] = np.sum(yearly_country_predicted_values, axis = 1)/yearly_country_predicted_values.shape[1]
        yearly_countries_predicted_values_weighted[idx] = np.sum(yearly_country_predicted_values_weighted, axis = 1)/yearly_country_predicted_values_weighted.shape[1]

        yearly_countries_predicted_values_seasonal[idx] = np.sum(yearly_country_predicted_values_seasonal, axis = 1)/yearly_country_predicted_values_seasonal.shape[1]
        yearly_countries_predicted_values_weighted_seasonal[idx] = np.sum(yearly_country_predicted_values_weighted_seasonal, axis = 1)/yearly_country_predicted_values_weighted_seasonal.shape[1]


    dust_exposure_predicted_df = pd.DataFrame(yearly_countries_predicted_values, index = country_list, columns = range(1980,2016+1))
    dust_exposure_predicted_weighted_df = pd.DataFrame(yearly_countries_predicted_values_weighted, index = country_list, columns = range(1980,2016+1))

    dust_exposure_predicted_seasonal_df = pd.DataFrame(yearly_countries_predicted_values_seasonal, index = country_list, columns = range(1980,2016+1))
    dust_exposure_predicted_weighted_seasonal_df = pd.DataFrame(yearly_countries_predicted_values_weighted_seasonal, index = country_list, columns = range(1980,2016+1))

    return dust_exposure_predicted_df, dust_exposure_predicted_weighted_df, dust_exposure_predicted_seasonal_df, dust_exposure_predicted_weighted_seasonal_df

def create_dust_exposure_df_country_weighted(predicted_values, predicted_values_weighted,country_list, years, daily_seasonal_indices):
    #takes only weighted values of populated pixels, others are omitted
    
    yearly_countries_predicted_values = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')
    yearly_countries_predicted_values_weighted = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')

    yearly_countries_predicted_values_seasonal = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')
    yearly_countries_predicted_values_weighted_seasonal = np.zeros((len(country_list), (2016-1980)+1), dtype='float32')

    seasonal_indices_by_year = extract_yearly_indices(years, daily_seasonal_indices)

    for idx, country in enumerate(country_list):
        daily_country_predicted_values = np.zeros((predicted_values.shape[0], return_region_pixel_array(country).shape[0]), dtype='float32')
        #get shape of populated pixels array
        temp_shape = get_pixels_data_one_dim(predicted_values_weighted[0], return_region_pixel_array(country))
        shape_population_array = temp_shape[~np.isnan(temp_shape)]
        daily_country_predicted_values_weighted = np.zeros((predicted_values_weighted.shape[0], shape_population_array.shape[0]), dtype='float32')
        for day in range(predicted_values.shape[0]):
            daily_country_predicted_values[day] = get_pixels_data_one_dim(predicted_values[day], return_region_pixel_array(country))
            #use temporal data 
            temp_daily_weighted_data = get_pixels_data_one_dim(predicted_values_weighted[day], return_region_pixel_array(country))
            #only take values above zero (pixels with no population were set to -1 in the predicted_values_weighted array)
            temp_data = temp_daily_weighted_data[~np.isnan(temp_daily_weighted_data)]
            daily_country_predicted_values_weighted[day] = temp_data
        yearly_country_predicted_values = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')
        yearly_country_predicted_values_weighted = np.zeros(((2016-1980)+1, shape_population_array.shape[0]), dtype='float32')

        yearly_country_predicted_values_seasonal = np.zeros(((2016-1980)+1, return_region_pixel_array(country).shape[0]), dtype='float32')
        yearly_country_predicted_values_weighted_seasonal = np.zeros(((2016-1980)+1, shape_population_array.shape[0]), dtype='float32')

        current_days = 0
        for year_idx in range((2016-1980)+1):
            if(year_idx%4 == 0):
                yearly_country_predicted_values[year_idx] = np.sum(daily_country_predicted_values[current_days:current_days+366], axis = 0)/366
                yearly_country_predicted_values_weighted[year_idx] = np.sum(daily_country_predicted_values_weighted[current_days:current_days+366], axis = 0)/366
                current_days += 366
            else:
                yearly_country_predicted_values[year_idx] = np.sum(daily_country_predicted_values[current_days:current_days+365], axis = 0)/365
                yearly_country_predicted_values_weighted[year_idx] = np.sum(daily_country_predicted_values_weighted[current_days:current_days+365], axis = 0)/365
                current_days += 365
            
            daily_seasonal_data = np.zeros((return_region_pixel_array(country).shape[0]), dtype='float32')
            daily_seasonal_data_weighted = np.zeros((shape_population_array.shape[0]), dtype='float32')

            for day in seasonal_indices_by_year[year_idx]:
                daily_seasonal_data += daily_country_predicted_values[day]
                daily_seasonal_data_weighted += daily_country_predicted_values_weighted[day]
            
            yearly_country_predicted_values_seasonal[year_idx] = daily_seasonal_data/len(seasonal_indices_by_year[year_idx])
            yearly_country_predicted_values_weighted_seasonal[year_idx] = daily_seasonal_data_weighted/len(seasonal_indices_by_year[year_idx])

        yearly_countries_predicted_values[idx] = np.sum(yearly_country_predicted_values, axis = 1)/yearly_country_predicted_values.shape[1]
        yearly_countries_predicted_values_weighted[idx] = np.sum(yearly_country_predicted_values_weighted, axis = 1)/yearly_country_predicted_values_weighted.shape[1]

        yearly_countries_predicted_values_seasonal[idx] = np.sum(yearly_country_predicted_values_seasonal, axis = 1)/yearly_country_predicted_values_seasonal.shape[1]
        yearly_countries_predicted_values_weighted_seasonal[idx] = np.sum(yearly_country_predicted_values_weighted_seasonal, axis = 1)/yearly_country_predicted_values_weighted_seasonal.shape[1]


    dust_exposure_predicted_df = pd.DataFrame(yearly_countries_predicted_values, index = country_list, columns = range(1980,2016+1))
    dust_exposure_predicted_weighted_df = pd.DataFrame(yearly_countries_predicted_values_weighted, index = country_list, columns = range(1980,2016+1))

    dust_exposure_predicted_seasonal_df = pd.DataFrame(yearly_countries_predicted_values_seasonal, index = country_list, columns = range(1980,2016+1))
    dust_exposure_predicted_weighted_seasonal_df = pd.DataFrame(yearly_countries_predicted_values_weighted_seasonal, index = country_list, columns = range(1980,2016+1))

    return dust_exposure_predicted_df, dust_exposure_predicted_weighted_df, dust_exposure_predicted_seasonal_df, dust_exposure_predicted_weighted_seasonal_df


def lag(x, n):
    if n == 0:
        return x
    if isinstance(x, pd.Series):
        return x.shift(n) 
    else:
        x = pd.Series(x)
        return x.shift(n) 

    x = x.copy()
    x[n:] = x[0:-n]
    x[:n] = np.nan
    return x

def create_lag_array_from_df(data, lag_num):
    lag_array = np.zeros((lag_num+1, data.shape[0]), dtype='float32')
    for lags in range(lag_num+1):
        lag_array[lags] = lag(data,lags)
    return lag_array

def create_multiple_lag_array_from_df(data_list, lag_num, dataframe = False, column_names = [], index_names = []):

    total_lag_array = np.zeros((len(data_list), lag_num+1, data_list[0].shape[1]*len(data_list[0])), dtype='float32')

    for country in range(len(data_list[0])):
        current_lag_array = np.zeros((len(data_list), lag_num+1, data_list[0].shape[1]), dtype='float32')

        for variable in range(len(data_list)):
            current_lag_array = create_lag_array_from_df(data_list[variable].iloc[country], lag_num)
            for lag in range(lag_num+1):
                total_lag_array[variable][lag][country*37:(country+1)*37] = current_lag_array[lag]
    
    if dataframe:
        total_lag_array = np.concatenate(total_lag_array.swapaxes(1,2), axis =1)
        return pd.DataFrame(total_lag_array, columns = column_names)
    else:
        return total_lag_array

def growth_dataframe(df_wbdi_growth, df_mpd_growth, df_pwt_growth, country_num, current_df):

    wbdi_growth = []
    mpd_growth = []
    pwt_growth = []

    for country_num in range(12):
        wbdi_growth.append(df_wbdi_growth.T[2:-1][country_num].values)
        mpd_growth.append(df_mpd_growth.T[2:-1][country_num].values)
        pwt_growth.append(df_pwt_growth.T[2:][country_num].values)
    wbdi_growth = np.concatenate(wbdi_growth)
    mpd_growth = np.concatenate(mpd_growth)
    pwt_growth = np.concatenate(pwt_growth)

    return_df = current_df.copy()

    return_df.insert(3, "wbdi_growth", wbdi_growth, allow_duplicates=True)
    return_df.insert(3, "mpd_growth", mpd_growth, allow_duplicates=True)
    return_df.insert(3, "pwt_growth", pwt_growth, allow_duplicates=True)

    return return_df

def country_centroids_one_dim(country_centroids,countries_list,years):
    country_latitudes = np.empty((years*len(countries_list)), dtype = 'float32')
    country_longitudes = np.empty((years*len(countries_list)), dtype = 'float32')
    idx = 0
    for country in countries_list:
        for year in range(years):
            country_latitudes[idx] = country_centroids.iloc[:,1].loc[country_centroids['name'] == str(country).title()].values[0]
            country_longitudes[idx] = country_centroids.iloc[:,2].loc[country_centroids['name'] == str(country).title()].values[0]
            idx += 1
    
    return country_latitudes, country_longitudes

## lon lat dataframe

def create_yearly_dust_exposure_pixel_df(predicted_values, predicted_values_weighted, years, daily_seasonal_indices):

    #extract seasonal indices by year, so we can later jsut get dry season values
    seasonal_indices_by_year = extract_yearly_indices(years, daily_seasonal_indices)

    #init return arrays
    yearly_pixel_predicted_values = np.zeros(((2016-1980)+1,predicted_values.shape[1], predicted_values.shape[2]), dtype = 'float32')
    yearly_pixel_predicted_values_weighted = np.zeros(((2016-1980)+1,predicted_values_weighted.shape[1], predicted_values_weighted.shape[2]), dtype = 'float32')
    yearly_pixel_predicted_values_seasonal = np.zeros(((2016-1980)+1,predicted_values.shape[1], predicted_values.shape[2]), dtype = 'float32')
    yearly_pixel_predicted_values_weighted_seasonal = np.zeros(((2016-1980)+1,predicted_values_weighted.shape[1], predicted_values_weighted.shape[2]), dtype = 'float32')

    current_days = 0
    for year_idx in range((2016-1980)+1):
        # get yearly averages for each pixel
        # control for leap years
        if(year_idx%4 == 0):
            yearly_pixel_predicted_values[year_idx] = np.sum(predicted_values[current_days:current_days+366], axis = 0)/366
            yearly_pixel_predicted_values_weighted[year_idx] = np.sum(predicted_values_weighted[current_days:current_days+366], axis = 0)/366
            # year_indices[current_days:current_days+366] = years[year_idx]
            current_days += 366
        else:
            yearly_pixel_predicted_values[year_idx] = np.sum(predicted_values[current_days:current_days+365], axis = 0)/365
            yearly_pixel_predicted_values_weighted[year_idx] = np.sum(predicted_values_weighted[current_days:current_days+365], axis = 0)/365
            # year_indices[current_days:current_days+365] = years[year_idx]
            current_days += 365

        #init temp seasonal values arrays
        daily_pixel_predicted_values_seasonal = np.zeros((predicted_values.shape[1], predicted_values.shape[2]), dtype='float32')
        daily_pixel_predicted_values_seasonal_weighted = np.zeros((predicted_values_weighted.shape[1], predicted_values_weighted.shape[2]), dtype='float32')

        # 
        for day in seasonal_indices_by_year[year_idx]:
            daily_pixel_predicted_values_seasonal += predicted_values[day]
            daily_pixel_predicted_values_seasonal_weighted += predicted_values_weighted[day]
        
        yearly_pixel_predicted_values_seasonal[year_idx] = daily_pixel_predicted_values_seasonal/len(seasonal_indices_by_year[year_idx])
        yearly_pixel_predicted_values_weighted_seasonal[year_idx] = daily_pixel_predicted_values_seasonal_weighted/len(seasonal_indices_by_year[year_idx])

    return yearly_pixel_predicted_values, yearly_pixel_predicted_values_weighted, yearly_pixel_predicted_values_seasonal, yearly_pixel_predicted_values_weighted_seasonal

def array_reshape_one_dim(value_array):
    one_dim_array = np.zeros(value_array.shape[0]*value_array.shape[1]*value_array.shape[2])
    idx = 0
    for year in range(value_array.shape[0]):
        for latitude in range(value_array.shape[1]):
            for longitude in range(value_array.shape[2]):
                one_dim_array[idx] = value_array[year,latitude,longitude]
                idx += 1
    return one_dim_array

def one_dim_lat_lon_array(latitudes, longitudes, years):
    one_dim_lat_array = np.empty((years*latitudes.shape[0]*longitudes.shape[0]), dtype = 'float32')
    one_dim_lon_array = np.empty((years*latitudes.shape[0]*longitudes.shape[0]), dtype = 'float32')
    idx = 0
    for year in range(years):
        for latitude in latitudes:
            for longitude in longitudes:
                one_dim_lat_array[idx] = latitude
                one_dim_lon_array[idx] = longitude
                idx += 1

    return one_dim_lat_array, one_dim_lon_array

def one_dim_country_lat_lon_array(latitudes, longitudes, countries_list, years):
    country_array = np.empty((latitudes.shape[0],longitudes.shape[0]), dtype = object)
    for country in countries_list:
        country_pixels = return_region_pixel_array(country)
        for pixel in country_pixels:
            country_array[pixel[0], pixel[1]] = country
    one_dim_country_array = np.empty((years*latitudes.shape[0]*longitudes.shape[0]), dtype = object)
    idx = 0
    for year in range(years):
        for latitude in range(latitudes.shape[0]):
            for longitude in range(longitudes.shape[0]):
                one_dim_country_array[idx] = country_array[latitude,longitude]
                idx += 1
    
    return one_dim_country_array

def one_dim_year_array(latitudes, longitudes, years_list):
    one_dim_years_array = np.empty((len(years_list)*latitudes.shape[0]*longitudes.shape[0]), dtype = int)
    idx = 0
    for year in years_list:
        for latitude in range(latitudes.shape[0]):
            for longitude in range(longitudes.shape[0]):
                one_dim_years_array[idx] = year
                idx += 1
    

    return one_dim_years_array

def lag_lat_lon_df(dataframe, lag_list, columns_list):
    return_df = dataframe
    for col in columns_list:
        for l in lag_list:
            return_df.loc[:,dataframe.columns[col]+"_"+str(l)] = dataframe[dataframe.columns[col]].shift(l*9555)
    return return_df

def one_dim_growth_array(latitudes, longitudes, countries_list, years, years_list, df_wbdi_growth, df_mpd_growth, df_pwt_growth):
    country_array = np.empty((latitudes.shape[0],longitudes.shape[0]), dtype = object)
    for country in countries_list:
        country_pixels = return_region_pixel_array(country)
        for pixel in country_pixels:
            country_array[pixel[0], pixel[1]] = country
    
    wbdi_growth_array = np.empty((years*latitudes.shape[0]*longitudes.shape[0]), dtype = 'float32')
    mpd_growth_array = np.empty((years*latitudes.shape[0]*longitudes.shape[0]), dtype = 'float32')
    pwt_growth_array = np.empty((years*latitudes.shape[0]*longitudes.shape[0]), dtype = 'float32')

    idx = 0
    for year in range(years):
        for latitude in range(latitudes.shape[0]):
            for longitude in range(longitudes.shape[0]):

                if (len(df_wbdi_growth[str(years_list[year])].loc[df_wbdi_growth['country'] == str(country_array[latitude,longitude]).title()]) == 0):
                    wbdi_growth_array[idx] = None
                else:
                    wbdi_growth_array[idx] = df_wbdi_growth[str(years_list[year])].loc[df_wbdi_growth['country'] == str(country_array[latitude,longitude]).title()].values
                if (len(df_mpd_growth[str(years_list[year])].loc[df_mpd_growth['country'] == str(country_array[latitude,longitude]).title()]) == 0):
                    mpd_growth_array[idx] = None
                else:
                    mpd_growth_array[idx] = df_mpd_growth[str(years_list[year])].loc[df_mpd_growth['country'] == str(country_array[latitude,longitude]).title()].values
                if (len(df_pwt_growth[str(years_list[year])].loc[df_pwt_growth['country'] == str(country_array[latitude,longitude]).title()]) == 0):
                    pwt_growth_array[idx] = None
                else:
                    pwt_growth_array[idx] = df_pwt_growth[str(years_list[year])].loc[df_pwt_growth['country'] == str(country_array[latitude,longitude]).title()].values
                idx += 1
    

    return wbdi_growth_array, mpd_growth_array, pwt_growth_array

"--------------------------------------------------------------------"
'Miscellaneous Functions'
"--------------------------------------------------------------------"



#taken from: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula

@jit
def distance2(lat1, lon1, lat2, lon2):
    p = np.pi/180
    a = 0.5 - np.cos((lat2-lat1)*p)/2 + np.cos(lat1*p) * np.cos(lat2*p) * (1-np.cos((lon2-lon1)*p))/2
    return 12742 * np.arcsin(np.sqrt(a)) #2*R*asin...