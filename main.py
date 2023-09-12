# This is a sample Python script.
import pandas as pd
import warnings
import re
import os
from datetime import date, datetime, timedelta

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# by importing, the scripts below are executed

import data_collectors # download misc data (in ./data/misc)
import data_aggregation_tools # create aggregated_dataframe (in ./data/) and compare new with previous months' misc data
import numerical_bias_cause_rrc # calculate and save in rrcCdf.json the numerical bias cause for rrcs
import numerical_bias_cause # calculate and save in platfCdf.json the numerical bias cause for platforms (Atlas, RIS etc)
import rrc_distr # calculate and save in ./figures_rrc/ the numerical distributions for rrc
import rrc_distr_categ # calculate and save in ./figures_rrc/ the categorical distributions for rrc
import example_script_calculate_bias # calculate and save in ./figures all the distributions for platforms
import random_sets_bias # calculate random samples' bias for platforms
import insert_in_database # insert in db all the files

today = date.today()
DATE = str(today).replace('-', '')
MISC_PATH = './data/misc'


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':

    # the new agg_df is created in data_aggregation tools, as well as the datacollectors are called there too.

res = os.listdir(MISC_PATH)
# print(res)
# data_aggregation_tools.create_dataframe_from_multiple_datasets(ALL_DATASETS)
# if not COMPARE_DF['warnings'].isnull().all():
#     warnings.warn('AGGREGATED DATAFRAME HAS SOME CHANGES!')
#
# COMPARE_DF.to_csv('df_changes.csv')


# def return_compare_df():
#     return COMPARE_DF, ALL_DATASETS
#
# df = pd.read_csv('df_changes.csv', header=0)
# print(df['Difference in size (current - previous)'])

for fileName in res:
    if 'CTI' not in fileName:
        date = (re.search("([0-9]{2}[0-9]{2}[0-9]{4})", fileName)).group(1)
        # date = fileName.rsplit('(')[1].rsplit(')')[0]
        print(fileName)
        # remove previous month's data
        # if date != DATE:
        #     os.remove(MISC_PATH+'/'+fileName)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
