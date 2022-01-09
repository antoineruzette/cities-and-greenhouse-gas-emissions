# Created: 01/05/2021
# Author: Team Somalia

import pandas as pd


def get_data(year, column_name_x, column_name_y):
    """
        Retrieving the emissions from CDP webservice
    """

    # loading data
    emission_2017 = pd.read_csv('https://data.cdp.net/resource/kyi6-dk5h.csv')
    emission_2016 = pd.read_csv('https://data.cdp.net/resource/dfed-thx7.csv')

    # composing the dataframe to be outputted
    df = []

    return df
