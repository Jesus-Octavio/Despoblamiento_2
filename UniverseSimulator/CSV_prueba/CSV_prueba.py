#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 10:13:17 2022

@author: jesus
"""
import sys
import datetime, time

for i in range(20):
    sys.stdout.flush()
    print("origen;" + "destine;" + str(i) + str(";") +"año")
    
# nohup python3 CSV_prueba.py >  output.csv
