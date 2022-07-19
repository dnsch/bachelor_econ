import os
import pickle
import numpy as np
import pandas as pd

os.environ["PROJ_LIB"] = "C:\\Users\\Daniel\\anaconda3\\Library\\share"; #fixr


from functions import process_merra_data, process_outcome_data, hourly_data_to_daily_mean, three_hourly_data_to_daily_mean, extract_seasonal_data
from functions import three_hourly_data_to_daily_mean

parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import warnings
warnings.filterwarnings("ignore")

def main():


    ######################################################################
    # Processing MERRA2 Data
    ######################################################################
    with open(parent_directory + '\\processed_data\\daily_novapr_indices', 'rb') as pickle_file:
        daily_novapr_indices = pickle.load(pickle_file)

    with open(parent_directory + '\\processed_data\\daily_junsep_indices', 'rb') as pickle_file:
        daily_junsep_indices = pickle.load(pickle_file)


    "--------------------------------------------------------------------"
    '2.1_dust_data'
    "--------------------------------------------------------------------"

    print('processing hourly pm2.5 components raw data ...')
    #pm2.5

    pm25_hourly_data = np.zeros((324360, 91, 105), dtype='float32')

    bc_hourly_data = process_merra_data('\\raw_data\\test_data\\pm_data\\', 
                                            seasonal_indices = False, variables = ['BCSMASS'], two_vars = False, 
                                            timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                            datatype = 'float32')[3]
    
    pm25_hourly_data += bc_hourly_data

    bc_daily_data = hourly_data_to_daily_mean(bc_hourly_data)

    bc_daily_data_novapr, bc_daily_data_junsep = extract_seasonal_data(bc_daily_data, daily_novapr_indices, daily_junsep_indices)

    with open(parent_directory + '\\processed_data\\bc_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, bc_hourly_data.data)
    with open(parent_directory + '\\processed_data\\bc_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, bc_daily_data.data)
    with open(parent_directory + '\\processed_data\\bc_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, bc_daily_data_novapr.data)
    with open(parent_directory + '\\processed_data\\bc_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, bc_daily_data_junsep.data)
    del bc_hourly_data, bc_daily_data, bc_daily_data_novapr, bc_daily_data_junsep

    oc_hourly_data = process_merra_data('\\raw_data\\test_data\\pm_data\\',
                                            seasonal_indices = False, variables = ['OCSMASS'], two_vars = False, 
                                            timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                            datatype = 'float32')[3]

    pm25_hourly_data += (1.8*oc_hourly_data)

    oc_daily_data = hourly_data_to_daily_mean(oc_hourly_data)

    oc_daily_data_novapr, oc_daily_data_junsep = extract_seasonal_data(oc_daily_data, daily_novapr_indices, daily_junsep_indices)

    with open(parent_directory + '\\processed_data\\oc_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, oc_hourly_data.data)
    with open(parent_directory + '\\processed_data\\oc_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, oc_daily_data.data)
    with open(parent_directory + '\\processed_data\\oc_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, oc_daily_data_novapr.data)
    with open(parent_directory + '\\processed_data\\oc_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, oc_daily_data_junsep.data)
    del oc_hourly_data, oc_daily_data, oc_daily_data_novapr, oc_daily_data_junsep

    dust_hourly_data = np.load(parent_directory + '\\processed_data\\dust_hourly_data.npy')

    pm25_hourly_data += dust_hourly_data
    del dust_hourly_data

    ss_hourly_data = process_merra_data('\\raw_data\\test_data\\pm_data\\',
                                            seasonal_indices = False, variables = ['SSSMASS25'], two_vars = False, 
                                            timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                            datatype = 'float32')[3]

    pm25_hourly_data += ss_hourly_data

    ss_daily_data = hourly_data_to_daily_mean(ss_hourly_data)

    ss_daily_data_novapr, ss_daily_data_junsep = extract_seasonal_data(ss_daily_data, daily_novapr_indices, daily_junsep_indices)

    with open(parent_directory + '\\processed_data\\ss_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, ss_hourly_data.data)
    with open(parent_directory + '\\processed_data\\ss_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, ss_daily_data.data)
    with open(parent_directory + '\\processed_data\\ss_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, ss_daily_data_novapr.data)
    with open(parent_directory + '\\processed_data\\ss_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, ss_daily_data_junsep.data)
    del ss_hourly_data, ss_daily_data, ss_daily_data_novapr, ss_daily_data_junsep                                  

    so4_hourly_data = process_merra_data('\\raw_data\\test_data\\pm_data\\',
                                            seasonal_indices = False, variables = ['SO4SMASS'], two_vars = False, 
                                            timing = 'hourly', time_steps = 324360, y_steps = 91, x_steps = 105, 
                                            datatype = 'float32')[3]

    pm25_hourly_data += (1.375*so4_hourly_data)

    so4_daily_data = hourly_data_to_daily_mean(so4_hourly_data)

    so4_daily_data_novapr, so4_daily_data_junsep = extract_seasonal_data(so4_daily_data, daily_novapr_indices, daily_junsep_indices)

    with open(parent_directory + '\\processed_data\\so4_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, so4_hourly_data.data)
    with open(parent_directory + '\\processed_data\\so4_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, so4_daily_data.data)
    with open(parent_directory + '\\processed_data\\so4_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, so4_daily_data_novapr.data)
    with open(parent_directory + '\\processed_data\\so4_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, so4_daily_data_junsep.data)
    del so4_hourly_data, so4_daily_data, so4_daily_data_novapr, so4_daily_data_junsep  

    pm25_daily_data = hourly_data_to_daily_mean(pm25_hourly_data)

    pm25_daily_data_novapr, pm25_daily_data_junsep = extract_seasonal_data(pm25_daily_data, daily_novapr_indices, daily_junsep_indices)

    print('processed hourly pm2.5 components raw data ...')


    print('saving processed hourly pm2.5 components arrays to \\processed_data ...')
    #pm2.5
    with open(parent_directory + '\\processed_data\\pm25_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, pm25_hourly_data.data)
    del pm25_hourly_data

    with open(parent_directory + '\\processed_data\\pm25_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, pm25_daily_data.data)
    del pm25_daily_data

    with open(parent_directory + '\\processed_data\\pm25_daily_data_novapr.npy', 'wb') as numpy_array:
        np.save(numpy_array, pm25_daily_data_novapr.data)
    del pm25_daily_data_novapr

    with open(parent_directory + '\\processed_data\\pm25_daily_data_junsep.npy', 'wb') as numpy_array:
        np.save(numpy_array, pm25_daily_data_junsep.data)
    del pm25_daily_data_junsep
    print('saved processed hourly pm2.5 components arrays to \\processed_data')



if __name__ == "__main__":
    main()

