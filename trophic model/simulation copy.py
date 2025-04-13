import alligator as a
import numpy as np
import datetime
import matplotlib.pyplot as plt


class Simulation:
    ''' 
    this class creates and runs the simulation, saves data to .csv file and makes plots

    Args:
        clutch_size (int): by default 1
        start_date_str (str): in the format "mm/dd/yy"
        simulation_duration (str): in days

    Attributes:
        clutch_size (int): stores clutch size
        start_date (datetime): stores beginning date of simulation
        curr_date (datetime): stores incremented date each day
        sim_dur (int): stores duration in days
        alligators (array): for alligator objects
        results (array): save results

    '''
    def __init__ (self, start_date_str, simulation_duration, clutch_size = 1):

        self.clutch_size = clutch_size  
        self.start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%y") 
        self.curr_date = self.start_date # increased during run   
        self.sim_dur = simulation_duration
        self.alligators = [a.Alligator() for i in range(self.clutch_size)]
        self.results = []  # empty list to save results   
        
    def run(self, output_interval = 10):
        '''
        starts the simulation, saves data to .csv file
         
        Args:
            output_interval(int): in days, default 10
        
        '''

        # daily loop
        for t in range(self.sim_dur):
            for alligator in self.alligators:
                # age, mabe put in the end?
                alligator.age += 1 

                # first all individuals calculate the change in their state variables and contam load based on the current conditions
                alligator.calc_dU_E()  
                alligator.calc_dU_H()
                alligator.calc_dU_R()
                alligator.calc_dL()
                alligator.calc_dC()

                # if prey dynamics are set to "logistic" the change in prey density is calculated
                #if self.food_dynamics == "logistic":    
                #    calc_d_X()
                
                #then the state variables of the individuals and prey are updated based on the delta value
                alligator.update() 

                # mature individual check if they have enough energy in their reproduction buffer to repdroduce
                if alligator.U_H >= alligator.U_Hp:
                    if alligator.is_female:
                        if self.curr_date.month == alligator.reprod_month: # only reproduce during one month a year
                            if alligator.tried_reprod_this_year == False:
                                #if np.random.randint(0,100)<alligator.repro_prob*100: # reproduction only about 50% of alligators                            
                                while alligator.calc_lay_eggs_possible():
                                    alligator.calc_embryo_reserve_investment()      # if so, they calculate how much energy to invest in an embryo
                                    alligator.lay_egg()                             # and they produce one offspring and substract energy from mother                           
                                    
                                alligator.tried_reprod_this_year = True

                        if self.curr_date.month == 1 and self.curr_date.day == 1:   # flag is resetted at beginning of each year
                            alligator.tried_reprod_this_year = False   

            # save results every 'output_interval' interval    
            if t % output_interval == 0:
                for alligator in self.alligators:
                    #original: self.results.append([float(alligator.id), float(t), float(self.curr_date.day), float(self.curr_date.month), float(self.curr_date.year), float(alligator.U_E), float(alligator.U_H), float(alligator.U_R), float(alligator.sNV_length), float(alligator.dU_E), float(alligator.dU_H), float(alligator.dU_R), float(alligator.dL), float(alligator.offsprings_count), float(alligator.c_pp_DDE), float(alligator.c_dieldrin), float(alligator.c_toxaphene), float(alligator.c_trans_nonachlor), float(alligator.pp_DDE), float(alligator.dieldrin), float(alligator.toxaphene), float(alligator.trans_nonachlor), float(alligator.mass), float(alligator.d_pp_DDE_mt), float(alligator.d_dieldrin_mt), float(alligator.d_toxaphene_mt), float(alligator.d_trans_nonachlor_mt)])  # add more attr ? #  
                    self.results.append([str(alligator.id), str(t), str(self.curr_date.year) + "-" + str(self.curr_date.month) + "-" + str(self.curr_date.day), str(alligator.U_E), str(alligator.U_H), str(alligator.U_R), str(alligator.sNV_length), str(alligator.dU_E), str(alligator.dU_H), str(alligator.dU_R), str(alligator.dL), str(alligator.offsprings_count), str(alligator.c_pp_DDE), str(alligator.c_dieldrin), str(alligator.c_toxaphene), str(alligator.c_trans_nonachlor), str(alligator.pp_DDE), str(alligator.dieldrin), str(alligator.toxaphene), str(alligator.trans_nonachlor), str(alligator.mass), str(alligator.d_pp_DDE_mt), str(alligator.d_dieldrin_mt), str(alligator.d_toxaphene_mt), str(alligator.d_trans_nonachlor_mt)])  # add more attr ? #  
                    #self.results.append([str(alligator.id), str(t), str(self.curr_date.year) + "-" + str(self.curr_date.month) + "-" + str(self.curr_date.day), str(alligator.U_E)])  # add more attr ? #  

                print(t,"out of", str(self.sim_dur))

            self.curr_date += datetime.timedelta(days=1)

        # append results[] to csv file
        #orgininal: np.savetxt("/Users/dan/Downloads/internship/model/IbmAlligator-DEB-model/Alligator IBM/results.csv", self.results, delimiter = ',', header = "id, sim. day, current day, current month, current year, energy buffer, maturity level, repro. buffer, SNV length, DELTA energy buffer, DELTA maturity level, DELTA repro buffer, DELTA structural length, offsprings count, concentration of pp_DDE, concentration of dieldrin, concentration of toxaphene, concentration of trans-nonachlor, load of pp DDE, load of dieldrin, load of toxaphene, load of trans nonachlor, alligator mass, mat transfer ppDDE, mat transfer dieldrin, mat transfer toxaphene, mat transfer trans nonachlor")# 
        np.savetxt("/Users/dan/Downloads/internship/model/IbmAlligator-DEB-model/Alligator IBM/results.csv", self.results, fmt="%s", delimiter = ',', header = "id,sim. day,current year-month-day,energy buffer,maturity level,repro. buffer,SNV length,DELTA energy buffer,DELTA maturity level,DELTA repro buffer,DELTA structural length,offsprings count,concentration of pp_DDE,concentration of dieldrin,concentration of toxaphene,concentration of trans-nonachlor,load of pp DDE,load of dieldrin,load of toxaphene,load of trans nonachlor,alligator mass,mat transfer ppDDE,mat transfer dieldrin,mat transfer toxaphene,mat transfer trans nonachlor")# 
        #np.savetxt("/Users/dan/Downloads/internship/model/IbmAlligator-DEB-model/Alligator IBM/results.csv", self.results, fmt="%s", delimiter = ',', header = "id, sim. day, current year-month-day, energy buffer")# 
       
        #/vol/milkunB/ES_students/dhahn/simulation_results.csv
    
    def plot(self):
        '''
        for quick overview of results, only plots first alligator in self.alligators
        
        Attributes: 
            a lot of arrays to store values
        '''

        #getting x y values as arrays
        day_array = []

        energy_buffer_array = []
        maturity_level_array = []
        repro_buffer_array = []
        sNV_length_array = []
        mass_array = []
        
        c_pp_DDE_array = []
        c_dieldrin_array = []
        c_toxaphene_array = []
        c_trans_nonachlor_array = []
        
        pp_DDE_array = []
        dieldrin_array = []
        toxaphene_array = []
        trans_nonachlor_array = []
        
        for line in range(0, len(self.results), len(self.alligators)): 
            day_array.append(float(self.results[line][1]))           

            energy_buffer_array.append(float(self.results[line][3])) 
            maturity_level_array.append(float(self.results[line][4]))
            repro_buffer_array.append(float(self.results[line][5]))
            sNV_length_array.append(float(self.results[line][6])) 
            
            c_pp_DDE_array.append(float(self.results[line][12]))
            c_dieldrin_array.append(float(self.results[line][13]))
            c_toxaphene_array.append(float(self.results[line][14]))
            c_trans_nonachlor_array.append(float(self.results[line][15]))
            
            pp_DDE_array.append(float(self.results[line][16]))
            dieldrin_array.append(float(self.results[line][17]))
            toxaphene_array.append(float(self.results[line][18]))
            trans_nonachlor_array.append(float(self.results[line][19]))

            mass_array.append(float(self.results[line][20]))  

        # create plots from arrays
        fig, axs = plt.subplots(4) 
        fig.suptitle('DEB parameters over time for 1 Alligator')

        axs[2].plot(day_array, energy_buffer_array)
        #axs[5].set_title("energy buffer (time)")
        axs[2].set(xlabel='time [d]', ylabel='energy buffer [J]')

        axs[0].plot(day_array, sNV_length_array)
        axs[0].set(xlabel='time [d]', ylabel='SNV length [cm]')
        
        # axs[1].plot(day_array, c_pp_DDE_array)
        # axs[1].set(xlabel='days', ylabel='conc. pp DDE(ug/kg)')

        # axs[2].plot(day_array, c_dieldrin_array)
        # axs[2].set(xlabel='days', ylabel='conc. dieldrin(ug/kg)')
                
        # axs[3].plot(day_array, c_toxaphene_array) 
        # axs[3].set(xlabel='days', ylabel='conc. toxaphene(ug/kg)')

        # axs[4].plot(day_array, c_trans_nonachlor_array) 
        # axs[4].set(xlabel='days', ylabel='conc. trans-nonachlor(ug/kg)')
                
        axs[3].plot(day_array, repro_buffer_array)
        axs[3].set(xlabel='time [d]', ylabel='repro buffer [J]')
        
        axs[1].plot(day_array, maturity_level_array)
        axs[1].set(xlabel='time [d]', ylabel='maturity level [J]')

        #axs[1].plot(day_array, pp_DDE_array)
        #axs[1].set(xlabel='days', ylabel='pp DDE(ug)')

        #axs[2].plot(day_array, dieldrin_array)
        #axs[2].set(xlabel='days', ylabel='dieldrin(ug)')
                
        #axs[3].plot(day_array, toxaphene_array) 
        #axs[3].set(xlabel='days', ylabel='toxaphene(ug)')

        #axs[4].plot(day_array, trans_nonachlor_array) 
        #axs[4].set(xlabel='days', ylabel='trans-nonachlor(ug)')

        #axs[6].plot(day_array, mass_array)
        #axs[6].set(xlabel='days', ylabel='mass(kg)')
        
        plt.show()


'initiate a simulation' 
s1 = Simulation("02/14/08", 25000, clutch_size=1)

'run simulation'
s1.run()
s1.plot()
#print(str(s1.alligators[0].U_init))
#print(str(s1.alligators[0].c_T))

#help(Simulation)

