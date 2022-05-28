import os
import pickle
import numpy as np
import pandas as pd
import gc


from functions import process_merra_data, process_outcome_data, hourly_data_to_daily_mean, three_hourly_data_to_daily_mean, extract_seasonal_data
from functions import three_hourly_data_to_daily_mean

parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():


    ######################################################################
    # Processing MERRA2 Data
    ######################################################################


    "--------------------------------------------------------------------"
    '2.1_dust_data'
    "--------------------------------------------------------------------"

    print('processing monthly aerosol optical depth raw data ...')
    #aod
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

    print('saving processed monthly aerosol optical depth arrays to \\processed_data ...')
    #aod data
    with open(parent_directory + '\\processed_data\\aod_monthly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_monthly_data.data)
    del aod_monthly_data
    
    with open(parent_directory + '\\processed_data\\aod_monthly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_monthly_novapr_data.data)
    del aod_monthly_novapr_data

    with open(parent_directory + '\\processed_data\\aod_monthly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_monthly_junsep_data.data)
    del aod_monthly_junsep_data
    print('saved processed monthly aerosol optical depth arrays to \\processed_data')

    #invoke garbage collector
    gc.collect()

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

    print('saving processed hourly wind arrays to \\processed_data ...')
    #wind data
    with open(parent_directory + '\\processed_data\\wind_eastward_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_hourly_data.data)
    del wind_eastward_hourly_data
    
    with open(parent_directory + '\\processed_data\\wind_northward_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_hourly_data.data)
    del wind_northward_hourly_data

    with open(parent_directory + '\\processed_data\\wind_eastward_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_hourly_novapr_data.data)
    del wind_eastward_hourly_novapr_data

    with open(parent_directory + '\\processed_data\\wind_eastward_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_hourly_junsep_data.data)
    del wind_eastward_hourly_junsep_data
    
    with open(parent_directory + '\\processed_data\\wind_northward_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_hourly_novapr_data.data)
    del wind_northward_hourly_novapr_data
    
    with open(parent_directory + '\\processed_data\\wind_northward_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_hourly_junsep_data.data)
    del wind_northward_hourly_junsep_data
    print('saved processed hourly wind arrays to \\processed_data')
    
    #invoke garbage collector
    gc.collect()

    print('processing dustmass - pm 2.5 raw data ...')                                                    
    dust_hourly_data = process_merra_data('\\raw_data\\3.1_physical_model\\hourly_dusmass_pm2.5\\', 
                                            seasonal_indices = False, variables = ['DUSMASS25'], two_vars = False, 
                                            timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                            datatype = 'float32')[3]

    dust_hourly_novapr_data, dust_hourly_junsep_data = extract_seasonal_data(dust_hourly_data, hourly_novapr_indices, hourly_junsep_indices)

    dust_daily_data = hourly_data_to_daily_mean(dust_hourly_data)

    dust_daily_data_novapr, dust_daily_data_junsep = extract_seasonal_data(dust_daily_data, daily_novapr_indices, daily_junsep_indices)

    print('processed dustmass - pm 2.5 raw data')   

    print('saving processed hourly dust arrays to \\processed_data ...')
    #dust data
    with open(parent_directory + '\\processed_data\\dust_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_hourly_data.data)
    del dust_hourly_data
    
    with open(parent_directory + '\\processed_data\\dust_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_hourly_novapr_data.data)
    del dust_hourly_novapr_data

    with open(parent_directory + '\\processed_data\\dust_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_hourly_junsep_data.data)
    del dust_hourly_junsep_data

    with open(parent_directory + '\\processed_data\\dust_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_daily_data.data)
    del dust_daily_data

    with open(parent_directory + '\\processed_data\\dust_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_daily_data_novapr.data)
    del dust_daily_data_novapr

    with open(parent_directory + '\\processed_data\\dust_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_daily_data_junsep.data)
    del dust_daily_data_junsep
    print('saved processed hourly dust arrays to \\processed_data')

    #invoke garbage collector
    gc.collect()


    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"


    print('processing hourly bias corrected total precipitation raw data ...') 
    precipitation_hourly_data = process_merra_data('\\raw_data\\3.3_model_implementation\\hourly_precipitation\\', 
                                                    seasonal_indices = False, variables = ['PRECTOTCORR'], two_vars = False, 
                                                    timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                    datatype = 'float32')[3]

    precipitation_daily_data = hourly_data_to_daily_mean(precipitation_hourly_data)
    precipitation_daily_data_novapr, precipitation_daily_data_junsep = extract_seasonal_data(precipitation_daily_data, daily_novapr_indices, daily_junsep_indices)
    print('processed hourly bias corrected total precipitation raw data')  

    print('saving processed hourly and daily mean precipitation arrays to \\processed_data ...')
    #precipitation data
    with open(parent_directory + '\\processed_data\\precipitation_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_hourly_data.data)
    del precipitation_hourly_data
    
    with open(parent_directory + '\\processed_data\\precipitation_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_daily_data.data)
    del precipitation_daily_data

    with open(parent_directory + '\\processed_data\\precipitation_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_daily_data_novapr.data)
    del precipitation_daily_data_novapr

    with open(parent_directory + '\\processed_data\\precipitation_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_daily_data_junsep.data)
    del precipitation_daily_data_junsep
    print('saved processed hourly and daily mean precipitation arrays to \\processed_data')

    #invoke garbage collector
    gc.collect()

    print('processing surface temperature raw data ...') 
    temperature_hourly_data = process_merra_data('\\raw_data\\3.3_model_implementation\\hourly_temperature\\', 
                                                  seasonal_indices = False, variables = ['TLML'], two_vars = False, 
                                                  timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                  datatype = 'float32')[3]

    temperature_daily_data = hourly_data_to_daily_mean(temperature_hourly_data)
    temperature_daily_data_novapr, temperature_daily_data_junsep = extract_seasonal_data(temperature_daily_data, daily_novapr_indices, daily_junsep_indices)                                
    print('processed surface temperature raw data')  

    print('saving processed hourly and daily mean temperature arrays to \\processed_data ...')
    #temperature data
    with open(parent_directory + '\\processed_data\\temperature_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_hourly_data.data)
    del temperature_hourly_data
    
    with open(parent_directory + '\\processed_data\\temperature_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_daily_data.data)
    del temperature_daily_data

    with open(parent_directory + '\\processed_data\\temperature_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_daily_data_novapr.data)
    del temperature_daily_data_novapr
    
    with open(parent_directory + '\\processed_data\\temperature_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_daily_data_junsep.data)
    del temperature_daily_data_junsep
    print('saved processed hourly and daily mean temperature arrays to \\processed_data')

    #invoke garbage collector
    gc.collect()

    print('processing aerosol optical depth raw data ...')                                                    
    (three_hourly_time,
    aod_three_hourly_data,
    three_hourly_junsep_indices,
    daily_junsep_indices,
    three_hourly_novapr_indices,
    daily_novapr_indices) = process_merra_data('\\raw_data\\3.3_model_implementation\\three_hourly_aod\\', 
                                                seasonal_indices = True, variables = ['AODANA'], two_vars = False, 
                                                timing = 'three_hourly', time_steps = 108120, y_steps = 91, x_steps = 105, 
                                                datatype = 'float32')[2:]
    aod_daily_data = three_hourly_data_to_daily_mean(aod_three_hourly_data)
    print('processed aerosol optical depth raw data') 

    print('saving processed three hourly and daily mean aerosol optical depth arrays to \\processed_data ...')
    #temperature data
    with open(parent_directory + '\\processed_data\\aod_three_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_three_hourly_data.data)
    del aod_three_hourly_data
    
    with open(parent_directory + '\\processed_data\\aod_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_daily_data.data)
    del aod_daily_data
    print('saved processed three hourly and daily mean aerosol optical depth arrays to \\processed_data')

    #invoke garbage collector
    gc.collect()

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
        np.save(numpy_array, total_longitudes.data)
    del total_longitudes
    
    with open(parent_directory + '\\processed_data\\total_latitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, total_latitudes.data)
    del total_latitudes
    
    with open(parent_directory + '\\processed_data\\west_africa_longitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, west_africa_longitudes.data)
    
    with open(parent_directory + '\\processed_data\\west_africa_latitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, west_africa_latitudes.data)

    #time data
    with open(parent_directory + '\\processed_data\\monthly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, monthly_time.data)    
    del monthly_time

    with open(parent_directory + '\\processed_data\\three_hourly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, three_hourly_time.data)
    del three_hourly_time

    with open(parent_directory + '\\processed_data\\hourly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, hourly_time.data)
    del hourly_time
    print('saved processed monthly and hourly geographical and time arrays to \\processed_data')

    


    "--------------------------------------------------------------------"
    '2.2_outcome_data'
    "--------------------------------------------------------------------"


    print('processing outcome data ...')
    #process and save outcome data
    (df_pwt, df_pwt_growth, df_pwt_per_cap, df_pwt_growth_per_cap,
    df_wbdi, df_wbdi_per_cap, df_wbdi_pop, df_wbdi_growth, df_wbdi_per_cap_growth,
    df_mpd, df_mpd_growth, df_mpd_pop, df_mpd_per_cap, df_mpd_per_cap_growth) = process_outcome_data()
    # df_pwt_resid_log, df_wbdi_resid_log, df_mpd_resid_log = process_outcome_data()
    print('processed outcome data')

    print('saving processed outcome data .csv to \\processed_data ...')
    df_pwt.to_csv(parent_directory + '\\processed_data\\df_pwt.csv')
    del df_pwt
    df_pwt_growth.to_csv(parent_directory + '\\processed_data\\df_pwt_growth.csv')
    del df_pwt_growth
    df_pwt_per_cap.to_csv(parent_directory + '\\processed_data\\df_pwt_per_cap.csv')
    del df_pwt_per_cap
    df_pwt_growth_per_cap.to_csv(parent_directory + '\\processed_data\\df_pwt_growth_per_cap.csv')
    del df_pwt_growth_per_cap
    df_wbdi.to_csv(parent_directory + '\\processed_data\\df_wbdi.csv')
    del df_wbdi
    df_wbdi_per_cap.to_csv(parent_directory + '\\processed_data\\df_wbdi_per_cap.csv')
    del df_wbdi_per_cap
    df_wbdi_pop.to_csv(parent_directory + '\\processed_data\\df_wbdi_pop.csv')
    del df_wbdi_pop
    df_wbdi_growth.to_csv(parent_directory + '\\processed_data\\df_wbdi_growth.csv')
    del df_wbdi_growth
    df_wbdi_per_cap_growth.to_csv(parent_directory + '\\processed_data\\df_wbdi_per_cap_growth.csv')
    del df_wbdi_per_cap_growth
    df_mpd.to_csv(parent_directory + '\\processed_data\\df_mpd.csv')
    del df_mpd
    df_mpd_growth.to_csv(parent_directory + '\\processed_data\\df_mpd_growth.csv')
    del df_mpd_growth
    df_mpd_pop.to_csv(parent_directory + '\\processed_data\\df_mpd_pop.csv')
    del df_mpd_pop
    df_mpd_per_cap.to_csv(parent_directory + '\\processed_data\\df_mpd_per_cap.csv')
    del df_mpd_per_cap
    df_mpd_per_cap_growth.to_csv(parent_directory + '\\processed_data\\df_mpd_per_cap_growth.csv')
    del df_mpd_per_cap_growth

    # df_pwt_resid_log.to_csv(parent_directory + '\\processed_data\\pwt_resid_log.csv')
    # del df_pwt_resid_log
    # df_wbdi_resid_log.to_csv(parent_directory + '\\processed_data\\wbdi_resid_log.csv')
    # del df_wbdi_resid_log
    # df_mpd_resid_log.to_csv(parent_directory + '\\processed_data\\mpd_resid_log.csv')
    # del df_mpd_resid_log
    print('saved processed outcome data .csv to \\processed_data')

    #invoke garbage collector
    gc.collect()


    "--------------------------------------------------------------------"
    '3.1_physical_model'
    "--------------------------------------------------------------------"


    

    


    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"


    




if __name__ == "__main__":
    main()

