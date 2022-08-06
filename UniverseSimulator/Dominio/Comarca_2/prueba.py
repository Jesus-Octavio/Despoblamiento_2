#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 17:20:39 2022

@author: jesus
"""

import pandas as pd
df = pd.read_csv("df_distances_2_large_cities.csv", index_col = 0)
print(df)
temp = pd.DataFrame(df.loc[[39017]]) 
print(temp)
print(temp["39027"])