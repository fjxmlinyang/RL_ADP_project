import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
#from LAC_PSH_profit_max import LAC_PSH_Profitmax
from Any_Sprice_E_curve_method import *

# from get_benchmark_dict import *


###################################### Set input and output folder and parameters ##############################################

Input_folder_parent='./Input_Curve/PSH-Rolling Window'
#'/Users/yanglin/Desktop/JCIK-Math/0JCIK-Paper Working/7leiwu-risk/3project-PSH/7code-UC&market/Toy_case_study_multi_stages_for_Stevens/Input/PSH-Rolling Window/March 07 2019/prd_dataframe_wlen_24_March 07 2019.csv'## Pick a date
####date='March 20 2019'
#date='April 01 2019'
#date='April 15 2019'
#date='April 22 2019'
date='March 07 2019'
#date='May 04 2019'


Input_folder=Input_folder_parent+'/'+date
Output_folder='./Output_Curve'
Input_folder=Input_folder_parent+'/'+date
Output_folder='./Output_Curve'
# set the length of the rolling window
LAC_window=1
# indicate if the current window is the last window, default as 0
LAC_last_windows=0
# 0:apply the deterministic forecast, 1:apply the probabilistic forecast
probabilistic=0
# read time periods
time_periods=[]
filename = Input_folder + '/prd_dataframe_wlen_24_'+date+'.csv'
Data = pd.read_csv(filename)
df = pd.DataFrame(Data)
LMP_Scenario= df['RT_LMP']
for i in range(len(LMP_Scenario)-1):
    time_periods.append('T' + str(i))

############################################################################################################################


###################################### Rolling window starts ##############################################
PSH_Results=[]
SOC_Results=[]




# dict = get_benchmark_dict(benchmark = 3 , percentile = '95', bootstrap= False, single = False) ##



def sort_point(in_list): 
    ###sort the points   
    length=len(in_list)
    for i in range(length-1):
        left=i
        right=i+1
        while right<= length-1:
            if in_list[right]<in_list[left]:
                temp=in_list[left]
                in_list[left]=in_list[right]
                in_list[right]=temp
            right+=1
    return in_list


SOC_min=0
SOC_max=3000


###construct the points we want

from curve import *
benchmark = 4
curve1 = Curve(benchmark, 0, 3000)
curve1.seg_initial()
curve1.curve_initial()
# point_X=curve_1.point_X()
# point_Y=curve_1.point_Y()


for i in time_periods:
    price_index=time_periods.index(i)
    start_hour=time_periods.index(i)
    LAC_bhour = start_hour
    if start_hour+LAC_window <= len(time_periods):
        # 1:RT price data, 0: DA price data
        RT_DA=1
        ##############################################
        PSH_Profitmax=Any_Sprice_E_curve_method(LAC_bhour, LAC_last_windows, Input_folder, Output_folder, date, RT_DA, probabilistic, curve1.point_X, curve1.point_Y, SOC_min,SOC_max,benchmark)
        print(start_hour+LAC_window)
        PSH_Results.append(PSH_Profitmax[1][0])
        SOC_Results.append(PSH_Profitmax[0][0])
################################



###########DA




#########after_fact














###################################output############################

filename = Input_folder + '/PSH.csv'
Data = pd.read_csv(filename)
df = pd.DataFrame(Data)
PSHefficiency = list(df['Efficiency'])

filename = Input_folder + '/Reservoir.csv'
Data = pd.read_csv(filename)
df = pd.DataFrame(Data)
Eend = float(df['End'])
# write results
filename = Output_folder + '/PSH_Profitmax_Rolling_Results_'+date+'.csv'
PSH_Results.append((SOC_Results[-1]-Eend)/PSHefficiency[0])
SOC_Results.append(Eend)




df =pd.DataFrame({ 'SOC_Results': SOC_Results, 'PSH_Results': PSH_Results })
df.to_csv(filename)




######################################################################










