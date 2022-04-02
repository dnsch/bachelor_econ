import os
import pickle
import numpy as np
import pandas as pd


from functions import process_merra_data, process_outcome_data, hourly_data_to_daily_mean, three_hourly_data_to_daily_mean, extract_seasonal_data
from functions import advection_diffusion_fd
from functions import return_region_pixel_array
from functions import three_hourly_data_to_daily_mean, create_regression_df
from functions import get_time_span_region_data, get_regional_mean_data

parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():


    ######################################################################
    # Processing MERRA2 Data
    ######################################################################


    "--------------------------------------------------------------------"
    '2.1_dust_data'
    "--------------------------------------------------------------------"

    print('processing monthly aerosol optical depth raw data ...')
    (total_longitudes,
    total_latitudes,
    monthly_time,
    aod_monthly_data,
    monthly_junsep_indices,
    monthly_novapr_indices) = process_merra_data('\\raw_data\\2.1_dust_data\\monthly_aod\\', 
                                                 seasonal_indices = True, variables = ['AODANA'], two_vars = False, 
                                                 timing = 'monthly', time_steps = 444, y_steps = 361, x_steps = 576, 
                                                 datatype = 'float32')

    aod_monthly_novapr_data, aod_monthly_junsep_data = extract_seasonal_data(aod_monthly_data, monthly_novapr_indices, monthly_junsep_indices)
    print('processed monthly aerosol optical depth raw data')


    "--------------------------------------------------------------------"
    '3.1_physical_model'
    "--------------------------------------------------------------------"


    print('processing wind raw data ...')
    (west_africa_longitudes,
    west_africa_latitudes,
    hourly_time,
    wind_eastward_hourly_data,
    wind_northward_hourly_data,
    hourly_junsep_indices,
    daily_junsep_indices,
    hourly_novapr_indices,
    daily_novapr_indices) =   process_merra_data('\\raw_data\\3.1_physical_model\\hourly_wind\\', 
                                                 seasonal_indices = True, variables = ['ULML', 'VLML'], two_vars = True, 
                                                 timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                 datatype = 'float32')
                                                 
    wind_eastward_hourly_novapr_data, wind_eastward_hourly_junsep_data = extract_seasonal_data(wind_eastward_hourly_data, hourly_novapr_indices, hourly_junsep_indices)     
    wind_northward_hourly_novapr_data, wind_northward_hourly_junsep_data = extract_seasonal_data(wind_northward_hourly_data, hourly_novapr_indices, hourly_junsep_indices) 
    print('processed wind raw data')

    print('processing dustmass - pm 2.5 raw data ...')                                                    
    (west_africa_longitudes,
    west_africa_latitudes,
    hourly_time,
    dust_hourly_data) = process_merra_data('\\raw_data\\3.1_physical_model\\hourly_dusmass_pm2.5\\', 
                                            seasonal_indices = False, variables = ['DUSMASS25'], two_vars = False, 
                                            timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                            datatype = 'float32')

    dust_hourly_novapr_data, dust_hourly_junsep_data = extract_seasonal_data(dust_hourly_data, hourly_novapr_indices, hourly_novapr_indices)

    # dust_daily_data = hourly_data_to_daily_mean(dust_hourly_data)
    print('processed dustmass - pm 2.5 raw data')   


    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"


    print('processing hourly bias corrected total precipitation raw data ...') 
    (west_africa_longitudes,
    west_africa_latitudes,
    hourly_time,
    precipitation_hourly_data) = process_merra_data('\\raw_data\\3.3_model_implementation\\hourly_precipitation\\', 
                                                    seasonal_indices = False, variables = ['PRECTOTCORR'], two_vars = False, 
                                                    timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                    datatype = 'float32')

    precipitation_daily_data = hourly_data_to_daily_mean(precipitation_hourly_data)
    print('processed hourly bias corrected total precipitation raw data')  

    print('processing surface temperature raw data ...') 
    (west_africa_longitudes,
    west_africa_latitudes,
    hourly_time,
    temperature_hourly_data) = process_merra_data('\\raw_data\\3.3_model_implementation\\hourly_temperature\\', 
                                                  seasonal_indices = False, variables = ['TLML'], two_vars = False, 
                                                  timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                  datatype = 'float32')

    temperature_daily_data = hourly_data_to_daily_mean(temperature_hourly_data)                                  
    print('processed surface temperature raw data')  

    print('processing aerosol optical depth raw data ...')                                                    
    (west_africa_longitudes,
    west_africa_latitudes,
    three_hourly_time,
    aod_three_hourly_data,
    three_hourly_junsep_indices,
    daily_junsep_indices,
    three_hourly_novapr_indices,
    daily_novapr_indices) = process_merra_data('\\raw_data\\3.3_model_implementation\\three_hourly_aod\\', 
                                                seasonal_indices = True, variables = ['AODANA'], two_vars = False, 
                                                timing = 'three_hourly', time_steps = 108120, y_steps = 91, x_steps = 105, 
                                                datatype = 'float32')
    aod_daily_data = three_hourly_data_to_daily_mean(aod_three_hourly_data)
    print('processed aerosol optical depth raw data') 

    ######################################################################
    # Saving MERRA2 Data
    ######################################################################
    

    "--------------------------------------------------------------------"
    '2.1_dust_data'
    "--------------------------------------------------------------------"


    print('saving processed monthly and hourly seasonal indices to \\processed_data ...')
    #save lists as pickle files
    with open(parent_directory + '\\processed_data\\monthly_junsep_indices', 'wb') as pickle_file:
        pickle.dump(monthly_junsep_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\monthly_novapr_indices', 'wb') as pickle_file:
        pickle.dump(monthly_novapr_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\daily_junsep_indices', 'wb') as pickle_file:
        pickle.dump(daily_junsep_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\daily_novapr_indices', 'wb') as pickle_file:
        pickle.dump(daily_novapr_indices, pickle_file)
    
    with open(parent_directory + '\\processed_data\\three_hourly_junsep_indices', 'wb') as pickle_file:
        pickle.dump(three_hourly_junsep_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\three_hourly_novapr_indices', 'wb') as pickle_file:
        pickle.dump(three_hourly_novapr_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\hourly_junsep_indices', 'wb') as pickle_file:
        pickle.dump(hourly_junsep_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\hourly_novapr_indices', 'wb') as pickle_file:
        pickle.dump(hourly_novapr_indices, pickle_file)
    print('saved processed monthly and hourly seasonal indices to \\processed_data')
    
    print('saving processed monthly and hourly geographical and time arrays to \\processed_data ...')
    #save numpy arrays
    #geo data
    with open(parent_directory + '\\processed_data\\total_longitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, total_longitudes)
    del total_longitudes
    
    with open(parent_directory + '\\processed_data\\total_latitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, total_latitudes)
    del total_latitudes
    
    with open(parent_directory + '\\processed_data\\west_africa_longitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, west_africa_longitudes)
    
    with open(parent_directory + '\\processed_data\\west_africa_latitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, west_africa_latitudes)

    #time data
    with open(parent_directory + '\\processed_data\\monthly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, monthly_time)    
    del monthly_time

    with open(parent_directory + '\\processed_data\\three_hourly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, three_hourly_time)
    del three_hourly_time

    with open(parent_directory + '\\processed_data\\hourly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, hourly_time)
    del hourly_time
    print('saved processed monthly and hourly geographical and time arrays to \\processed_data')

    print('saving processed monthly aerosol optical depth arrays to \\processed_data ...')
    #aod data
    with open(parent_directory + '\\processed_data\\aod_monthly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_monthly_data)
    del aod_monthly_data
    
    with open(parent_directory + '\\processed_data\\aod_monthly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_monthly_novapr_data)
    del aod_monthly_novapr_data

    with open(parent_directory + '\\processed_data\\aod_monthly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_monthly_junsep_data)
    del aod_monthly_junsep_data
    print('saved processed monthly aerosol optical depth arrays to \\processed_data')


    "--------------------------------------------------------------------"
    '2.2_outcome_data'
    "--------------------------------------------------------------------"


    print('processing outcome data ...')
    #process and save outcome data
    df_pwt_resid_log, df_wbdi_resid_log, df_mpd_resid_log = process_outcome_data()
    print('processed outcome data')

    print('saving processed outcome data .csv to \\processed_data ...')
    df_pwt_resid_log.to_csv(parent_directory + '\\processed_data\\pwt_resid_log.csv')
    del df_pwt_resid_log
    df_wbdi_resid_log.to_csv(parent_directory + '\\processed_data\\wbdi_resid_log.csv')
    del df_wbdi_resid_log
    df_mpd_resid_log.to_csv(parent_directory + '\\processed_data\\mpd_resid_log.csv')
    del df_mpd_resid_log
    print('saved processed outcome data .csv to \\processed_data')


    "--------------------------------------------------------------------"
    '3.1_physical_model'
    "--------------------------------------------------------------------"


    print('saving processed hourly wind arrays to \\processed_data ...')
    #wind data
    with open(parent_directory + '\\processed_data\\wind_eastward_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_hourly_data)
    
    with open(parent_directory + '\\processed_data\\wind_northward_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_hourly_data)

    with open(parent_directory + '\\processed_data\\wind_eastward_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_hourly_novapr_data)

    with open(parent_directory + '\\processed_data\\wind_eastward_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_hourly_junsep_data)
    
    with open(parent_directory + '\\processed_data\\wind_northward_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_hourly_novapr_data)
    
    with open(parent_directory + '\\processed_data\\wind_northward_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_hourly_junsep_data)
    print('saved processed hourly wind arrays to \\processed_data')

    print('saving processed hourly dust arrays to \\processed_data ...')
    #dust data
    with open(parent_directory + '\\processed_data\\dust_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_hourly_data)
    
    with open(parent_directory + '\\processed_data\\dust_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_hourly_novapr_data)

    with open(parent_directory + '\\processed_data\\dust_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_hourly_junsep_data)
    print('saved processed hourly dust arrays to \\processed_data')


    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"


    print('saving processed hourly and daily mean precipitation arrays to \\processed_data ...')
    #precipitation data
    with open(parent_directory + '\\processed_data\\precipitation_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_hourly_data)
    
    with open(parent_directory + '\\processed_data\\precipitation_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_daily_data)
    print('saved processed hourly and daily mean precipitation arrays to \\processed_data')

    print('saving processed hourly and daily mean temperature arrays to \\processed_data ...')
    #temperature data
    with open(parent_directory + '\\processed_data\\temperature_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_hourly_data)
    
    with open(parent_directory + '\\processed_data\\temperature_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_daily_data)
    print('saved processed hourly and daily mean temperature arrays to \\processed_data')

    print('saving processed three hourly and daily mean aerosol optical depth arrays to \\processed_data ...')
    #temperature data
    with open(parent_directory + '\\processed_data\\aod_three_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_three_hourly_data)
    
    with open(parent_directory + '\\processed_data\\aod_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_daily_data)
    print('saved processed three hourly and daily mean aerosol optical depth arrays to \\processed_data')

    

    ######################################################################
    # Preparing Regression Data
    ######################################################################

    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"

    bodele_region_pixels = return_region_pixel_array(region_name='bodele')

    togo_coast_pixel = return_region_pixel_array(region_name='togo_coast')

    daily_bodele_aod_data = get_regional_mean_data(get_time_span_region_data(aod_daily_data, bodele_region_pixels))
    daily_togo_coast_aod_data = get_time_span_region_data(aod_daily_data, togo_coast_pixel)

    # daily_bodele_dust_data = get_regional_mean_data(get_time_span_region_data(dust_total_data, bodele_region_pixels))
    # daily_togo_coast_dust_data = get_time_span_region_data(dust_total_data, togo_coast_pixel)

    daily_togo_precipitation_data = get_time_span_region_data(precipitation_daily_data, togo_coast_pixel)
    daily_togo_temperature_data = get_time_span_region_data(temperature_daily_data, togo_coast_pixel)

    aod_reg_df = create_regression_df(daily_bodele_aod_data, 10, [daily_togo_precipitation_data,daily_togo_temperature_data],
                                        daily_togo_coast_aod_data, daily_junsep_indices, daily_novapr_indices,
                                        variable_names =   ['wet_season', 'dry_season', 'bod_aod_t-10', 'bod_aod_t-9',
                                                            'bod_aod_t-8', 'bod_aod_t-7','bod_aod_t-6', 'bod_aod_t-5',
                                                            'bod_aod_t-4', 'bod_aod_t-3','bod_aod_t-2', 'bod_aod_t-1',
                                                            'bod_aod_t-0', 'precipitation', 'temperature'],
                                        y_name = 'togo_coast_aod')
                            
    # dust_reg_df = create_regression_df(daily_bodele_dust_data, 10, [daily_togo_precipitation_data,daily_togo_temperature_data],
    #                                     daily_togo_coast_dust_data, daily_junsep_indices, daily_novapr_indices,
    #                                     variable_names =   ['wet_season', 'dry_season', 'bod_aod_t-10', 'bod_dust_t-9',
    #                                                         'bod_dust_t-8', 'bod_dust_t-7','bod_dust_t-6', 'bod_dust_t-5',
    #                                                         'bod_dust_t-4', 'bod_dust_t-3','bod_dust_t-2', 'bod_dust_t-1',
    #                                                         'bod_dust_t-0', 'precipitation', 'temperature'],
    #                                     y_name = 'togo_coast_dust')

    aod_reg_df[(aod_reg_df['dry_season']==True)].iloc[: ,[0,3,14,15]].to_csv(parent_directory + '\\processed_data\\aod_reg_df_novapr.csv', index=False)

    aod_reg_df[(aod_reg_df['wet_season']==True)].iloc[: ,[0,3,14,15]].to_csv(parent_directory + '\\processed_data\\aod_reg_df_junsep.csv', index=False)



if __name__ == "__main__":
    main()

