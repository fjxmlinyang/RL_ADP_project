import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from Model_SetUp import *
from CurrModelPara import *
from Curve import *
from Main_cal_opt import find_optimal_value

date = 'March 07 2019'
#date = 'April 01 2019'
#date = 'April 15 2019'
#date = 'April 22 2019'

start = 1
end = 20
Curr_Scenario_Cost_Total = []

current_stage = 'training_50'

for curr_scenario in range(start, end):
    PSH_Results = []
    SOC_Results = []
    curr_scenario_cost_total = 0

    for curr_time in range(23):

        curr_model = CurrModelPara(0, 1, 1,  date, curr_time, curr_scenario, current_stage)
        #LAC_last_windows,  probabilistic, RT_DA, date, LAC_bhour, scenario
        print('################################## psh_system set up ##################################')
        psh_model_1 = curr_model
        psh_system_1 = PshSystem(psh_model_1)
        psh_system_1.set_up_parameter()
        print(psh_system_1.parameter)

        print('################################## e_system set up ##################################')
        e_model_1 = curr_model
        e_system_1 = ESystem(e_model_1)
        e_system_1.set_up_parameter()
        print(e_system_1.parameter)

        print('################################## lmp_system set up ##################################')
        lmp_model_1 = curr_model
        print(lmp_model_1.date)  ##first is for last window second are stochastic, third is for the date, last is for hour
        lmp_1 = LMP(lmp_model_1)
        lmp_1.set_up_parameter()
        print('lmp_quantiles=', lmp_1.lmp_quantiles)
        print('lmp_scenarios=', lmp_1.lmp_scenarios)
        print('lmp_Nlmp_s=', lmp_1.Nlmp_s)

        print('################################## curve set up ##################################')
        # how to choose previous curve inside?
        curve_old = Curve(100, 0, 3000)

        curve_old.input_curve(curr_time, curr_scenario - 1)

        print(curve_old.segments)

        print('################################## ADP training model set up ##################################')

        print(e_system_1.parameter['EName'])
        model_1 = Model('DAMarket')
        ADP_train_model_para = curr_model
        ###input prev_lmp and curve
        if curr_time != 22:
        ##lmp, time =t+1, scenario= n
            prev_model = CurrModelPara(0, 1, 1,  date, curr_time + 1, curr_scenario, current_stage)
            prev_lmp = LMP(prev_model)
            prev_lmp.set_up_parameter()
        ##curve, time =t+1, scenario= n-1
            pre_curve = Curve(100, 0, 3000)
            pre_curve.input_curve(curr_time + 1, curr_scenario - 1)
        elif curr_time == 22:
            prev_model = CurrModelPara(0, 1, 1,  date, curr_time, curr_scenario, current_stage)
            prev_lmp = LMP(prev_model)
            prev_lmp.set_up_parameter()

            pre_curve = Curve(100, 0, 3000)
            pre_curve.input_curve(curr_time, curr_scenario - 1)
        ######
        ADP_train_system = RLSetUp(psh_system_1, e_system_1, lmp_1, curve_old, ADP_train_model_para, model_1, prev_lmp, pre_curve)
        ADP_train_system.SPARstorage_model()


        ##output SOC and Psh
        # print(ADP_train_system.soc)
        #print(ADP_train_system.optimal_soc_sum)
        #print(ADP_train_system.optimal_profit)
        print('##############################'+ str(curr_time) +'######################################')

        SOC_Results.append(ADP_train_system.optimal_soc_sum)
        if ADP_train_system.optimal_psh_gen_sum > 1:
            PSH_Results.append(ADP_train_system.optimal_psh_gen_sum)
        else:
            PSH_Results.append(-ADP_train_system.optimal_psh_pump_sum)

        ##output curr cost
        curr_scenario_cost_total += ADP_train_system.curr_cost
        print(curr_scenario_cost_total)


    # add the last one

    filename = './Output_Curve' + '/PSH_Profitmax_Rolling_Results_' + str(curr_scenario) +'_'+ curr_model.date + '.csv'
    if SOC_Results[-1] - e_system_1.parameter['EEnd'][0]> 0.1:
        PSH_Results.append((SOC_Results[-1] - e_system_1.parameter['EEnd'][0]) * psh_system_1.parameter['GenEfficiency'][0])
    else:
        PSH_Results.append((SOC_Results[-1] - e_system_1.parameter['EEnd'][0]) / psh_system_1.parameter['PumpEfficiency'][0])

    SOC_Results.append(e_system_1.parameter['EEnd'][0])

    df = pd.DataFrame({'SOC_Results_'+ str(curr_scenario): SOC_Results, 'PSH_Results_'+ str(curr_scenario): PSH_Results})
    #df = pd.DataFrame({'PSH_Results_' + str(curr_scenario): PSH_Results})
    #df.to_csv(filename)
    if curr_scenario == start:
        df_total = df
    else:
        df_total = pd.concat([df_total, df], axis = 1)

    ##calculate total cost
    Curr_Scenario_Cost_Total.append(curr_scenario_cost_total)





#output the psh and soc
filename = './Output_Curve' + '/PSH_Profitmax_Rolling_Results_' + 'total' +'_'+ curr_model.date + '.csv'
df_total.to_csv(filename)

#output curr_cost
filename = './Output_Curve' + '/Current_Cost_Total_Results_' + str(curr_scenario) + '_' + curr_model.date + '.csv'
df = pd.DataFrame({'Curr_Scenario_Cost_Total': Curr_Scenario_Cost_Total})
df.to_csv(filename)



#compare with the da_price
#find_optimal_value(date, start , end)

#test
