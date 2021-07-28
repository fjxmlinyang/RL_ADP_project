import pandas as pd
from LAC_PSH_profit_max import LAC_PSH_Profitmax
from LAC_PSH_profit_max import PSH_profitmax_plot

###################################### Set input and output folder and parameters ##############################################

Input_folder_parent='./Input/PSH-Rolling Window'
## Pick a date
date='March 07 2019'
date='April 01 2019'
date='April 15 2019'


Input_folder=Input_folder_parent+'/'+date
Output_folder='./Output'
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

###################################### Rolling window starts ##############################################
PSH_Results=[]
SOC_Results=[]
for i in time_periods:
    start_hour=time_periods.index(i)
    LAC_bhour = start_hour
    if start_hour+LAC_window <= len(time_periods):
        # 1:RT price data, 0: DA price data
        RT_DA=0
        PSH_Profitmax = LAC_PSH_Profitmax(LAC_bhour, LAC_last_windows, Input_folder, Output_folder,date,RT_DA,probabilistic)
        PSH_Results.append(PSH_Profitmax[1][0])
        SOC_Results.append(PSH_Profitmax[0][0])

###################################### Solve benchmark problem and collect results ##############################################
# After the last window been solved, generate benchmark results
LAC_bhour=len(time_periods)
LAC_last_windows=1
# Real-time benchmark using the after the fact RT price
RT_DA=1
PSH_Profitmax = LAC_PSH_Profitmax(LAC_bhour, LAC_last_windows, Input_folder, Output_folder,date,RT_DA,probabilistic)
After_fact_SOC=PSH_Profitmax[0]
After_fact_PSH =PSH_Profitmax[1]
# DA benchmark using the DA price
RT_DA=0
PSH_Profitmax = LAC_PSH_Profitmax(LAC_bhour, LAC_last_windows, Input_folder, Output_folder,date,RT_DA,probabilistic)
DA_SOC = PSH_Profitmax[0]
DA_PSH = PSH_Profitmax[1]
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
df =pd.DataFrame({'After_fact_SOC':After_fact_SOC, 'SOC_Results': SOC_Results,'DA_SOC': DA_SOC,
                  'After_fact_PSH':After_fact_PSH, 'PSH_Results':PSH_Results, 'DA_PSH':DA_PSH})
df.to_csv(filename)

###################################### Plot Section ##############################################RT_DA=1
# benchmark with RT after-the-fact results
RT_DA=1
PSH_profitmax_plot(Input_folder,Output_folder,date,RT_DA,probabilistic)
# benchmark with DA results
RT_DA=0
PSH_profitmax_plot(Input_folder,Output_folder,date,RT_DA,probabilistic)

