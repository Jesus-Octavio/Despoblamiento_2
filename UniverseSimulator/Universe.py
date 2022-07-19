#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:43:03 2022

@author: jesus
"""

# Load model architecture
from PopulationCentre import PopulationCentre
from LargeCity import LargeCity
from Agents import Agents
from Family_version_3 import Family
from Family_version_3 import Fam_one_person
from Family_version_3 import Fam_kids

# Load regression metrics
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score                         

# Queues for families
from collections import deque

# Load basic libraries
import pandas as pd
import random
import numpy as np
import random, time, math, sys
import warnings
import re
from varname import nameof
from itertools import chain

# Load libraries for plots
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as py

# Libraries for distances
import geopy.distance

# Load libraries for warnings
import warnings
warnings.simplefilter("always")



def myround(x, base=5):     
    """
    Auxiliary function. Given an age, returns its range according to
    the discretization in the read data.
        
    Examples
    ------
    >>> myround(1)
    0-4        
    >>> myround(23)
    20-24        
    >>> myround(106)
    >100
    """
    init = base * math.floor(float(x) / base)    
    if init >= 100:
        return '>' + str(100)     
    end =  base * math.ceil(float(x) / base)
    if init == end:
        end = end + 5
    return str(init) + '-' + str(end - 1)

        

class Universe():
    # MAIN CLASS
    
    def __init__(self,
                 year,
                 df_historic_ages,
                 df_families,
                 df_features,
                 df_income_spend,
                 df_features_large_cities,
                 df_income_spend_large_cities,
                 
                 # TPB: Behavioural attitude
                 betas, #list/array of 11
                 # TPB: Subjective norm
                 gamma, #float
                 # TPB: Perceived behavioural control
                 theta, #float
                 # TPB: Intention
                 alphas #list/array of 3
                 
                 ):
        
        # CONSTRUCTOR
        global agent_idx
        agent_idx = 0
        # Year
        self.year = str(year)
        # Read data from dataframe (population,......)
        self.df_historic_ages = df_historic_ages
        
        # Theory of planned behaviour
        # Behavioural attitue
        self.betas = betas
        self.gamma = gamma
        self.theta = theta
        self.alphas = alphas
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        # Read data from dataframe (FAMILIES)
        self.df_families     = df_families
        self.df_features     = df_features
        self.df_income_spend = df_income_spend 
        ######################################################################
        

        # List of population centres (nucleos de poblacion) if the universe
        population_centres = self.PopulationCentreBuilder()
        self.population_centres  = population_centres[0]
        self.cols_update = population_centres[1]
        # List of persons in the universe
        self.universe_persons = self.AgentsBuilder()
        
        
        
        ##################### TRYING TO BUILD UP FAMILES #####################
        self.FamilyBuilder()
        ######################################################################
        
        
        # LARGE CITIES
        self.df_features_large_cities = df_features_large_cities
        self.df_income_spend_large_cities = df_income_spend_large_cities
        self.large_cities = self.LargeCityBuilder()
        
        
        

    def PopulationCentreBuilder(self):
        # METHOD TO BUILD UP POPULATION CENTRES
        # List to store population centres
        population_centres = [] 
        # As we are reading from a datafrase (assume each population centre 
        # appears just once in the dataframe), consider each row:
        for population in range(self.df_historic_ages.shape[0]):
            
            
            # Select specific row, i..e. specific population centre
            df_temp      = self.df_historic_ages.iloc[population]
            identifier   = df_temp["CODMUN"]
            df_temp_2    = self.df_features.\
                                query('CODMUN == ' + str(identifier))
            df_temp_3    = self.df_income_spend.\
                                query('CODMUN == ' + str(identifier))
            
                    
            #my_cols   = ["HOM" + self.year, "MUJ" + self.year,
            #             "NAT" + self.year, "MOR" + self.year, 
            #            "SALDOTT" + self.year]
            my_cols   = ["HOM" + self.year, "MUJ" + self.year,
                         "NAT" + self.year, "MOR" + self.year]
            
            #my_cols_update = ["NAT", "MOR", "SALDOTT"]
            my_cols_update = ["NAT", "MOR"]
            
            d_args = {}
            for column in my_cols:
                d_args[column[:len(column)-4].lower()] = df_temp[column]
            
            # Invoke Population Center constructor
            the_population = PopulationCentre(
                    year        = self.year,
                    identifier  = identifier,
                    name        = df_temp["Nombre"],
                    num_men     = 0,
                    num_women   = 0,
                    # Select features for the population centre
                    # To compute geodesic distance ...
                    longitud    = df_temp_2["LONGITUD_E"],
                    latitud     = df_temp_2["LATITUD_ET"],
                    # Height about the sea level
                    minmdt      = df_temp_2["MINMDT"],
                    maxmdt      = df_temp_2["MAXMDT"] ,
                    meanmdt     = df_temp_2["MEANMDT"],
                    stdmdt      = df_temp_2["STDMDT"],
                    # Slope
                    minpendi    = df_temp_2["MINPENDI"],
                    maxpendi    = df_temp_2["MAXPENDI"],
                    meanpendi   = df_temp_2["MEANPENDI"],
                    stdpendi    = df_temp_2["STDPENDI"],
                    # Distance to 10k population centre
                    mindisn10m  = df_temp_2["MINDISN10M"],
                    maxdisn10m  = df_temp_2["MAXDISN10M"],
                    meandisn10m = df_temp_2["MEANDISN10M"],
                    stddisn10m  = df_temp_2["STDDISN10M"],
                    # Distance to road
                    mincarretn  = df_temp_2["MINCARRETN"],
                    maxcarretn  = df_temp_2["MAXCARRETN"],
                    meancarretn = df_temp_2["MEANCARRETN"],
                    stdcarretn  = df_temp_2["STDCARRETN"],
                    # Distance to highway
                    mindisaut   = df_temp_2["MINDISAUT"],
                    maxdisaut   = df_temp_2["MAXDISAUT"],
                    meandisaut  = df_temp_2["MEANDISAUT"],
                    stddisaut   = df_temp_2["STDDISAUT"],
                    # Distance to railroad
                    mindisferr  = df_temp_2["MINDISFERR"],
                    maxdisferr  = df_temp_2["MAXDISFERR"],
                    meandisferr = df_temp_2["MEANDISFERR"],
                    stddisferr  = df_temp_2["STDDISFERR"],
                    # Distance to hospitals
                    disthospit  = df_temp_2["DISTHOSPIT"],
                    # Distance to pharmacies
                    distfarma   = df_temp_2["DISTFARMA"],
                    # Distance to education centres
                    distceduc   = df_temp_2["DISTCEDUC"],
                    # Distance to emercengy centres
                    distcurgh   = df_temp_2["DISTCURGH"],
                    # Distance to primary healthcare centres
                    distatprim  = df_temp_2["DISTATPRIM"],
                    # Data about income and spenditures
                    #salario     = df_temp_3["SALARIO_MEAN_" + str(self.year)], 
                    #gasto       = df_temp_3["GASTO_MEAN_"   + str(self.year)],
                    **d_args)

            # Add specific population to the universe
            population_centres.append(the_population)
        
        return  [population_centres, my_cols_update]
    
    
    def LargeCityBuilder(self): 
        # METHOD TO BUILD UP LARGE CITIES
        # List to store population centres
        large_cities = [] 
        # As we are reading from a datafrase (assume each population centre 
        # appears just once in the dataframe), consider each row:
        for city in range(self.df_features_large_cities.shape[0]):
            
            # Select specific row, i..e. specific population centre
            df_temp_2  = self.df_features_large_cities.iloc[city]
            identifier = df_temp_2["CODMUN"]
            df_temp_3  = self.df_income_spend_large_cities.\
                                query('CODMUN == ' + str(identifier))
            

            
        
            # Invoke Population Center constructor
            the_population = LargeCity(
                    identifier  = df_temp_2["CODMUN"],
                    name        = df_temp_2["NOMBRE"],
                    # Select features for the population centre
                    # To compute geodesic distance ...
                    longitud    = df_temp_2["LONGITUD_E"],
                    latitud     = df_temp_2["LATITUD_ET"],
                    # Height about the sea level
                    minmdt      = df_temp_2["MINMDT"],
                    maxmdt      = df_temp_2["MAXMDT"] ,
                    meanmdt     = df_temp_2["MEANMDT"],
                    stdmdt      = df_temp_2["STDMDT"],
                    # Slope,
                    minpendi    = df_temp_2["MINPENDI"],
                    maxpendi    = df_temp_2["MAXPENDI"],
                    meanpendi   = df_temp_2["MEANPENDI"],
                    stdpendi    = df_temp_2["STDPENDI"],
                    # Distance to 10k population centre
                    mindisn10m  = df_temp_2["MINDISN10M"],
                    maxdisn10m  = df_temp_2["MAXDISN10M"],
                    meandisn10m = df_temp_2["MEANDISN10M"],
                    stddisn10m  = df_temp_2["STDDISN10M"],
                    # Distance to road
                    mincarretn  = df_temp_2["MINCARRETN"],
                    maxcarretn  = df_temp_2["MAXCARRETN"],
                    meancarretn = df_temp_2["MEANCARRETN"],
                    stdcarretn  = df_temp_2["STDCARRETN"],
                    # Distance to highway,
                    mindisaut   = df_temp_2["MINDISAUT"],
                    maxdisaut   = df_temp_2["MAXDISAUT"],
                    meandisaut  = df_temp_2["MEANDISAUT"],
                    stddisaut   = df_temp_2["STDDISAUT"] ,
                    # Distance to railroad
                    mindisferr  = df_temp_2["MINDISFERR"] ,
                    maxdisferr  = df_temp_2["MAXDISFERR"] ,
                    meandisferr = df_temp_2["MEANDISFERR"],
                    stddisferr  = df_temp_2["STDDISFERR"],
                    # Distance to hospitals
                    disthospit  = df_temp_2["DISTHOSPIT"],
                    # Distance to pharmacies
                    distfarma   = df_temp_2["DISTFARMA"],
                    # Distance to education centres
                    distceduc   = df_temp_2["DISTCEDUC"],
                    # Distance to emercengy centres
                    distcurgh   = df_temp_2["DISTCURGH"],
                    # Distance to primary healthcare centres
                    distatprim  = df_temp_2["DISTATPRIM"])
                    #salario     = df_temp_3["SALARIO_MEAN_" + str(self.year)],
                    #gasto       = df_temp_3["GASTO_MEAN_" + str(self.year)])

            # Add specific population to the universe
            large_cities.append(the_population)
        
        return large_cities
        
        

    
    
    def AgentsBuilder(self):
        # Method to build up agents
        global agent_idx
        agents = []
        age_cols = [col for col in self.df_historic_ages.columns if col.startswith('Edad_')]
        #age_cols =self.df_historic_ages.filter(regex = r'^Edad_.*?$', axis = 1)
        #male_cols =  self.df_historic_ages.filter(regex = r'^Edad_M.*?$', axis = 1)
        #female_ cols = self.df_historic_ages.filter(regex = r'^Edad_F.*?$', axis = 1)
        for population in self.population_centres:
            # Dictionary for age ranges
            age_range = {self.year + "M" : {}, self.year + "F" : {}}
            # Select subdataframe
            df_temp = self.df_historic_ages.\
                query('CODMUN == ' + str(population.population_id))[age_cols]
                
            for col in df_temp.columns:
                sex = col.split(":")[0][-1]
                if "-" in col:
                    init = int(col.split(":")[1].split("-")[0])
                    end  = int(col.split(":")[1].split("-")[1])
                    key  = str(init) + '-' + str(end)
                else:
                    init = int(col.split(":")[1].split(">")[1])
                    end  = 110
                    key  = ">" + str(init)
                    
                # Update dictionay for age ranges
                if key not in age_range[self.year + sex].keys():
                    age_range[self.year + sex].update({key : int(df_temp[col])})
                else: 
                    age_range[self.year + sex][key] += int(df_temp[col])
                        
                for i in range(int(df_temp[col])):
                               
                    # Crate agent
                    # Other values? distributions?
                    the_agent = Agents(
                            identifier        = agent_idx,
                            sex               = sex,
                            age               = random.randint(init, end),
                            population_centre = population,
                            mdt               = population.meanmdt,
                            pendi             = population.meanpendi,
                            carretn           = population.meancarretn,
                            aut               = population.meandisaut,
                            ferr              = population.meandisferr,
                            dis10m            = population.meandisn10m,
                            hospi             = population.disthospit,
                            farma             = population.distfarma,
                            ceduc             = population.distceduc,
                            curgh             = population.distcurgh,
                            atprim            = population.distatprim,
                            betas = self.betas
                            )
                    
                    ############### TRYING TO BUILD UP FAMILES ###############
                    the_agent.family_role()
                    ##########################################################

                    # Add agent to population centre
                    the_agent.add_agent()
                    # Add agent to global list
                    agents.append(the_agent)
                    # Update identifier
                    agent_idx += 1
            
            # Update dictionary with age ranges and historial
            population.ages_hist = age_range
            # Update historial for ages
            population.update_population_hist()
            # Update historial for families
            population.update_families_hist()
            
            
        return agents
            
    
    # Different approach
    def FamilyBuilder(self):
        
        # Consider each population_centre
        for population in self.population_centres:
            
            # Given a population centre, select specific row in df
            df_temp = self.df_families.\
                query('CODMUN == ' + str(population.population_id))
                
            # Number of kids for each population centre:
            num_kids = 0
            for key in list(population.ages_hist.keys()):
                for key_2 in population.ages_hist[key].keys():
                    if "-" in key_2:
                        if int(key_2.split("-")[1]) < 25:
                            num_kids += population.ages_hist[key][key_2]
                            
            
            ##### 3-4-5 people families #####
            # fam3p -> father + mother + kidx1
            fam3p = df_temp["3PER"].values[0]
            # fam4p -> father + mother + kidx2
            fam4p = df_temp["4PER"].values[0]
            # fam5p -> father + mother + kidx3
            fam5p = df_temp["5PER"].values[0]
            
            # Total families with kids
            fam = fam3p + fam4p + fam5p
            
            #print(population.population_name)
            #print("kids  %f" % num_kids)
            #print("fam3p %f" % fam3p)
            #print("fam4p %f" % fam4p)
            #print("fam5p %f" % fam5p)
            #print("fam   %f" % fam)
            
            # Percentage of each type
            fam3p = math.ceil(num_kids * (fam3p / fam))
            fam4p = math.ceil(num_kids * (fam4p / fam))
            fam5p = math.ceil(num_kids * (fam5p / fam))
            
            # UNCOMMIT TO CHECK RESULTS
            #print("Nº of kids: %s" % num_kids)
            #print("Nº of families with 1 kid : %s"  % fam3p)
            #print("Nº of families with 2 kids: %s" % int(math.ceil(fam4p / 2)))
            #print("Nº of families with 3 kids: %s" % int(math.ceil(fam5p / 3)))
            temp = fam3p + int(math.ceil(fam4p / 2))*2 + int(math.ceil(fam5p / 3))*3
            #print("Space for %s kids" % temp)
            #print("\n")
            
            # Declare queue for families
            queue_families = deque()
            
            # Create families
            for i in range(fam3p):
                # Build up family
                fam = Fam_kids(population_centre = population, kids_limit = 1)    
                # Append left to queue
                queue_families.appendleft(fam)
            
            for i in range(int(math.ceil(fam4p / 2))):
                # Build up family
                fam = Fam_kids(population_centre = population, kids_limit = 2)
                # Append left to queue
                queue_families.appendleft(fam)
            
            for i in range(int(math.ceil(fam5p / 3))):
                # Build up family
                fam = Fam_kids(population_centre = population, kids_limit = 3)
                # Append left to queue
                queue_families.appendleft(fam)
        
        
            # PROBLEMA DE ESTA INICIALIZACION: HIJOS CON EDADES MUY HOMOGENEAS
            # Search for kids
            for agent in population.inhabitants:
            
                # If the agent is neither a kid nor a parent
                if (not agent.is_kid) and (not agent.maybe_parent):
                    # Build up one person family
                    my_family = Fam_one_person(population)
                    my_family.update(agent)
                    population.families["fam_one_person"].append(my_family)
                        
                    # If the agent is a kid
                elif agent.is_kid and (not agent.family):
                    # Consider first family in queue
                    # If there's room for the kid
                    if len(queue_families[0].kids) < queue_families[0].kids_limit:
                        queue_families[0].update(agent, "kid")
                    # If there's no room for the kid
                    else:
                        # The family has as many kids as possible so add to the universe
                        population.families["fam_kids"].append(queue_families[0])
                        # and remode from the queue
                        queue_families.popleft()
                        # The kid must be added to the next family
                        queue_families[0].update(agent, "kid")
            # In case there are any families in the queu, move them to the universe
            while len(queue_families) > 0:
                if len(queue_families[0].kids) > 0:
                    population.families["fam_kids"].append(queue_families[0])
                queue_families.popleft()
        

            # Search for parents
            for agent in population.inhabitants:
                if agent.maybe_parent and (not agent.family):
                    # Consider each family with kids
                    for family in population.families["fam_kids"]:
                        my_bool = True
                        # If the agent is a male
                        if agent.sex == "M":
                            # If the family has no father
                            if not family.father:
                                # Check parents/kids ages are compatible
                                for kid in family.kids:
                                    my_bool = agent.age >= kid.age + 25
                        
                                if my_bool:
                                    # If theres no mother
                                    if not family.mother:
                                        family.update(agent, "father")
                                        break
                                    else: # Verify ages
                                        my_bool = (family.mother.age - 5 <= agent.age <= family.mother.age - 5) or (agent.age - 5 <= family.mother.age <= agent.age + 5)
                                        if my_bool:
                                            family.update(agent, "father")
                                            break
                                        else:
                                            pass
                                    
                    
                        else: #agent.sex = "F"
                            if not family.mother:
                                # If the family has no father
                                for kid in family.kids:
                                    # Check parents/kids ages are compatible
                                    my_bool = agent.age >= kid.age + 25
                        
                                if my_bool:
                                    # if theres no father
                                    if not family.mother:
                                        family.update(agent, "mother")
                                        break
                                    else: # verify ages
                                        my_bool = (family.father.age - 5 <= agent.age <= family.father.age + 5) or (agent.age - 5 <= family.father.age <= agent.age + 5)
                                        if my_bool:
                                            family.update(agent, "mother")
                                            break
                                        else:
                                            pass
                                
            
                # agent is neither compatible with kids or partner
                if not agent.family:
                    my_family = Fam_one_person(population)
                    my_family.update(agent)
                    population.families["fam_one_person"].append(my_family)
                                    
            # Update families hist
            population.update_families_hist()
        
        
    ###########################################################################
    
    
            
        
                    
    def update(self):
        global agent_idx
        # Update year for Universe
        self.year = str(int(self.year) + 1)
        # Consider each population centre
        for population in self.population_centres:
            # Intialize dictoinary with age ranges to previous year
            population.ages_hist[self.year + "M"] = population.ages_hist[str(int(self.year) - 1) + "M"].copy()
            population.ages_hist[self.year + "F"] = population.ages_hist[str(int(self.year) - 1) + "F"].copy()
            
            #print("INICIO ACTUALIZACION")
            #print("HOMBRES")
            #print(population.ages_hist[self.year + "M"])
            #print("\n")
            #print("MUJERES")
            #print(population.ages_hist[self.year + "F"])
            #print("\n")

            
            ### PEOPLE WHO LEAVE THE POPULATION CENTRE ###
            ## THOSE WHO DIE
            # Who is going to die?
            # I suppose the oldest people die (before, some random people died)
            # If I considere that, this while loop
            # can be transformed into a for loop
            
            deaths = 0
            while deaths < population.mortality:
                max_age = 0
                person_to_die = None
                for person in population.inhabitants:
                    if person.age > max_age:
                        max_age = person.age
                        person_to_die = person
                        
                # Update dictionary with ages by range:
                interval = myround(person_to_die.age)
                population.ages_hist[self.year + person_to_die.sex][interval] -= 1
                
                ################ TRYING TO BUILD UP FAMILES ################
                # Remove family
                person_to_die.family.remove_family() # It's working !
                ############################################################
                
                # Remove person
                person_to_die.remove_agent()
                self.remove_person_from_universe(person_to_die)
                deaths += 1
            
            
            """
            # and some random people
            while deaths <= population.mortality:
                person_to_die = random.choice(population.inhabitants)
                #print(str(person_to_die.person_id) + " - " + person_to_die.sex + " - " + str(person_to_die.age) + " - " + str(myround(person_to_die.age)))
                # Update dictionary with ages by range:
                interval = myround(person_to_die.age)
                population.ages_hist[self.year + person_to_die.sex][interval] -= 1
                # Remove person
                person_to_die.remove_agent()
                self.remove_person_from_universe(person_to_die)
                deaths += 1
            """
                
                
            #print("\n")    
            #print("ESTADO TRAS MUERTES")
            #print("HOMBRES")
            #print(population.ages_hist[self.year + "M"])
            #print("\n")
            #print("MUJERES")
            #print(population.ages_hist[self.year + "F"])
            #print("\n")
            """
            ## SALDO MIGRATORIO (?):
            ## THOSE WHO ARE UNHAPPY ARE GOING TO LEAVE
            #### ¿Y si no hay tantan gente infeliz como gente que se tiene que ir?
            ### Solo hay male ya que los he metido primero en la lista
            ### shuffle of inhabitants list ??????
            
            if population.saldo_migratorio_total < 0:
                saldo = 0
                # Consider each inhabitant
                for person in population.inhabitants:
                    ### THE MOST UNHAPPUY PEOPLE MUST LEAVE !
                    
                    # Is the person unhappy? If so -> remove
                    # But, where is the person going?
                    # (BY NOW) I ASSUME THE PERSON GOES TO A LARGE CITY
                    b = person.migrate()
                    if b and (isinstance(person.family, Fam_one_person)): # CHANGE LATER
                        # I could assume they leave the universe but not
                        #  self.remove_person_from_universe(person)
                        saldo -= 1
                        # Update dictionary with ages by range:
                        interval = myround(person.age)
                        population.ages_hist[self.year + person.sex][interval] -= 1
                        person.remove_agent() # ya esta en person.migrate()
                        
                        # Remove family (origin)
                        person.family.remove_family()
                        
                        # Agent arrives at a large city
                        person.population_centre = random.choice(self.large_cities)
                        
                        # Add agent to destination 
                        person.add_agent()
                        
                        # Add family (destination)
                        person.family.add_family()
                        
                        
                    if saldo == population.saldo_migratorio_total:
                        break
                
        
            ### PEOPLE WHO ARRIVE AT THE POPULATION CENTRE ### 
            
            ## SALDO MIGRATORIO
            ## New guys on the town ! Where are they coming from? 
            ## Dont know, just create new people
            ## CONSIDERING ONLY ONE_PERSON_FAM
            if population.saldo_migratorio_total > 0:
                new_guys = 0
                while new_guys < population.saldo_migratorio_total:
                    # Uodate agent identifiers
                    agent_idx = agent_idx + 1
                    # Create agent
                    the_agent = Agents(identifier = agent_idx,
                                       sex = random.choice(["M", "F"]),
                                       age = random.randrange(25, 101), # Sure?
                                       population_centre = population)
                    
                    # Update family role
                    the_agent.family_role()
                    
                    # Create family for agent
                    my_family = Fam_one_person(population)
                    my_family.update(the_agent)
                    my_family.add_family()
                    
                                       
                    # Add person to the universe
                    self.add_person_to_universe(the_agent)
                    the_agent.add_agent()
                    new_guys += 1
                   
                    # Update dictionary with ages by range:
                    interval = myround(the_agent.age)
                    population.ages_hist[self.year + the_agent.sex][interval] += 1
            
            
            """
            
            ### UPDATE AGES ###
            for person in population.inhabitants:
                #if person.population_centre.population_name not in ["Madrid", "Barcelona"]:
                interval_1 = myround(person.age)
                person.age += 1
                interval_2 = myround(person.age)
                if interval_1 != interval_2:
                    person.population_centre.ages_hist[self.year + person.sex][interval_1] -= 1
                    person.population_centre.ages_hist[self.year + person.sex][interval_2] += 1
                else:
                    pass
                #else:
                #    person.age += 1
                
            
                    
            
            #################### TRYING TO BUILD UP FAMILIES ##################
            # Time to disband families with kids
            kids_to_adult = 0
            adults_no_kids = 0
            disbanded_fams = 0
            for family in population.families["fam_kids"].copy():
                b = family.disband()
                if not b[0]:
                    kids_to_adult += b[1]
                    adults_no_kids += b[2]
                if b[0]:
                    kids_to_adult += b[1]
                    adults_no_kids += b[2]
                    disbanded_fams += 1
            #print("UPDATE -> DISBANDED FAMILIES with kids: %s" % disbanded_fams)
            #print("UPDATE -> KIDS TO ADULTS              : %s" % kids_to_adult)
            #print("UPDATE -> FREE ADULTS                 : %s" % adults_no_kids)
            #print("\n")
            ###################################################################
            
            
            
            
            ## THOSE WHO ARE NEWBORN BABIES
            # Newborns need a family so we nee dto search for parents
            # Some of them will be assigned to families with previous kids
            # Some of them will be assigned to new parents
            new_borns = 0
            
            #################### TRYING TO BUILD UP FAMILIES ##################
            t0 = 0
            t1 = 0
            t2 = 0
            ####################################################################
            
            while new_borns < population.natality:
                
                agent_idx = agent_idx + 1
                
                # Create agent
                the_agent = Agents(
                            identifier = agent_idx,
                            sex = random.choice(["M", "F"]),
                            age = 0,
                            population_centre = population,
                            mdt               = population.meanmdt,
                            pendi             = population.meanpendi,
                            carretn           = population.meancarretn,
                            aut               = population.meandisaut,
                            ferr              = population.meandisferr,
                            dis10m            = population.meandisn10m,
                            hospi             = population.disthospit,
                            farma             = population.distfarma,
                            ceduc             = population.distceduc,
                            curgh             = population.distcurgh,
                            atprim            = population.distatprim,
                            betas = self.betas
                            )
                
                # Update family role
                the_agent.family_role()
                    
                ## Add agent to the universe
                self.add_person_to_universe(the_agent)
                # Add agent to population centre
                the_agent.add_agent()
                # Update counter
                new_borns += 1
                # Update dictionary with ages by range:
                interval = myround(the_agent.age)
                population.ages_hist[self.year + the_agent.sex][interval] += 1
                
                ################## TRYING TO BUILD UP FAMILIES ################
                # Time to assign kids to families
                dice = random.uniform(0, 1)
                
                if dice < 0.75: # Assign kid to an existing family with one kind
                    for family in population.families["fam_kids"]:
                        # If available space for kids
                        if len(family.kids) < family.kids_limit:
                            t0 += 1
                            family.update(the_agent, "kid")
                            break
                            
                        elif (family.kids_limit == 1) and (len(family.kids) == 1):
                            t1 += 1
                            family.kids_limit += 1
                            family.update(the_agent, "kid")
                            break
                    if not the_agent.family:
                        print("FAMILY NOT FOUND FOR KID DICE < THRES")
                        
                        
                else: # Build up a new family   
                    
                    bool_father = False
                    bool_mother = False
                            
                    for family in population.families["fam_one_person"]:
                                                        
                        if family.members.sex == "M":
                            if ((not bool_father) and 
                                (family.members.maybe_parent) and
                                (not family.members.is_kid)):
                                            
                                        
                                if bool_mother:
                                    my_bool = (my_mother.age - 5 <= family.members.age <= my_mother.age + 5)
                                    if my_bool:
                                        my_father = family.members
                                        my_father_family = family
                                        bool_father = True
                                                
                                            
                                else:
                                    if family.members.age in range(random.randint(25, 40)):
                                        my_father = family.members
                                        my_father_family = family
                                        bool_father = True
                                    
                                
                        else: #family2.members.sex == "F":
                            if ((not bool_mother) and 
                                (family.members.maybe_parent) and
                                (not family.members.is_kid)):
                                        
                                        
                                if bool_father:
                                    my_bool = (my_father.age - 5 <= family.members.age <= my_father.age + 5)
                                    if my_bool:
                                        my_mother = family.members
                                        my_mother_family = family
                                        bool_mother = True
                                                       
                                else:
                                    if family.members.age in range(random.randint(25, 40)):
                                        my_mother = family.members
                                        my_mother_family = family
                                        bool_mother = True
                                
                        
                        if (bool_mother) and (bool_father):
                            my_father.family = False
                            my_father_family.remove_family()
                                    
                            my_mother.family = False
                            my_mother_family.remove_family()
                                    
                            my_family = Fam_kids(population, 1)
                            my_family.update(my_father, "father")
                            my_family.update(my_mother, "mother")
                            my_family.update(the_agent, "kid")
                            my_family.add_family()
                                    
                            t2 += 1
                            break
                                
                if not the_agent.family:
                    print("FAMILY NOT FOUND FOR KID")
                    print("\n")
                            
        
                        
            #print("BUG0 %s" % t0)
            #print("BUG1 %s" % t1)
            #print("BUG2 %s" % t2)
                        
                    
                
                ###############################################################

            
            ### UPDATE MORTALITY, NATALITY, .... ###
            d_args_update = {}
            for column in self.cols_update:
                d_args_update[column.lower()] = self.df_historic_ages.\
                    query('CODMUN == ' + str(population.population_id))[column+self.year]
            
            population.update_population(**d_args_update)            
                        
            #print("\n")
            #print("FINAL ACTUALIZACION")
            #print("HOMBRES")
            #print(population.ages_hist[self.year + "M"])
            #print("\n")
            #print("MUJERES")
            #print(population.ages_hist[self.year + "F"])
            #print("\n")
            
            # Update year for the population centre
            population.year = int(population.year) + 1
            # Update historial for ages
            population.update_population_hist()
            # Update historial for families
            population.update_families_hist()
            
            
            
            
               
               
    def remove_person_from_universe(self, agent):
        # METHOD TO REMOVE PEOPLE FROM UNIVERSE (those who die mainly)
        # Remove from the universe
        self.universe_persons.remove(agent)
        
        
    def add_person_to_universe(self, agent):
        # METHOD TO ADD PEOPLE TO THE UNIVERSE (newborn babies mainly)
        self.universe_persons.append(agent)    
        
        
    ###########################################################################
    ###########################################################################  
    #########                   MONITORIZATION                        #########
    ###########################################################################
    ###########################################################################
    
    def plot_population_hist(self, population_code):
        # METHOD FOR PLOTTING POPULATION HISTORIAL IN A
        # SPECIFIED POPULATION CENTRE.

        #population_code = int(input("Please, enter a population code: "))
        
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
        
        
        data  = {"NAT" : my_population.natality_hist,
                 "MOR" : my_population.mortality_hist,
                 "HOM" : my_population.men_hist,
                 "MUJ" : my_population.women_hist,
                  #"SALDOMIG" : my_population.saldo_hist,
                 "YEAR" : my_population.year_hist}
        
        df = pd.DataFrame.from_dict(data)
        
        print(df)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["HOM"]),
                      mode = "lines",
                      name = "Hombres"))
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["MUJ"]),
                      mode = "lines",
                      name = "Mujeres"))
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["NAT"]),
                      mode = "lines",
                      name = "Natalidad"))
        
        fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["MOR"]),
                      mode = "lines",
                      name = "Mortalidad"))
        
        # SALDO MIGRATORIO NEGATIVO -> ERROR !!!
        #fig.add_trace(go.Scatter(x = df["YEAR"], y = np.log(df["SALDOMIG"]),
        #              mode = "lines",
        #              name = "Saldo migratorio"))
        
        fig.update_layout(title = "Evolución de variables en %s" % my_population.population_name,
                    xaxis_title = "Año",
                    yaxis_title = "Total personas (log-scale)")
  
        
        #fig.show()
        return fig
        
    
    
    def plot_population_pyramid_2(self, population_code, year):
        # I guess the plot for population pyramids was a mess
        # Too many pyramids for a tiny window
        # So I thik is better to show each pyramid individually
        
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
        
        
        df = pd.DataFrame.from_dict(my_population.ages_hist)
        my_cols = [col for col in df.columns if str(year) in col]
        df = df[my_cols]
        
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
                          y = df.index.values.tolist(),
                          x = df.iloc[:, 0],
                          name  = "Hombres",
                          marker_color = "blue",
                          orientation = "h",
                          showlegend = True),
                          )
            
        fig.add_trace(go.Bar(
                          y = df.index.values.tolist(),
                          x = - df.iloc[:, 1],
                          name  = "Mujeres",
                          marker_color = "orange",
                          orientation = "h",
                          showlegend = True),
                          )
            
        fig.update_layout(barmode = 'relative',
                               bargap = 0.0, bargroupgap = 0)
        fig.update_xaxes(tickangle = 90)
        
        fig.update_layout(
                    title_text="Pirámide poblacional de %s en %s " 
                        % (my_population.population_name, year),
                    bargap = 0.0, bargroupgap = 0,)
        #fig.show()
        return fig
        
       
        
    def plot_population_pyramid(self, population_code):
        # METHOD FOR PLOTTING POPULATION HISTORIAL IN A
        # SPECIFIED POPULATION CENTRE. ALDO PLOTS POPULATION PYRAMID

        #population_code = int(input("Please, enter a population code: "))
        
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
        
        
        df = pd.DataFrame.from_dict(my_population.ages_hist)
        
        
        fig = make_subplots(rows = int(len(df.columns) / 2), cols = 1,
                 subplot_titles = np.unique([x[:-1] for x in df.columns]))
        
        
        # Function 2Z -> Z ... i guess not
        row = 1
        for i in range(0, len(df.columns), 2):
            if i == 0:
                show = True
            else:
                show = False
        

            fig.add_trace(go.Bar(
                          y = df.index.values.tolist(),
                          x = df.iloc[:, i],
                          name  = "Hombres",
                          marker_color = "blue",
                          orientation = "h",
                          showlegend = show),
                          row = row, col = 1)
            
            fig.add_trace(go.Bar(
                          y = df.index.values.tolist(),
                          x = - df.iloc[:, i + 1],
                          name  = "Mujeres",
                          marker_color = "orange",
                          orientation = "h",
                          showlegend = show),
                          row = row, col = 1)
            
            fig.update_layout(barmode = 'relative',
                               bargap = 0.0, bargroupgap = 0)
            fig.update_xaxes(tickangle = 90)


            #for t in fig2.data:
            #    fig.append_trace(t , row = row, col = 1)
                
            row += 1
            
        
        fig.update_layout(
                    title_text="Evolución de la pirámide poblacional en %s" 
                        % my_population.population_name,
                    bargap = 0.0, bargroupgap = 0,)
        #fig.show()
        return fig
    
    
    
    def plot_in_out(self, population_code):
        # Plot in/out migration
                
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
        
        df_temp = self.df_historic_ages.\
                query('CODMUN == ' + str(population.population_id))
                
        years = population.year_hist
        my_in  = ""
        my_out = ""
        for year in years:
            my_out = my_out  + ".*BAJASTT.*" + str(year) +  "|" 
            my_in  = my_in   + ".*ALTASTT.*" + str(year) +  "|"
        
        
        in_val  = df_temp.filter(regex = my_in[:-1],  axis = 1)
        out_val = df_temp.filter(regex = my_out[:-1], axis = 1)
        
        balance = [x-y for (x,y) in zip(in_val.values, out_val.values)]        
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(x = years,
                             y = list(*chain(in_val.values.tolist())),
                             name = "Altas",
                             marker_color = "violet"))
        
        out_val = list(map(lambda x: -x, list(*chain(out_val.values.tolist()))))
        fig.add_trace(go.Bar(x = years,
                             y = out_val,
                             name = "Bajas",
                             marker_color = "yellow"))
        
        fig.add_trace(go.Scatter(x = years,
                                 y = list(*chain(balance)),
                                 name = "Balance",
                                 marker_color = "green"))
        
        fig.update_layout(barmode = 'overlay',
                          xaxis_tickangle = -45,
                          title = "Altas y bajas en %s" %  my_population.population_name)
        
        return fig
        
        
        
        
        
        
    
    def plot_families(self, population_code):
        
        my_population = False
        for population in self.population_centres:
            if population.population_id == population_code:
                my_population = population
        
        if my_population == False:
            raise Exception("Population centre not found")
            
        df = pd.DataFrame.from_dict(my_population.families_hist).transpose()
        df = df.iloc[::-1]
        l = [x + y for (x,y) in zip(my_population.men_hist, my_population.women_hist)]
        l.reverse()
        
        # Creating two subplots
        fig = make_subplots(rows = 1, cols = 2, specs = [[{}, {}]],
                 shared_xaxes = True, shared_yaxes = False,
                 vertical_spacing = 0.002) 
        
        fig.add_trace(go.Bar(
                y = list(df.index.astype(str)),
                x = list(df["num_fam_one_person"]),
                name = 'Familias unipersonales',
                orientation='h',
                marker=dict(
                        color = 'rgba(246, 78, 139, 0.6)',
                        line = dict(color = 'rgba(246, 78, 139, 1.0)', width = 3)
                )
        ), 1, 1)

        fig.add_trace(go.Bar(
                y = list(df.index.astype(str)),
                x = list(df["num_fam_kids"]),
                name = 'Familias con hijos',
                orientation = 'h',
                marker = dict(
                        color = 'rgba(58, 71, 80, 0.6)',
                        line = dict(color = 'rgba(58, 71, 80, 1.0)', width = 3)
                )
        ), 1, 1)

        fig.update_layout(barmode='stack')

        fig.add_trace(go.Scatter(
                x = l,
                y = list(df.index.astype(str)),
                mode = 'lines+markers',
                line_color = 'rgb(128, 0, 128)',
                name = 'Población total',
        ), 1, 2)
        
        fig.update_layout(
                title = 'Evolución del número de familias y población en %s'
                        % my_population.population_name,
                yaxis = dict(
                        showgrid = False,
                        showline = False,
                        showticklabels = True,
                        domain = [0, 0.85],
                ),
            
                yaxis2 = dict(
                        showgrid = False,
                        showline = True,  
                        showticklabels = False,
                        linecolor = 'rgba(102, 102, 102, 0.8)',
                        linewidth = 2,
                        domain = [0, 0.85],
                ),  
                
                xaxis = dict(
                        zeroline = False,
                        showline = False,
                        showticklabels = True,
                        showgrid = True,
                        domain = [0, 0.42],
                ),

                xaxis2 = dict(
                        zeroline = False,
                        showline = False,
                        showticklabels = True,
                        showgrid = True,
                        domain = [0.47, 1],
                        side = 'top',
                        dtick = int(round((max(l) - min(l))/5)),
                ),
                        
                legend = dict(x = 0.029, y = 1.038, font_size = 12),
                margin = dict(l = 100, r = 20, t = 70, b = 70),
                paper_bgcolor = 'rgb(248, 248, 255)',
                plot_bgcolor  = 'rgb(248, 248, 255)',
        )   

        return fig

        
        
   
        
    
    def regression_metrics(self):
        print("--- REGRESSION METRICS ---")
        for population in self.population_centres:
            years = population.year_hist
            total_pred = [sum(x) for x in zip(population.men_hist, population.women_hist)]
            total_obs = []
            for year in years:
                temp = self.df_historic_ages.\
                    query('CODMUN == ' + str(population.population_id))["POB"+ str(year)].\
                    values
                temp = int(temp)
                total_obs.append(temp)
        
            
            print("- " + population.population_name.upper() + " -")
            print(total_pred)
            print(total_obs)
            print("Explained variance:  %s" % explained_variance_score(total_pred, total_obs))
            print("MAE:  %s" % mean_absolute_error(total_pred, total_obs))
            print("MSE:  %s" % mean_squared_error(total_pred, total_obs))
            print("R2:  %s" % r2_score(total_pred, total_obs))
            print("\n")
        
        
        
    def Print(self):
        print('###################################################')
        print('###################################################')
        print('#    POPULATION CENTRES IN THE UNIVERSE. ' + self.year +'     #')
        print('###################################################')
        print('###################################################')
        print("Universe population: %s persons" % len(self.universe_persons))
        print("\n")
        for population in self.population_centres:
            population.Print()
            #population.Print_features()
            ################### TRYING TO BUILD UP FAMILIES ###################
            print("\n")
            #population.Print_families()
            ###################################################################
        #for city in self.large_cities:
        #    city.Print_features()   
