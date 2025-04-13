import numpy as np

class Environment:
    '''
    this class handles the environment: prey mass and prey contamination, later add prey density

    ----------------
    (tilapia) calories data from: 
        https://www.nutritionvalue.org/Fish%2C_raw%2C_american%2C_shad_nutritional_value.html
        Data from USDA National Nutrient Database

    (golden shiner) calories data from:
        https://www.fitatu.com/catalog/de/goldbrasse-dorade-frisch--57446697

    (crappie, raw gar, Fresh Bluegill Fish) calories data from:
        https://www.myfitnesspal.com/food/calories/fish-645849931

    (brown bullhead) calories data from:
        http://www.fische.info/speisefische/x-y-z/schwarzer-zwergwels.html

    (No.2038 raw gizzard shad) calories data from:
        COMPOSITION OF FOODS
        https://books.googleusercontent.com/books/content?req=AKW5QaeQzVCk5a-5UDib1_e697JMs48zFJzwh6T-1fP8HQKity7cYo-HeAqOFefp6uZ7gMIRGoYGZ9Z1C0hkUQ44bqA8cQjGCQRdotD0IvP19xJR2h8Jmt8kaWt5dV_m9tftNjicP8rU-53k3XIQtvzYGyJk_M92BADiQhufslXBbVuMKAir1Mor3X1buebXg9SbXdIFCVfDLNK_KrXvbcVqgu_xWZ_voTO6QZxjckwWzCI_ExMldO24VjUjx9JW8np7PQJcHcI4CuljkjarMJJlHKJ4MU5tYQ

    k-cal to Joule conversion:
        https://www.rapidtables.com/convert/energy/kcal-to-joule.html

    ----------------
    contamination rates from SJRWMD, FishOCP_Apopka
    ----------------
    dietary portions from Lyan Tempelman, Food Web
    ----------------
    shad is treated as gizzard shad, catfish is treated like brown bullhead
    ----------------

    Attributes: 
        fish portions
        conversion parameters: energy to mass

    '''
    def __init__(self):

        'portion of alligator diet'
        
        # #self.portion_shad = 0.2283 #
        # self.portion_gizzard_shad = 0.1895 + 0.2283 # 
        # self.portion_bluegill = 0.0010 # 
        # self.portion_tilapia = 0.20# 
        # self.portion_gizzard_golden_shiner = 0.0021# 
        # self.portion_black_crappie = 0.0147 # 
        # self.portion_gar = 0.1675# 
        # #self.portion_catfish = 0.0817 # 
        # self.portion_brown_bullhead = 0.0419 + 0.0817 # 
        # self.portion_anhinga = 0.0733 # 
        
        'fish portion normalised to 100% without anhinga'
        self.portion_gizzard_shad = 0.4508
        self.portion_bluegill = 0.0011
        self.portion_tilapia = 0.2158
        self.portion_gizzard_golden_shiner = 0.0023
        self.portion_black_crappie = 0.0159
        self.portion_gar = 0.1807
        self.portion_brown_bullhead = 0.1334

        'conversion parameters: energy to mass'
        self.m_per_E_gizzard_shad = 1.0/8368000.0           #kg/J
        self.m_per_E_bluegill = 1.0/4765576.0              #kg/J
        self.m_per_E_tilapia = 1.0/4016640.0                #kg/J
        self.m_per_E_golden_shiner = 1.0/4644240.0         #kg/J
        self.m_per_E_black_crappie = 1.0/5020800.0          #kg/J
        self.m_per_E_gar = 1.0/4644240.0                    #kg/J
        self.m_per_E_brown_bullhead = 1.0/5522880.0         #kg/J
    
        'conversion parameters: mass to contamination, ug/kg --> see calcNewFishConc()' 
        # # mean values for latest measurement dates (14.02.08, except golden shiner: 23.2.05)
        # self.conam_conc_fish_2008_dict = {}

        # # gizzard shad - use for all shad
        # self.conam_conc_fish_2008_dict["pp_DDE_gizzard_shad"] = np.random.normal(loc = 53.03 , scale = 10.53, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_gizzard_shad"] =  np.random.normal(loc = 0.69 , scale = 0.39, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_gizzard_shad"] =  np.random.normal(loc = 31.57 , scale = 2.10, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_gizzard_shad"] =  np.random.normal(loc = 0.90 , scale = 0.44, size = None)
        # # bluegill
        # self.conam_conc_fish_2008_dict["pp_DDE_bluegill"] = np.random.normal(loc = 28.52 , scale = 30.41, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_bluegill"] =  np.random.normal(loc = 0.32 , scale = 0, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_bluegill"] =  np.random.normal(loc = 24 , scale = 0, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_bluegill"]=  np.random.normal(loc = 0.44 , scale = 0.13, size = None)
        # # tilapia
        # self.conam_conc_fish_2008_dict["pp_DDE_tilapia"] = np.random.normal(loc = 18.3 , scale = 16.22, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_tilapia"] =  np.random.normal(loc = 0.42 , scale = 0.12, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_tilapia"]=  np.random.normal(loc = 24 , scale = 0, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_tilapia"]=  np.random.normal(loc = 0.50 , scale = 0.14, size = None)
        # # golden shiner
        # self.conam_conc_fish_2008_dict["pp_DDE_golden_shiner"] = np.random.normal(loc = 64.5 , scale = 64.35, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_golden_shiner"]=  np.random.normal(loc = 0.54 , scale = 0, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_golden_shiner"]=  np.random.normal(loc = 23 , scale = 0, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_golden_shiner"]=  np.random.normal(loc = 1.68 , scale = 1.73, size = None)
        # # black crappie
        # self.conam_conc_fish_2008_dict["pp_DDE_black_crappie"] = np.random.normal(loc = 24.57 , scale = 22.62, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_black_crappie"]=  np.random.normal(loc = 0.33 , scale = 0.02, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_black_crappie"]=  np.random.normal(loc = 24.43 , scale = 1.06, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_black_crappie"]=  np.random.normal(loc = 0.43 , scale = 0.11, size = None)
        # # gar
        # self.conam_conc_fish_2008_dict["pp_DDE_gar"] = np.random.normal(loc = 366.5 , scale = 301.93, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_gar"] =  np.random.normal(loc = 0.54 , scale = 0.30, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_gar"]=  np.random.normal(loc = 73 , scale = 21.92, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_gar"]=  np.random.normal(loc = 2.2 , scale = 1.56, size = None)
        # # brown bullhead - use for all catfish
        # self.conam_conc_fish_2008_dict["pp_DDE_brown_bullhead"] = np.random.normal(loc = 23.2 , scale = 16.05, size = None)
        # self.conam_conc_fish_2008_dict["dieldrin_brown_bullhead"] =  np.random.normal(loc = 0.43 , scale = 0.19, size = None)
        # self.conam_conc_fish_2008_dict["toxaphene_brown_bullhead"] =  np.random.normal(loc = 24 , scale = 0, size = None)
        # self.conam_conc_fish_2008_dict["trans_nonachlor_brown_bullhead"] =  np.random.normal(loc = 0.49 , scale = 0.18, size = None)

        
        
        # # mean values for measurement dates after 2000 (ca. 2004-2008), NO SD
        # self.conam_conc_fish_meanAfter2000_dict = {}

        # # gizzard shad - use for all shad
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_gizzard_shad"] = np.random.normal(loc = 56.45 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_gizzard_shad"] =  np.random.normal(loc = 1.06 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_gizzard_shad"] =  np.random.normal(loc = 42.71 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_gizzard_shad"] =  np.random.normal(loc = 1.52 , scale = 0, size = None)
        # # bluegill
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_bluegill"] = np.random.normal(loc = 27.15 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_bluegill"] =  np.random.normal(loc = 0.58 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_bluegill"] =  np.random.normal(loc = 33.37 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_bluegill"]=  np.random.normal(loc = 0.59 , scale = 0, size = None)
        # # tilapia
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_tilapia"] = np.random.normal(loc = 25.09 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_tilapia"] =  np.random.normal(loc = 0.66 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_tilapia"]=  np.random.normal(loc = 37.71 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_tilapia"]=  np.random.normal(loc = 0.78 , scale = 0, size = None)
        # # golden shiner
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_golden_shiner"] = np.random.normal(loc = 64.5 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_golden_shiner"]=  np.random.normal(loc = 0.54 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_golden_shiner"]=  np.random.normal(loc = 23 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_golden_shiner"]=  np.random.normal(loc = 1.68 , scale = 0, size = None) # changed scale: real scale value: = 1.73, TODO make lognormal??
        # # black crappie
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_black_crappie"] = np.random.normal(loc = 35.66 , scale = 0, size = None) # changed scale: real scale value: = 37.24
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_black_crappie"]=  np.random.normal(loc = 0.64 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_black_crappie"]=  np.random.normal(loc = 31.08 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_black_crappie"]=  np.random.normal(loc = 0.70 , scale = 0, size = None) # changed scale: real scale value: = 0.76
        # # gar
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_gar"] = np.random.normal(loc = 415.5 , scale = 0, size = None) # changed scale: real scale value: = 448.89
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_gar"] =  np.random.normal(loc = 1.01 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_gar"]=  np.random.normal(loc = 91.4 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_gar"]=  np.random.normal(loc = 3.72 , scale = 0, size = None) # changed scale: real scale value: = 5.25
        # # brown bullhead - use for all catfish
        # self.conam_conc_fish_meanAfter2000_dict["pp_DDE_brown_bullhead"] = np.random.normal(loc = 30.22 , scale = 0, size = None) # changed scale: real scale value: = 32.49
        # self.conam_conc_fish_meanAfter2000_dict["dieldrin_brown_bullhead"] =  np.random.normal(loc = 0.63 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["toxaphene_brown_bullhead"] =  np.random.normal(loc = 31.13 , scale = 0, size = None)
        # self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_brown_bullhead"] =  np.random.normal(loc = 0.71 , scale = 0, size = None)


        '----------------------------------------------------------------------------------'

        
        'other attributes'
        #global J_XAm_rate_int
        #global F_m
        #self.X = J_XAm_rate_int / F_m       # no. / cm^2, prey density, set initial value of prey to their carrying capacity
        #self.d_X                            # change of prey density in time
    
    def energy_to_contam(self, energy):
        '''method first calls createNewFishConc(), then energy_to_mass(), then mass_to_contam()
        
        Args:
            energy(float): amount of energy in joule to convert into conamtination levels

        Returns: 
            contam dict.
        '''

        self.createNewFishConc()

        return self.mass_to_contam(self.energy_to_mass(energy))

    def energy_to_mass(self, energy): 
        '''method creates a dict. that assigns calulated masses to fishes
        
        Args:
            energy(float): amount of energy in joule to convert into conamtination levels

        Returns: 
            mass_dict(dict.): masses in kg
        '''
        
        mass_dict = {}

        mass_dict["gizzard_shad"] = energy * self.portion_gizzard_shad * self.m_per_E_gizzard_shad
        mass_dict["bluegill"] = energy * self.portion_bluegill * self.m_per_E_bluegill
        mass_dict["tilapia"] = energy * self.portion_tilapia * self.m_per_E_tilapia
        mass_dict["golden_shiner"] = energy * self.portion_gizzard_golden_shiner * self.m_per_E_golden_shiner
        mass_dict["black_crappie"] = energy * self.portion_black_crappie * self.m_per_E_black_crappie
        mass_dict["gar"] = energy * self.portion_gar * self.m_per_E_gar
        mass_dict["brown_bullhead"] = energy * self.portion_brown_bullhead * self.m_per_E_brown_bullhead
        
        return mass_dict
        
    def mass_to_contam(self, mass_dict): 
        '''method creates a dict. that assigns calulated amounts to contaminants
        
        Args:
            mass_dict(dict.): masses in kg

        Returns: 
            contam_dict(dict): amounts of contam in ug 
        '''
        
        contam_dict = {}

        contam_dict["pp_DDE"] = mass_dict["gizzard_shad"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_gizzard_shad"] + mass_dict["bluegill"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_bluegill"] + mass_dict["tilapia"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_tilapia"] + mass_dict["golden_shiner"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_golden_shiner"] + mass_dict["black_crappie"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_black_crappie"] + mass_dict["gar"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_gar"] + mass_dict["brown_bullhead"] * self.conam_conc_fish_meanAfter2000_dict["pp_DDE_brown_bullhead"] 
        contam_dict["dieldrin"] = mass_dict["gizzard_shad"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_gizzard_shad"] + mass_dict["bluegill"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_bluegill"] + mass_dict["tilapia"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_tilapia"] + mass_dict["golden_shiner"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_golden_shiner"] + mass_dict["black_crappie"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_black_crappie"] + mass_dict["gar"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_gar"] + mass_dict["brown_bullhead"] * self.conam_conc_fish_meanAfter2000_dict["dieldrin_brown_bullhead"] 
        contam_dict["toxaphene"] = mass_dict["gizzard_shad"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_gizzard_shad"] + mass_dict["bluegill"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_bluegill"] + mass_dict["tilapia"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_tilapia"] + mass_dict["golden_shiner"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_golden_shiner"] + mass_dict["black_crappie"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_black_crappie"] + mass_dict["gar"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_gar"] + mass_dict["brown_bullhead"] * self.conam_conc_fish_meanAfter2000_dict["toxaphene_brown_bullhead"] 
        contam_dict["trans_nonachlor"] = mass_dict["gizzard_shad"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_gizzard_shad"] + mass_dict["bluegill"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_bluegill"] + mass_dict["tilapia"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_tilapia"] + mass_dict["golden_shiner"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_golden_shiner"] + mass_dict["black_crappie"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_black_crappie"] + mass_dict["gar"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_gar"] + mass_dict["brown_bullhead"] * self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_brown_bullhead"] 

        return contam_dict

    def createNewFishConc(self):
        '''method creates new fish contam conc. with SD and saves them in a dict.
        
        
        '''
        # mean values for measurement dates after 2000 (ca. 2004-2008)
        self.conam_conc_fish_meanAfter2000_dict = {}

        # gizzard shad - use for all shad
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_gizzard_shad"] = np.random.normal(loc = 56.45 , scale = 23.53, size = None)
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_gizzard_shad"] =  np.random.normal(loc = 1.06 , scale = 0.81, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_gizzard_shad"] =  np.random.normal(loc = 42.71 , scale = 25.44, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_gizzard_shad"] =  np.random.normal(loc = 1.52 , scale = 1.17, size = None)
        # bluegill
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_bluegill"] = np.random.normal(loc = 27.15 , scale = 25.76, size = None)
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_bluegill"] =  np.random.normal(loc = 0.58 , scale = 0.21, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_bluegill"] =  np.random.normal(loc = 33.37 , scale = 15.85, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_bluegill"]=  np.random.normal(loc = 0.59 , scale = 0.44, size = None)
        # tilapia
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_tilapia"] = np.random.normal(loc = 25.09 , scale = 23.75, size = None)
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_tilapia"] =  np.random.normal(loc = 0.66 , scale = 0.30, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_tilapia"]=  np.random.normal(loc = 37.71 , scale = 30.87, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_tilapia"]=  np.random.normal(loc = 0.78 , scale = 0.57, size = None)
        # golden shiner
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_golden_shiner"] = np.random.normal(loc = 64.5 , scale = 64.35, size = None)
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_golden_shiner"]=  np.random.normal(loc = 0.54 , scale = 0.0, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_golden_shiner"]=  np.random.normal(loc = 23.0 , scale = 0.0, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_golden_shiner"]=  np.random.normal(loc = 1.68 , scale = 1.68, size = None) # changed scale: real scale value: = 1.73, TODO make lognormal??
        # black crappie
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_black_crappie"] = np.random.normal(loc = 35.66 , scale = 35.66, size = None) # changed scale: real scale value: = 37.24
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_black_crappie"]=  np.random.normal(loc = 0.64 , scale = 0.49, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_black_crappie"]=  np.random.normal(loc = 31.08 , scale = 13.52, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_black_crappie"]=  np.random.normal(loc = 0.70 , scale = 0.70, size = None) # changed scale: real scale value: = 0.76
        # gar
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_gar"] = np.random.normal(loc = 415.5 , scale = 415.5, size = None) # changed scale: real scale value: = 448.89
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_gar"] =  np.random.normal(loc = 1.01 , scale = 0.78, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_gar"]=  np.random.normal(loc = 91.4 , scale = 72.66, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_gar"]=  np.random.normal(loc = 3.72 , scale = 3.72, size = None) # changed scale: real scale value: = 5.25
        # brown bullhead - use for all catfish
        self.conam_conc_fish_meanAfter2000_dict["pp_DDE_brown_bullhead"] = np.random.normal(loc = 30.22 , scale = 30.22, size = None) # changed scale: real scale value: = 32.49
        self.conam_conc_fish_meanAfter2000_dict["dieldrin_brown_bullhead"] =  np.random.normal(loc = 0.63 , scale = 0.27, size = None)
        self.conam_conc_fish_meanAfter2000_dict["toxaphene_brown_bullhead"] =  np.random.normal(loc = 31.13 , scale = 12.33, size = None)
        self.conam_conc_fish_meanAfter2000_dict["trans_nonachlor_brown_bullhead"] =  np.random.normal(loc = 0.71 , scale = 0.68, size = None)
