#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 21:52:38 2022

@author: jesus
"""

from joblib import dump, load
import keras
import tensorflow as tf
 

import tkinter as tk
from tkinter import messagebox
import sys
from PIL import ImageTk, Image
from paho.mqtt.client import Client 
from time import sleep

from Universe import Universe
from PopulationCentre import PopulationCentre
from LargeCity import LargeCity
from Agents import Agents
from Family_version_3 import Fam_one_person
from Family_version_3 import Fam_kids


from SeaofBTCapp import Pages
from SeaofBTCapp import SeaofBTCapp
from SeaofBTCapp import StartPage
from SeaofBTCapp import PageOne
from SeaofBTCapp import PopulationCentrePage
from SeaofBTCapp import YearsPage
from SeaofBTCapp import PlotPage

import pandas as pd
import numpy as np
  
          
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import plotly.offline as py
import sys

     
if __name__ == "__main__":
    
    year             = 2010
    
    # COMARCA 2
    path             = "Dominio/Comarca_2/"
    df_historic_ages = pd.read_csv(path + "df_2_historic_ages.csv")
    df_families      = pd.read_csv(path + "df_2_families.csv")
    df_features      = pd.read_csv(path + "df_2_infra_coords_normal.csv")
    df_income_spend  = pd.read_csv(path + "df_2_income_spend_normal.csv") 
    
    
    df_features_large_cities     = pd.read_csv(path + "df_large_cities_infra_coords_normal.csv")
    df_income_spend_large_cities = pd.read_csv(path + "df_large_cities_income_spend_normal.csv")
    
    path = "Modelos/"
    #keras.models.load_model
    natality_model  = keras.models.load_model(path + "natality_model_subset_ann.h5")
    mortality_model = load(path + "mortality_model_subset_linreg.joblib")
    
    # betas: list of 11
    #beta_mdt, beta_pendi, beta_carretn, beta_aut,
    #beta_ferr, beta_dis10m, beta_hospi, beta_farma,
    #beta_ceduc, beta_curgh, beta_arptim
    
    # gamma: parameter for subjective norm
                 
    my_universe = Universe(year                         = year,
                           df_historic_ages             = df_historic_ages,
                           df_families                  = df_families,
                           df_features                  = df_features,
                           df_income_spend              = df_income_spend,
                           df_features_large_cities     = df_features_large_cities,
                           df_income_spend_large_cities = df_income_spend_large_cities,
                           betas  = list(np.random.uniform(0, 1, 11)),
                           gamma  = np.random.uniform(0, 1),
                           theta  = np.random.uniform(0, 1),
                           alphas = list(np.random.uniform(0, 1, 3)),
                           natality_model  = natality_model,
                           mortality_model = mortality_model)
    my_universe.Print()

    
        
    for i in range(1, 5):
        my_universe.update()
        #my_universe.Print()
    
    
    #my_universe.regression_metrics()
    app = SeaofBTCapp(universe = my_universe)
    app.mainloop()
       
#app = SeaofBTCapp()
#app.mainloop()