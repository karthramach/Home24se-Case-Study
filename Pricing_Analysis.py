# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 12:03:42 2022

@author: Karthikeyan
"""

# Importing the libraries
import pandas as pd

# Importing the datasets
Old_Multiplier = pd.read_csv('Old_multiplier.csv', sep=',')
Market_Price = pd.read_csv('MarketPriceSampleCaseStudy.csv', sep=',')

# Splitting the string to extract country code from id column
Market_Price['country'] = Market_Price['id'].str.split('_').str[2]

# Dropping the redundant columns 
Market_Price.drop(['Unnamed: 0', 'id', 'price_rule'], axis = 1, inplace = True)

# Imputing the priceAPI null values with the google shopping price values 
Market_Price['priceAPI'] = Market_Price['priceAPI'].fillna(Market_Price.pop('google_shopping_price'))

# Countrywise old multiplier under main_category granularity level
Old_Multiplier_Main = Old_Multiplier.groupby(['country','main_cat'],as_index=False).agg({'old_mult': "mean"})

# Countrywise old multiplier under sub_category granularity level
Old_Multiplier_Sub = Old_Multiplier.groupby(['country','sub_cat1'],as_index=False).agg({'old_mult': "mean"})

# Grouping Market_Price dataframe and extracting DE country values as a seperate baseline dataframe and merging the two dataframes for further analysis
Market_Price_New = Market_Price.groupby(['country','main_category','sub_category'],as_index=False).agg({'priceAPI': "mean"})

Market_Price_Base = Market_Price_New.loc[Market_Price_New['country'] == 'DE']

Market_Multipliers_New= pd.merge(Market_Price_New, Market_Price_Base, on=['main_category','sub_category'], how='inner')

# Dropping the rows with DE values from the country column as it will be used as a baseline for calculating new multipliers 
Market_Multipliers_New = Market_Multipliers_New.loc[Market_Multipliers_New['country_x'] != 'DE']

# Dropping the redundant columns 
Market_Multipliers_New.drop(['country_y'], axis = 1, inplace = True)

# Calculating the New_Multipliers for all main and sub categories across countries
Market_Multipliers_New['New_Multiplier'] = Market_Multipliers_New['priceAPI_x'] / Market_Multipliers_New['priceAPI_y']

# Countrywise New multiplier under main_category granularity level
Market_Multipliers_New_Main = Market_Multipliers_New.groupby(['country_x','main_category'],as_index=False).agg({'New_Multiplier': "mean"})

# Countrywise New multiplier under main_category granularity level
Market_Multipliers_New_Sub = Market_Multipliers_New.groupby(['country_x','sub_category'],as_index=False).agg({'New_Multiplier': "mean"})

