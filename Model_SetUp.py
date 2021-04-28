import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from System_SetUp import *
from CurrModelPara import *
from Curve import *

class OptModelSetUp():

    def __init__(self, psh_system, e_system, lmp, curve, curr_model_para, gur_model):
        self.gur_model = gur_model
        self.psh_system = psh_system
        self.e_system = e_system
        self.lmp = lmp
        self.curve = curve
        self.curr_model_para = curr_model_para

    def add_var_e(self, var_name):
        return self.gur_model.addVars(self.e_system.parameter['EName'], ub=float('inf'),lb=-float('inf'), vtype="C", name=var_name)

    def add_var_I(self, var_name):
        return self.gur_model.addVars(self.e_system.parameter['EName'], vtype="B", name=var_name)

    def add_var_psh(self, var_name):
        return self.gur_model.addVars(self.psh_system.parameter['PSHName'], ub=float('inf'),lb=-float('inf'),vtype="C",name=var_name)

    def add_constraint_epsh(self):
        for j in self.psh_system.parameter['PSHName']:  # all are lists
            self.gur_model.addConstr(self.psh_gen[j] <= self.psh_system.parameter['GenMax'], name='%s_%s' % ('psh_gen_max0', j))
            self.gur_model.addConstr(self.psh_gen[j] >= self.psh_system.parameter['GenMin'], name='%s_%s' % ('psh_gen_min0', j))
            self.gur_model.addConstr(self.psh_pump[j] <= self.psh_system.parameter['PumpMax'], name='%s_%s' % ('psh_pump_max0', j))
            self.gur_model.addConstr(self.psh_pump[j] >= self.psh_system.parameter['PumpMin'], name='%s_%s' % ('psh_pump_min0', j))

        for k in self.e_system.parameter['EName']:
            self.gur_model.addConstr(self.e[k] <= self.e_system.parameter['EMax'], name='%s_%s' % ('e_max0', k))
            self.gur_model.addConstr(self.e[k] >= self.e_system.parameter['EMin'], name='%s_%s' % ('e_min0', k))


    def add_constraint_curve(self):
        for k in self.e_system.parameter['EName']:
            _temp_sum = 0
            for i in range(self.curve.numbers):
                _temp_sum += self.soc[i][k]
            LHS = self.e[k]
            RHS = _temp_sum  # RHS=soc[0][k]+soc[1][k]+soc[2][k]+soc[3][k]+soc[4][k]
            self.gur_model.addConstr(LHS == RHS, name='%s_%s' % ('curve', k))

    def add_constraint_soc(self):
    ### how to constraint for  d_1I_2 <= soc_1 <=d_1I_1?############################
        for k in self.e_system.parameter['EName']:
            for i in range(self.curve.numbers):
                name_num = str(i + 1)
                bench_num = i
                if bench_num == 0:
                    self.gur_model.addConstr(self.soc[bench_num][k] <= str(self.d[bench_num]) * self.I[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_max', k))
                    self.gur_model.addConstr(str(self.d[bench_num]) * self.I[bench_num + 1][k] <= self.soc[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_min', k))
                elif bench_num == self.curve.numbers - 1:
                    self.gur_model.addConstr(self.soc[bench_num][k] <= str(self.d[bench_num]) * self.I[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_max', k))
                    self.gur_model.addConstr(0 <= self.soc[bench_num][k], name='%s_%s' % ('soc_' + name_num + '_min', k))
                else:
                    self.gur_model.addConstr(self.soc[bench_num][k] <= str(self.d[bench_num]) * self.I[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_max', k))
                    self.gur_model.addConstr(str(self.d[bench_num]) * self.I[bench_num + 1][k] <= self.soc[bench_num][k],
                                    name='%s_%s' % ('soc_' + name_num + '_min', k))

    def add_constraint_I(self):
        for s in range(self.lmp.Nlmp_s):
            for k in self.e_system.parameter['EName']:
                for i in range(self.curve.numbers - 1):
                    name_num = str(i + 1)
                    name_num_next = str(i + 2)
                    bench_num = i
                    self.gur_model.addConstr(self.I[bench_num + 1][k] <= self.I[bench_num][k],
                                    name='%s_%s' % ('I_' + name_num_next + '_' + name_num, k))






class RLSetUp(OptModelSetUp):
#psh_system, e_system, lmp, curve, curr_model_para, gur_model
    def set_up_variable(self):
    #add gen/pump
        self.psh_gen = self.add_var_psh('psh_gen')
        self.psh_pump = self.add_var_psh('psh_pump')

    # add e
        self.e = self.add_var_e('e')

    #add soc and I
        #self.len_var = self.curve.numbers #len(self.curve.point_X)-1
        self.soc = []
        self.I = []
        for i in range(self.curve.numbers):
            name_num = str(i + 1)
            self.soc.append(self.add_var_e('soc_' + name_num))
            self.I.append(self.add_var_I('I_' + name_num))

    #add d
        d = []
        for i in range(self.curve.numbers):
            d.append(self.curve.point_X[i+1]-self.curve.point_X[i])
        self.d = d

        self.gur_model.update()

    def set_up_constraint(self):

    # upper and lower constraint
        self.add_constraint_epsh()
    # curve constraint
        self.add_constraint_curve()
    # constraint for  d_1I_2 <= soc_1 <=d_1I_1?
        self.add_constraint_soc()
    # constraint for I_1<=I_2<=I_3
        self.add_constraint_I()

        self.gur_model.update()

    def set_up_object(self):
        self.profit_max = []
        for s in range(self.lmp.Nlmp_s):
            p_s = self.lmp.lmp_quantiles[s]
            for j in self.psh_system.parameter['PSHName']:
                self.profit_max.append((self.psh_gen[j] - self.psh_pump[j]) * self.lmp.lmp_scenarios[s][0] * p_s)

        for k in self.e_system.parameter['EName']:
            for i in range(self.curve.numbers):
                bench_num = i
                self.profit_max.append(self.curve.point_Y[bench_num] * self.soc[bench_num][k])
        print(self.profit_max)
        self.obj = quicksum(self.profit_max)


    def solve_model(self):
        self.set_up_variable()
        self.set_up_constraint()
        self.set_up_object()

        self.gur_model.setObjective(self.obj, GRB.MAXIMIZE)
        self.gur_model.optimize()

        # print results for variables
        for v in self.gur_model.getVars():
            print("%s %f" % (v.Varname, v.X))
            # print("%s %f %f" % (v.Varname, v.X, v.Pi))



    #get optimal soc
        self.optimal_soc = []
        self.optimal_psh_pump = []
        self.optimal_psh_gen= []
        _temp = list(self.e_system.parameter['EName'])[0]
        for v in [v for v in self.gur_model.getVars() if (_temp in v.Varname and 'soc' in v.Varname)]:
            soc = v.X
            self.optimal_soc.append(soc)
        self.optimal_soc_sum = sum(self.optimal_soc)

    #get optimal_psh_gen/pump
        for v in [v for v in self.gur_model.getVars() if 'psh_gen' in v.Varname]:
            psh = v.X
            self.optimal_psh_gen.append(psh)
        self.optimal_psh_gen_sum = sum(self.optimal_psh_gen)
        for v in [v for v in self.gur_model.getVars() if 'psh_pump' in v.Varname]:
            psh = v.X
            #psh0.append(-psh)
            self.optimal_psh_pump.append(psh)
        self.optimal_psh_pump_sum = sum(self.optimal_psh_pump)

    #get optimal profit
        self.optimal_profit = self.calculate_pts(self.optimal_soc_sum)



#after we get the current self.optimal_profit and self.optimal_soc_sum, we have to update the curve


    def get_new_curve(self, alpha = 0.5):
        self.alpha = alpha
    #how can we get each new curve_point_X
        self.second_curve_soc = self.curve.point_X

    #get new curve_profit
        self.second_curve_profit = []
        for value in self.second_curve_soc:
            point_y = self.calculate_pts(value)
            self.second_curve_profit.append(point_y)

    #get new curve_slope
        self.second_curve_slope = [0]
        for index in range(1, len(self.second_curve_soc)):
            temp_slop = (self.second_curve_profit[index]- self.second_curve_profit[index -1])/self.curve.steps
            self.second_curve_slope.append(temp_slop)
        self.second_curve_slope[0] = self.second_curve_slope[1]

    #new curve combine with the old_slope
        self.new_curve_slope = []
        for i in range(len(self.second_curve_soc)):
            _temp = (1 - self.alpha)*self.curve.point_Y[i] + self.alpha*self.second_curve_slope[i]
            self.new_curve_slope.append(_temp) #this is the new slope we need

    #new curve: self.new_curve_slope
    #update the new curve with the two new points
        self.get_important_pt()
        self.curve.curve_update(self.new_curve_slope, self.update_point_1, self.update_point_2)


    def calculate_pts(self, point_X):
        #put the soc_sum in, we get the profit
        point_x_soc = self.x_to_soc(point_X)
        point_profit = []
        for s in range(self.lmp.Nlmp_s):
            p_s = self.lmp.lmp_quantiles[s]
            for j in self.psh_system.parameter['PSHName']:
                point_profit.append((self.optimal_psh_gen_sum - self.optimal_psh_pump_sum) * self.lmp.lmp_scenarios[s][0] * p_s)

        for k in self.e_system.parameter['EName']:
            for i in range(self.curve.numbers):
                bench_num = i
                point_profit.append(self.curve.point_Y[bench_num] * point_x_soc[bench_num])
        point_profit_sum = sum(point_profit)
        return point_profit_sum

    def x_to_soc(self, point_X):
        #change soc_sum to soc_1 + soc_2 + soc_3
        turn_1 = point_X // self.curve.steps
        rest = point_X % self.curve.steps
        point_x_soc = []
        for i in range(self.curve.numbers):
            if turn_1 >  0:
                point_x_soc.append(self.curve.steps)
                turn_1 -= 1
            elif turn_1 == 0:
                point_x_soc.append(rest)
                turn_1 -= 1
            else:
                point_x_soc.append(0)
        return point_x_soc

    def get_important_pt(self):
        #need find another point #be careful boundary case
    # get second point
    # get second point profit
        if self.optimal_soc_sum + self.curve.steps > self.curve.up_bd:
            self.second_point_soc_sum = self.optimal_soc_sum - self.curve.steps
            self.second_point_profit = self.calculate_pts(self.second_point_soc_sum)
        else:
            self.second_point_soc_sum = self.optimal_soc_sum + self.curve.steps
            self.second_point_profit = self.calculate_pts(self.second_point_soc_sum)

    # get previous point profit
        if self.optimal_soc_sum + self.curve.steps > self.curve.up_bd:
            self.previous_point_soc_sum = self.optimal_soc_sum -  self.curve.steps
            self.previous_point_profit = self.calculate_pts(self.second_point_soc_sum)
        else:
            self.previous_point_soc_sum = self.optimal_soc_sum - self.curve.steps
            self.previous_point_profit = self.calculate_pts(self.second_point_soc_sum)

    #calcuate self.update_point_1/2(point_x, point_curve)
        if self.optimal_soc_sum + self.curve.steps > self.curve.up_bd:
            #self.optimal_profit and self.optimal_soc_sum
            #need check?
            self.update_point_1_x = self.optimal_soc_sum
            self.update_point_1_y = (self.optimal_profit - self.previous_point_profit) / self.curve.steps
            self.update_point_2_x = self.optimal_profit
            self.update_point_2_y = (self.optimal_profit - self.previous_point_profit) / self.curve.steps
        else:
            self.update_point_1_x = self.optimal_soc_sum
            self.update_point_1_y = (self.optimal_profit - self.previous_point_profit)/self.curve.steps
            self.update_point_2_x = self.second_point_soc_sum
            self.update_point_2_y = (self.second_point_profit - self.optimal_profit)/self.curve.steps
        self.update_point_1 = [self.update_point_1_x, self.update_point_1_y]
        self.update_point_2 = [self.update_point_2_x, self.update_point_2_y]


















# print(e_system_1.parameter['EName'])
# model_1 = Model('DAMarket')
# ADP_train_model_para = CurrModelPara(1, 0, 1, 'March 07 2019', 1)
#
# ADP_train_system = RLSetUp(psh_system_1, e_system_1, lmp_1, curve_1, ADP_train_model_para, model_1)
# ADP_train_system.set_up_variable()
# ADP_train_system.set_up_constraint()
# ADP_train_system.set_up_object()
# ADP_train_system.solve_model()
# print(ADP_train_system.soc)




# test for x_to_soc
# def x_to_soc(point_X):
#     numbers = 100
#     steps = 30
#     turn_1 = point_X // steps
#     rest = point_X % steps
#     point_x_soc = []
#     for i in range(numbers):
#         if turn_1 >  0:
#             point_x_soc.append(steps)
#             turn_1 -= 1
#         elif turn_1 == 0:
#             point_x_soc.append(rest)
#             turn_1 -= 1
#         else:
#             point_x_soc.append(0)
#     return point_x_soc
#
# point_x_soc = x_to_soc(157)
# print(point_x_soc)
# print(len(point_x_soc))