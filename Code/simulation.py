import os
import pickle
import numpy as np
import pandas as pd


from functions import extract_seasonal_data
from functions import advection_diffusion_fd


parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():

    ######################################################################
    # Running Advection Diffusion Simulation
    ######################################################################


    print('loading data ...')
    with open(parent_directory + '\\processed_data\\hourly_junsep_indices', 'rb') as pickle_file:
        hourly_junsep_indices = pickle.load(pickle_file)
    with open(parent_directory + '\\processed_data\\hourly_novapr_indices', 'rb') as pickle_file:
        hourly_novapr_indices = pickle.load(pickle_file)

    dust_hourly_data = np.load(parent_directory + '\\processed_data\\dust_hourly_data.npy') 
    wind_eastward_hourly_data = np.load(parent_directory + '\\processed_data\\wind_eastward_hourly_data.npy')
    wind_northward_hourly_data = np.load(parent_directory + '\\processed_data\\wind_northward_hourly_data.npy')
    print('data loaded successfully')

    print('running dust advection diffusion simulation ...')
    #create and save simulation data
    min_time = 0
    max_time = dust_hourly_data.shape[0]
    time_step = (max_time - min_time)
    simulated_dustmass_hourly_data =  advection_diffusion_fd(time_step, 105, 91, min_time, max_time, 91, 105, .4, dust_hourly_data, wind_eastward_hourly_data, wind_northward_hourly_data)
    simulated_dustmass_hourly_novapr_data, simulated_dustmass_hourly_junsep_data = extract_seasonal_data(simulated_dustmass_hourly_data, hourly_novapr_indices, hourly_junsep_indices)
    print('dust advection diffusion simulation terminated successfully')


    ######################################################################
    # Saving Advection Diffusion Simulation Data
    ######################################################################

    print('saving simulated dust advection diffusion array to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass_hourly_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_hourly_data)
    del simulated_dustmass_hourly_data
    print('saved simulated dust advection diffusion array to \\processed_data')

    print('saving simulated dust advection diffusion nov-apr array to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass_hourly_novapr_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_hourly_novapr_data)
    del simulated_dustmass_hourly_novapr_data
    print('saved simulated dust advection diffusion nov-apr array to \\processed_data')

    print('saving simulated dust advection diffusion jun-sep array to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass_hourly_junsep_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_hourly_junsep_data)
    del simulated_dustmass_hourly_junsep_data
    print('saved simulated dust advection diffusion jun-sep array to \\processed_data')

    # print('calculating dust advection diffusion simulation total mean...')
    # simulated_dustmass_total_mean = np.sum(simulated_dustmass, axis = 0)/simulated_dustmass.shape[0]
    # print('calculation terminated succesfully')

    # print('saving simulation total mean array to \\processed_data ...')
    # with open(parent_directory + '\\processed_data\\simulated_dustmass_total_mean.npy', 'wb') as numpy_array:
    #     np.save(numpy_array, simulated_dustmass_total_mean)
    # print('saved simulation total mean array to \\processed_data')

    # print('calculating dust advection diffusion simulation seasonal mean...')
    # simulated_dustmass_junsep_mean = np.zeros((91, 105), dtype='float32')
    # for i in hourly_junsep_indices:
    #     simulated_dustmass_junsep_mean += simulated_dustmass[i]
    # simulated_dustmass_junsep_mean /= len(hourly_junsep_indices)

    # simulated_dustmass_novapr_mean = np.zeros((91, 105), dtype='float32')
    # for i in hourly_novapr_indices:
    #     simulated_dustmass_novapr_mean += simulated_dustmass[i]
    # simulated_dustmass_novapr_mean /= len(hourly_novapr_indices)
    # print('calculation terminated succesfully')

    # print('saving simulation seasonal mean arrays to \\processed_data ...')
    # with open(parent_directory + '\\processed_data\\simulated_dustmass_junsep_mean.npy', 'wb') as numpy_array:
    #     np.save(numpy_array, simulated_dustmass_junsep_mean)

    # with open(parent_directory + '\\processed_data\\simulated_dustmass_novapr_mean.npy', 'wb') as numpy_array:
    #     np.save(numpy_array, simulated_dustmass_novapr_mean)
    # print('saved simulation seasonal mean arrays to \\processed_data')
    


if __name__ == "__main__":
    main()

