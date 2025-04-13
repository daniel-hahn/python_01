# -*- coding: utf-8 -*-

"""
Created on Sept. 8th 2021

@author: Peter, Daniel, 
    template program  https://cream-itn.eu/creamwp/wp-content/uploads/deb_ibm-model-v3.txt, 
    DEB model data from AmP database https://www.bio.vu.nl/thb/deb/deblab/add_my_pet/entries_web/Alligator_mississippiensis/Alligator_mississippiensis_par.html 
    
Revision of Peter
     - ordering globals by theme, and putting values on them
     - checked implementation of change in reserves (calc_dU_E method)

Updates by Daniel
    - transcribing template
    - adding first data 

    - printing values to console in each delta method
    - setting values to 0 at declaration
    - moving globals to Alligator class
    - checked all delta methods and update()
    - adding a first runnable simulation for 1000 day for 1 Alligator without repro

    - extended created .csv file
    - separated classes into modules
    - adding basic plots
    - replaced initial call of calc_embryo_reserve_investment() with fixed value for U_E
    - added lay_egg()
    - added reprod_month

    - added Environment class and dietary data
    - added d_C and update_load_and_c()
    - added SNV-length and alligator mass
    - added plots and values for .csv file
    - made everything more beautiful

    - added more fish contam conc.
    - new fish conc. calc. every day
    - changed fixed init energy value back to being calculated
    - added c_T and applied to self.k_J_rate_int, self.p_m, self.v_rate_int
    - .csv saved values as float(), not int()
    - added intitial yolk contam conc

    - make SD in maternal transfer smaller, calculated mean rates for 3 lakes
    - c_T only to dL
    - adding docstrings

    - changing body temp to 33C
    - making f lognormal to simulate indiv. feeding patterns to result in indiv. variation
    - implementing simulation scenarios

when running model
    -> check np.savetxt(path)  in simulation
    -> check s1 = Simulation(start_date, sim_duration, clutch_size) in simulation
    -> check s1.plot() in simulation

TODO:
    - see READ ME

"""
#--------------------------------------------------------------------

'Importing packages'
import environment as e
import numpy as np
import math

'Setting globals'
# alligator id
last_id = 0

# maybe for future updates
# F_m = 6.5          # l/d.cm^2	{F_m}, max spec searching rate
# J_XAm_rate_int

