import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from Model_SetUp import *
from CurrModelPara import *
from Curve import *


# psh_folder_info = Folder_Info(Input_folder_parent, Output_folder, curr_model)
# Curr_Model(LAC_last_windows是否是最后,  probabilistic是否是随机模型, RT_DA是否是RT, date, LAC_bhour开始时间)


print('################################## psh_system set up ##################################')

psh_model_1 = CurrModelPara(1, 0, 1, 'March 07 2019', 1)   ##first is for last window second are stochastic, third is for the date, last is for hour
psh_system_1 = PshSystem(psh_model_1)
psh_system_1.set_up_parameter()
print(psh_system_1.parameter)

print('################################## e_system set up ##################################')
e_model_1 = CurrModelPara(1, 0, 1, 'March 07 2019', 1)   ##first is for last window second are stochastic, third is for the date, last is for hour
e_system_1 = ESystem(e_model_1)
e_system_1.set_up_parameter()
print(e_system_1.parameter)


print('################################## lmp_system set up ##################################')
lmp_model_1 = CurrModelPara(1, 0, 1, 'March 07 2019', 1)
print(lmp_model_1.date)  ##first is for last window second are stochastic, third is for the date, last is for hour
lmp_1 = LMP(lmp_model_1)
lmp_1.set_up_parameter()
print('lmp_quantiles=', lmp_1.lmp_quantiles)
print('lmp_scenarios=', lmp_1.lmp_scenarios)
print('lmp_Nlmp_s=', lmp_1.Nlmp_s)


print('################################## curve set up ##################################')
curve_old = Curve(100, 0, 3000)
curve_old.seg_initial()
curve_old.curve_initial()
print(curve_old.segments)


print('################################## ADP training model set up ##################################')


print(e_system_1.parameter['EName'])
model_1 = Model('DAMarket')
ADP_train_model_para = CurrModelPara(1, 0, 1, 'March 07 2019', 1)

ADP_train_system = RLSetUp(psh_system_1, e_system_1, lmp_1, curve_old, ADP_train_model_para, model_1)
ADP_train_system.solve_model()

point1 = ADP_train_system.optimal_soc_sum

#print(ADP_train_system.soc)
print(ADP_train_system.optimal_psh_pump_sum)
print(ADP_train_system.optimal_profit)
