import os
import pickle
import numpy as np
import pandas as pd


from Functions import process_merra_data, process_outcome_data
from Functions import advection_diffusion_fd

parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():


    ######################################################################
    # Processing MERRA2 Data
    ######################################################################


    "--------------------------------------------------------------------"
    '2.1_dust_data'
    "--------------------------------------------------------------------"


    print('processing aod raw data ...')
    (monthly_longitudes,
    monthly_latitudes,
    monthly_time,
    monthly_junsep_indices,
    monthly_novapr_indices,
    aod_mean_data_junsep,
    aod_mean_data_novapr,
    aod_mean_data_total) =  process_merra_data('\\raw_data\\2.1_dust_data\\MERRA2_instM_2d_gas_Nx\\', 
                                                seasonal = True, variables = ['AODANA'], two_vars = False, 
                                                hourly = False, time_steps = 0, y_steps = 0, x_steps = 0, 
                                                datatype = 'float32')
    print('processed aod raw data')


    "--------------------------------------------------------------------"
    '3.1_physical_model'
    "--------------------------------------------------------------------"


    print('processing wind raw data ...')
    (hourly_longitudes,
    hourly_latitudes,
    hourly_time,
    wind_eastward_total_data,
    wind_northward_total_data,
    hourly_junsep_indices,
    hourly_novapr_indices,
    wind_eastward_mean_data_junsep,
    wind_eastward_mean_data_novapr,
    wind_eastward_mean_data_total,
    wind_northward_mean_data_junsep,
    wind_northward_mean_data_novapr,
    wind_northward_mean_data_total) =   process_merra_data('\\raw_data\\3.1_physical_model\\wind\\', 
                                                            seasonal = True, variables = ['ULML', 'VLML'], two_vars = True, 
                                                            hourly = True, time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                            datatype = 'float32')
    print('processed wind raw data')

    print('processing dustmass - pm 2.5 raw data ...')                                                    
    (hourly_longitudes,
    hourly_latitudes,
    hourly_time,
    dust_total_data,
    hourly_junsep_indices,
    hourly_novapr_indices,
    dust_mean_data_junsep,
    dust_mean_data_novapr,
    dust_mean_data_total) = process_merra_data('\\raw_data\\3.1_physical_model\\dusmass_pm2.5\\', 
                                                seasonal = True, variables = ['DUSMASS25'], two_vars = False, 
                                                hourly = True, time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                datatype = 'float32')
    print('processed dustmass - pm 2.5 raw data')   


    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"


    print('processing bias corrected total precipitation raw data ...')                                                    
    (hourly_longitudes,
    hourly_latitudes,
    hourly_time,
    precipitation_total_data,
    hourly_junsep_indices,
    hourly_novapr_indices,
    precipitation_mean_data_junsep,
    precipitation_mean_data_novapr,
    precipitation_mean_data_total) = process_merra_data('\\raw_data\\3.3_model_implementation\\precipitation\\', 
                                                seasonal = True, variables = ['PRECTOTCORR'], two_vars = False, 
                                                hourly = True, time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                datatype = 'float32')
    print('processed bias corrected total precipitation raw data')  

    print('processing surface temperature raw data ...')                                                    
    (hourly_longitudes,
    hourly_latitudes,
    hourly_time,
    temperature_total_data,
    hourly_junsep_indices,
    hourly_novapr_indices,
    temperature_mean_data_junsep,
    temperature_mean_data_novapr,
    temperature_mean_data_total) = process_merra_data('\\raw_data\\3.3_model_implementation\\temperature\\', 
                                                seasonal = True, variables = ['TLML'], two_vars = False, 
                                                hourly = True, time_steps = 324360, y_steps = 91, x_steps = 105, 
                                                datatype = 'float32')
    print('processed surface temperature raw data')  

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

    with open(parent_directory + '\\processed_data\\hourly_junsep_indices', 'wb') as pickle_file:
        pickle.dump(hourly_junsep_indices, pickle_file)

    with open(parent_directory + '\\processed_data\\hourly_novapr_indices', 'wb') as pickle_file:
        pickle.dump(hourly_novapr_indices, pickle_file)
    print('saved processed monthly and hourly seasonal indices to \\processed_data')
    
    print('saving processed monthly and hourly geographical and time arrays to \\processed_data ...')
    #save numpy arrays
    #monthly geo and time data
    with open(parent_directory + '\\processed_data\\monthly_longitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, monthly_longitudes)
    
    with open(parent_directory + '\\processed_data\\monthly_latitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, monthly_latitudes)

    with open(parent_directory + '\\processed_data\\monthly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, monthly_time)

    #hourly geo and time data
    with open(parent_directory + '\\processed_data\\hourly_longitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, hourly_longitudes)
    
    with open(parent_directory + '\\processed_data\\hourly_latitudes.npy', 'wb') as numpy_array:
        np.save(numpy_array, hourly_latitudes)

    with open(parent_directory + '\\processed_data\\hourly_time.npy', 'wb') as numpy_array:
        np.save(numpy_array, hourly_time)
    print('saved processed monthly and hourly geographical and time arrays to \\processed_data')


    print('saving processed aod arrays to \\processed_data ...')
    #aod data
    with open(parent_directory + '\\processed_data\\aod_mean_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_mean_data_junsep)
    
    with open(parent_directory + '\\processed_data\\aod_mean_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_mean_data_novapr)

    with open(parent_directory + '\\processed_data\\aod_mean_data_total.npy', 'wb') as numpy_array:
        np.save(numpy_array, aod_mean_data_total)
    print('saved processed aod arrays to \\processed_data')


    "--------------------------------------------------------------------"
    '2.2_outcome_data'
    "--------------------------------------------------------------------"


    print('processing outcome data ...')
    #process and save outcome data
    df_pwt_resid_log, df_wbdi_resid_log, df_mpd_resid_log = process_outcome_data()
    print('processed outcome data')

    print('saving processed outcome data .csv to \\processed_data ...')
    df_pwt_resid_log.to_csv(parent_directory + '\\processed_data\\pwt_resid_log.csv')
    df_wbdi_resid_log.to_csv(parent_directory + '\\processed_data\\wbdi_resid_log.csv')
    df_mpd_resid_log.to_csv(parent_directory + '\\processed_data\\mpd_resid_log.csv')
    print('saved processed outcome data .csv to \\processed_data')


    "--------------------------------------------------------------------"
    '3.1_physical_model'
    "--------------------------------------------------------------------"


    print('saving processed wind arrays to \\processed_data ...')
    #wind data
    with open(parent_directory + '\\processed_data\\wind_eastward_total_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_total_data)
    
    with open(parent_directory + '\\processed_data\\wind_northward_total_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_total_data)

    with open(parent_directory + '\\processed_data\\wind_eastward_mean_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_mean_data_junsep)

    with open(parent_directory + '\\processed_data\\wind_eastward_mean_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_mean_data_novapr)
    
    with open(parent_directory + '\\processed_data\\wind_eastward_mean_data_total.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_eastward_mean_data_total)
    
    with open(parent_directory + '\\processed_data\\wind_northward_mean_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_mean_data_junsep)

    with open(parent_directory + '\\processed_data\\wind_northward_mean_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_mean_data_novapr)
    
    with open(parent_directory + '\\processed_data\\wind_northward_mean_data_total.npy', 'wb') as numpy_array:
        np.save(numpy_array, wind_northward_mean_data_total)
    print('saved processed wind arrays to \\processed_data')

    print('saving processed dust arrays to \\processed_data ...')
    #dust data
    with open(parent_directory + '\\processed_data\\dust_total_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_total_data)
    
    with open(parent_directory + '\\processed_data\\dust_mean_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_mean_data_junsep)

    with open(parent_directory + '\\processed_data\\dust_mean_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_mean_data_novapr)
    
    with open(parent_directory + '\\processed_data\\dust_mean_data_total.npy', 'wb') as numpy_array:
        np.save(numpy_array, dust_mean_data_total)
    print('saved processed dust arrays to \\processed_data')


    "--------------------------------------------------------------------"
    '3.3_model_implementation'
    "--------------------------------------------------------------------"


    print('saving processed precipitation arrays to \\processed_data ...')
    #precipitation data
    with open(parent_directory + '\\processed_data\\precipitation_total_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_total_data)
    
    with open(parent_directory + '\\processed_data\\precipitation_mean_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_mean_data_junsep)

    with open(parent_directory + '\\processed_data\\precipitation_mean_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_mean_data_novapr)
    
    with open(parent_directory + '\\processed_data\\precipitation_mean_data_total.npy', 'wb') as numpy_array:
        np.save(numpy_array, precipitation_mean_data_total)
    print('saved processed precipitation arrays to \\processed_data')

    print('saving processed temperature arrays to \\processed_data ...')
    #temperature data
    with open(parent_directory + '\\processed_data\\temperature_total_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_total_data)
    
    with open(parent_directory + '\\processed_data\\temperature_mean_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_mean_data_junsep)

    with open(parent_directory + '\\processed_data\\temperature_mean_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_mean_data_novapr)
    
    with open(parent_directory + '\\processed_data\\temperature_mean_data_total.npy', 'wb') as numpy_array:
        np.save(numpy_array, temperature_mean_data_total)
    print('saved processed temperature arrays to \\processed_data')


    ######################################################################
    # Running Advection Diffusion Simulation
    ######################################################################
    

    print('running dust advection diffusion simulation ...')
    #create and save simulation data
    min_time = 0
    max_time = dust_total_data.shape[0]
    time_step = (max_time - min_time)
    simulated_dustmass =  advection_diffusion_fd(time_step, 105, 91, min_time, max_time, 91, 105, .4, dust_total_data, wind_eastward_total_data, wind_northward_total_data)
    print('dust advection diffusion simulation terminated sucessfully')


    ######################################################################
    # Saving Advection Diffusion Simulation Data
    ######################################################################

    print('saving simulated dust advection diffusion array to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass)
    print('saved simulated dust advection diffusion array to \\processed_data')

    print('calculating dust advection diffusion simulation total mean...')
    simulated_dustmass_total_mean = np.sum(simulated_dustmass, axis = 0)/simulated_dustmass.shape[0]
    print('calculation terminated succesfully')

    print('saving simulation total mean array to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass_total_mean.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_total_mean)
    print('saved simulation total mean array to \\processed_data')

    print('calculating dust advection diffusion simulation seasonal mean...')
    simulated_dustmass_junsep_mean = np.zeros((91, 105), dtype='float32')
    for i in hourly_junsep_indices:
        simulated_dustmass_junsep_mean += simulated_dustmass[i]
    simulated_dustmass_junsep_mean /= len(hourly_junsep_indices)

    simulated_dustmass_novapr_mean = np.zeros((91, 105), dtype='float32')
    for i in hourly_novapr_indices:
        simulated_dustmass_novapr_mean += simulated_dustmass[i]
    simulated_dustmass_novapr_mean /= len(hourly_novapr_indices)
    print('calculation terminated succesfully')

    print('saving simulation seasonal mean arrays to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass_junsep_mean.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_junsep_mean)

    with open(parent_directory + '\\processed_data\\simulated_dustmass_novapr_mean.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_novapr_mean)
    print('saved simulation seasonal mean arrays to \\processed_data')
    


if __name__ == "__main__":
    main()

