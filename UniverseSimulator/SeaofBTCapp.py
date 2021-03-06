#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:37:41 2022

@author: jesus
"""



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

import pandas as pd
import numpy as np
  
          
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import plotly.offline as py
import sys


LARGE_FONT = ("Verdana", 12)


class Pages:
    name = None
    _id  = None
    year = None

class SeaofBTCapp(Pages, tk.Tk):

    def __init__(self, universe, *args, **kwargs):
               
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.universe = universe
        self.frames = {}

        for F in (StartPage, PageOne, PopulationCentrePage, PlotPage, YearsPage):

            frame = F(container, self)

            self.frames[F] = frame
            
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
    def show_frame_set_population(self, cont, name, _id):
        
        frame = self.frames[cont]
        frame.tkraise()
        
        Pages.name = name
        Pages._id = _id
        
        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        global welcome_pic 
        
        tk.Frame.__init__(self,parent)
        
        welcome_pic = ImageTk.PhotoImage(Image.open("/home/jesus/Escritorio/welcome.jpg"))
        tk.Label(self,
                 image = welcome_pic).pack()
        
        self.configure(background='black')
        
        tk.Button(self,
                  text = "ENTER",
                  command = lambda: controller.show_frame(PageOne)).pack()
        
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        tk.Button(self,
                  text = "CONSULTA", 
                  command = lambda: controller.show_frame(PopulationCentrePage)).pack()
        
        tk.Button(self,
                  text = "ATR??S",
                  command = lambda: controller.show_frame(StartPage)).pack()
        
        
      
class PopulationCentrePage(Pages, tk.Frame,):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        var = tk.StringVar()

        def selection():
            towns_names = []
            cname = lb.curselection()
            for i in cname:
                op = lb.get(i)
                towns_names.append(op)
            
            towns_object = []
            for town in towns_names:
                for population in controller.universe.population_centres:
                    if town == population.population_name:
                        towns_object.append(population)
            
            return [towns_names, towns_object]
        
        
        def showSelected():
            towns = selection()
            for item in towns:
                print(item)
            
            
        show = tk.Label(self, text = "SELECCIONE UN MUNICIPIO", font = ("Times", 14), padx = 10, pady = 10)
        show.pack() 
        lb = tk.Listbox(self, selectmode = "multiple")
        lb.pack(padx = 10, pady = 10, fill = "both") 
        
        
        for item in range(len(controller.universe.population_centres)): 
            lb.insert("end", controller.universe.population_centres[item].population_name) 
            lb.itemconfig(item, bg="#bdc1d6") 

        tk.Button(self,
                  text = "CONFIRMAR CONSULTA",
                  command = showSelected).pack()
        
        tk.Button(self,
                  text = "SIGUIENTE",
                  command= lambda : controller.show_frame_set_population(PlotPage, name = selection()[0][0], _id = str(selection()[1][0].population_id))).pack()
        
        tk.Button(self,
                  text = "ATR??S",
                  command = lambda : controller.show_frame(PageOne)).pack()
    


class YearsPage(Pages, tk.Frame,):
    
    def __init__(self, parent, controller):
        
        def plotter(year):
            fig = controller.universe.plot_population_pyramid_2(int(Pages._id), year)    
            py.plot(fig, filename = "piramide.html", auto_open = True)
        
        tk.Frame.__init__(self, parent)
        
        
        #_id = int(Pages._id)
        #for item in range(len(controller.universe.population_centres)):
        #    if item.population_id == _id:
        #        my_population = item
        
        years = list(controller.universe.population_centres[0].year_hist)
        
        for year in years:
            tk.Button(self,
                  text = "A??O %s" % year, 
                  command = lambda year=year: plotter(int(year))).pack()
                  
        tk.Button(self,
                  text = "ATR??S",
                  command = lambda: controller.show_frame(PlotPage)).pack()

 
class PlotPage(tk.Frame, Pages):
    
    def __init__(self, parent, controller):
        
        def button_1_plot():
            fig = controller.universe.plot_population_hist(int(Pages._id))    
            py.plot(fig, filename = "multiline.html", auto_open = True)
            
        def button_2_plot():
            fig = controller.universe.plot_population_pyramid(int(Pages._id))    
            py.plot(fig, filename = "piramide.html", auto_open = True)
            
        def button_3_plot():
            fig = controller.universe.plot_families(int(Pages._id))    
            py.plot(fig, filename = "piramide.html", auto_open = True)
                        
        def button_4_plot():
            fig = controller.universe.plot_in_out(int(Pages._id))    
            py.plot(fig, filename = "in_out.html", auto_open = True)
            
        ## All of these files mut de removed
        
        global comein_pic
        
        tk.Frame.__init__(self, parent)
        
        tk.Button(self,
                  text = "CONSULTA ACUTAL",
                  command = self.confirm_query).pack()
        
        
        self.label = tk.Label(self, text = "SELECCIONE TIPO DE GR??FICO").pack()
        
        tk.Button(self,
                  text = "GR??FICO MULTILINEA: EVOLUCI??N TEMPORAL",
                  command = button_1_plot).pack()
        
        tk.Button(self,
                  text="PIR??MIDE POBLACIONAL: EVOLUCI??N TEMPORAL",
                  command = lambda: controller.show_frame(YearsPage)).pack()
                  # In case we want all the population pyramids shown in the same window
                  #command = lambda: button_2_plot).pack()
        
        tk.Button(self,
                  text="FAMILIAS: EVOLUCI??N TEMPORAL",
                  command = button_3_plot).pack()
        
        tk.Button(self,
                  text="MIGRACIONES: IN-OUT",
                  command = button_4_plot).pack()
        
        tk.Button(self,
                  text = "ATR??S",
                  command = lambda: controller.show_frame(PopulationCentrePage)).pack()
        
        button_destroy = tk.Button(self,
                                   text = "CERRAR",
                                   command = lambda: controller.destroy())
        
        button_destroy.pack(side = "bottom")
        
     
    def confirm_query(self):
        text = str("HA ESCOGIDO EL MUNICIPIO %s CON C??DIGO %s" % (Pages.name, Pages._id))
        self.label = tk.Label(self, text = text).pack()

        
        
        
        
        



     
if __name__ == "__main__":
    
    year             = 2012
    
    # COMARCA 2
    path             = "Dominio/Comarca_2/"
    df_historic_ages = pd.read_csv(path + "df_2_historic_ages.csv")
    df_families      = pd.read_csv(path + "df_2_families.csv")
    df_features      = pd.read_csv(path + "df_2_infra_coords_normal.csv")
    df_income_spend  = pd.read_csv(path + "df_2_income_spend_normal.csv") 
    
    
    df_features_large_cities     = pd.read_csv(path + "df_large_cities_infra_coords_normal.csv")
    df_income_spend_large_cities = pd.read_csv(path + "df_large_cities_income_spend_normal.csv")
    
    
    # betas: list of 11
    #beta_mdt, beta_pendi, beta_carretn, beta_aut,
    #beta_ferr, beta_dis10m, beta_hospi, beta_farma,
    #beta_ceduc, beta_curgh, beta_arptim
                 
    my_universe = Universe(year                         = year,
                           df_historic_ages             = df_historic_ages,
                           df_families                  = df_families,
                           df_features                  = df_features,
                           df_income_spend              = df_income_spend,
                           df_features_large_cities     = df_features_large_cities,
                           df_income_spend_large_cities = df_income_spend_large_cities,
                           betas = list(np.random.uniform(0, 1, 11)))
    my_universe.Print()

    
        
    #for i in range(1, 2):
    #    my_universe.update()
    #    my_universe.Print()
    
    
    #my_universe.regression_metrics()
    #app = SeaofBTCapp(universe = my_universe)
    #app.mainloop()
       
#app = SeaofBTCapp()
#app.mainloop()