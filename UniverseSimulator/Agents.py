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
    
    def __init__(self, identifier, sex, age, population_centre,
                 mdt, pendi, carretn, aut, ferr, dis10m,
                 hospi, farma, ceduc, curgh, atprim,
                 betas):
        # AGENTS/PEOPLE CONSTRUCTOR
        
        self.person_id         = identifier
        self.sex               = sex
        self.age               = age
        self.population_centre = population_centre
        
        # RELATED TO FEATURES OF THEIR POPULATION CENTRE
        # Data about the agent's location
        # Height abput the sea level
        self.mdt      = mdt
        # Slope
        self.pendi    = pendi
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
        
        
        ##################### THEORY OF PLANNED BEHAVIOUR #####################
        # BEHAVIOURAL ATTITUDE
        # Following Vietnam PAPER
        #ba = np.random.uniform(0,1,11)
        #ba = [(x - min(ba)) / (max(ba) - min(ba)) for x in ba]
        #ba = [x / sum(ba) for x in ba]
        
        # Height abput the sea level
        #self.beta_mdt      = ba[0]
        # Slope
        #self.beta_pendi    = ba[1]
        # Distance to road
        #self.beta_carretn  = ba[2]
        # Distance to highway
        #self.beta_aut      = ba[3]
        # Distance to railroads
        #self.beta_ferr     = ba[4]
        # Distamce to 10k population centre
        #self.beta_dis10m   = ba[5]
        # Distance to hospital
        #self.beta_hospi    = ba[6]
        # Distamce to pharmacy
        #self.beta_farma    = ba[7]
        # Distance to education centre
        #self.beta_ceduc    = ba[8]
        # Distance to emergency centre
        #self.beta_curgh    = ba[9]
        # Distance to primary healthcare centre
        #self.beta_atprim   = ba[10]
        
        # Following Vietnam THESIS
        self.betas = betas
        ba = [np.random.uniform(1, x) for x in self.betas]
        ba = [(x - min(ba)) / (max(ba) - min(ba)) for x in ba]
        ba = [x / sum(ba) for x in ba]
        
        # Height abput the sea level
        self.beta_mdt      = ba[0]
        # Slope
        self.beta_pendi    = ba[1]
        # Distance to road
        self.beta_carretn  = ba[2]
        # Distance to highway
        self.beta_aut      = ba[3]
        # Distance to railroads
        self.beta_ferr     = ba[4]
        # Distamce to 10k population centre
        self.beta_dis10m   = ba[5]
        # Distance to hospital
        self.beta_hospi    = ba[6]
        # Distamce to pharmacy
        self.beta_farma    = ba[7]
        # Distance to education centre
        self.beta_ceduc    = ba[8]
        # Distance to emergency centre
        self.beta_curgh    = ba[9]
        # Distance to primary healthcare centre
        self.beta_atprim   = ba[10]
        
        
        
        
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
        Theory of planned behaviour: behavioural attitude
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
        
        
        
        