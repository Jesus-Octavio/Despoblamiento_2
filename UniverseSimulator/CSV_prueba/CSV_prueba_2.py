#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 10:27:37 2022

@author: jesus
"""
import time, csv

for i in range(10):
    row = ['1', '2', '3']

    with open('results.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(row)
        csvfile.flush()

    