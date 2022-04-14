#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:55:24 2022

@author: Kat
"""

import pandas as pd



link = 'https://raw.githubusercontent.com/KatHusar/CSE5544_Lab3/main/ClimateData.csv' 
df_data = pd.read_csv(link) #read data

#select 2010-2019
years = ['Country\year', '2010', '2011','2012','2013','2014','2015','2016','2017','2018','2019']
df_data = df_data[years]

#select countries
countries = ['United States', 'Russia', 'France', 'Germany', 'Canada', 'Romania', 'Italy', 'Ukraine','United Kingdom','Japan']
df = df_data.loc[df_data['Country\year'].isin(countries)]
df = df.reset_index(drop= True )
df = df.rename(columns={"Country\year": "Country"}, errors="raise")

#save new data
df.to_csv('EmissionsSubset.csv',header= True)