
from multiprocess import *
import time



class MultiRLSetUp():

    def __init__(self):
        self.alpha = 0.8  # 0.2
        self.date = 'March 07 2019'
        self.LAC_last_windows = 0  # 1#0
        self.probabilistic = 1  # 0#1
        self.RT_DA = 1  # 0#1
        self.curr_time = 0
        self.curr_scenario = 1
        self.current_stage = 'training_500'

    def calculate_new_soc(self, initial_soc):
        pre_model_para = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time,
                                  self.curr_scenario, self.current_stage)
        # LAC_last_windows,  probabilistic, RT_DA, date, LAC_bhour, scenario

        psh_system_2 = PshSystem(pre_model_para)
        psh_system_2.set_up_parameter()


        e_system_2 = ESystem(pre_model_para)
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
            self.pre_curve = Curve(100, 0, 3000)
            self.pre_curve.input_curve(self.curr_time + 1, self.curr_scenario - 1)
        elif self.curr_time == 22:
            self.prev_model = CurrModelPara(self.LAC_last_windows, self.probabilistic, self.RT_DA, self.date, self.curr_time,
                                       self.curr_scenario, self.current_stage)
            self.prev_lmp = LMP(self.prev_model)
            self.prev_lmp.set_up_parameter()

            self.pre_curve = Curve(100, 0, 3000)
            self.pre_curve.input_curve(self.curr_time, self.curr_scenario - 1)

        model_1 = Model('DAMarket')
        a = self.prev_lmp.lmp_scenarios
        print(a)
        b = self.pre_curve.point_Y
        print(b)

        pre_model = RLSetUp(psh_system_2, e_system_2, self.prev_lmp, self.pre_curve, pre_model_para, model_1)
        pre_model.optimization_model_with_input()
        rt = pre_model.optimal_profit

    def calculate_new(self):
        initial_soc = [4, 5, 6, 7, 8, 9, 10, 11]
        MultiRL = MultiRLSetUp()
        MultiRL.CalOpt(initial_soc)
        self.optimal_profit = MultiRL.optimal_profit




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




time_1 = time.time()
training = test()
#training.calculate_new_soc()
training.calculate_new()
print(training.optimal_profit)
time_2 = time.time()
print(time_2 - time_1)















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
#
#     def calculate_new(self):
#         initial_soc = [4, 5, 6, 7, 8, 9, 10, 11]
#         MultiRL = MultiRLSetUp()
#         MultiRL.CalOpt(initial_soc)
#         self.optimal_profit = MultiRL.optimal_profit
#
#
#
#
# time_1 = time.time()
# training = test()
# #training.calculate_new_soc()
# training.calculate_new()
# print(training.optimal_profit)
# time_2 = time.time()
# print(time_2 - time_1)


























# import multiprocessing
#
#
#
# def test(input_soc):
#     input_soc = input_soc+1
#     return input_soc
#
# def fun(SOC):
#     x = SOC +1
#     return x
#
# tasks = [1,2,3]
#
# cores = multiprocessing.cpu_count()
# pool = multiprocessing.Pool(processes=cores)
#
# print(pool.map(fun,tasks))
#



#
import multiprocessing
# import time
#
#
# class A(object):
#     def __init__(self):
#         self.a = None
#         self.b = None
#
#     def get_num_a(self):
#         time.sleep(3)
#         self.a = 10
#
#     def get_num_b(self):
#         time.sleep(5)
#         self.b = 10
#
#     def sum(self):
#         print("a的值为:{}".format(self.a))
#         print("b的值为:{}".format(self.b))
#         ret = self.a + self.b
#         return ret
#
#     def run(self):
#         p1 = multiprocessing.Process(target=self.get_num_a)
#         p2 = multiprocessing.Process(target=self.get_num_b)
#         p1.start()
#         p2.start()
#         p1.join()
#         p2.join()
#         #print(self.sum())
#
#
# if __name__ == '__main__':
#
#     t1 = time.time()
#     a = A()
#     a.run()
#     t2 = time.time()
#     print("cost time :{}".format(t2 - t1))
# #



# import multiprocessing
# import time
#
# class A(object):
#     def __init__(self):
#         self.a = None
#         self.b = None
#         # 初始化一个共享字典
#         self.my_dict = multiprocessing.Manager().dict() #这个是soc_curve的储存
#         self.test =10
#
#     def get_num_a(self): #这个是算soc_curve的第一个点
#         time.sleep(3)
#         self.my_dict["a"] = 10
#         self.test = self.test+1
#
#     def get_num_b(self): #这个是算soc_curve的第二个点
#         time.sleep(5)
#         self.my_dict["b"] = 6
#
#     def sum(self): #合并点
#         self.a = self.my_dict["a"]
#         self.b = self.my_dict["b"]
#         print("a的值为:{}".format(self.a))
#         print("b的值为:{}".format(self.b))
#         ret = self.a + self.b
#         return ret
#
#     def run(self): #主程序部分
#         self.my_dict = multiprocessing.Manager().dict()
#         p1 = multiprocessing.Process(target=self.get_num_a)
#         p2 = multiprocessing.Process(target=self.get_num_b)
#         p1.start()
#         p2.start()
#         p1.join()
#         p2.join()
#         print(self.sum())

# class B(object):
#     def
#
# if __name__ == '__main__':
#     t1 = time.time()
#     a = A()
#     a.run()
#     t2 = time.time()
#     print("cost time :{}".format(t2 - t1))
#
#



# import time
#
#
# class A(object):
#     def __init__(self):
#         self.a = None
#         self.b = None
#
#     def get_num_a(self):
#         print("计算逻辑A")
#         time.sleep(3)
#         self.a = 10
#
#     def get_num_b(self):
#         print("计算逻辑B")
#         time.sleep(5)
#         self.b = 6
#
#     def sum(self):
#         print("a的值为:{}".format(self.a))
#         print("b的值为:{}".format(self.b))
#         ret = self.a + self.b
#         return ret
#
#     def run(self):
#         self.get_num_a()
#         self.get_num_b()
#         print(self.sum())
#
#
# if __name__ == '__main__':
#     t1 = time.time()
#     a = A()
#     a.run()
#     t2 = time.time()
#     print("cost time :{}".format(t2 - t1))
