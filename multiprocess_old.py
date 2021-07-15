
#
#
# def para_cal(check_soc_curve, second_curve_soc):
#
#
#
#
#     def
#     second_curve_profit = []
#     for cur_idx in range(len(check_soc_curve)):
#
#         check = check_soc_curve[cur_idx]
#         value = second_curve_soc[cur_idx]
#         if check == 1:
#             point_y = calculate_new_soc(value)
#         if check == 0:
#             point_y = -1000000
#         second_curve_profit.append(point_y)
#
#
#
#     return  second_curve_profit
#

# only for like parameter multiprocess


import multiprocessing as mp
import gurobipy as gp
from gurobipy import GRB
import time
from ModelSetUp import *

class MultiRLSetUp():

    def solve_model(self, a):
        self.a = a
        with gp.Env() as env, gp.Model(env=env) as self.model:
        #with gp.Model as model:
            self.add_Var()
            #add_var()

            time.sleep(5)
            self.add_constraint()
            # define model

            self.model.optimize()
            obj = self.model.getObjective() #self.calculate_pts(self.optimal_soc_sum)
            self.optimal_profit = obj.getValue()
            print(self.optimal_profit)
            self.optimal_profit_list.append(self.optimal_profit)

            # retrieve data from model
    def add_Var(self):
        self.x = self.model.addVar(vtype=GRB.BINARY, name="x")
        self.y = self.model.addVar(vtype=GRB.BINARY, name="y")
        self.z = self.model.addVar(vtype=GRB.BINARY, name="z")

    def add_constraint(self):
        self.model.setObjective(self.x + self.y + 2 * self.z, GRB.MAXIMIZE)
        self.model.addConstr(self.x + 2 * self.y + 3 * self.z <= self.a, "c0")
        self.model.addConstr(self.x + self.y >= 1, "c1")

    def cal(self, initial_soc):
    #if __name__ == '__main__':
        self.optimal_profit_list = []
        with mp.Pool() as pool:
            pool.map(self.solve_model, initial_soc)



# a = A()
# initial_soc = [4, 5, 6, 7, 8, 9, 10, 11]
# a.cal(initial_soc)


# def solve_model(a):
#     with gp.Env() as env, gp.Model(env=env) as model:
#         x = model.addVar(vtype=GRB.BINARY, name="x")
#         y = model.addVar(vtype=GRB.BINARY, name="y")
#         z = model.addVar(vtype=GRB.BINARY, name="z")
#         # add_var()
#
#         time.sleep(5)
#         model.setObjective(x + y + 2 * z, GRB.MAXIMIZE)
#         model.addConstr(x + 2 * y + 3 * z <= a, "c0")
#         model.addConstr(x + y >= 1, "c1")
#         # define model
#
#         model.optimize()
#
#         # retrieve data from model
#
#
#
# # if __name__ == '__main__':
# time_1 = time.time()
# with mp.Pool() as pool:
#     pool.map(solve_model, [4, 5, 6, 7, 8, 9, 10, 11])
# time_2 = time.time()
# print(time_2 - time_1)













#
# def solve_model(a):
#
#     with gp.Env() as env, gp.Model(env=env) as model:
#         x = model.addVar(vtype=GRB.BINARY, name="x")
#         y = model.addVar(vtype=GRB.BINARY, name="y")
#         z = model.addVar(vtype=GRB.BINARY, name="z")
#         add_var()
#         time_1 = time.time()
#         time.sleep(5)
#         model.setObjective(x + y + 2 * z, GRB.MAXIMIZE)
#         model.addConstr(x + 2 * y + 3 * z <= a, "c0")
#         model.addConstr(x + y >= 1, "c1")
#         # define model
#
#         model.optimize()
#         time_2 = time.time()
#         # retrieve data from model
#         print(time_2-time_1)
#
# #if __name__ == '__main__':
# with mp.Pool() as pool:
#     pool.map(solve_model, [4, 5, 6])