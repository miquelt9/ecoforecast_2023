import pandas as pd
import numpy as np
import os
from pytz import timezone
from utils import get_gen_data_from_entsoe, get_load_data_from_entsoe, perform_get_request, xml_to_load_dataframe, xml_to_gen_data
import argparse

RELOAD_L = False
RELOAD_G = False
DEBUG = False

parser = argparse.ArgumentParser()

parser.add_argument("--update_load", action="store_true", help="Set flag_a to False")
parser.add_argument("--update_gen", action="store_true", help="Set flag_a to False")

args = parser.parse_args()

flag_load = args.update_load
flag_gen = args.update_gen

if flag_load:
    RELOAD_L = True

if flag_gen:
    RELOAD_G = True

def most_surplus(l_sp, g_sp, l_uk, g_uk, l_de, g_de, l_dk, g_dk, l_hu, g_hu, l_se, g_se, l_it, g_it, l_po, g_po, l_nl, g_nl):
    diffs = {}
    diffs['sp'] = g_sp - l_sp
    diffs['uk'] = g_uk - l_uk
    diffs['de'] = g_de - l_de
    diffs['dk'] = g_dk - l_dk
    diffs['hu'] = g_hu - l_hu
    diffs['se'] = g_se - l_se
    diffs['it'] = g_it - l_it
    diffs['po'] = g_po - l_po
    diffs['nl'] = g_nl - l_nl
    max_diff = max(diffs, key=diffs.get)
    # max_diff_value = diffs[max_diff]
    # print(diffs)
    # print(max_diff)
    return str(max_diff).upper()
    
def get_country_number(cc):
     return country_codes[cc]

country_codes = {
    "ES": 0,
    "UK": 1,
    "DE": 2,
    "DK": 3,
    "HU": 5,
    "SE": 4,
    "IT": 6,
    "PL": 7,
    "NL": 8,
}

regions = {
    'HU': '10YHU-MAVIR----U',
    'IT': '10YIT-GRTN-----B',
    'PO': '10YPL-AREA-----S',
    'SP': '10YES-REE------0',
    'UK': '10Y1001A1001A92E',
    'DE': '10Y1001A1001A83F',
    'DK': '10Y1001A1001A65H',
    'SE': '10YSE-1--------K',
    'NE': '10YNL----------L',
}

# Create a NumPy array from the country codes dictionary
country_codes_mat = np.array(list(country_codes.values()))

#-----------------------------------------------------------------------------#

# Electricity consumption (load)
if (RELOAD_L):
    print("Retriving load information...")
    get_load_data_from_entsoe(regions)

merged_df = None

for code in regions:
    file_name = "load_" + code + ".csv"
    column_name = "load_" + code
    print("Reading "+ file_name + "...")
    df = pd.read_csv(f'./data/' + file_name)

    if not all(df['UnitName'] == 'MAW'):
                raise Exception("Not all MAW")
            
    selected_columns = ['StartTime', 'Load']
    df = df[selected_columns]
    df['Load'] = df['Load'].astype(float)
    df = df.rename(columns={'StartTime': 'Datetime'})
    df = df.rename(columns={'Load': column_name})

    df['Datetime'] = df['Datetime'].str.replace('T', ' ')
    df['Datetime'] = df['Datetime'].str.replace('Z', '')
    df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True)
    df.set_index('Datetime', inplace=True)
    df_resampled = df.resample('1H').sum()
    df_resampled.reset_index(inplace=True)

    if (DEBUG): print(df_resampled)

    if merged_df is None:
        merged_df = df_resampled.copy()
    else:
        merged_df = pd.merge(merged_df, df_resampled, on='Datetime', how='outer')
    # print(df_resampled)

#-------------------------------------------------------------------------------------------------------------------------#

# Generation by green energies
if (RELOAD_G):
    print("Retriving generation information...")
    get_gen_data_from_entsoe(regions)

green_energies = ["B01", "B09", "B10", "B11", "B12", "B13", "B15", "B16", "B18", "B19"]

for code in regions:
    column_name = "gen_green_" + code
    df_green = None

    for energy in green_energies:
        file_name = "gen_" + code + "_" + energy + ".csv"
        file_path = 'data/' + file_name
        if os.path.exists(file_path):
            print("Reading "+ file_name + "...")
            df = pd.read_csv(file_path)
            if not all(df['UnitName'] == 'MAW'):
                raise Exception("Not all MAW")
            
            selected_columns = ['StartTime', 'quantity']
            df = df[selected_columns]
            df['quantity'] = df['quantity'].astype(float)
            df = df.rename(columns={'StartTime': 'Datetime'})
            df = df.rename(columns={'quantity': 'quantity_' + energy})
            # print(df.columns.to_list())

            if df_green is None:
                    df_green = df.copy()
            else:
                df_green = pd.merge(df_green, df, on='Datetime', how='outer')

        else:
            print("File "+ file_path + " doesn't exist.")
        
    if (DEBUG): print(df_green)
    df_green['Datetime'] = df_green['Datetime'].str.replace('T', ' ')
    df_green['Datetime'] = df_green['Datetime'].str.replace('Z', '')
    df_green['Datetime'] = pd.to_datetime(df_green['Datetime'], utc=True)
    df_green.set_index('Datetime', inplace=True)
    df_green = df_green.resample('1H').sum()
    df_green.reset_index(inplace=True)
    df_green['quantity'] = df_green.filter(like='quantity_').sum(axis=1)
    # Drop individual quantity_*
    df_green = df_green.drop(columns=df_green.filter(like='quantity_').columns)
    df_green = df_green.rename(columns={'quantity': column_name})
    if (DEBUG): print(df_green)

    if merged_df is None:
        merged_df = df_green.copy()
    else:
        merged_df = pd.merge(merged_df, df_green, on='Datetime', how='outer')
    

#---------------------------------------------------------------------------------------#

# load_cols = [col for col in merged_df.columns if col.startswith('load_')]
# merged_df[load_cols] = merged_df[load_cols].shift(1)
merged_df = merged_df.fillna(0)
# merged_df = merged_df.drop(merged_df.index[0]).reset_index(drop=True)


merged_df['country_code'] = np.nan
merged_df['country_num'] = np.nan
for index, row in merged_df.iterrows():
    cc = most_surplus(row['load_SP'], row['gen_green_SP'],	row['load_UK'],	row['gen_green_UK'], row['load_DE'], row['gen_green_DE'], row['load_DK'], row['gen_green_DK'],	row['load_HU'],	row['gen_green_HU'], row['load_SE'], row['gen_green_SE'], row['load_IT'], row['gen_green_IT'], row['load_PO'], row['gen_green_PO'], row['load_NE'], row['gen_green_NE'])
    merged_df.loc[index, 'country_code'] = cc
    merged_df.loc[index, 'country_num'] = get_country_number(cc)

print(merged_df)
merged_df.to_csv("./data/processed_data.csv")
