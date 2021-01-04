import requests
import json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

food_list = ['albanese gummi bears', 'wild roots omega powerhouse trail mix']
api_key = 'empty'

# Search each entry in top_products_by_aisle by USDA database through API
def fdcID_retrieval(food_to_search, branded=True, api_key=api_key):
    '''
    This function uses USDA's REST access API to retrieve
    information from FoodData Central (https://fdc.nal.usda.gov/).
    This function returns the FDCID for the item searched by attempting to
    retrieve the closest match by using Levenshtein distance calculations.
    An API key is required for use and can be acquired for free, here:
    https://fdc.nal.usda.gov/api-key-signup.html

    Parameters
    ----------
    food_to_search : list
        A list of strings of foods
    branded : flag
        Whether or not we want to search branded food

    Returns
    -------
    fdcIDs : list
        The most likely FDCIDs for the food items searched.
    '''
    # set API details
    requested_url = 'https://api.nal.usda.gov/fdc/v1/search?api_key='
    headers = {'Content-Type': 'application/json'}
    # onitiate pull
    fdcIDs = []  # container for results
    # for each item in the list
    for item in food_to_search:
        # pull item in list
        data = {"generalSearchInput": item}
        # convert to json format
        data_str = json.dumps(data).encode("utf-8")
        # commit an API request for the item
        response = requests.post(requested_url + api_key, headers=headers, data=data_str)
        # parse the generated data
        parsed = json.loads(response.content)
        # set up metrics for eventual item selection
        best_idx = None
        best_ratio = 0
        # for each item in the generated data
        for idx, i in enumerate(parsed['foods']):
            # if we are looking for a branded item
            if branded is True:
                # try condition for non-branded food
                try:
                    # use a flexibile levenshtein distance to compare
                    curr_ratio = fuzz.token_set_ratio(item, i['brandOwner'] + ' ' + i['description'])
                    # if we find better matches for what we are looking for
                    if curr_ratio > best_ratio:
                        # record them
                        best_idx = idx
                        best_ratio = curr_ratio
                except:
                    # in case of error/no result, pass
                    pass
            # if we are not looking for a branded item
            if branded is False:
                # do the same as above
                try:
                    curr_ratio = fuzz.token_set_ratio(item, i['description'])
                    if curr_ratio > best_ratio:
                        best_idx = idx
                        best_ratio = curr_ratio
                except:
                    pass
        # save the best performing item as the most likely match from the db
        fdcIDs.append(parsed['foods'][best_idx]['fdcId'])
    return fdcIDs

fdcIDs = fdcID_retrieval(food_list)


def nutrition_retrieval(fdcIDs, api_key=api_key):
    ''' This function collects nutritional data for each FDCID.
    It does so by making calls to the USDA database,
    FoodData Central (https://fdc.nal.usda.gov/), and it
    then retrieves the returned JSON data for the relevant nutritional data.

    Parameters
    ----------
    fdcIDs : list
        A list of FDCIDs that we want nutrition data for
    api_key : string
        Our API key

    Returns
    -------
    nutrient_df : pandas data frame
        A data frame containing our results
    '''

    # Set container storage and ordering
    nutrient_container = []
    nutrient_list = ['trans_fat', 'sat_fat', 'cholesterol', 'sodium',
    'carbs', 'fiber','sugars', 'protein', 'vit_a', 'vit_c', 'calcium',
    'iron', 'fdcID']
    nutrient_container.append(nutrient_list)

    # set API details
    USDA_URL = 'https://api.nal.usda.gov/fdc/v1/'
    headers = {'Content-Type': 'application/json'}
    # 'https://api.nal.usda.gov/fdc/v1/478834?api_key=dvCyz1caFZ12A2Q04pm7ZQ9b9Z8h4pcK7dl4GI8K'
    # Loop over each FDCID; commit a API request for each
    for i in fdcIDs:
        fdcId = str(i)
        requested_url = USDA_URL + fdcId + '?api_key=' + api_key
        response = requests.get(requested_url, headers=headers)
        parsed = json.loads(response.content)
        trans_fat = 0
        trans_fat_poly = 0
        trans_fat_mono = 0
        sat_fat = 0
        cholesterol = 0
        sodium = 0
        carbs = 0
        fiber = 0
        sugars = 0
        protein = 0
        vit_a = 0
        vit_c = 0
        calcium = 0
        iron = 0
        energy = 0
        fdc_id = i
        # Loop over dictionary length to look for desired data
        for j in range(0, len(parsed)):
            try:
                if parsed['foodNutrients'][j]['nutrient']['id'] == 1257:
                    trans_fat = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1293:
                    trans_fat_poly = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1292:
                    trans_fat_mono = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1258:
                    sat_fat = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1253:
                    cholesterol = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1093:
                    sodium = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1005:
                    carbs = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1079:
                    fiber = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 2000:
                    sugars = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1003:
                    protein = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1104:
                    vit_a = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1162:
                    vit_c = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1087:
                    calcium = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1089:
                    iron = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1008:
                    energy = parsed['foodNutrients'][j]['amount']
            # In case of nutrition not found; continue anyways
            except:
                    pass

        # combine fats
        trans_fat = trans_fat + trans_fat_poly + trans_fat_mono

        # append data
        nutrient_container.append([trans_fat, sat_fat, cholesterol,
        sodium, carbs, fiber, sugars, protein, vit_a, vit_c,
        calcium, iron, energy, fdc_id])

        # turn nutrient_list into df for preprocessing
        nutrient_df = pd.DataFrame(data=nutrient_container[1::],
                                   columns=['trans_fat', 'sat_fat',
                                            'cholesterol', 'sodium', 'carbs',
                                            'fiber', 'sugars', 'protein',
                                            'vit_a', 'vit_c', 'calcium',
                                            'iron', 'energy', 'fdcID'])

    return nutrient_df


nutrient_df = nutrition_retrieval(fdcIDs=fdcIDs, api_key=api_key)


# Preprocess the nutrient data
def nutrient_preprocessing(dataframe):
    ''' This function preprocesses the nutrient data by converting each
    nutrient to a common base of 1 kcal.

    Parameters
    ----------
    dataframe : pandas data frame
        A data frame containing un-scaled nutritional data

    Returns
    -------
    dataframe : pandas data frame
        A data frame containing scaled nutritional data
    '''

    # Convert nutrients to base 1 energy
    dataframe['protein'] = dataframe['protein'] / dataframe['energy']
    dataframe['fiber'] = dataframe['fiber'] / dataframe['energy']
    dataframe['trans_fat'] = dataframe['trans_fat'] / dataframe['energy']
    dataframe['sat_fat'] = dataframe['sat_fat'] / dataframe['energy']
    dataframe['sugars'] = dataframe['sugars'] / dataframe['energy']

    dataframe['calcium'] = dataframe['calcium'] / dataframe['energy']
    dataframe['vit_c'] = dataframe['vit_c'] / dataframe['energy']
    dataframe['sodium'] = dataframe['sodium'] / dataframe['energy']

    return dataframe

nutrient_df = nutrient_preprocessing(nutrient_df)
