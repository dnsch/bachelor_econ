import os
import pickle
import numpy as np
import pandas as pd


from functions import return_region_pixel_array, get_time_span_region_data, get_regional_mean_data, create_lag_regression_data
from functions import daily_dust_country_regression, get_mse_data
from functions import create_population_array, create_population_weight_array
from functions import create_dust_exposure_df, create_multiple_lag_array_from_df, growth_dataframe, country_centroids_one_dim, create_dust_exposure_df_weighted


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
    daily_togo_coast_dust_data = get_time_span_region_data(dust_daily_data, togo_coast_pixel)
    daily_togo_precipitation_data = get_time_span_region_data(precipitation_daily_data, togo_coast_pixel)
    daily_togo_temperature_data = get_time_span_region_data(temperature_daily_data, togo_coast_pixel)

    togo_dust_reg_df = create_lag_regression_data(daily_bodele_dust_data, 10, [daily_togo_precipitation_data,daily_togo_temperature_data],
                                            daily_togo_coast_dust_data, daily_junsep_indices, daily_novapr_indices, dataframe=True,
                                            variable_names =   ['wet_season', 'dry_season', 'bod_aod_t-0', 'bod_aod_t-1',
                                                                'bod_aod_t-2', 'bod_aod_t-3','bod_aod_t-4', 'bod_aod_t-5',
                                                                'bod_aod_t-6', 'bod_aod_t-7','bod_aod_t-8', 'bod_aod_t-9',
                                                                'bod_aod_t-10', 'precipitation', 'temperature'],
                                            y_name = 'togo_coast_aod')
    print('created togo coast pixel regression data')


    ######################################################################
    # Running Source-Outcome Regression
    ######################################################################
    
    from functions import daily_dust_regression

    print('running source-outcome regression ...')
    # predicted_daily_dust_data, r_squared_map = daily_dust_regression(dust_daily_data, daily_bodele_dust_data, precipitation_daily_data,
    #                                                                  temperature_daily_data, daily_junsep_indices, daily_novapr_indices)

    predicted_daily_dust_data = np.load(parent_directory + '\\processed_data\\predicted_daily_dust_data.npy') 
    r_squared_map = np.load(parent_directory + '\\processed_data\\r_squared_map_dust.npy') 
    
    mse_array = get_mse_data(dust_daily_data, predicted_daily_dust_data)

    mse_array = np.sum(mse_array, axis = 0)/mse_array.shape[0]
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
    predicted_daily_dust_data_weighted = predicted_daily_dust_data * population_weigth_array
    precipitation_daily_data_weighted = precipitation_daily_data * population_weigth_array
    temperature_daily_data_weighted = temperature_daily_data * population_weigth_array

    # weighing variable arrays with popoulation data, but only for populated areas (see explanation above)
    aod_daily_data_country_weighted = aod_daily_data * country_population_weigth_array
    dust_daily_data_country_weighted = dust_daily_data * country_population_weigth_array
    predicted_daily_dust_data_country_weighted = predicted_daily_dust_data * country_population_weigth_array
    precipitation_daily_data_country_weighted = precipitation_daily_data * country_population_weigth_array
    temperature_daily_data_country_weighted = temperature_daily_data * country_population_weigth_array

    # population_weigth_array = create_population_weight_array_old(population_array)

    # create additional data for dry season regression

    # weighted data:
    
    aod_weighted_dry_season_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[3]

    dust_weighted_dry_season_df =  create_dust_exposure_df(dust_daily_data, dust_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                        37, daily_novapr_indices)[3]                                                                   

    dust_predicted_weighted_dry_season_df =  create_dust_exposure_df(predicted_daily_dust_data, predicted_daily_dust_data_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                          37, daily_novapr_indices)[3]

    precipitation_weighted_yearly_df = create_dust_exposure_df(precipitation_daily_data, precipitation_daily_data_weighted,
                                                                   ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                    37, daily_novapr_indices)[1]

    temperature_weighted_yearly_df = create_dust_exposure_df(temperature_daily_data, temperature_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                     37, daily_novapr_indices)[1]
    
    precipitation_weighted_dry_season_df = create_dust_exposure_df(precipitation_daily_data, precipitation_daily_data_weighted,
                                                                   ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                    37, daily_novapr_indices)[3]

    temperature_weighted_dry_season_df = create_dust_exposure_df(temperature_daily_data, temperature_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                     37, daily_novapr_indices)[3]

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

    # unweighted data

    aod_dry_season_df = create_dust_exposure_df(aod_daily_data, aod_daily_data_weighted,
                                                                        ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                         37, daily_novapr_indices)[2]

    dust_dry_season_df =  create_dust_exposure_df(dust_daily_data, dust_daily_data_weighted,
                                                                    ['benin', 'burkina_faso', 'gambia', 'ghana', 'guinea',
                                                                         'liberia','mali', 'niger', 'nigeria', 'senegal',
                                                                         'sierra_leone', 'togo'],
                                                                        37, daily_novapr_indices)[2]                                                                   

    dust_predicted_dry_season_df =  create_dust_exposure_df(predicted_daily_dust_data, predicted_daily_dust_data_weighted,
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

    #country weighted:
    combined_first_stage_df = create_multiple_lag_array_from_df([aod_country_weighted_yearly_df,
                                                        aod_country_weighted_dry_season_df,
                                                        precipitation_country_weighted_dry_season_df,
                                                        temperature_country_weighted_dry_season_df,
                                                        precipitation_dry_season_df,
                                                        temperature_dry_season_df,
                                                        precipitation_country_weighted_yearly_df,
                                                        temperature_country_weighted_yearly_df,
                                                        precipitation_yearly_df,
                                                        temperature_yearly_df,
                                                        dust_country_weighted_dry_season_df,
                                                        dust_country_weighted_yearly_df,
                                                        dust_predicted_country_weighted_dry_season_df],
                                                        5, dataframe = True,
                                                        column_names = ['aod_wt_yr_t-0','aod_wt_yr_t-1','aod_wt_yr_t-2',
                                                                        'aod_wt_yr_t-3','aod_wt_yr_t-4','aod_wt_yr_t-5',
                                                                        'aod_wt_dry_t-0','aod_wt_dry_t-1','aod_wt_dry_t-2',
                                                                        'aod_wt_dry_t-3','aod_wt_dry_t-4','aod_wt_dry_t-5',
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
                                                                        'dust_wt_dry_t-0','dust_wt_dry_t-1','dust_wt_dry_t-2',
                                                                        'dust_wt_dry_t-3','dust_wt_dry_t-4','dust_wt_dry_t-5',
                                                                        'dust_wt_yr_t-0','dust_wt_yr_t-1','dust_wt_yr_t-2',
                                                                        'dust_wt_yr_t-3','dust_wt_yr_t-4','dust_wt_yr_t-5',
                                                                        'dust_pred_wt_dry_t-0','dust_pred_wt_dry_t-1','dust_pred_wt_dry_t-2',
                                                                        'dust_pred_wt_dry_t-3','dust_pred_wt_dry_t-4','dust_pred_wt_dry_t-5',])

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
    
    combined_first_stage_df_clean = combined_first_stage_df.copy().dropna(how='any')



    ######################################################################
    # Preparing Econometric Model Setup Regression Data
    ######################################################################


    print('creating econometric model setup regression data ...')
    growth_country_level_df = growth_dataframe(df_wbdi_growth, df_mpd_growth, df_pwt_growth, 12, combined_first_stage_df)
    growth_country_level_df_clean = growth_country_level_df.copy().dropna(how='any')


    print('created econometric model setup regression data')


    ######################################################################
    # Saving Source-Outcome Regression Data
    ######################################################################


    print('saving togo coast pixel regression data to \\processed_data ...')
    togo_dust_reg_df.to_csv(parent_directory + '\\processed_data\\togo_dust_reg_df.csv')
    del togo_dust_reg_df
    print('saved togo coast pixel regression data to \\processed_data')

    print('saving source-outcome regression data to \\processed_data ...')
    # with open(parent_directory + '\\processed_data\\predicted_daily_dust_data.npy', 'wb') as numpy_array:
    #     np.save(numpy_array, predicted_daily_dust_data)
    # del predicted_daily_dust_data

    # with open(parent_directory + '\\processed_data\\r_squared_map.npy', 'wb') as numpy_array:
    #     np.save(numpy_array, r_squared_map)
    # del r_squared_map

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


    ######################################################################
    # Saving First Stage Country Level Regression Data
    ######################################################################


    print('saving first stage country level regression data to \\processed_data ...')
    combined_first_stage_df.to_csv(parent_directory + '\\processed_data\\combined_first_stage_df.csv')
    del combined_first_stage_df
    print('saved first stage country level regression data to \\processed_data')

    print('saving cleaned first stage country level regression data to \\processed_data ...')
    combined_first_stage_df_clean.to_csv(parent_directory + '\\processed_data\\combined_first_stage_df_clean.csv')
    del combined_first_stage_df_clean
    print('saved cleaned first stage country level regression data to \\processed_data')

    ######################################################################
    # Saving First Stage Country Level Regression Data
    ######################################################################


    print('saving econometric model setup regression data to \\processed_data ...')
    growth_country_level_df.to_csv(parent_directory + '\\processed_data\\growth_country_level_df.csv')
    del growth_country_level_df
    print('saved econometric model setup regression data to \\processed_data')

    print('saving cleaned econometric model setup regression data to \\processed_data ...')
    growth_country_level_df_clean.to_csv(parent_directory + '\\processed_data\\growth_country_level_df_clean.csv')
    del growth_country_level_df_clean
    print('saved cleaned econometric model setup regression data to \\processed_data')


if __name__ == "__main__":
    main()

