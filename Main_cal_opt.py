import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from Model_SetUp import *
from CurrModelPara import *
from Curve import *


#this is for
date = 'March 07 2019'
#date = 'April 01 2019'
#date = 'April 15 2019'
#date = 'April 22 2019'
start = 1
end = 50

current_stage = 'training_50'

def find_optimal_value(date, start, end):
    opt_results = []
    Curr_Scenario_Cost_Total = []
    for curr_scenario  in range(start, end):
        PSH_Results = []
        SOC_Results = []
        curr_scenario_cost_total = 0

        for curr_time in range(23):

            #this for day ahead
            curr_model = CurrModelPara(1 , 1, 0,  date, curr_time, curr_scenario, current_stage)
            psh_model_1 = curr_model
            psh_system_1 = PshSystem(psh_model_1)
            psh_system_1.set_up_parameter()

            e_model_1 = curr_model
            e_system_1 = ESystem(e_model_1)
            e_system_1.set_up_parameter()
            print(e_system_1.parameter)

            lmp_model_1 = curr_model
            lmp_1 = LMP(lmp_model_1)
            lmp_1.set_up_parameter()
            prev_lmp = lmp_1

            curve_old = Curve(100, 0, 3000)
            curve_old.input_curve(curr_time, curr_scenario - 1)
            print(curve_old.point_Y)
            pre_curve = curve_old

            model_1 = Model('DAMarket')
            ADP_opt_model_para = curr_model
            ADP_opt = RLSetUp(psh_system_1, e_system_1, lmp_1, curve_old, ADP_opt_model_para, model_1, prev_lmp, pre_curve)
            ADP_opt.SPARstorage_model()
      ##output SOC and Psh
        # print(ADP_train_system.soc)
        #print(ADP_train_system.optimal_soc_sum)
        #print(ADP_train_system.optimal_profit)
            print('##############################'+ str(curr_time) +'######################################')

            SOC_Results.append(ADP_opt.optimal_soc_sum)
            if ADP_opt.optimal_psh_gen_sum > 1:
                PSH_Results.append(ADP_opt.optimal_psh_gen_sum)
            else:
                PSH_Results.append(-ADP_opt.optimal_psh_pump_sum)

            ##output curr cost
            curr_scenario_cost_total += ADP_opt.curr_cost
            print(curr_scenario_cost_total)

        # add the last one

        filename = './Output_Curve' + '/PSH_Profitmax_Rolling_Results_' + str(
            curr_scenario) + '_' + curr_model.date + '.csv'
        if SOC_Results[-1] - e_system_1.parameter['EEnd'][0] > 0.1:
            PSH_Results.append(
                (SOC_Results[-1] - e_system_1.parameter['EEnd'][0]) * psh_system_1.parameter['GenEfficiency'][0])
        else:
            PSH_Results.append(
                (SOC_Results[-1] - e_system_1.parameter['EEnd'][0]) / psh_system_1.parameter['PumpEfficiency'][0])

        SOC_Results.append(e_system_1.parameter['EEnd'][0])

        df = pd.DataFrame(
            {'SOC_Results_' + str(curr_scenario): SOC_Results, 'PSH_Results_' + str(curr_scenario): PSH_Results})
        # df = pd.DataFrame({'PSH_Results_' + str(curr_scenario): PSH_Results})
        # df.to_csv(filename)
        if curr_scenario == start:
            df_total = df
        else:
            df_total = pd.concat([df_total, df], axis=1)

        ##calculate total cost
        Curr_Scenario_Cost_Total.append(curr_scenario_cost_total)

    #output the psh and soc
    filename = './Output_Curve' + '/test_PSH_Profitmax_Rolling_Results_' + 'total' +'_'+ curr_model.date + '.csv'
    df_total.to_csv(filename)

    #output curr_cost
    filename = './Output_Curve' + '/test_Current_Cost_Total_Results_' + str(curr_scenario) + '_' + curr_model.date + '.csv'
    df = pd.DataFrame({'Curr_Scenario_Cost_Total': Curr_Scenario_Cost_Total})
    df.to_csv(filename)



find_optimal_value(date, start, end)







#
#             soc_results.append(ADP_opt.optimal_soc_sum)
#             if ADP_opt.optimal_psh_gen_sum > 1:
#                 psh_results.append(ADP_opt.optimal_psh_gen_sum)
#             else:
#                 psh_results.append(-ADP_opt.optimal_psh_pump_sum)
#         lmp_results.append(lmp_1.lmp_scenarios[0])
#
#         ##add the current cost
#         curr_scenario_cost_total += ADP_opt.curr_cost
#         print(curr_scenario_cost_total)
#         # add the last one
#
#         filename = './Output_Curve' + '/PSH_Profitmax_Rolling_Results_' + str(curr_scenario) +'_'+curr_model.date + '.csv'
#         psh_results.append((soc_results[-1] - e_system_1.parameter['EEnd'][0]) / psh_system_1.parameter['GenEfficiency'][0])
#         soc_results.append(e_system_1.parameter['EEnd'][0])
#
#         curr_optimal_solution = 0
#         for i in range(23):
#             curr_optimal_solution += psh_results[i] * lmp_results[i]
#
#         opt_results.append(curr_optimal_solution)
#
#     df = pd.DataFrame({ 'opt_results': opt_results})
#     filename = './Output_Curve' + '/Optimal_Solution_Results_' + 'total' +'_'+ curr_model.date + '.csv'
#     df.to_csv(filename)
#
#     Curr_Scenario_Cost_Total.append(curr_scenario_cost_total)
#
#
#
#     filename = './Output_Curve' + '/Opt_Cost_Total_Results_' + str(curr_scenario) + '_' + curr_model.date + '.csv'
#     df = pd.DataFrame({'Opt_Cost_Total': Curr_Scenario_Cost_Total})
#     df.to_csv(filename)
#
#
#
# find_optimal_value(date, start, end)