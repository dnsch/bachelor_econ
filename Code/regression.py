import os
import pickle
import numpy as np
import pandas as pd


from functions import return_region_pixel_array, get_time_span_region_data, get_regional_mean_data, create_lag_regression_data
from functions import daily_dust_country_regression, get_mse_data
from functions import create_population_array, create_population_weigth_array


parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():

    "--------------------------------------------------------------------"
    '3.1_model_implementation'
    "--------------------------------------------------------------------"


    ######################################################################
    # Preparing First Togo Coast Pixel Regression Data
    ######################################################################


    print('loading data ...')
    with open(parent_directory + '\\processed_data\\daily_junsep_indices', 'rb') as pickle_file:
        daily_junsep_indices = pickle.load(pickle_file)
    with open(parent_directory + '\\processed_data\\daily_novapr_indices', 'rb') as pickle_file:
        daily_novapr_indices = pickle.load(pickle_file)

    aod_daily_data = np.load(parent_directory + '\\processed_data\\aod_daily_data.npy') 
    precipitation_daily_data = np.load(parent_directory + '\\processed_data\\precipitation_daily_data.npy')
    temperature_daily_data = np.load(parent_directory + '\\processed_data\\temperature_daily_data.npy')

    benin_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_ben.csv')
    burkina_faso_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_bfa.csv')
    gambia_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_gmb.csv')
    ghana_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_gha.csv')
    guinea_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_gin.csv')
    liberia_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_lbr.csv')
    mali_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_mli.csv')
    niger_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_ner.csv')
    nigeria_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_nga.csv')
    sierra_leone_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_sle.csv')
    senegal_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_sen.csv')
    togo_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_tgo.csv')

    west_africa_longitudes = np.load(parent_directory + '\\processed_data\\west_africa_longitudes.npy')
    west_africa_latitudes = np.load(parent_directory + '\\processed_data\\west_africa_latitudes.npy')
    print('data loaded successfully')

    print('creating togo coast pixel regression data...')
    bodele_region_pixels = return_region_pixel_array(region_name='bodele')
    togo_coast_pixel = return_region_pixel_array(region_name='togo_coast')
    daily_bodele_aod_data = get_regional_mean_data(get_time_span_region_data(aod_daily_data, bodele_region_pixels))
    daily_togo_coast_aod_data = get_time_span_region_data(aod_daily_data, togo_coast_pixel)
    daily_togo_precipitation_data = get_time_span_region_data(precipitation_daily_data, togo_coast_pixel)
    daily_togo_temperature_data = get_time_span_region_data(temperature_daily_data, togo_coast_pixel)

    aod_reg_df = create_lag_regression_data(daily_bodele_aod_data, 10, [daily_togo_precipitation_data,daily_togo_temperature_data],
                                            daily_togo_coast_aod_data, daily_junsep_indices, daily_novapr_indices, dataframe=True,
                                            variable_names =   ['wet_season', 'dry_season', 'bod_aod_t-0', 'bod_aod_t-1',
                                                                'bod_aod_t-2', 'bod_aod_t-3','bod_aod_t-4', 'bod_aod_t-5',
                                                                'bod_aod_t-6', 'bod_aod_t-7','bod_aod_t-8', 'bod_aod_t-9',
                                                                'bod_aod_t-10', 'precipitation', 'temperature'],
                                            y_name = 'togo_coast_aod')
    print('created togo coast pixel regression data')


    ######################################################################
    # Running Source-Outcome Regression
    ######################################################################
    

    print('running source-outcome regression')
    predicted_daily_aod_data, r_squared_map = daily_dust_country_regression(aod_daily_data, daily_bodele_aod_data, precipitation_daily_data,
                                                                            temperature_daily_data, daily_junsep_indices, daily_novapr_indices,
                                                                            ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea', 'liberia',
                                                                            'mali', 'niger', 'nigeria', 'sierra_leone', 'senegal', 'togo'])

    mse_array = get_mse_data(aod_daily_data, predicted_daily_aod_data, 
                             ['benin', 'burkina_faso', 'gambia', 'ghana',
                             'guinea', 'liberia','mali', 'niger', 'nigeria',
                             'sierra_leone', 'senegal', 'togo'])
    mse_array = np.sum(mse_array, axis = 0)/mse_array.shape[0]
    print('source-outcome regression completed succesfully')


    ######################################################################
    # Preparing Gridded Population of the World Data
    ######################################################################


    print('loading gpw data ...')
   
    print('gpw data loaded successfully')

    print('creating additional gpw data ...')
    population_array = create_population_array([benin_population_df, burkina_faso_population_df, gambia_population_df,
                                            ghana_population_df, guinea_population_df, liberia_population_df,
                                            mali_population_df, niger_population_df, nigeria_population_df,
                                            sierra_leone_population_df, senegal_population_df, togo_population_df],
                                            west_africa_longitudes, west_africa_latitudes)

    # population_weigth_array = create_population_weigth_array(population_array)
    print('created additional gpw data ...')

    ######################################################################
    # Saving Regression Data
    ######################################################################


    print('saving togo coast pixel regression data to \\processed_data ...')
    aod_reg_df.to_csv(parent_directory + '\\processed_data\\aod_reg_df.csv')
    del aod_reg_df
    print('saved togo coast pixel regression data to \\processed_data')

    print('saving source-outcome regression data to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\predicted_daily_aod_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, predicted_daily_aod_data)
    del predicted_daily_aod_data

    with open(parent_directory + '\\processed_data\\r_squared_map.npy', 'wb') as numpy_array:
        np.save(numpy_array, r_squared_map)
    del r_squared_map

    with open(parent_directory + '\\processed_data\\mse_array.npy', 'wb') as numpy_array:
        np.save(numpy_array, mse_array)
    del mse_array
    print('saved source-outcome regression data to \\processed_data')

    
    ######################################################################
    # Saving GPW Data
    ######################################################################

    print('saving gridded population of the world data to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\population_array.npy', 'wb') as numpy_array:
        np.save(numpy_array, population_array)
    del population_array
    print('saved gridded population of the world data to \\processed_data')


if __name__ == "__main__":
    main()

