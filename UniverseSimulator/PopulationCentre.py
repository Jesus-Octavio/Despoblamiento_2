#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 14:01:22 2022

@author: jesus
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from Family_version_3 import Family
from Family_version_3 import Fam_one_person
from Family_version_3 import Fam_kids



class PopulationCentre():
    # POPULATION CENTRES CONSTRUCTOE
    
    def __init__(self, year, identifier, name,
                 num_men, num_women,
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
                 distatprim,
                 salario,
                 gasto,
                 hom, muj, nat, mor, saldott):
        
        self.year = year
        self.population_id = identifier
        self.population_name = name
        #self.num_men_init = hom
        self.num_men = num_men
        #self.num_women_init = muj
        self.num_women = num_women
        self.natality = nat
        self.mortality = mor
        self.saldo_migratorio_total = saldott
        self.inhabitants = []
        #self.inhabitant = inhabitants
        
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
        
        self.salario     = salario
        self.gasto       = gasto
                    
        # Mean happiness for inhabitants
        self.mean_happiness = self.update_mean_happiness()
        
        ## PLOT. MULILINE CHART: POPULATION DYNAMICS
        self.natality_hist  = []
        self.mortality_hist = []
        self.men_hist       = []
        self.women_hist     = []
        self.saldo_hist     = []
        self.year_hist      = []
        
        ## PLOT. POPULATION PYRAMID
        self.ages_hist = {}
        
        
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        # Goal: families as a dictionary.
        # I consider several types of family:
        #    * fam_one_person: single member family -lives alone-
        #    * fam_kids: family with kids: mother + father`+ kids
        # I pretend to create a dictionary whose keys are family types and
        # his values are families
        self.families = {"fam_one_person" : [],
                         "fam_kids"       : []}
        # Store families evolution
        self.families_hist = {}
        ######################################################################
        
    
        
    def update_population(self, nat, mor, saldott):
        self.natality = int(nat)
        self.mortality = int(mor)
        self.saldo_migratorio_total = int(saldott)
        
        
    def update_population_hist(self):
        self.natality_hist.append(int(self.natality))
        self.mortality_hist.append(int(self.mortality))
        self.men_hist.append(int(self.num_men))
        self.women_hist.append(int(self.num_women))
        self.saldo_hist.append(int(self.saldo_migratorio_total))
        self.year_hist.append(int(self.year))
        
    ####################### TRYING TO BUILD UP FAMILES ########################
    def update_families_hist(self):
        self.families_hist[self.year] = {
                "num_fam_one_person" : len(self.families["fam_one_person"]),
                "num_fam_kids" : len(self.families["fam_kids"])}
    ###########################################################################
            
    
    def update_mean_happiness(self):
        """
        Method to compute mean happiness for the population centre.
        The mean happiness for a population centre is the result 
        of averaging inhabitants's happiness
        """
        mean_happiness = 0
        # Both must be the same !!! Are they? 
        # Problemns with initialization by ages
        num_inhabitants = self.num_men + self.num_women
        #num_inhabitants_2 = len(self.inhabitants)
        for agent in self.inhabitants:
            mean_happiness = mean_happiness + (agent.happiness  / num_inhabitants)
        return mean_happiness
    
    
      
        
    def Print(self):
        print('###################################################')
        print('#           Population centre ' + str(self.population_id) + '               #')
        print('###################################################')
        print("Population Centre  : %s." % self.population_name)
        print("Total  inhabitants : %s." % (self.num_men + self.num_women))
        print("Male   inhabitants : %s." % self.num_men)
        print("Female inhabitants : %s." % self.num_women)
        #print("\n")
        
    
    def Print_features(self):
        print('--------------------------------------------------')
        print('|                    FEATURES                    |')
        print('--------------------------------------------------')
        print("Latitude:                                %f" % self.latitud)
        print("Longitude:                               %f" % self.longitud)
        print("Min  height above the sea level (m):     %f" % self.minmdt)
        print("Man  height above the sea level (m):     %f" % self.maxmdt)
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
        
    def Print_families(self):
        
        kids = 0
        adults = 0
        for agent in self.inhabitants:
            if (agent.is_kid and (not agent.family)):
                kids += 1
            elif (agent.is_kid != None) and (agent.maybe_parent != None) and (not agent.family):
                adults += 1
        print("KIDS   WITHOUT FAMILY: %s" % kids)
        print("ADULTS WITHOUT FAMILY: %s" % adults)
        print("\n")
        for key in self.families.keys():
            print("FAMILY: "  + key + " -> " + str(len(self.families[key])))
        print("\n")
        
        
        for family in self.families["fam_kids"]:
            if (not family.father) and (family.kids) and (not family.mother):
                raise Exception("FAMILY WITHOUT PARENTS")
            elif (not family.father) and (family.kids):
                raise Exception("FAMILY WITHOUT FATHER")
            elif (not family.mother) and (family.kids):
                print("FAMILY WITHOUT MOTHER")
            elif (family.mother) and (family.father) and (not family.kids):
                raise Exception("FAMILY WITHOUT KIDS BUT WITH PARENTS")
            
        print("\n")
    