import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from System_SetUp import *
from curve import *


# psh_folder_info = Folder_Info(Input_folder_parent, Output_folder, curr_model)
# Curr_Model(LAC_last_windows是否是最后,  probabilistic是否是随机模型, RT_DA是否是RT, date, LAC_bhour开始时间)


print('################################## psh_system set up ##################################')

psh_model = CurrModel(1, 0 , 1,'March 07 2019', 1)   ##first is for last window second are stochastic, third is for the date, last is for hour
psh_system = PshSystem(psh_model)
psh_system.set_up_parameter()
print(psh_system.parameter)

print('################################## e_system set up ##################################')
e_model = CurrModel(1, 0 ,1, 'March 07 2019', 1)   ##first is for last window second are stochastic, third is for the date, last is for hour
e_system = ESystem(e_model)
e_system.set_up_parameter()
print(e_system.parameter)


print('################################## lmp_system set up ##################################')
lmp_model = CurrModel(1, 0 ,1, 'March 07 2019', 1) 
print(lmp_model.date)  ##first is for last window second are stochastic, third is for the date, last is for hour
lmp = LMP(lmp_model)
lmp.set_up_parameter()
print('lmp_quantiles=', lmp.lmp_quantiles)
print('lmp_scenarios=', lmp.lmp_scenarios)
print('lmp_Nlmp_s=', lmp.Nlmp_s)


print('################################## curve set up ##################################')
curve = Curve(100, 0, 3000)
curve.seg_initial()
curve.curve_initial()
print(curve.segments)


print('################################## ADP training model set up ##################################')

class RL_OptModel_SetUp():
    def __init__(self, psh_system, e_system, lmp, curve, ADP_train_model_para, model):
        return
    
    def add_e(self, var_name):
        return model.addVars(e_system.parameter['EName'], ub=float('inf'),lb=-float('inf'), vtype="C", name=var_name)
        
    def add_I(self, var_name):
        return model.addVars(e_system.parameter['EName'], vtype="B", name=var_name)
        
    def add_psh(self, var_name):
        return model.addVars(psh_system.parameter['PSHName'], ub=float('inf'),lb=-float('inf'),vtype="C",name=var_name)






    def set_up_variable(self):
        #add gen/pump
        self.psh_gen = self.add_psh('psh_gen')
        self.psh_pump = self.add_psh('psh_pump')

        # add e
        self.e = self.add_e('e')
        
        #add soc and I
        len_var = len(curve.point_X)-1
        self.soc = []
        self.I = []
        for i in range(len_var):
            name_num = str(i + 1)
            self.soc.append(self.add_e('e_' + 'name_num'))
            self.I.append(self.add_I('I_' + 'name_num'))

        #add d
        d = []
        for i in range(curve.numbers):
            d.append(curve.point_X[i+1]-curve.point_X[i])
        self.d = d

    def set_up_constraint(self):









print(e_system.parameter['EName'])
model = Model('DAMarket')
ADP_train_model_para= CurrModel(1, 0, 1, 'March 07 2019', 1)

ADP_train_system = RL_OptModel_SetUp(psh_system, e_system, lmp, curve, ADP_train_model_para, model)
ADP_train_system.set_up_variable()
print(ADP_train_system.I)