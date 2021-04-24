import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np


#len_var is the length of the length of the dynamic variable soc_n and I_n

class System():
    def __init__(self, curr_model):
        self.curr_model = curr_model
        self.Input_folder_parent = None
        self.filename = None
        self.Input_folder = None
        self.Output_folder = None
        self.parameter = {}
    
    def input_parameter(self, paranameter_name, in_model_name):
        Data = pd.read_csv(self.filename)
        df  = pd.DataFrame(Data)
        ret = list(df[paranameter_name])
        self.parameter[in_model_name] = ret[0]


class Curr_Model():
    def __init__(self, LAC_last_windows,  probabilistic, date, LAC_bhour):
        self.LAC_last_windows = LAC_last_windows
        self.LAC_bhour = LAC_bhour
        self.probabilistic = probabilistic
        self.date = date


# class Folder_Info():
#     def __init__(self, Input_folder_parent, Output_folder, curr_model):
#         self.curr_model = curr_model
#         self.Input_folder_parent = Input_folder_parent
#         self.Output_folder = self.Output_folder
#         self.date = self.curr_model.date
#         self.Input_folder = self.Input_folder_parent + '/' +self.date
#         self.filename = None



class PSH_system(System):

    def set_up_parameter(self):
##这个是给标量 #how to input one by one?
        self.Input_folder_parent = './Input_Curve/PSH-Rolling Window'
        self.Input_folder = self.Input_folder_parent +'/'+ self.curr_model.date
        self.filename = self.Input_folder +'/PSH.csv'
        self.input_parameter('GenMin', 'GenMin')
        self.input_parameter('GenMax', 'GenMax')
        self.input_parameter('PumpMin', 'PumpMin')
        self.input_parameter('PumpMax', 'PumpMax')
        self.input_parameter('Cost', 'Cost')
        self.input_parameter('Efficiency', 'GenEfficiency')
        self.input_parameter('Efficiency', 'PumpEfficiency')
        self.input_parameter('Name', 'PSHName')       

        self.Input_folder = None
        self.filename = None




class E_system(System):

    def set_up_parameter(self):
##这个是给标量 #how to input one by one?
        self.Input_folder_parent = './Input_Curve/PSH-Rolling Window'
        self.Input_folder = self.Input_folder_parent +'/'+ self.curr_model.date 
        self.filename = self.Input_folder +  '/Reservoir.csv'
        self.input_parameter('Min', 'EMin')
        self.input_parameter('Max', 'EMax')
        self.input_parameter('Name', 'EName') 
        self.input_parameter('End', 'EEnd')

        self.Output_folder='./Output_Curve'   
        if self.curr_model.LAC_bhour==0 or self.curr_model.LAC_last_windows:
            self.input_parameter('Start', 'EStart')
        else:
            filename = self.Output_folder+'/LAC_Solution_System_SOC_' + str(curr_model.LAC_bhour-1) + '.csv'
            self.input_parameter('SOC', 'EStart')
        self.Input_folder = None
        self.filename = None
        self.Output_folder = None



# class LMP(system):
    
#     def set_up_parameter(self):
#         return Pass







# psh_folder_info = Folder_Info(Input_folder_parent, Output_folder, curr_model)
psh_model = Curr_Model(1, 0 , 'March 07 2019', 1)   ##first is for last window second are stochastic, third is for the date, last is for hour
psh_system = PSH_system(psh_model)
psh_system.set_up_parameter()
print(psh_system.parameter)

e_model = Curr_Model(1, 0 , 'March 07 2019', 1)   ##first is for last window second are stochastic, third is for the date, last is for hour
e_system =E_system(e_model)
e_system.set_up_parameter()
print(e_system.parameter)



    

