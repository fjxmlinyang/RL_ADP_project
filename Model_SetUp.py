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

class OptModelSetUp():
    def __init__(self, psh_system, e_system, lmp, curve, ADP_train_model_para, model):
        return
    
    def add_e(self, var_name):
        return model.addVars(e_system.parameter['EName'], ub=float('inf'),lb=-float('inf'), vtype="C", name=var_name)
        
    def add_I(self, var_name):
        return model.addVars(e_system.parameter['EName'], vtype="B", name=var_name)
        
    def add_psh(self, var_name):
        return model.addVars(psh_system.parameter['PSHName'], ub=float('inf'),lb=-float('inf'),vtype="C",name=var_name)


    def add_constraint_epsh(self):
        for j in psh_system.parameter['PSHName']:  # all are lists
            model.addConstr(self.psh_gen[j] <= psh_system.parameter['GenMax'], name='%s_%s' % ('psh_gen_max0', j))
            model.addConstr(self.psh_gen[j] >= psh_system.parameter['GenMin'], name='%s_%s' % ('psh_gen_min0', j))
            model.addConstr(self.psh_pump[j] <= psh_system.parameter['PumpMax'], name='%s_%s' % ('psh_pump_max0', j))
            model.addConstr(self.psh_pump[j] >= psh_system.parameter['PumpMin'], name='%s_%s' % ('psh_pump_min0', j))

        for k in e_system.parameter['EName']:
            model.addConstr(self.e[k] <= e_system.parameter['EMax'], name='%s_%s' % ('e_max0', k))
            model.addConstr(self.e[k] >= e_system.parameter['EMin'], name='%s_%s' % ('e_min0', k))


    def add_constraint_curve(self):
        for k in e_system.parameter['EName']:
            _temp_sum = 0
            for i in range(self.len_var):
                _temp_sum += self.soc[i][k]
            LHS = self.e[k]
            RHS = _temp_sum  # RHS=soc[0][k]+soc[1][k]+soc[2][k]+soc[3][k]+soc[4][k]
            model.addConstr(LHS == RHS, name='%s_%s' % ('curve', k))

    def add_constraint_soc(self):
    ### how to constraint for  d_1I_2 <= soc_1 <=d_1I_1?############################
        for k in e_system.parameter['EName']:
            for i in range(self.len_var):
                name_num = str(i + 1)
                bench_num = i
                if bench_num == 0:
                    model.addConstr(self.soc[bench_num][k] <= str(self.d[bench_num]) * self.I[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_max', k))
                    model.addConstr(str(self.d[bench_num]) * self.I[bench_num + 1][k] <= self.soc[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_min', k))
                elif bench_num == self.len_var - 1:
                    model.addConstr(self.soc[bench_num][k] <= str(self.d[bench_num]) * self.I[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_max', k))
                    model.addConstr(0 <= self.soc[bench_num][k], name='%s_%s' % ('soc_' + name_num + '_min', k))
                else:
                    model.addConstr(self.soc[bench_num][k] <= str(self.d[bench_num]) * self.I[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_max', k))
                    model.addConstr(str(self.d[bench_num]) * self.I[bench_num + 1][k] <= self.soc[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_min', k))

    def add_constraint_I(self):
        for s in range(lmp.Nlmp_s):
            for k in e_system.parameter['EName']:
                for i in range(self.len_var - 1):
                    name_num = str(i + 1)
                    name_num_next = str(i + 2)
                    bench_num = i
                    model.addConstr(self.I[bench_num + 1][k] <= self.I[bench_num][k],
                                    name='%s_%s' % ('I_' + name_num_next + '_' + name_num, k))

    def set_up_variable(self):
    #add gen/pump
        self.psh_gen = self.add_psh('psh_gen')
        self.psh_pump = self.add_psh('psh_pump')

    # add e
        self.e = self.add_e('e')
        
    #add soc and I
        self.len_var = len(curve.point_X)-1
        self.soc = []
        self.I = []
        for i in range(self.len_var):
            name_num = str(i + 1)
            self.soc.append(self.add_e('soc_' + name_num))
            self.I.append(self.add_I('I_' + name_num))

    #add d
        d = []
        for i in range(curve.numbers):
            d.append(curve.point_X[i+1]-curve.point_X[i])
        self.d = d

        model.update()

    def set_up_constraint(self):

    # upper and lower constraint
        self.add_constraint_epsh()
    # curve constraint
        self.add_constraint_curve()
    # constraint for  d_1I_2 <= soc_1 <=d_1I_1?
        self.add_constraint_soc()
    # constraint for I_1<=I_2<=I_3
        self.add_constraint_I()

        model.update()








print(e_system.parameter['EName'])
model = Model('DAMarket')
ADP_train_model_para= CurrModel(1, 0, 1, 'March 07 2019', 1)

ADP_train_system = OptModelSetUp(psh_system, e_system, lmp, curve, ADP_train_model_para, model)
ADP_train_system.set_up_variable()
ADP_train_system.set_up_constraint()
print(ADP_train_system.soc)