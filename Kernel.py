import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from ModelSetUp import *
from CurrModelPara import *
from Curve import *
#from Main_cal_opt import find_optimal_value



class RL_Kernel():
    def __init__(self):
        #self.reward = None
        #self.value = None
        #self.action = None
        self.alpha = 0.2
        self.date = 'March 07 2019'
        self.LAC_last_windows = 1#0
        self.probabilistic = 0#1
        self.RT_DA = 0#1
        self.curr_time = 0
        self.curr_scenario = 1
        self.current_stage ='training_50'

    def main_function(self):
        start = 1
        end = 49
        for curr_scenario in range(start, end):
            for i in range(0, 23):
                self.curr_time = i
                self.curr_scenario = curr_scenario
                self.calculate_optimal_soc()
                self.get_final_curve_main()





    def calculate_optimal_soc(self):
        self.curr_model_para = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time, self.curr_scenario, self.current_stage)
        # LAC_last_windows,  probabilistic, RT_DA, date, LAC_bhour, scenario

        print('##############################' + 'scenario = ' + str(self.curr_scenario) + ', and curr_time = ' + str(self.curr_time) + '######################################')



        print('################################## psh_system set up ##################################')
        self.psh_system = PshSystem(self.curr_model_para)
        self.psh_system.set_up_parameter()
        print(self.psh_system.parameter)

        print('################################## e_system set up ##################################')
        self.e_system = ESystem(self.curr_model_para)
        self.e_system.set_up_parameter()
        print(self.e_system.parameter)

        print('################################## lmp_system set up ##################################')
        self.lmp = LMP(self.curr_model_para)
        self.lmp.set_up_parameter()
        #print(self.lmp.date)
        print('lmp_quantiles=', self.lmp.lmp_quantiles)
        print('lmp_scenarios=', self.lmp.lmp_scenarios)
        print('lmp_Nlmp_s=', self.lmp.Nlmp_s)

        print('################################## curve set up ##################################')
        self.old_curve = Curve(30, 0, 3000)
        self.old_curve.input_curve(self.curr_time, self.curr_scenario - 1)
        print(self.old_curve.segments)

        print('################################## ADP training model set up ##################################')
        model_1 = Model('DAMarket')
        self.curr_model = RLSetUp(self.psh_system, self.e_system, self.lmp, self.old_curve, self.curr_model_para, model_1)
        self.curr_model.optimization_model()
        self.optimal_soc_sum = self.curr_model.optimal_soc_sum
        self.optimal_psh_gen_sum = self.curr_model.optimal_psh_gen_sum
        self.optimal_psh_pump_sum = self.curr_model.optimal_psh_pump_sum
        print(self.curr_model.optimal_soc_sum)


    def calculate_new_soc(self, initial_soc):
        pre_model = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time,
                                  self.curr_scenario, self.current_stage)
        # LAC_last_windows,  probabilistic, RT_DA, date, LAC_bhour, scenario

        psh_system_2 = PshSystem(pre_model)
        psh_system_2.set_up_parameter()


        e_system_2 = ESystem(pre_model)
        e_system_2.set_up_parameter()
        e_system_2.parameter['EStart'] = initial_soc
        print('e_system_2.parameter is ' + str(e_system_2.parameter))


        if self.curr_time != 22:
            # lmp, time = t+1, scenario= n
            self.prev_model = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time + 1,
                                       self.curr_scenario, self.current_stage)
            self.prev_lmp = LMP(self.prev_model)
            self.prev_lmp.set_up_parameter()
            # curve, time = t+1, scenario= n-1
            self.pre_curve = Curve(30, 0, 3000)
            self.pre_curve.input_curve(self.curr_time + 1, self.curr_scenario - 1)
        elif self.curr_time == 22:
            self.prev_model = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time,
                                       self.curr_scenario, self.current_stage)
            self.prev_lmp = LMP(self.prev_model)
            self.prev_lmp.set_up_parameter()

            self.pre_curve = Curve(30, 0, 3000)
            self.pre_curve.input_curve(self.curr_time, self.curr_scenario - 1)

        model_1 = Model('DAMarket')
        ADP_train_model_para = pre_model


        pre_model = RLSetUp(psh_system_2, e_system_2, self.prev_lmp, self.pre_curve, ADP_train_model_para, model_1)
        pre_model.optimization_model_with_input()
        rt = pre_model.optimal_profit
        return rt



