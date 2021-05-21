import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
from Model_SetUp import *
from CurrModelPara import *
from Curve import *



for curr_scenario in range(1,50):
    PSH_Results = []
    SOC_Results = []
    for curr_time in range(24):
        curr_model = CurrModelPara(0, 1, 1, 'March 07 2019', curr_time, curr_scenario)
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
        if curr_time != 23:
        ##lmp, time =t+1, scenario= n
            prev_model = CurrModelPara(0, 1, 1, 'March 07 2019', curr_time + 1 , curr_scenario)
            prev_lmp = LMP(prev_model)
            prev_lmp.set_up_parameter()
        ##curve, time =t+1, scenario= n-1
            pre_curve = Curve(100, 0, 3000)
            pre_curve.input_curve(curr_time +1, curr_scenario - 1)
        elif curr_time == 23:
            prev_model = CurrModelPara(0, 1, 1, 'March 07 2019', curr_time , curr_scenario)
            prev_lmp = LMP(prev_model)
            prev_lmp.set_up_parameter()

            pre_curve = Curve(100, 0, 3000)
            pre_curve.input_curve(curr_time , curr_scenario - 1)
        ######
        ADP_train_system = RLSetUp(psh_system_1, e_system_1, lmp_1, curve_old, ADP_train_model_para, model_1, prev_lmp, pre_curve)
        ADP_train_system.SPARstorage_model()

        # print(ADP_train_system.soc)
        print(ADP_train_system.optimal_soc_sum)
        print(ADP_train_system.optimal_profit)
        # ADP_train_system.get_important_pt()
        # print(ADP_train_system.second_point_soc_sum)
        # print(ADP_train_system.second_point_profit)
        #
        # print(ADP_train_system.update_point_1)
        # print(ADP_train_system.update_point_2)


        #print(curve_old.segments)
        #
        # print(ADP_train_system.second_point_soc_sum)
        # print(ADP_train_system.second_point_profit)
        # print(ADP_train_system.update_point_1)
        # print(ADP_train_system.update_point_2)
        # print(ADP_train_system.curve.point_Y)
        # print(ADP_train_system.second_curve_soc)
        # print(ADP_train_system.second_curve_slope)
        #
        # print(ADP_train_system.new_curve_slope)
        #
        # print(ADP_train_system.curve.segments)
        #ADP_train_system.curve.show_curve()
        print('##############################'+ str(curr_time) +'######################################')

        SOC_Results.append(ADP_train_system.optimal_soc_sum)
        if ADP_train_system.optimal_psh_gen_sum > 1:
            PSH_Results.append(ADP_train_system.optimal_psh_gen_sum)
        else:
            PSH_Results.append(-ADP_train_system.optimal_psh_pump_sum)


# add the last one

    filename = './Output_Curve' + '/PSH_Profitmax_Rolling_Results_' + str(curr_scenario) +'_'+curr_model.date + '.csv'
    PSH_Results.append((SOC_Results[-1] - e_system_1.parameter['EEnd'][0]) / psh_system_1.parameter['GenEfficiency'][0])
    SOC_Results.append(e_system_1.parameter['EEnd'][0])

    df = pd.DataFrame({'SOC_Results_'+str(curr_scenario): SOC_Results, 'PSH_Results_'+ str(curr_scenario): PSH_Results})
    #df = pd.DataFrame({'PSH_Results_' + str(curr_scenario): PSH_Results})
    #df.to_csv(filename)
    if curr_scenario == 1:
        df_total = df
    else:
        df_total = pd.concat([df_total, df], axis = 1)




filename = './Output_Curve' + '/PSH_Profitmax_Rolling_Results_' + 'total' +'_'+ curr_model.date + '.csv'
df_total.to_csv(filename)