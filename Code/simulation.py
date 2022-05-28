import os
import pickle
import numpy as np
import pandas as pd


from functions import extract_seasonal_data, hourly_data_to_daily_mean
from functions import advection_diffusion_fd

from functions import simulation_comparison_animation


parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():

    "--------------------------------------------------------------------"
    '3.1_physical_model'
    "--------------------------------------------------------------------"

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

    west_africa_longitudes = np.load(parent_directory + '\\processed_data\\west_africa_longitudes.npy')
    west_africa_latitudes = np.load(parent_directory + '\\processed_data\\west_africa_latitudes.npy')   
    print('data loaded successfully')

    print('running dust advection diffusion simulation ...')
    #create and save simulation data
    min_time = 0
    max_time = dust_hourly_data.shape[0]
    time_step = (max_time - min_time)
    simulated_dustmass_hourly_data =  advection_diffusion_fd(time_step, 105, 91, min_time, max_time, west_africa_latitudes, west_africa_longitudes,
                                                             .4, dust_hourly_data, wind_eastward_hourly_data, wind_northward_hourly_data)
    simulated_dustmass_hourly_novapr_data, simulated_dustmass_hourly_junsep_data = extract_seasonal_data(simulated_dustmass_hourly_data, hourly_novapr_indices, hourly_junsep_indices)
    simulated_dustmass_daily_data = hourly_data_to_daily_mean(simulated_dustmass_hourly_data)
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

    print('saving simulated dust advection diffusion jun-sep array to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\simulated_dustmass_daily_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, simulated_dustmass_daily_data)
    del simulated_dustmass_daily_data
    print('saved simulated dust advection diffusion jun-sep array to \\processed_data')

    print('saving simulated dust advection diffusion comparison video ...')
    # simulation_comparison_animation(simulated_dustmass_hourly_data, dust_hourly_data, west_africa_latitudes, west_africa_longitudes, extent=[-30,29,-15,29],
    #                                 add_source_region = False, borders = True, cbar_min = 0, cbar_max = 7,
    #                                 unit = 10 ** -7, min_time = 9000, max_frames = 999, fpers = 10, save_as = "anim_9000_9999.mp4")
    print('saved simulated dust advection diffusion comparison video')

    

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

