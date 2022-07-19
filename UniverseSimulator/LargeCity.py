#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:39:38 2022

@author: jesus
"""

class LargeCity():
    
    # LARGE CITY CONSTRUCTOR
    def __init__(self, 
                 identifier, name,
                 longitud, latitud,
                 minmdt, maxmdt, meanmdt, stdmdt,
                 minpendi, maxpendi, meanpendi, stdpendi,
                 mindisn10m, maxdisn10m, meandisn10m, stddisn10m,
                 mincarretn, maxcarretn, meancarretn, stdcarretn,
                 mindisaut, maxdisaut, meandisaut, stddisaut,
                 mindisferr, maxdisferr, meandisferr, stddisferr,
                 disthospit, 
                 distfarma,
                 distceduc,
                 distcurgh,
                 distatprim,):
                 #salario,
                 #gasto,):
        
        self.population_id = identifier
        self.population_name = name
        
        # FEATURES
        self.longitud    = longitud,
        self.latitud     = latitud
        self.minmdt      = minmdt
        self.maxmdt      = maxmdt
        self.meanmdt     = meanmdt
        self.stdmdt      = stdmdt
        self.minpendi    = minpendi
        self.maxpendi    = maxpendi
        self.meanpendi   = meanpendi
        self.stdpendi    = stdpendi
        self.mindisn10m  = mindisn10m
        self.maxdisn10m  = maxdisn10m
        self.meandisn10m = meandisn10m
        self.stddisn10m  = stddisn10m
        self.mincarretn  = mincarretn
        self.maxcarretn  = maxcarretn
        self.meancarretn = meancarretn
        self.stdcarretn  = stdcarretn
        self.mindisaut   = mindisaut
        self.maxdisaut   = maxdisaut
        self.meandisaut  = meandisaut
        self.stddisaut   = stddisaut
        self.mindisferr  = mindisferr
        self.maxdisferr  = maxdisferr
        self.meandisferr = meandisferr
        self.stddisferr  = stddisferr
        self.disthospit  = disthospit 
        self.distfarma   = distfarma
        self.distceduc   = distceduc
        self.distcurgh   = distcurgh
        self.distatprim  = distatprim
        
        #self.salario     = salario
        #self.gasto       = gasto
        
    """
    def Print(self):
        print('---------------------------------------------------')
        print('|        Large City (Out-of-the-universe?)        |')
        print('---------------------------------------------------')
        print("LARGE CITY: %s. Code: %s." 
              % (self.population_name, self.population_id))
        print("Total inhabitants : %s." % (self.num_men + self.num_women))
        print("Male  inhabitants : %s."% self.num_men)
        print("Women inhabitants : %s." % self.num_women)
        print("\n")
        
        for key in self.families.keys():
            print("###### FAMILY: "  + key + " : " + str(len(self.families[key])) +   " #######")
        print("\n")
    """
    
    def Print_features(self):
        print('###################################################')
        print('|        Large City (Out-of-the-universe?)        |')
        print('###################################################')
        print("LARGE CITY: %s. Code: %s." 
              % (self.population_name, self.population_id))
        print('--------------------------------------------------')
        print('|                    FEATURES                    |')
        print('--------------------------------------------------')
        print("Latitude:                                %f" % self.latitud)
        print("Longitude:                               %f" % self.longitud)
        print("Min  height above the sea level (m):     %f" % self.minmdt)
        print("Max  height above the sea level (m):     %f" % self.maxmdt)
        print("Mean height above the sea level (m):     %f" % self.meanmdt)
        print("Std  height above the sea level (m):     %f" % self.stdmdt)
        print("Min  slope (m):                          %f" % self.minpendi)
        print("Max  slope (m):                          %f" % self.maxpendi)
        print("Mean slope (m):                          %f" % self.meanpendi)
        print("Std  slope (m):                          %f" % self.stdpendi)
        print("Min  distance to a 10k pop. centre (m):  %f" % self.mindisn10m)
        print("Max  distance to a 10k pop. centre (m):  %f" % self.maxdisn10m)
        print("Mean distance to a 10k pop. centre (m):  %f" % self.meandisn10m)
        print("Std  distance to a 10k pop. centre (m):  %f" % self.stddisn10m)
        print("Min  distance to road (m):               %f" % self.mincarretn)
        print("Max  distance to road (m):               %f" % self.maxcarretn)
        print("Mean distance to road (m):               %f" % self.meancarretn)
        print("Std  distance to road (m):               %f" % self.stdcarretn)
        print("Min  distance to highway (m):            %f" % self.mindisaut)
        print("Max  distance to highway (m):            %f" % self.maxdisaut)
        print("Mean distance to highway (m):            %f" % self.meandisaut)
        print("Std  distance to highway (m):            %f" % self.stddisaut)
        print("Min  distance to railroad (m):           %f" % self.mindisferr)
        print("Max  distance to railroad (m):           %f" % self.maxdisferr)
        print("Mean distance to railroad (m):           %f" % self.meandisferr)
        print("Std  distance to railroad (m):           %f" % self.stddisferr)
        print("Mean distance to hospital (m):           %f" % self.disthospit)
        print("Mean distance to pharmacy (m):           %f" % self.distfarma)
        print("Mean distance to education centre (m):   %f" % self.distceduc)
        print("Mean distance to emergency centre (m):   %f" % self.distcurgh)
        print("Mean distance to healthcare centre (m):  %f" % self.distatprim)
        print("Mean annual income:                      %f" % self.salario)
        print("Mean annaual spenditure:                 %f" % self.gasto)
        print("\n")
    