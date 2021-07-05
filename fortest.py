
from multiprocess import *
import time

class test():
    def __init__(self):
        #self.reward = None
        #self.value = None
        #self.action = None
        self.alpha = 0.8#0.2
        self.date = 'March 07 2019'
        self.LAC_last_windows = 0#1#0
        self.probabilistic = 1#0#1
        self.RT_DA = 1#0#1
        self.curr_time = 0
        self.curr_scenario = 1
        self.current_stage ='training_500'

    def calculate_new(self):

        initial_soc = [4, 5, 6, 7, 8, 9, 10, 11]
        a = A()
        a.cal(initial_soc)

time_1 = time.time()
training = test()
training.calculate_new()
print(training.optimal_profit)
time_2 = time.time()
print(time_2 - time_1)


























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
