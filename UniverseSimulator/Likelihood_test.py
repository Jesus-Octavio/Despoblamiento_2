#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 12:26:12 2022

@author: jesus
"""

from scipy import stats
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel
from Universe import Universe

from joblib import dump, load

 

import tkinter as tk
from tkinter import messagebox
import sys
from PIL import ImageTk, Image
from paho.mqtt.client import Client 
from time import sleep

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



class MyLikelihood(GenericLikelihoodModel):
    
    def __init__(self, endog, exog, **kwds):
        super(MyLikelihood, self).__init__(endog, exog, **kwds)

    def loglike(self, params):
        Y = self.endog
        X = self.exog
        my_universe = Universe(year                     = year,
                           df_historic_ages             = df_historic_ages,
                           df_families                  = df_families,
                           df_features                  = df_features,
                           df_income_spend              = df_income_spend,
                           #df_features_large_cities     = df_features_large_cities,
                           #df_income_spend_large_cities = df_income_spend_large_cities,
                           df_social                    = df_social,
                           df_distances                 = df_distances,
                           betas  = params[0:3],
                           gamma  = params[3],
                           theta  = params[4],
                           alphas = params[5:],
                           natality_model  = natality_model,
                           mortality_model = mortality_model)
        temp = my_universe.update()
        print(temp)
        res = temp - Y
        return -res
        
    
     
if __name__ == "__main__":
    
    year             = 2010
    
    # COMARCA 2
    path             = "Dominio/Comarca_2/Normal_wrt_Comarca_2/"
    df_historic_ages = pd.read_csv(path + "df_2_historic_ages.csv")
    df_families      = pd.read_csv(path + "df_2_families.csv")
    df_features      = pd.read_csv(path + "df_2_infra_coords_normal.csv")
    df_income_spend  = pd.read_csv(path + "df_2_income_spend_normal.csv") 
    df_distances     = pd.read_csv(path + "df_2_distances.csv", index_col = 0).fillna(0)
    
    # Large Cities
    #path             = "Dominio/Comarca_2/"
    #df_features_large_cities     = pd.read_csv(path + "df_large_cities_infra_coords_normal.csv")
    #df_income_spend_large_cities = pd.read_csv(path + "df_large_cities_income_spend_normal.csv")
    
    # Subjective norm (social)
    path             = "Dominio/Social_Norm/"
    df_social = pd.read_csv(path + "df_social.csv")
    
    # Natality and mortality models
    path = "Modelos/"
    #keras.models.load_model
    natality_model  = load(path + "natality_model_subset_linreg.joblib")
    mortality_model = load(path + "mortality_model_subset_linreg.joblib")
    
    # betas: list of 3
    # beta[0] -> slope and height above the sea
    # beta[1] -> distance 10k, road, highway, railroad, 
    # beta[2] -> hostital, pharmacy, education, emergency, healthcare 
    
    # gamma: parameter for subjective norm
    
    
    Y = [1]
    X = [1]
    mod = MyLikelihood(endog = Y, exog = X)
    res = mod.fit(
            start_params = np.array(np.random.uniform(0, 1, 8)),
            maxiter = 1)