#after we get the current self.optimal_profit and self.optimal_soc_sum, we have to update the curve

    def get_final_curve_main(self):
        self.get_new_curve_step_1()  # 基于此次最优解的model
        print(self.curve.segments)
        self.get_new_curve_step_2_curve_comb()  # (1-\alpha)*old_curve + \alpha*old_curve

        # new curve: self.new_curve_slope
        self.get_new_curve_step_3_two_pts()  # update the new curve with the two new points
        # new points: self.update_point_1 and self.update_point_2
        self.curve.curve_update(self.new_curve_slope, self.update_point_1, self.update_point_2)
        print(self.curve.segments)
        self.output_curve()
        self.output_curve_sum()


    def get_new_curve_step_1(self):
    #how can we get each new curve_point_X
        self.curve = self.old_curve
        self.second_curve_soc = self.curve.point_X

    #get new curve_profit
        self.second_curve_profit = []
        beta = 0.001

        # make sure its terminal soc works

        for value in self.second_curve_soc:
            left_value = (value - float(self.e_system.parameter['EEnd'])) - (
                    (23 - self.curr_time) * float(self.psh_system.parameter['GenMax']) / (
                    float(self.psh_system.parameter['GenEfficiency']) + beta))
            right_value = (value - float(self.e_system.parameter['EEnd'])) - (
                    -(23 - self.curr_time) * float(self.psh_system.parameter['PumpMax']) * (
                    float(self.psh_system.parameter['PumpEfficiency']) - beta))
            if (left_value < 0 and right_value > 0):
                point_y = self.calculate_new_soc(value)
            else:
                point_y = self.calculate_pts(value)

            self.second_curve_profit.append(point_y)


    #get new curve_slope
        self.second_curve_slope = [self.old_curve.intial_slope_set]
        for index in range(1, len(self.second_curve_soc)):
            temp_slop = (self.second_curve_profit[index] - self.second_curve_profit[index -1])/self.curve.steps
            self.second_curve_slope.append(temp_slop)
            #change the first back
        #self.second_curve_slope[0] = self.second_curve_slope.intial_slope_set

    # make sure it is convex
        for i in range(len(self.second_curve_slope)):
            _cur = len(self.second_curve_slope) - i - 1
            if _cur != 0 and self.second_curve_slope[_cur] > self.second_curve_slope[_cur-1]:
                self.second_curve_slope[_cur - 1] = self.second_curve_slope[_cur]





    def get_new_curve_step_2_curve_comb(self):
    #new curve combine with the old_slope
        self.new_curve_slope = []
        for i in range(len(self.second_curve_soc)):
            _temp = (1 - self.alpha)*self.old_curve.point_Y[i] + self.alpha*self.second_curve_slope[i]
            self.new_curve_slope.append(_temp) #this is the new slope we need
        print(self.new_curve_slope)

    def get_new_curve_step_3_two_pts(self):
        #need find another point #be careful boundary case

        # get second point
        # get second point profit
        if self.optimal_soc_sum + 1 > self.curve.up_bd:
            self.second_point_soc_sum = self.optimal_soc_sum - 1#self.curve.steps
            self.second_point_profit = self.calculate_new_soc(self.second_point_soc_sum)
        else:
            self.second_point_soc_sum = self.optimal_soc_sum + 1  # self.curve.steps
            self.second_point_profit = self.calculate_new_soc(self.second_point_soc_sum)

        # get previous point profit
        if self.optimal_soc_sum - 1 < self.curve.up_bd:
            self.previous_point_soc_sum = self.optimal_soc_sum + 1#self.curve.steps
            self.previous_point_profit = self.calculate_new_soc(self.previous_point_soc_sum)
        else:
            self.previous_point_soc_sum = self.optimal_soc_sum - 1  # self.curve.steps
            self.previous_point_profit = self.calculate_new_soc(self.previous_point_soc_sum)
        # shall we get the optimal at previous???
        self.pre_scen_optimal_profit = self.calculate_new_soc(self.optimal_soc_sum)

        #calcuate self.update_point_1/2(point_x, point_curve)
        if self.optimal_soc_sum + 1 > self.curve.up_bd:
            # self.optimal_profit and self.optimal_soc_sum
            self.update_point_1_x = self.optimal_soc_sum
            self.update_point_1_y = (self.pre_scen_optimal_profit - self.previous_point_profit) #self.curve.steps
            #
            self.update_point_2_x = self.optimal_soc_sum
            self.update_point_2_y = (self.pre_scen_optimal_profit - self.previous_point_profit) #self.curve.steps

        elif self.optimal_soc_sum - 1 < self.curve.lo_bd:
            #self.optimal_profit and self.optimal_soc_sum
            self.update_point_1_x = self.optimal_soc_sum
            self.update_point_1_y = (self.second_point_profit - self.pre_scen_optimal_profit) #self.curve.steps
            ##这里写错了，到底是update前面的点，还是这个点？
            self.update_point_2_x = self.optimal_soc_sum
            self.update_point_2_y = (self.second_point_profit - self.pre_scen_optimal_profit) #self.curve.steps
        else:
            self.update_point_1_x = self.optimal_soc_sum
            self.update_point_1_y = (self.pre_scen_optimal_profit - self.previous_point_profit) #self.curve.steps
            self.update_point_2_x = self.second_point_soc_sum
            self.update_point_2_y = (self.second_point_profit - self.pre_scen_optimal_profit) #self.curve.steps
        self.update_point_1 = [self.update_point_1_x, self.update_point_1_y]
        self.update_point_2 = [self.update_point_2_x, self.update_point_2_y]

    def output_curve(self):
    #output the curve
        scenario = self.curr_scenario
        filename = self.e_system.e_start_folder + '/Curve_'+ 'time_'+ str(self.curr_model_para.LAC_bhour)+ '_scenario_' +  str(scenario)  + '.csv'
        df = pd.DataFrame(self.curve.segments, columns =['soc_segment','slope'])
        df.to_csv(filename, index=False, header=True)


    def output_curve_sum(self):
        #input the original
        curr_time = self.curr_model_para.LAC_bhour
        scenario = self.curr_model_para.scenario

        if scenario == 1:
            filename = self.e_system.e_start_folder  + '/Curve_' + 'time_' + str(curr_time) + '_scenario_' + str(scenario) + '.csv'
            df = pd.read_csv(filename)
        else:
            filename = self.e_system.e_start_folder + '/Curve_total_' + 'time_' + str(self.curr_model_para.LAC_bhour) + '.csv'
            df = pd.read_csv(filename)
        #output the current


        #df_cur = pd.DataFrame(self.curve.segments, columns=['soc_segment', 'slope_time_' + str(curr_time) + str(scenario)])
        df_cur = pd.DataFrame(self.curve.point_Y, columns=[ 'slope_time_' + str(curr_time) + str(scenario)])
        df = pd.concat([df, df_cur], axis = 1)

        filename = self.e_system.e_start_folder + '/Curve_total_' + 'time_' + str(self.curr_model_para.LAC_bhour)+'.csv'
        df.to_csv(filename, index=False, header=True)


    def calculate_pts(self, point_X):
        #put the soc_sum in, we get the profit
        point_x_soc = self.x_to_soc(point_X)
        point_profit = []
        for s in range(self.lmp.Nlmp_s):
            p_s = self.lmp.lmp_quantiles[s]
            for j in self.psh_system.parameter['PSHName']:
                point_profit.append((self.optimal_psh_gen_sum - self.optimal_psh_pump_sum) * self.lmp.lmp_scenarios[s][0] * p_s)
        # for j in self.psh_system.parameter['PSHName']:
        #     point_profit.append((self.psh_gen[j] - self.psh_pump[j]) * self.lmp.lmp_scenarios[0][0])

        self.curr_cost = sum(point_profit)
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





test = RL_Kernel()
#test.calculate_old_curve()
test.main_function()



