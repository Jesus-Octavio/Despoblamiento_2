#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:44:44 2022

@author: jesus
"""

import numpy as np
import numpy.random

from PopulationCentre import PopulationCentre

from Family_version_3 import Family
from Family_version_3 import Fam_one_person
from Family_version_3 import Fam_kids

class Agents():
    
    def __init__(self,
                 identifier,
                 sex,
                 age,
                 population_centre,
                 population_others,
                 mdt,
                 carretn,
                 aut,
                 ferr,
                 dis10m,
                 hospi,
                 farma,
                 ceduc,
                 curgh,
                 atprim,
                 betas):
        
        
        # AGENTS/PEOPLE CONSTRUCTOR
        
        self.person_id         = identifier
        self.sex               = sex
        self.age               = age
        self.population_centre = population_centre
        self.population_others = population_others
        
        # RELATED TO FEATURES OF THEIR POPULATION CENTRE
        # Data about the agent's location
        # Height abput the sea level
        self.mdt      = mdt
        # Distance to road
        self.carretn  = carretn
        # Distance to highway
        self.aut      = aut
        # Distance to railroads
        self.ferr     = ferr
        # Distamce to 10k population centre
        self.dis10m   = dis10m
        # Distance to hospital
        self.hospi    = hospi
        # Distamce to pharmacy
        self.farma    = farma
        # Distance to education centre
        self.ceduc    = ceduc
        # Distance to emergency centre
        self.curgh    = curgh
        # Distance to primary healthcare centre
        self.atprim   = atprim
        
        
        # Following Vietnam THESIS
        self.betas = betas
        ba = [np.random.uniform(0, x) for x in self.betas]
        ba = [x / sum(ba) for x in ba]

        self.beta_0 = ba[0]
        self.beta_1 = ba[1]
        self.beta_2 = ba[2]
        
        self.ba_hist = {}
        
        
        # Features about the place each person is living in
        self.features = 1
        # Welfare coefficient (I know this coefficient has no much sense
        # but I was trying to create a criterion to decide is s person wants to 
        # migrate or not)
        #if self.features: # non-empty dict
        #    self.happiness = float(np.inner(np.random.dirichlet(np.ones(len(self.features)), size = 1),
        #                     list(self.features.values())) / np.sum(list(self.features.values())))
        #else: # empty dict -> default = 1
        self.happiness = 1
        
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        # Boolean that inidicetes whether an agent is member of a family
        self.family = False
        self.is_kid = None
        self.maybe_parent = None
        ######################################################################
    
    
    def behavioural_attitude(self):
        """
        Theory of planned behaviour: behavioural attitude.
        """
        
        year = self.population_centre.year
        if year in self.population_centre.ba_hist.keys():
            pass
        else:
            self.population_centre.ba_hist[year] = {}
        
        
        #print("Currently living in %s" % self.population_centre.population_name)
        temp = self.population_others.copy()
        temp.remove(self.population_centre)
        #for elem in temp:
        #    print("Other %s" % elem.population_name)
        #print("\n")
        #return None
        factor_0 = self.beta_0 * self.mdt
    
        factor_1 = self.beta_1 * np.mean([self.carretn, self.aut,
                                          self.ferr, self.dis10m])
    
        factor_2 = self.beta_2 * np.mean([self.hospi, self.farma, self.ceduc,
                                          self.curgh, self.atprim])
        
        ba_current = factor_0 + factor_1 + factor_2
        
        self.ba_hist[self.population_centre.population_id] = float(ba_current)
        
        if not self.population_centre.population_id in self.population_centre.ba_hist[year].keys():
            self.population_centre.ba_hist[year][self.population_centre.population_id] = [float(ba_current)]
        else:
            self.population_centre.ba_hist[year][self.population_centre.population_id].append(float(ba_current))
        
        
        for elem in temp:
            
            factor_0 = self.beta_0 * elem.meanmdt
            
            factor_1 = self.beta_1 * np.mean([elem.meancarretn, elem.meandisaut,
                                              elem.meandisferr, elem.meandisn10m])
    
            factor_2 = self.beta_2 * np.mean([elem.disthospit, elem.distfarma, 
                                              elem.distceduc, elem.distcurgh,
                                              elem.distatprim])
    
            ba_current = factor_0 + factor_1 + factor_2
            
            self.ba_hist[elem.population_id] = float(ba_current)
            
            if not elem.population_id in self.population_centre.ba_hist[year].keys():
                self.population_centre.ba_hist[year][elem.population_id] = [float(ba_current)]
            else:
                self.population_centre.ba_hist[year][elem.population_id].append(float(ba_current))
            

            
        
    
    def perceived_beahavioural_control(self):
        """
        Theory of planned behaviour. perceived behavioural control.
        """
        return None
    
    def subjective_norm(self):
        """
        Theory of planned behaviour: subjective norm.
        
        """
        return None

    def migrate(self):
        # If a person want to migrate
        # If the peson is "unhappy" (?)
        if self.happiness <= 0.15:
            # If the person is old enough (just trying to model what we said about families..)
            # I think we will are able to "create" famillies but i have 
            # doubts about some of variables (i will try later)
            if self.age >= 18: # better 18
                self.new_migration = 1
                self.migration = self.new_migration
                # That person is leaving the population centre 
                # but is the person leaving the universe ???????????
                #self.remove_agent()
                b = True
            else:
                b = False
        else:
            b = False
        return b
    

    ####################### TRYING TO BUILD UP FAMILES #######################
    # When updating, roles change
    def family_role(self):
        if self.age < 18:
            self.is_kid = True
            self.maybe_parent = False
        elif 18 <= self.age <= 60:
            self.is_kid = False
            self.maybe_parent = True
        else:
            self.is_kid = False
            self.maybe_parent = False
    ##########################################################################
        
    
    def add_agent(self, new = True):
        # Add agent to population centre
        self.population_centre.inhabitants.append(self)
        if new:
            if self.sex == "M":
                self.population_centre.num_men += 1
            else:
                self.population_centre.num_women += 1
                
        
            
    def remove_agent(self):
        # Remove agent from population centre
        self.population_centre.inhabitants.remove(self)
        if self.sex == "M":
            self.population_centre.num_men -= 1
        else: # sex = "F"
            self.population_centre.num_women -= 1
    
    def die(self):
        self.remove_agent()
            
        

        
    def Print(self):
        print('- - - - - - - - - - - - - - - - - - - - - - - - - -')
        print('|                      AGENT                      |')
        print('- - - - - - - - - - - - - - - - - - - - - - - - - -')
        print("Lives in %s" % self.population_centre.population_name)
        print("Agent id: %s" % self.person_id)
        print("Age: %s" % self.age)
        print("Sex: %s" % self.sex)
        print("Happiness: %s" % self.happiness)
        print("\n")
        
        
        
        