import os
import pickle
import numpy as np
import pandas as pd

os.environ["PROJ_LIB"] = "C:\\Users\\Daniel\\anaconda3\\Library\\share"; #fixr



from functions import return_region_pixel_array, get_time_span_region_data, get_regional_mean_data, create_lag_regression_data
from functions import daily_dust_country_regression, get_mse_data
from functions import create_population_array, create_population_weight_array
from functions import create_dust_exposure_df, create_multiple_lag_array_from_df, growth_dataframe, country_centroids_one_dim

import warnings
warnings.filterwarnings("ignore")


parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

def main():

    "--------------------------------------------------------------------"
    '3.1_model_implementation'
    "--------------------------------------------------------------------"


    ######################################################################
    # Loading Regression Data
    ######################################################################


    print('loading data ...')
    with open(parent_directory + '\\processed_data\\daily_junsep_indices', 'rb') as pickle_file:
        daily_junsep_indices = pickle.load(pickle_file)
    with open(parent_directory + '\\processed_data\\daily_novapr_indices', 'rb') as pickle_file:
        daily_novapr_indices = pickle.load(pickle_file)

    aod_daily_data = np.load(parent_directory + '\\processed_data\\aod_daily_data.npy') 
    dust_daily_data = np.load(parent_directory + '\\processed_data\\dust_daily_data.npy') 
    dust_daily_data_novapr = np.load(parent_directory + '\\processed_data\\dust_daily_data_novapr.npy') 
    dust_daily_data_junsep = np.load(parent_directory + '\\processed_data\\dust_daily_data_junsep.npy') 
    precipitation_daily_data = np.load(parent_directory + '\\processed_data\\precipitation_daily_data.npy')
    precipitation_daily_data_novapr = np.load(parent_directory + '\\processed_data\\precipitation_daily_data_novapr.npy')
    precipitation_daily_data_junsep = np.load(parent_directory + '\\processed_data\\precipitation_daily_data_junsep.npy')
    temperature_daily_data = np.load(parent_directory + '\\processed_data\\temperature_daily_data.npy')
    temperature_daily_data_novapr = np.load(parent_directory + '\\processed_data\\temperature_daily_data_novapr.npy')
    temperature_daily_data_junsep = np.load(parent_directory + '\\processed_data\\temperature_daily_data_junsep.npy')

    #pm2.5 daily data:
    pm25_daily_data = np.load(parent_directory + '\\processed_data\\pm25_daily_data.npy')


    benin_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_ben.csv')
    burkina_faso_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_bfa.csv')
    gambia_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_gmb.csv')
    ghana_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_gha.csv')
    guinea_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_gin.csv')
    liberia_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_lbr.csv')
    mali_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_mli.csv')
    niger_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_ner.csv')
    nigeria_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_nga.csv')
    senegal_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_sen.csv')
    sierra_leone_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_sle.csv')
    togo_population_df = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\population_estimates\\gpw_v4_admin_unit_center_points_population_estimates_rev11_tgo.csv')

    west_africa_longitudes = np.load(parent_directory + '\\processed_data\\west_africa_longitudes.npy')
    west_africa_latitudes = np.load(parent_directory + '\\processed_data\\west_africa_latitudes.npy')

    df_pwt_growth = pd.read_csv(parent_directory + '\\processed_data\\df_pwt_growth.csv')
    df_wbdi_growth = pd.read_csv(parent_directory + '\\processed_data\\df_wbdi_growth.csv')
    df_mpd_growth = pd.read_csv(parent_directory + '\\processed_data\\df_mpd_growth.csv')

    country_centroids = pd.read_csv(parent_directory + '\\raw_data\\3.3_model_implementation\\country_centroids\\country_centroids.txt', sep='\t')
    print('data loaded successfully')


    ######################################################################
    # Preparing First Togo Coast Pixel Regression Data
    ######################################################################


    print('creating togo coast pixel regression data ...')
    bodele_region_pixels = return_region_pixel_array(region_name='bodele')
    togo_coast_pixel = return_region_pixel_array(region_name='togo_coast')
    daily_bodele_dust_data = get_regional_mean_data(get_time_span_region_data(dust_daily_data, bodele_region_pixels))
    daily_bodele_dust_data_junsep = get_regional_mean_data(get_time_span_region_data(dust_daily_data_junsep, bodele_region_pixels))
    daily_bodele_dust_data_novapr = get_regional_mean_data(get_time_span_region_data(dust_daily_data_novapr, bodele_region_pixels))

    daily_togo_coast_dust_data = get_time_span_region_data(dust_daily_data, togo_coast_pixel)
    daily_togo_precipitation_data = get_time_span_region_data(precipitation_daily_data, togo_coast_pixel)
    daily_togo_temperature_data = get_time_span_region_data(temperature_daily_data, togo_coast_pixel)

    togo_dust_reg_df = create_lag_regression_data(daily_bodele_dust_data, 10, [daily_togo_precipitation_data,daily_togo_temperature_data],
                                            daily_togo_coast_dust_data, daily_junsep_indices, daily_novapr_indices, dataframe=True,
                                            variable_names =   ['wet_season', 'dry_season', 'bod_dust_t-0', 'bod_dust_t-1',
                                                                'bod_dust_t-2', 'bod_dust_t-3','bod_dust_t-4', 'bod_dust_t-5',
                                                                'bod_dust_t-6', 'bod_dust_t-7','bod_dust_t-8', 'bod_dust_t-9',
                                                                'bod_dust_t-10', 'precipitation', 'temperature'],
                                            y_name = 'togo_coast_dust')
    print('created togo coast pixel regression data')


    ######################################################################
    # Running Source-Outcome Regression
    ######################################################################
    
    from functions import daily_dust_regression

    print('running source-outcome regression ...')

    (predicted_daily_dust_data, predicted_daily_dust_data_dry, predicted_daily_dust_data_wet,
     r_squared_map, r_squared_map_dry, r_squared_map_wet) = daily_dust_regression(dust_daily_data, dust_daily_data_junsep, dust_daily_data_novapr, daily_bodele_dust_data,
                                                                                  daily_bodele_dust_data_junsep, daily_bodele_dust_data_novapr, precipitation_daily_data,
                                                                                  precipitation_daily_data_junsep, precipitation_daily_data_novapr, temperature_daily_data,
                                                                                  temperature_daily_data_junsep, temperature_daily_data_novapr, daily_junsep_indices, daily_novapr_indices)

    # predicted_daily_dust_data = np.load(parent_directory + '\\processed_data\\predicted_daily_dust_data.npy')
    # predicted_daily_dust_data_dry = np.load(parent_directory + '\\processed_data\\predicted_daily_dust_data_dry.npy')
    # predicted_daily_dust_data_wet = np.load(parent_directory + '\\processed_data\\predicted_daily_dust_data_wet.npy')
    # r_squared_map = np.load(parent_directory + '\\processed_data\\r_squared_map.npy')
    # r_squared_map_dry = np.load(parent_directory + '\\processed_data\\r_squared_map_dry.npy')
    # r_squared_map_wet = np.load(parent_directory + '\\processed_data\\r_squared_map_wet.npy')
    # mse_array = np.load(parent_directory + '\\processed_data\\mse_array.npy')
    # mse_array_dry = np.load(parent_directory + '\\processed_data\\mse_array_dry.npy')
    # mse_array_wet = np.load(parent_directory + '\\processed_data\\mse_array_wet.npy')

    simulated_dustmass_daily_data = np.load(parent_directory + '\\processed_data\\simulated_dustmass_daily_data.npy')
    
    
    mse_array = get_mse_data(dust_daily_data, predicted_daily_dust_data)
    mse_array_dry = get_mse_data(dust_daily_data_novapr, predicted_daily_dust_data_dry)
    mse_array_wet = get_mse_data(dust_daily_data_junsep, predicted_daily_dust_data_wet)

    mse_array = np.sum(mse_array, axis = 0)/mse_array.shape[0]
    mse_array_dry = np.sum(mse_array_dry, axis = 0)/mse_array_dry.shape[0]
    mse_array_wet = np.sum(mse_array_wet, axis = 0)/mse_array_wet.shape[0]

    print('source-outcome regression completed successfully')


    ######################################################################
    # Preparing Gridded Population of the World Data
    ######################################################################


    print('creating additional gpw data ...')
    population_array = create_population_array([benin_population_df, burkina_faso_population_df, gambia_population_df,
                                            ghana_population_df, guinea_population_df, liberia_population_df,
                                            mali_population_df, niger_population_df, nigeria_population_df,
                                            senegal_population_df,sierra_leone_population_df,togo_population_df],
                                            west_africa_longitudes, west_africa_latitudes)

    temp_pop_array = population_array.copy()
    # population_weigth_array = create_population_weight_array_old(temp_pop_array)
    population_weigth_array = create_population_weight_array(temp_pop_array, ['benin', 'burkina_faso', 'gambia', 'ghana',
                                                                              'guinea', 'liberia','mali', 'niger', 'nigeria',
                                                                              'senegal', 'sierra_leone', 'togo'])

    #create population weight array that only takes the pixels where there actually exists populaton data, the others are set to 'NaN'
    country_population_weigth_array = population_weigth_array
    country_population_weigth_array[country_population_weigth_array == 0] = float("NaN")

    print('created additional gpw data')


    ######################################################################
    # Preparing First Stage Country Level Regression Data
    ######################################################################
    

    print('creating first stage country level regression data ...')

    # weighing variable arrays with popoulation data, including unpopulated areas (set to zero)

    
    aod_daily_data_weighted = aod_daily_data * population_weigth_array
    dust_daily_data_weighted = dust_daily_data * population_weigth_array
    precipitation_daily_data_weighted = precipitation_daily_data * population_weigth_array
    temperature_daily_data_weighted = temperature_daily_data * population_weigth_array

    #pm25 data:
    pm25_daily_data_weighted = pm25_daily_data * population_weigth_array

    # weighing variable arrays with popoulation data, but only for populated areas (see explanation above)
    aod_daily_data_country_weighted = aod_daily_data * country_population_weigth_array
    dust_daily_data_country_weighted = dust_daily_data * country_population_weigth_array
    predicted_daily_dust_data_country_weighted = predicted_daily_dust_data * country_population_weigth_array
    precipitation_daily_data_country_weighted = precipitation_daily_data * country_population_weigth_array
    temperature_daily_data_country_weighted = temperature_daily_data * country_population_weigth_array
    simulated_dustmass_daily_data_country_weighted = simulated_dustmass_daily_data * country_population_weigth_array

    #pm25 data:
    pm25_daily_data_country_weighted = pm25_daily_data * country_population_weigth_array


    # country weighted data:

    from functions import create_dust_exposure_df_country_weighted 

    aod_country_weighted_yearly_df = create_dust_exposure_df_country_weighted(aod_daily_data, aod_daily_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[1]

    aod_country_weighted_dry_season_df = create_dust_exposure_df_country_weighted(aod_daily_data, aod_daily_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[3]

    dust_country_weighted_yearly_df =  create_dust_exposure_df_country_weighted(dust_daily_data, dust_daily_data_country_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                        37, daily_novapr_indices)[1] 

    dust_country_weighted_dry_season_df =  create_dust_exposure_df_country_weighted(dust_daily_data, dust_daily_data_country_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                        37, daily_novapr_indices)[3]                                                                   

    dust_predicted_country_weighted_dry_season_df =  create_dust_exposure_df_country_weighted(predicted_daily_dust_data, predicted_daily_dust_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                          37, daily_novapr_indices)[3]

    dust_simulated_country_weighted_dry_season_df =  create_dust_exposure_df_country_weighted(simulated_dustmass_daily_data, simulated_dustmass_daily_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                          37, daily_novapr_indices)[3]

    precipitation_country_weighted_yearly_df = create_dust_exposure_df_country_weighted(precipitation_daily_data, precipitation_daily_data_country_weighted,
                                                                   ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                    37, daily_novapr_indices)[1]

    temperature_country_weighted_yearly_df = create_dust_exposure_df_country_weighted(temperature_daily_data, temperature_daily_data_country_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                     37, daily_novapr_indices)[1]
    
    precipitation_country_weighted_dry_season_df = create_dust_exposure_df_country_weighted(precipitation_daily_data, precipitation_daily_data_country_weighted,
                                                                   ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                    37, daily_novapr_indices)[3]

    temperature_country_weighted_dry_season_df = create_dust_exposure_df_country_weighted(temperature_daily_data, temperature_daily_data_country_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                     37, daily_novapr_indices)[3]

    #pm25:
    pm25_country_weighted_dry_season_df = create_dust_exposure_df_country_weighted(pm25_daily_data, pm25_daily_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[3]

    # unweighted data

    aod_yearly_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                            ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                'sierra_leone', 'togo'],
                                                37, daily_novapr_indices)[0]

    aod_dry_season_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[2]

    dust_yearly_df =  create_dust_exposure_df(dust_daily_data, dust_daily_data_weighted,
                                            ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                            'liberia','mali', 'niger', 'nigeria', 'senegal',
                                            'sierra_leone', 'togo'],
                                            37, daily_novapr_indices)[0]   

    dust_dry_season_df =  create_dust_exposure_df(dust_daily_data, dust_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                        37, daily_novapr_indices)[2]                                                                   

    precipitation_yearly_df = create_dust_exposure_df(precipitation_daily_data, precipitation_daily_data_weighted,
                                                                   ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                    37, daily_novapr_indices)[0]

    temperature_yearly_df = create_dust_exposure_df(temperature_daily_data, temperature_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                     37, daily_novapr_indices)[0]
    
    precipitation_dry_season_df = create_dust_exposure_df(precipitation_daily_data, precipitation_daily_data_weighted,
                                                                   ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                    37, daily_novapr_indices)[2]

    temperature_dry_season_df = create_dust_exposure_df(temperature_daily_data, temperature_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                     37, daily_novapr_indices)[2]

    #pm25:
    pm25_dry_season_df = create_dust_exposure_df(pm25_daily_data, pm25_daily_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[2]

    pm25_yearly_df = create_dust_exposure_df(pm25_daily_data, pm25_daily_data_country_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[0]


    # reduced form regression aod
    bodele_dry_season_aod_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                                                ['bodele'],
                                                                    37, daily_novapr_indices)[2]

    bodele_dry_season_aod_df = bodele_dry_season_aod_df.transpose()
    # bodele_dry_season_df.insert(loc=0, column='year', value=np.array(list(range(1980,2017))))
    bodele_dry_season_aod_df.index.name = 'year'
    bodele_dry_season_aod_df = bodele_dry_season_aod_df.rename(columns={'bodele': 'bodele_aod_dry'})

    bodele_wet_season_aod_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                                                    ['bodele'],
                                                                        37, daily_junsep_indices)[2]

    bodele_wet_season_aod_df = bodele_wet_season_aod_df.transpose()
    # bodele_wet_season_df.insert(loc=0, column='year', value=np.array(list(range(1980,2017))))
    bodele_wet_season_aod_df.index.name = 'year'
    bodele_wet_season_aod_df.rename(columns={'bodele': 'bodele_aod_wet'})

    bodele_yr_aod_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                                                    ['bodele'],
                                                                        37, daily_junsep_indices)[0]

    bodele_yr_aod_df = bodele_yr_aod_df.transpose()
    # bodele_wet_season_df.insert(loc=0, column='year', value=np.array(list(range(1980,2017))))
    bodele_yr_aod_df.index.name = 'year'
    bodele_yr_aod_df.rename(columns={'bodele': 'bodele_aod_yearly'})



    # reduced form regression pm
    bodele_dry_season_pm25_df = create_dust_exposure_df(pm25_daily_data, pm25_daily_data_weighted,
                                                                ['bodele'],
                                                                    37, daily_novapr_indices)[2]

    bodele_dry_season_pm25_df = bodele_dry_season_pm25_df.transpose()
    # bodele_dry_season_df.insert(loc=0, column='year', value=np.array(list(range(1980,2017))))
    bodele_dry_season_pm25_df.index.name = 'year'
    bodele_dry_season_pm25_df = bodele_dry_season_pm25_df.rename(columns={'bodele': 'bodele_pm25_dry'})

    bodele_wet_season_pm25_df = create_dust_exposure_df(pm25_daily_data, pm25_daily_data_weighted,
                                                                    ['bodele'],
                                                                        37, daily_junsep_indices)[2]

    bodele_wet_season_pm25_df = bodele_wet_season_pm25_df.transpose()
    # bodele_wet_season_df.insert(loc=0, column='year', value=np.array(list(range(1980,2017))))
    bodele_wet_season_pm25_df.index.name = 'year'
    bodele_wet_season_pm25_df.rename(columns={'bodele': 'bodele_pm25_wet'})

    bodele_yr_pm25_df = create_dust_exposure_df(pm25_daily_data, pm25_daily_data,
                                                                    ['bodele'],
                                                                        37, daily_junsep_indices)[0]

    bodele_yr_pm25_df = bodele_yr_pm25_df.transpose()
    # bodele_wet_season_df.insert(loc=0, column='year', value=np.array(list(range(1980,2017))))
    bodele_yr_pm25_df.index.name = 'year'
    bodele_yr_pm25_df.rename(columns={'bodele': 'bodele_pm25_yearly'})



    #country weighted:
    combined_first_stage_df = create_multiple_lag_array_from_df([
                                                        aod_yearly_df,
                                                        aod_dry_season_df,
                                                        aod_country_weighted_yearly_df,
                                                        aod_country_weighted_dry_season_df,
                                                        pm25_dry_season_df,
                                                        pm25_yearly_df,
                                                        pm25_country_weighted_dry_season_df,
                                                        precipitation_country_weighted_dry_season_df,
                                                        temperature_country_weighted_dry_season_df,
                                                        precipitation_dry_season_df,
                                                        temperature_dry_season_df,
                                                        precipitation_country_weighted_yearly_df,
                                                        temperature_country_weighted_yearly_df,
                                                        precipitation_yearly_df,
                                                        temperature_yearly_df,
                                                        dust_yearly_df,
                                                        dust_dry_season_df,
                                                        dust_country_weighted_dry_season_df,
                                                        dust_country_weighted_yearly_df,
                                                        dust_predicted_country_weighted_dry_season_df,
                                                        dust_simulated_country_weighted_dry_season_df],
                                                        5, dataframe = True,
                                                        column_names = ['aod_yr_t-0','aod_yr_t-1','aod_yr_t-2',
                                                                        'aod_yr_t-3','aod_yr_t-4','aod_yr_t-5',
                                                                        'aod_dry_t-0','aod_dry_t-1','aod_dry_t-2',
                                                                        'aod_dry_t-3','aod_dry_t-4','aod_dry_t-5',
                                                                        'aod_wt_yr_t-0','aod_wt_yr_t-1','aod_wt_yr_t-2',
                                                                        'aod_wt_yr_t-3','aod_wt_yr_t-4','aod_wt_yr_t-5',
                                                                        'aod_wt_dry_t-0','aod_wt_dry_t-1','aod_wt_dry_t-2',
                                                                        'aod_wt_dry_t-3','aod_wt_dry_t-4','aod_wt_dry_t-5',
                                                                        'pm25_dry_t-0','pm25_dry_t-1','pm25_dry_t-2',
                                                                        'pm25_dry_t-3','pm25_dry_t-4','pm25_dry_t-5',
                                                                        'pm25_yr_t-0','pm25_yr_t-1','pm25_yr_t-2',
                                                                        'pm25_yr_t-3','pm25_yr_t-4','pm25_yr_t-5',
                                                                        'pm25_wt_dry_t-0','pm25_wt_dry_t-1','pm25_wt_dry_t-2',
                                                                        'pm25_wt_dry_t-3','pm25_wt_dry_t-4','pm25_wt_dry_t-5',
                                                                        'prec_wt_dry_t-0','prec_wt_dry_t-1','prec_wt_dry_t-2',
                                                                        'prec_wt_dry_t-3','prec_wt_dry_t-4','prec_wt_dry_t-5',
                                                                        'temp_wt_dry_t-0','temp_wt_dry_t-1','temp_wt_dry_t-2',
                                                                        'temp_wt_dry_t-3','temp_wt_dry_t-4','temp_wt_dry_t-5',
                                                                        'prec_dry_t-0','prec_dry_t-1','prec_dry_t-2',
                                                                        'prec_dry_t-3','prec_dry_t-4','prec_dry_t-5',
                                                                        'temp_dry_t-0','temp_dry_t-1','temp_dry_t-2',
                                                                        'temp_dry_t-3','temp_dry_t-4','temp_dry_t-5',
                                                                        'prec_wt_yr_t-0','prec_wt_yr_t-1','prec_wt_yr_t-2',
                                                                        'prec_wt_yr_t-3','prec_wt_yr_t-4','prec_wt_yr_t-5',
                                                                        'temp_wt_yr_t-0','temp_wt_yr_t-1','temp_wt_yr_t-2',
                                                                        'temp_wt_yr_t-3','temp_wt_yr_t-4','temp_wt_yr_t-5',
                                                                        'prec_yr_t-0','prec_yr_t-1','prec_yr_t-2',
                                                                        'prec_yr_t-3','prec_yr_t-4','prec_yr_t-5',
                                                                        'temp_yr_t-0','temp_yr_t-1','temp_yr_t-2',
                                                                        'temp_yr_t-3','temp_yr_t-4','temp_yr_t-5',
                                                                        'dust_yr_t-0','dust_yr_t-1','dust_yr_t-2',
                                                                        'dust_dry_t-3','dust_dry_t-4','dust_dry_t-5',
                                                                        'dust_dry_t-0','dust_dry_t-1','dust_dry_t-2',
                                                                        'dust_yr_t-3','dust_yr_t-4','dust_yr_t-5',
                                                                        'dust_wt_dry_t-0','dust_wt_dry_t-1','dust_wt_dry_t-2',
                                                                        'dust_wt_dry_t-3','dust_wt_dry_t-4','dust_wt_dry_t-5',
                                                                        'dust_wt_yr_t-0','dust_wt_yr_t-1','dust_wt_yr_t-2',
                                                                        'dust_wt_yr_t-3','dust_wt_yr_t-4','dust_wt_yr_t-5',
                                                                        'dust_pred_wt_dry_t-0','dust_pred_wt_dry_t-1','dust_pred_wt_dry_t-2',
                                                                        'dust_pred_wt_dry_t-3','dust_pred_wt_dry_t-4','dust_pred_wt_dry_t-5',
                                                                        'dust_sim_wt_dry_t-0','dust_sim_wt_dry_t-1','dust_sim_wt_dry_t-2',
                                                                        'dust_sim_wt_dry_t-3','dust_sim_wt_dry_t-4','dust_sim_wt_dry_t-5'])

    centroids_lat, centroids_lon = country_centroids_one_dim(country_centroids,['benin', 'burkina faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra leone', 'togo'], 37)

    combined_first_stage_df.insert(loc=0, column='pow_year', value=np.array((list(range(1980,2017)) * 12))**2)
    combined_first_stage_df.insert(loc=0, column='year', value=np.array((list(range(1980,2017)) * 12)))
    combined_first_stage_df.insert(loc=0, column='centroid_lon', value = centroids_lon)
    combined_first_stage_df.insert(loc=0, column='centroid_lat', value = centroids_lat)
    combined_first_stage_df.insert(loc=0, column='country', value=[i for i in ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'] for _ in range(37)])

    # combined_first_stage_df_clean = combined_first_stage_df.copy().dropna(how='any')



    ######################################################################
    # Preparing Econometric Model Setup Regression Data
    ######################################################################


    print('creating econometric model setup regression data ...')
    growth_country_level_df = growth_dataframe(df_wbdi_growth, df_mpd_growth, df_pwt_growth, 12, combined_first_stage_df)
    growth_country_level_df = pd.merge(growth_country_level_df, bodele_dry_season_aod_df, on ='year', how='left')
    growth_country_level_df = pd.merge(growth_country_level_df, bodele_wet_season_aod_df, on ='year', how='left')
    growth_country_level_df = pd.merge(growth_country_level_df, bodele_yr_aod_df, on ='year', how='left')

    growth_country_level_df = pd.merge(growth_country_level_df, bodele_dry_season_pm25_df, on ='year', how='left')
    growth_country_level_df = pd.merge(growth_country_level_df, bodele_wet_season_pm25_df, on ='year', how='left')
    growth_country_level_df = pd.merge(growth_country_level_df, bodele_yr_pm25_df, on ='year', how='left')

    

    # growth_country_level_df_clean = growth_country_level_df.copy().dropna(how='any')


    print('created econometric model setup regression data')


    ######################################################################
    # Saving Source-Outcome Regression Data
    ######################################################################


    print('saving togo coast pixel regression data to \\processed_data ...')
    togo_dust_reg_df.to_csv(parent_directory + '\\processed_data\\togo_dust_reg_df.csv')
    del togo_dust_reg_df
    print('saved togo coast pixel regression data to \\processed_data')

    print('saving source-outcome regression data to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\predicted_daily_dust_data.npy', 'wb') as numpy_array:
        np.save(numpy_array, predicted_daily_dust_data)
    del predicted_daily_dust_data

    with open(parent_directory + '\\processed_data\\predicted_daily_dust_data_dry.npy', 'wb') as numpy_array:
        np.save(numpy_array, predicted_daily_dust_data_dry)
    del predicted_daily_dust_data_dry

    with open(parent_directory + '\\processed_data\\predicted_daily_dust_data_wet.npy', 'wb') as numpy_array:
        np.save(numpy_array, predicted_daily_dust_data_wet)
    del predicted_daily_dust_data_wet

    with open(parent_directory + '\\processed_data\\r_squared_map.npy', 'wb') as numpy_array:
        np.save(numpy_array, r_squared_map)
    del r_squared_map

    with open(parent_directory + '\\processed_data\\r_squared_map_dry.npy', 'wb') as numpy_array:
        np.save(numpy_array, r_squared_map_dry)
    del r_squared_map_dry

    with open(parent_directory + '\\processed_data\\r_squared_map_wet.npy', 'wb') as numpy_array:
        np.save(numpy_array, r_squared_map_wet)
    del r_squared_map_wet

    with open(parent_directory + '\\processed_data\\mse_array.npy', 'wb') as numpy_array:
        np.save(numpy_array, mse_array)
    del mse_array

    with open(parent_directory + '\\processed_data\\mse_array_dry.npy', 'wb') as numpy_array:
        np.save(numpy_array, mse_array_dry)
    del mse_array_dry

    with open(parent_directory + '\\processed_data\\mse_array_wet.npy', 'wb') as numpy_array:
        np.save(numpy_array, mse_array_wet)
    del mse_array_wet
    print('saved source-outcome regression data to \\processed_data')
    

    
    ######################################################################
    # Saving GPW Data
    ######################################################################


    print('saving gridded population of the world data to \\processed_data ...')
    with open(parent_directory + '\\processed_data\\population_array.npy', 'wb') as numpy_array:
        np.save(numpy_array, population_array)
    del population_array
    print('saved gridded population of the world data to \\processed_data')


    ######################################################################
    # Saving First Stage Country Level Regression Data
    ######################################################################


    # print('saving first stage country level regression data to \\processed_data ...')
    # combined_first_stage_df.to_csv(parent_directory + '\\processed_data\\combined_first_stage_df.csv')
    # del combined_first_stage_df
    # print('saved first stage country level regression data to \\processed_data')

    # print('saving cleaned first stage country level regression data to \\processed_data ...')
    # combined_first_stage_df_clean.to_csv(parent_directory + '\\processed_data\\combined_first_stage_df_clean.csv')
    # del combined_first_stage_df_clean
    # print('saved cleaned first stage country level regression data to \\processed_data')

    ######################################################################
    # Saving First Stage Country Level Regression Data
    ######################################################################


    print('saving econometric model setup regression data to \\processed_data ...')
    growth_country_level_df.to_csv(parent_directory + '\\processed_data\\growth_country_level_df.csv')
    del growth_country_level_df
    print('saved econometric model setup regression data to \\processed_data')

    # print('saving cleaned econometric model setup regression data to \\processed_data ...')
    # growth_country_level_df_clean.to_csv(parent_directory + '\\processed_data\\growth_country_level_df_clean.csv')
    # del growth_country_level_df_clean
    # print('saved cleaned econometric model setup regression data to \\processed_data')


if __name__ == "__main__":
    main()