class Alligator:
    '''
    This class creates Alligator objects
    
    Args: 
        age(int) by default 0, TODO not yet implemented

    Attributes:
        a lot

    '''

    def __init__ (self, age = 0): 

        print('check 0:')
        'maternal transfer'
        self.d_pp_DDE_mt = 0.0
        self.d_dieldrin_mt = 0.0
        self.d_toxaphene_mt = 0.0
        self.d_trans_nonachlor_mt = 0.0

        'for temp correction'
        self.T_A = 8000 #K
        self.T_ref = 273.15 + 20.0 # K, reference body temp
        self.T_real = 273.15 + 33.0 #31.5 # K, real mean body temp, NOT FINAL, source: http://www.iucncsg.org/pages/Temperature-Regulation.html, N. Smith:avioral  and Physiological Thermoregulation of Crocodilians
        self.c_T = math.e ** ((self.T_A /self.T_ref)-(self.T_A/self.T_real)) # temp correction factor

        'factors relating to the environment'
        self.env = e.Environment()
        self.f = np.random.normal(loc = 0.8, scale = 0.1, size = None)   # based on size of feeding area of indiv. alligators, the food availability differs(paper:Rauschenberger et al (2010) Alligator & Amphibian Monitoring on Lake Apopka NSRA)          # - ,  functional response, food not abundantly available
        self.f_scaled = self.f          ## Peter: if we change the amount of food available, f_scaled 
                                        ## will change (e.g. using a Monod eq.) for now, just make f_scaled = f
        self.food_dynamics = "constant" ## Peter: for now we assume there is constant and sufficient food, hence this is the default
                                        ## Peter: not yet needed, let's assume that all alligators have plenty of food

        'factors relating to variation among individuals'
        self.cv = 0.0 #0.2                     ## Peter: Let's put it to 0 for now, meaning that all individuals are equal

        'add_my_pet (AmP) param for American Alligator'
        self.p_m = 14.6523 #* self.c_T       # Specific volume‐linked somatic maint. rate
        self.E_G = 7862.95                  # Volume‐specific costs of structure
        self.zoom = 49.5869                 # -, zoom factor
        self.E_Hb = 27140                   # J , scaled maturity at birth # threshold emb->juv
        self.E_Hp = 5.214e+07               # J , scaled maturity at puberty # threshold juv->adult

        'Initial values for the 8 standard parameters'
        ## Peter: values taken from AmP, and values of Martin et al 2012 between ()
        self.kap_int = 0.86654	                    # -, allocation fraction to soma  (0.75)
        self.kap_R_int = 0.95                       # -, reproduction efficiency (0.95)
        self.k_J_rate_int = 0.00056929 #* self.c_T	# 1/d, maturity maint rate coefficient (8.24E-4)
        self.v_rate_int = 0.044176 #* self.c_T	    # cm/d, energy conductance (0.1584) 

        #self.p_am = 549.021  #* self.c_T #?               # J/(d*cm^2)	{p_Am}, spec assimilation flux ## Peter: uncomment this, instead use the convert_parameters function
        # conversion of parameters: from add_my_pet to standard DEB parameters 
        self.p_am = self.p_m * self.zoom / self.kap_int # = 838,46 ## Peter: I don't think this is needed, as we have the p_am in the AmP database, TODO -> check why this was done
        self.U_Hb_int = self.E_Hb / self.p_am
        self.U_Hp_int = self.E_Hp / self.p_am
        self.k_M_rate_int = self.p_m / self.E_G
        self.g_int = (self.E_G * self.v_rate_int / self.p_am) / self.kap_int

        'state var, deltas will be calculated, need to be valued at declaration'
        self.L = 1e-05          # = L_0 # cm, structural length ## set to very small value
        self.dL = 0.0             # change of structural length in time
        self.U_H = 0.0            # t L^2, scaled maturity
        self.dU_H = 0.0           # change of scaled maturity in time
        self.U_E = 0.0            # will be calculated # t L^2, scaled reserves, no c_T: 732.421875 // c_T: 268.5546875
        self.dU_E = 0.0           # change of scaled reserves in time
        self.e_scaled = 0.0       # - , scaled reserves per unit of structure
        self.U_R = 0.0            # t L^2, scaled energy in reproduction buffer (not standard DEB)
        self.dU_R = 0.0           # change of energy in reproduction buffer (reproduction rate)

        'fluxes'
        self.S_A = 0.0        # cm^2, assimilation flux, #will be calculated
        self.S_C = 0.0        # cm^2, mobilisation flux, #will be calculated

        'embryo var, (we use different state variable to not affect the state variable of the mother)'
        self.e_scaled_embryo = 0.0#will be calculated
        self.e_ref = 0.0          #will be calculated
        self.U_E_embryo = 0.0     #will be calculated   
        self.S_C_embryo = 0.0     #will be calculated
        self.U_H_embryo = 0.0     #will be calculated
        self.L_embryo = 0.0       #will be calculated, in cm
        self.dU_E_embryo = 0.0    #will be calculated
        self.dU_H_embryo = 0.0    #will be calculated
        self.dL_embryo = 0.0      #will be calculated

        self.estimation = 0.0             #will be calculated    # estimated value for the costs for an egg / initial reserve
        self.is_lay_egg_poss = False    #will be calculated    # parameter needed to hand over if an egg can be laid
        self.sim = 0.0                    #will be calculated    # this keeps track of how many times the calc-egg-size loop is run

        'standard DEB model, converted parameters'
        self.g = 0.0                    #will be calculated # - , energy investment ratio
        self.v_rate = 0.0               #will be calculated # cm /d , energy conductance (velocity)
        self.kap = 0.86654            # - , allocation fraction to soma
        self.kap_R = 0.95             # - , reproduction efficiency
        self.k_M_rate = 0.0             #will be calculated   # 1/d, somatic maintenance rate coefficient
        self.k_J_rate = 0.0             #will be calculated   # 1/d, maturity maintenance rate coefficient
        self.U_Hb = 0.0                 #will be calculated # t L^2, scaled maturity at birth
        self.U_Hp = 0.0                 #will be calculated # t L^2, scaled maturity at puberty
        self.scatter_multiplier = 0.0   #will be calculated # parameter that is used to randomize the input parameters

        'additional parameters concerning individuals'
        #ID
        global last_id  
        last_id += 1
        self.id = last_id

        #shape conversion factors
        self.del_M = 0.12003	#	shape coefficient for total length
        self.del_S = 0.33561	#	shape coefficient for snout-to-vent length

        # physiological concerns
        self.L_0 = 1e-05                         # intial length, in cm
        self.sNV_length = self.L/self.del_S      # snout vent length, in cm
        self.mass = self.calc_M(self.sNV_length) # in kg
        self.age = age  
        self.lipid_content = 0.06                # from: Lipid composition of fat trimmings from farm- raised alligator # maybe calc mean value from all tissues 

        # for reproduction
        self.offsprings_count = 0
        self.reprod_month = 6               # june 
        self.tried_reprod_this_year = False # flag to only reproduce once a year
        self.is_female = True              # TODO set this in simulation class

        'yolk parameters'
        # yolk constants
        self.init_yolk_mass = 0.033         # in kg, from : Deeming-Ferguson1989_Article_EffectsOfIncubationTemperature.pdf, INCLUDED EMBRYO??
        self.init_yolk_lipid_perc = 0.199   # from Rauschenberger-et-al-2004a_contaminants_2021-05-12
        self.init_yolk_lipid_mass = self.init_yolk_mass * self.init_yolk_lipid_perc # in kg 

        # will change
        self.yolk_lipid_mass = self.init_yolk_lipid_mass # in kg,  see timeline at fig.1 Deeming-Ferguson1989_Article_EffectsOfIncubationTemperature.pdf

        'contaminant loads and concentraiton parameters'
        # yolk lipid normalised contaminant concentrations in ug/kg
        # set to initial values , TODO set in simulation class?
        # values from : otemigonus crysoleucas.pdf, tab3, eggs collected 2000/02
        self.yolk_c_pp_DDE = np.random.normal(loc = 4576 , scale = 948.3, size = None) / self.init_yolk_lipid_perc
        self.yolk_c_dieldrin = np.random.normal(loc = 323 , scale = 66.8, size = None) / self.init_yolk_lipid_perc
        self.yolk_c_toxaphene = np.random.normal(loc = 2738 , scale = 224.5, size = None) / self.init_yolk_lipid_perc
        self.yolk_c_trans_nonachlor = np.random.normal(loc = 157 , scale = 36.8, size = None) / self.init_yolk_lipid_perc

        # yolk contaminant loads in ug
        self.yolk_pp_DDE = self.yolk_c_pp_DDE * self.yolk_lipid_mass
        self.yolk_dieldrin = self.yolk_c_dieldrin * self.yolk_lipid_mass
        self.yolk_toxaphene = self.yolk_c_toxaphene * self.yolk_lipid_mass
        self.yolk_trans_nonachlor = self.yolk_c_trans_nonachlor * self.yolk_lipid_mass

        # alligators lipid normalised contaminant concentrations in ug/kg
        self.c_pp_DDE = 0.0
        self.c_dieldrin = 0.0
        self.c_toxaphene = 0.0
        self.c_trans_nonachlor = 0.0

        # alligator contaminant loads in ug
        self.pp_DDE = 0.0
        self.dieldrin = 0.0
        self.toxaphene = 0.0
        self.trans_nonachlor = 0.0

        # alligator delta loads in ug
        self.d_pp_DDE = 0.0
        self.d_dieldrin = 0.0
        self.d_toxaphene = 0.0
        self.d_trans_nonachlor = 0.0

        # prey dynamics (only relevant if prey-dynamics are set to logistic)
        #self.J_XAm_rate   # No. / (cm^2 t), surface-area-specific maximum ingestion rate
        #self.K            # No. / cm^2, (half) saturation coefficient

        self.ticks = 0
        self.U_init = 0.0
        #-------------------------------------------------------------------------

        self.individual_variability()             # first their individual variability in the parameter is set
        self.calc_embryo_reserve_investment()     # then the initial energy is calculated for each, this can be replaced by fixed value, may need to recalculate when changing self.cv etc.

    #-------------------------------------------------------------------------

    'set individal variability'

    def individual_variability(self):
        ''' individuals vary in their DEB paramters on a normal distribution with a mean on the input paramater and a coefficent of variation equal to the cv
        set cv to 0 for no variation        
        
        Attributes:
            scatter_multiplier(): affected by variation
            g(): affected by variation
            U_Hb():affected by variation
            U_Hp():affected by variation

            v_rate(): unaffected by variation
            kap(): unaffected by variation
            kap_R(): unaffected by variation
            k_M_rate(): unaffected by variation
            k_J_rate(): unaffected by variation

        '''

        #self.scatter_multiplier = np.random.normal(loc = 1.0, scale = self.cv, size = 1) # np.random.lognormal(1, self.cv, size = None)     
            ## Peter: a log normal distribution around mean 0, with standard deviation of 0
            ## -> TODO make it lognormal, instead of normal 
        self.g = self.g_int #/ self.scatter_multiplier
        self.U_Hb = self.U_Hb_int #/ self.scatter_multiplier 
        self.U_Hp = self.U_Hp_int #/ self.scatter_multiplier 

        self.v_rate = self.v_rate_int
        self.kap = self.kap_int
        self.kap_R = self.kap_R_int
        self.k_M_rate = self.k_M_rate_int
        self.k_J_rate = self.k_J_rate_int
        #self.J_XAm_rate = J_XAm_rate_int * self.scatter_multiplier # (only relevant if prey-dynamics are set to logistic)
        #self.K = self.J_XAm_rate / F_m #(only relevant if prey-dynamics are set to logistic)
        #print(str(self.g) + ' ' + str(self.U_Hb) + ' ' + str(self.U_Hp) + ' ' + str(self.v_rate) + ' ' + str(self.kap))

    #-------------------------------------------------------------------------

    'methods to calc delta values'
     
    def calc_dU_E(self):
        '''change in energy reserve
        
        Attributes: 
            e_scaled(): energy density
            S_C(): mobilisation rate
            S_A(): assimilation rate
            dU_E(): change in energy reserve
        '''

        if self.food_dynamics == "constant":
            if  self.U_H <= self.U_Hb:
                f = 0.0
            else: 
                f = self.f_scaled
        if self.food_dynamics == "logistic":   ## Peter: not yet implemented, this is ok for now
            if self.U_H <= self.U_Hb:
                f = 0.0
            else:
                f = self.env.X / (self.K + self.env.X)

        self.e_scaled = self.v_rate * (self.U_E / (self.L**3.0))
        self.S_C = self.L**2.0 * (self.g * self.e_scaled / (self.g + self.e_scaled)) * (1.0 + (self.L / (self.g * (self.v_rate / ( self.g * self.k_M_rate)))))  # mobilisation, 

        self.S_A = f * self.L**2.0
        self.dU_E = ( self.S_A - self.S_C )

    def calc_dU_H(self):
        '''change in maturity is calculated (for immature individuals only) '''

        if self.U_H < self.U_Hp: # they only invest into maturity until they reach puberty
            self.dU_H = ((1.0 - self.kap) * self.S_C - self.k_J_rate * self.U_H) 
        else:
            self.dU_H = 0.0
    
    def calc_dU_R(self):
        '''the following procedure calculates change in reprobuffer if mature  '''

        if self.U_H >= self.U_Hp:
            self.dU_R = ((1.0 - self.kap) * self.S_C - self.k_J_rate * self.U_Hp)
        else:
            self.dU_R = 0.0
 
    def calc_dL(self):
        '''the following procedure calculates change in structural length, if growth is negative the individual does not have enough energy to pay somatic maintenance and the starvation submodel is run
        where growth is set to 0 and individuals divirt enough energy from development (for juveniles) or reprodution (for adults) to pay maintenance costs
        '''
        
        self.dL = ((1.0 / 3.0) * (((self.v_rate /( self.g * self.L ** 2.0 )) * self.S_C) - self.k_M_rate * self.L) ) * self.c_T

        if self.e_scaled < (self.L / (self.v_rate / (self.g * self.k_M_rate))):  # if energy density < scaled length # if growth is negative use starvation strategy 3 from the DEB book
            self.dl = 0.0
            if self.U_H < self.U_Hp: # S_C = e_scaled * self.L ** 2
                self.dU_H = (1.0 - self.kap) * self.e_scaled * self.L ** 2.0 - self.k_J_rate * self.U_Hp - self.kap * self.L ** 2.0 * ( self.L / (self.v_rate / ( self.g * self.k_M_rate)) - self.e_scaled)
            else: 
                self.dU_R = (1.0 - self.kap) * self.e_scaled * self.L ** 2.0 - self.k_J_rate * self.U_Hp - self.kap * self.L ** 2.0 * ( self.L / (self.v_rate / ( self.g * self.k_M_rate)) - self.e_scaled)
            
            self.dU_E = self.S_A - self.e_scaled * self.L ** 2 # S_C = e_scaled * self.L ** 2
        
            if self.U_H < self.U_Hp:
                if self.dU_H < 0.0:
                    #[die]
                    print("alligator No. " + str(self.id) + " starved") 
            else:
                if self.U_R < 0.0:
                    #[die]
                    print("alligator No. " + str(self.id) + " starved")

    def calc_M(self, sNV_L):
        '''formula for SNV-Length based on scatter plot trendline 
        data from: Woodward et al (1992) Experimental Alligator Harvest - Final Report
        
        Args: 
            length(int): in cm
        
        Returns:
            mass(int): in kg 
        
        '''

        return 6.0*(10.0**-6.0)*(sNV_L**3.2982)

    # the following procedure calculates change in prey density this procedure is only run when prey dynamics are set to "logistic" in the user interface
    #to calc-d_X
    #set d_X (r_X) * X * (1 - (X / K_X))   - sum [ S_A * J_XAm_rate   ] of turtles-here / volume
    #end

    def calc_dC(self):
        '''calc changes in contamination (and yolk) loads'''

        if self.U_H >= self.U_Hb:
            required_energy = self.S_A * self.p_am # J/d
            contam_dict = self.env.energy_to_contam(required_energy)

            self.d_pp_DDE = contam_dict["pp_DDE"]  
            self.d_dieldrin = contam_dict["dieldrin"]  
            self.d_toxaphene = contam_dict["toxaphene"]  
            self.d_trans_nonachlor = contam_dict["trans_nonachlor"] 
        else:
            # calc deltas
            # same percentage as energy is absorbed from yolk
            self.d_pp_DDE = self.yolk_pp_DDE * (-self.dU_E)/self.U_E  
            self.d_dieldrin = self.yolk_dieldrin * (-self.dU_E)/self.U_E 
            self.d_toxaphene = self.yolk_toxaphene * (-self.dU_E)/self.U_E 
            self.d_trans_nonachlor = self.yolk_trans_nonachlor * (-self.dU_E)/self.U_E 

            # update yolk loads
            self.yolk_pp_DDE -= self.d_pp_DDE
            self.yolk_dieldrin -= self.d_dieldrin
            self.yolk_toxaphene -= self.d_toxaphene
            self.yolk_trans_nonachlor -= self.d_trans_nonachlor

            '''
            # update yolk concentrations
            # TODO lipid mass over time, data: fig1.,  Deeming-Ferguson1989_Article_EffectsOfIncubationTemperature.pdf
            self.yolk_c_pp_DDE = self.yolk_pp_DDE / self.yolk_lipid_mass 
            self.yolk_c_dieldrin = self.yolk_dieldrin / self.yolk_lipid_mass 
            self.yolk_c_toxaphene = self.yolk_toxaphene / self.yolk_lipid_mass 
            self.yolk_c_trans_nonachlor = self.yolk_trans_nonachlor / self.yolk_lipid_mass 
            '''

    #-------------------------------------------------------------------------

    'update state var and loads'
    
    def update(self):
        '''individuals update their state variables based on the calc_state variable proccesses'''

        # update state var
        self.U_E += self.dU_E
        self.U_H += self.dU_H
        self.U_R += self.dU_R
        self.L += self.dL

        # update length and mass
        self.sNV_length = self.L / self.del_S
        self.mass = self.calc_M(self.sNV_length)

        # update alligator loads and concentrations
        self.update_load_and_c(self.d_pp_DDE, self.d_dieldrin, self.d_toxaphene, self.d_trans_nonachlor)

        #if self.food_dynamics == "logistic": 
        #    self.environment.X +=  self.environment.d_X

    def update_load_and_c(self, d_pp_DDE, d_dieldrin, d_toxaphene, d_trans_nonachlor):
        '''
        update alligator contaminant loads and concentrations

        Args:
            d_pp_DDE(): change in ppDDE
            d_dieldrin(): change in dieldrin
            d_toxaphene(): change in toxaphene
            d_trans_nonachlor(): change in trans nonachlor

        '''

        # update alligator loads, in ug
        self.pp_DDE += d_pp_DDE
        self.dieldrin += d_dieldrin
        self.toxaphene += d_toxaphene
        self.trans_nonachlor += d_trans_nonachlor

        # if negative load, set to 0
        if self.pp_DDE < 0.0:
            self.pp_DDE = 0.0
        if self.dieldrin < 0.0:
            self.dieldrin = 0.0
        if self.toxaphene < 0.0:
            self.toxaphene = 0.0
        if self.trans_nonachlor < 0.0:
            self.trans_nonachlor = 0.0

        # update alligator concetrations, in ug/kg
        self.lipid_mass = self.lipid_content * self.mass # in kg

        self.c_pp_DDE = self.pp_DDE / (self.lipid_mass)
        self.c_dieldrin = self.dieldrin / (self.lipid_mass)
        self.c_toxaphene = self.toxaphene / (self.lipid_mass)
        self.c_trans_nonachlor = self.trans_nonachlor / (self.lipid_mass)

    #-------------------------------------------------------------------------

    'methods for reproduction'
    
    def calc_lay_eggs_possible(self):
        '''
        in the following, individuals determine if they have enough energy in their repro buffer to reproduce by creating an embryo with initial reserves set to the energy
        currently in their repro buffer * kap_R (conversion efficiancy of  reprobuffer to embryo) if the individual has enough energy to produce an offspring which will reach
        maturity and have a reserve density greater than the mothers when it hatches "lay-egg?" is set to one which will trigger the reproduction procedures "calc-egg-size" and "lay-eggs"
        '''

        self.L_embryo = self.L_0 # np.random.normal(loc = 1.5, scale = 2.5, size = None)
        self.U_E_embryo = self.U_R * self.kap_R
        self.U_H_embryo = 0.0
        self.is_lay_egg_poss = False
        #calls = 0

        while True:
            self.e_scaled_embryo = self.v_rate * (self.U_E_embryo / self.L_embryo  ** 3.0)
            self.S_C_embryo = self.L_embryo  ** 2.0 * (self.g * self.e_scaled_embryo / (self.g + self.e_scaled_embryo)) * (1.0 + (self.L_embryo  / (self.g * (self.v_rate / ( self.g * self.k_M_rate)))))

            self.dU_E_embryo = ( -1.0 * self.S_C_embryo )
            self.dU_H_embryo = ((1.0 - self.kap) * self.S_C_embryo - self.k_J_rate * self.U_H_embryo )
            self.dL_embryo = ((1.0 / 3.0) * (((self.v_rate /( self.g * self.L_embryo  ** 2.0 )) * self.S_C_embryo) - self.k_M_rate * self.L_embryo ))

            self.U_E_embryo = self.U_E_embryo +  self.dU_E_embryo 
            self.U_H_embryo = self.U_H_embryo  +  self.dU_H_embryo
            self.L_embryo =   self.L_embryo  +  self.dL_embryo  

            if self.U_H_embryo > self.U_Hb:
                #print("calc_lay_eggs_possible()")
                #print("embryo till hatching used up energy : " + str((self.U_R * self.kap_R) - self.U_E_embryo))
                #print("U_E_embryo after hatching: " + str(self.U_E_embryo))
                #print("U_H_embryo: " + str(self.U_H_embryo))
                #print("L_embryo: " + str(self.L_embryo))
                #print ("-------------------")
                self.is_lay_egg_poss = True
                return self.is_lay_egg_poss
                #break 

            if self.e_scaled_embryo < self.e_scaled: # why energy density used as criteria?
                return self.is_lay_egg_poss
                #break

            #calls += 1

        #print( "self.is_lay_egg_poss = " + str(self.is_lay_egg_poss))
        #print( "loops count in calc_lay_eggs_pssible() : " + str(calls))

    # new # when using, assign initital value for U_E and remove method call in init()
    # def calc_embryo_reserve_investment_new(self):
    #     '''
    #     calculate the initial energy of the first individuals using a bisection method
    #     '''

    #     lower_bound = 0
    #     upper_bound = self.U_R * self.kap_R # max usable repro energy 
        
    #     self.sim = 0

    #     while True:
    #         self.sim += 1

    #         self.estimation = 0.5 * (lower_bound + upper_bound)
    #         self.L_embryo = self.L_0 # np.random.normal(loc = 1.5, scale = 2.5, size = None)
    #         self.U_E_embryo = self.estimation
    #         self.U_H_embryo = 0
    #         self.e_scaled_embryo = self.v_rate * (self.U_E_embryo / self.L_embryo  ** 3)

    #         self.e_ref = self.e_scaled  # e_ref now determines which e_scaled_embryo to calculate: 1 for ticks = 0 (in the setup procedure), e_scaled otherwise

    #         while self.U_H_embryo < self.U_Hb and self.e_scaled_embryo > self.e_ref:
    #             self.e_scaled_embryo = self.v_rate * (self.U_E_embryo / self.L_embryo  ** 3)
    #             self.S_C_embryo = self.L_embryo  ** 2 * (self.g * self.e_scaled_embryo / (self.g + self.e_scaled_embryo)) * (1 + (self.L_embryo  / (self.g * (self.v_rate / ( self.g * self.k_M_rate)))))

    #             self.dU_E_embryo = ( -1 * self.S_C_embryo )
    #             self.dU_H_embryo = ((1 - self.kap) * self.S_C_embryo - self.k_J_rate * self.U_H_embryo)
    #             self.dL_embryo =  ((1 / 3) * (((self.v_rate /( self.g * self.L_embryo  ** 2 )) * self.S_C_embryo) - self.k_M_rate * self.L_embryo ))

    #             self.U_E_embryo =  self.U_E_embryo +  self.dU_E_embryo 
    #             self.U_H_embryo =  self.U_H_embryo  +  self.dU_H_embryo  
    #             self.L_embryo =  self.L_embryo  +  self.dL_embryo   

    #         if self.e_scaled_embryo < (0.05 + self.e_ref) and self.e_scaled_embryo > (-0.05 + self.e_ref) and self.U_H_embryo  >= self.U_Hb: 
    #             #print("calc_embryo_reserve_investment()")
    #             #print("embryo till hatching used up energy: " + str(self.estimation - self.U_E_embryo))
    #             #print("U_E_embryo after hatching: " + str(self.estimation))
    #             #print("U_H_embryo" + str(self.U_H_embryo))
    #             #print("L_embryo" + str(self.L_embryo))
    #             #print ("-----------------------------")

    #             break

    #         if self.U_H_embryo > self.U_Hb:
    #             upper_bound = self.estimation
    #         else:
    #             lower_bound = self.estimation
            
    #         if self.sim > 200 : #if the timestep is too big relative to the speed of growth of species this will no converge
    #             print("Embryo submodel did not converge. Timestep may need to be smaller.") 
    #             break

    # old
    def calc_embryo_reserve_investment(self):
        '''
        calculate the initial energy of the first individuals using a bisection method
        '''
        #print('check 1:')

        lower_bound = 0.0
        
        if self.ticks == 0: # first run
            upper_bound = 100000.0
        else: 
            upper_bound = self.U_R * self.kap_R # max usable repro energy 
        self.sim = 0


        while True:
            #print('check 2:')

            self.sim += 1

            self.estimation = 0.5 * (lower_bound + upper_bound)
            self.L_embryo = self.L_0 # np.random.normal(loc = 1.5, scale = 2.5, size = None)
            self.U_E_embryo = self.estimation
            self.U_H_embryo = 0.0
            self.e_scaled_embryo = self.v_rate * (self.U_E_embryo / self.L_embryo  ** 3.0)
        
            

            if self.ticks == 0:
                self.e_ref = 1.0
            else:
                self.e_ref = self.e_scaled  # e_ref now determines which e_scaled_embryo to calculate: 1 for ticks = 0 (in the setup procedure), e_scaled otherwise

            #print('check 3:')
            #print('U_H_embryo: ' +str(self.U_H_embryo) )
            #print('e_scaled_embryo: ' + str(self.e_scaled_embryo))


            while self.U_H_embryo < self.U_Hb and self.e_scaled_embryo > self.e_ref:
                #print('check 4:')
                self.e_scaled_embryo = self.v_rate * (self.U_E_embryo / self.L_embryo  ** 3.0)
                self.S_C_embryo = self.L_embryo  ** 2.0 * (self.g * self.e_scaled_embryo / (self.g + self.e_scaled_embryo)) * (1.0 + (self.L_embryo  / (self.g * (self.v_rate / ( self.g * self.k_M_rate)))))

                self.dU_E_embryo = ( -1.0 * self.S_C_embryo )
                self.dU_H_embryo = ((1.0 - self.kap) * self.S_C_embryo - self.k_J_rate * self.U_H_embryo)
                self.dL_embryo =  ((1.0 / 3.0) * (((self.v_rate /( self.g * self.L_embryo  ** 2.0 )) * self.S_C_embryo) - self.k_M_rate * self.L_embryo ))

                self.U_E_embryo =  self.U_E_embryo +  self.dU_E_embryo 
                self.U_H_embryo =  self.U_H_embryo  +  self.dU_H_embryo  
                self.L_embryo =  self.L_embryo  +  self.dL_embryo 

                
                #print('U_H_embryo: ' +str(self.U_H_embryo) + ', U_Hb' + str(self.U_Hb) )
                #print('e_ref: ' +str(self.e_ref) + ', e_scaled_embryo: ' + str(self.e_scaled_embryo))

  

            if self.e_scaled_embryo < (0.05 + self.e_ref) and self.e_scaled_embryo > (-0.05 + self.e_ref) and self.U_H_embryo  >= self.U_Hb: 

                if self.ticks == 0:
                    self.U_E = self.estimation 

                    break
                else: 
                    break

            if self.U_H_embryo > self.U_Hb:
                upper_bound = self.estimation
            else:
                lower_bound = self.estimation
            
            if self.sim > 200 : #if the timestep is too big relative to the speed of growth of species this will no converge
                print("Embryo submodel did not converge. Timestep may need to be smaller.") 
                break
    
        if self.ticks == 0:
            self.U_init = self.U_E

        self.ticks +=1

    def lay_egg(self):
        ''' method decreases reproduction energy of mother and calls method calc_maternal_contam_transfer()
        '''

        # decrease energy of mother
        self.U_R -= self.estimation
        self.offsprings_count +=1

        # calc maternal transfer
        self.calc_maternal_contam_transfer()

    def calc_maternal_contam_transfer(self):
        '''this calculates the reduction of contaminant concentration in lipid of maternal tissue through maternal transfer
        it is relative to lipid concentration in maternal adipose tissue

        # data from: Rauschenberger et al, 2004 --> Rauschenberger-et-al-2004a_contaminants_2021-05-12.xlsx
        # loc: calculated as average from tissues adipose, liver and muscle
        # scale calculated as combined SD of tissues adipose, liver and muscle

        '''
        

        'pp DDE'
        mat_tissue_to_yolk_c_ratio_pp_DDE = np.random.normal(loc = 3.76, scale = 0.38, size = None) #made up scale 
        yolk_c_pp_DDE =  self.c_pp_DDE / mat_tissue_to_yolk_c_ratio_pp_DDE
        d_pp_DDE = - yolk_c_pp_DDE * self.init_yolk_lipid_mass
        self.d_pp_DDE_mt = d_pp_DDE

        'dieldrin'
        mat_tissue_to_yolk_c_ratio_dieldrin = np.random.normal(loc = 15.00, scale = 1.50, size = None) #made up scale
        yolk_c_dieldrin = self.c_dieldrin / mat_tissue_to_yolk_c_ratio_dieldrin 
        d_dieldrin = - yolk_c_dieldrin * self.init_yolk_lipid_mass
        self.d_dieldrin_mt = d_dieldrin

        'toxaphene'
        mat_tissue_to_yolk_c_ratio_toxaphene = np.random.normal(loc = 1.17, scale = 0.12, size = None) #made up scale
        yolk_c_toxaphene = self.c_toxaphene / mat_tissue_to_yolk_c_ratio_toxaphene 
        d_toxaphene = - yolk_c_toxaphene * self.init_yolk_lipid_mass
        self.d_toxaphene_mt = d_toxaphene

        'trans-nonachlor'
        mat_tissue_to_yolk_c_ratio_trans_nonachlor = np.random.normal(loc = 4.65, scale = 0.47, size = None) #made up scale
        yolk_c_trans_nonachlor = self.c_trans_nonachlor / mat_tissue_to_yolk_c_ratio_trans_nonachlor
        d_trans_nonachlor = - yolk_c_trans_nonachlor * self.init_yolk_lipid_mass
        self.d_trans_nonachlor_mt = d_trans_nonachlor

        'update maternal concentrations and loads'
        self.update_load_and_c(d_pp_DDE, d_dieldrin, d_toxaphene, d_trans_nonachlor)