
from multiprocess import *
import time

from gurobipy import *

#
# class MultiRLSetUp():
#
#     def __init__(self):
#         self.alpha = 0.8  # 0.2
        # self.date = 'March 07 2019'
        # self.LAC_last_windows = 0  # 1#0
        # self.probabilistic = 1  # 0#1
        # self.RT_DA = 1  # 0#1
        # self.curr_time = 0
        # self.curr_scenario = 1
        # self.current_stage = 'training_500'

    #def calculate_new_soc(self):
        # self.alpha = 0.8  # 0.2
        # self.date = 'March 07 2019'
        # self.LAC_last_windows = 0  # 1#0
        # self.probabilistic = 1  # 0#1
        # self.RT_DA = 1  # 0#1
        # self.curr_time = 0
        # self.curr_scenario = 1
        # self.current_stage = 'training_500'
        # pre_model_para = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time,
        #                           self.curr_scenario, self.current_stage)
        # # LAC_last_windows,  probabilistic, RT_DA, date, LAC_bhour, scenario

        # psh_system_2 = PshSystem(pre_model_para)
        # psh_system_2.set_up_parameter()


        # e_system_2 = ESystem(pre_model_para)
        # e_system_2.set_up_parameter()
        # #e_system_2.parameter['EStart'] = initial_soc
 
        # if self.curr_time != 22:
        #     # lmp, time = t+1, scenario= n
        #     self.prev_model = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time + 1,
        #                                self.curr_scenario, self.current_stage)
        #     self.prev_lmp = LMP(self.prev_model)
        #     self.prev_lmp.set_up_parameter()
        #     # curve, time = t+1, scenario= n-1
        #     self.pre_curve = Curve(100, 0, 3000)
        #     self.pre_curve.input_curve(self.curr_time + 1, self.curr_scenario - 1)
        # elif self.curr_time == 22:
        #     self.prev_model = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time,
        #                                self.curr_scenario, self.current_stage)
        #     self.prev_lmp = LMP(self.prev_model)
        #     self.prev_lmp.set_up_parameter()

        #     self.pre_curve = Curve(100, 0, 3000)
        #     self.pre_curve.input_curve(self.curr_time, self.curr_scenario - 1)

        # model_1 = Model('DAMarket')
        # a = self.prev_lmp.lmp_scenarios
        # print(a)
        # b = self.pre_curve.point_Y
        # print(b)
        # MultiRL = OptModelSetUp(psh_system_2, e_system_2, self.prev_lmp, self.pre_curve, pre_model_para, model_1)



    # def calculate_new(self):
    #     initial_soc = [0, 30, 60, 90, 120, 150,180,210,240,270,300]
    #     MultiRL = RLSetUp()
    #     MultiRL.CalOpt(initial_soc)
    #     self.optimal_profit = MultiRL.optimal_profit_list
        #print('test result #######################', MultiRL.optimal_profit_list)




# class test():
#     def __init__(self):
#         #self.reward = None
#         #self.value = None
#         #self.action = None
#         self.alpha = 0.8#0.2
#         self.date = 'March 07 2019'
#         self.LAC_last_windows = 0#1#0
#         self.probabilistic = 1#0#1
#         self.RT_DA = 1#0#1
#         self.curr_time = 0
#         self.curr_scenario = 1
#         self.current_stage ='training_500'

#     def calculate_new(self):
#         initial_soc = [4, 5, 6, 7, 8, 9, 10, 11]
#         MultiRL = MultiRLSetUp()
#         MultiRL.CalOpt(initial_soc)
#         self.optimal_profit = MultiRL.optimal_profit




# time_1 = time.time()
# training = MultiRLSetUp()
# #training.calculate_new_soc()
# training.calculate_new()
#
# time_2 = time.time()
# print('the time is', time_2 - time_1)
# print(training.optimal_profit)
#


time_1 = time.time()
initial_soc = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 630, 660, 690, 720, 750,\
                780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080, 1110, 1140, 1170, 1200, 1230, 1260, 1290, 1320, 1350, 1380, 1410,\
                1440, 1470, 1500]
MultiRL = RLSetUp()
#MultiRL = OptModelSetUp()
MultiRL.CalOpt(initial_soc)
time_2 = time.time()
print('the time is', time_2 - time_1)
print(MultiRL.optimal_profit_list)



