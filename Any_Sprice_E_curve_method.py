import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np


#len_var is the length of the length of the dynamic variable soc_n and I_n


def Any_Sprice_E_curve_method(LAC_bhour, LAC_last_windows, Input_folder, Output_folder, date, RT_DA, probabilistic, point_X, point_Y, SOC_min, SOC_max, benchmark):
    # Input_folder_parent='./Input/PSH-Rolling Window'
    # date='April 01 2019'
    # Input_folder=Input_folder_parent+'/'+date
    # Output_folder='./Output'
    # LAC_bhour=0
    # LAC_last_windows=0
    # probabilistic=0
    print('################################## LAC_PSH_profit_max #', LAC_bhour, 'probabilistic=',probabilistic,' ##################################')


# S_1_x, S_1_y=1300, 25
# S_2_x, S_2_y=1500, 27
# S_3_x, S_3_y=1700, 30
# [[1277.7777777777778, 30.196470253562275], 
# [1457.7777777777778, 29.301117060971652], 
# [1500.0, 29.50251240565363], 


# [1680.0, 29.603908812407425], 
# [1860.0, 29.264758964308296]]
# SOC_min=0
# SOC_max=3000

######buidling variable d######################
    d=[]
    # for i in range(benchmark):
    #     if i==0:
    #         d.append(point_X[i]-SOC_min)
    #     elif i==benchmark-1:
    #         d.append(SOC_max-point_X[i-1])
    #     else:
    #         d.append(point_X[i]-point_X[i-1])
    for i in range(benchmark):
        d.append(point_X[i+1]-point_X[i])
    # d_1=S_1_x-SOC_min
    # d_2=S_2_x-S_1_x
    # d_3=SOC_max-S_2_x

############################read the PSH######################################
    filename = Input_folder + '/PSH.csv'
    Data = pd.read_csv(filename)
    df=pd.DataFrame(Data)
    PSHmin_g = df['GenMin']
    PSHmax_g = df['GenMax']
    PSHmin_p = df['PumpMin']
    PSHmax_p = df['PumpMax']
    PSHcost = df['Cost']
    PSHefficiency = list(df['Efficiency'])
    PSHname = list(df['Name'])
############################################################################

###################read the reservoir########################################
    filename = Input_folder + '/Reservoir.csv'
    Data = pd.read_csv(filename)
    df=pd.DataFrame(Data)
    Emin = df['Min']
    Emax = df['Max']
    Ename = df['Name']
    Edayend= float(df['End'])
############################################################################


    ####be careful, since it is rolling method, the LMP shall be input each time
    if LAC_bhour==0 or LAC_last_windows:
        Estart = df['Start']
    else:
        filename = Output_folder+'/LAC_Solution_System_SOC_' + str(LAC_bhour-1) + '.csv'
        Data = pd.read_csv(filename)
        df = pd.DataFrame(Data)
        Estart = df['SOC'][0]
##########################read the  LMP############################################

    if LAC_last_windows:
        # filename = Input_folder + '\LMP_Hindsight' + '.csv'
        filename = Input_folder + '/prd_dataframe_wlen_24_'+date + '.csv'
    else:
        # filename = Input_folder+'\LMP_Scenarios_' + 'T' + str(LAC_bhour) +'_DA'+ '.csv'
        if probabilistic:
            filename = Input_folder + '/DA_lmp_Scenarios_wlen_' + str(24-LAC_bhour) + '_'+date+'_50' + '.csv'
        else:
            filename = Input_folder + '/prd_dataframe_wlen_'+str(24-LAC_bhour)+'_'+date + '.csv'

    Data = pd.read_csv(filename)
    df = pd.DataFrame(Data)
    Column_name=list(Data.columns)
    lmp_quantiles = []
    lmp_scenarios = []
    DA_lmp=[]
    if LAC_last_windows:
        Nlmp_s = 1
        # probability of each scenario is evenly distributed
        lmp_quantiles.append(1.0 / Nlmp_s)
        if RT_DA==1:
            lmp_scenarios.append(list(df['RT_LMP']))
        else:
            lmp_scenarios.append(list(df['DA_LMP']))
    else:
        if probabilistic:
            Nlmp_s=len(Column_name)
            for i in range(Nlmp_s):
                # probability of each scenario is evenly distributed
                lmp_quantiles.append(1.0 / Nlmp_s)
                lmp_scenarios.append(list(df[Column_name[i]]))
        else:
            # for deterministic forecast, there is a singel scenario
            Nlmp_s =1
            lmp_quantiles.append(1.0 / Nlmp_s)
            # deterministic forecast is the single point prediction
            lmp_scenarios.append(list(df['prd']))

    e_time_periods = []
    for i in range(1,len(lmp_scenarios[0])):
        e_time_periods.append('T' + str(i))

#############################################################################

################################ Build Model ################################################################


    ########################add coeff ######################################
    model = Model('DAMarket')
    ### define variables
    psh_max_g = {}
    psh_min_g = {}
    psh_max_p = {}
    psh_min_p = {}
    e_max = {}
    e_min = {}
    ## edit 00: rewrite the pshmax
    psh0_max_g = {}
    psh0_min_g = {}
    psh0_max_p = {}
    psh0_min_p = {}
    for j in PSHname:
        psh0_max_g[(j)] = list(PSHmax_g)[list(PSHname).index(j)]
        psh0_min_g[(j)] = list(PSHmin_g)[list(PSHname).index(j)]
        psh0_max_p[(j)] = list(PSHmax_p)[list(PSHname).index(j)]
        psh0_min_p[(j)] = list(PSHmin_p)[list(PSHname).index(j)]
    #for i in e_time_periods:
    for k in PSHname:
        for s in range(Nlmp_s):
            psh_max_g[(s, k)]=list(PSHmax_g)[list(PSHname).index(k)]
            psh_min_g[(s, k)]=list(PSHmin_g)[list(PSHname).index(k)]
            psh_max_p[(s, k)]=list(PSHmax_p)[list(PSHname).index(k)]
            psh_min_p[(s, k)]=list(PSHmin_p)[list(PSHname).index(k)]
    #for i in e_time_periods:
    for f in Ename:
        for s in range(Nlmp_s):
            e_max[(s,f)]=list(Emax)[list(Ename).index(f)]
            e_min[(s,f)]=list(Emin)[list(Ename).index(f)]

    e_max_inf = {}
    e_min_inf = {}
    psh_max_inf = {}
    psh_min_inf = {}

    #for i in e_time_periods:
    for k in PSHname:
        for s in range(Nlmp_s):
            psh_max_inf[(s,  k)] = float('inf')
            psh_min_inf[(s,  k)] = -float('inf')

    #for i in e_time_periods:
    for f in Ename:
        for s in range(Nlmp_s):
            e_max_inf[(s, f)] = float('inf')
            e_min_inf[(s, f)] = -float('inf')
    #############################################################################


    ##########################add variables ######################################
    class add_dynamic_var:
        def __init__(self,name):
            self.name = name

        def add_soc(self):
            return model.addVars(list(Ename), ub=float('inf'),lb=-float('inf'), vtype="C", name=self.name)
        
        def add_I(self):
            return model.addVars(list(Ename), vtype="B", name=self.name)
        
        def add_psh(self):
            return model.addVars(list(PSHname),ub=float('inf'),lb=-float('inf'),vtype="C",name=self.name)
        
        def add_e(self):
            return model.addVars(list(Ename), ub=e_max_inf, lb=e_min_inf, vtype="C",name=self.name)

    ##add psh
    psh0_gen=add_dynamic_var('psh0_gen').add_psh()
    psh0_pump=add_dynamic_var('psh0_pump').add_psh()
    ##add e
    e0 = add_dynamic_var('e0').add_e()
    ##add soc and I
    len_var=len(point_X)-1
    soc=[]
    I = []
    ##for here we have soc_1, soc2,....; I_1, I_2,....
    for i in range(len_var):  
        name_num = str(i+1)
        soc.append(add_dynamic_var('soc_'+'name_num').add_soc())
        I.append(add_dynamic_var('I_'+'name_num').add_I())

    
    model.update()




###########################add constraint#####################################

    ##################rolling constaint############################
    ## SOC0: e_0=E_start; loop from 0 to 22; e_1=e_0+psh1;....e_23=e_22+psh_23; when loop to 22; directly add e_23=E_end
    for k in Ename:
        print('Estart:', float(Estart))
        LHS = e0[k] + grb.quicksum(psh0_gen[j]/PSHefficiency[PSHname.index(j)] for j in PSHname)\
            - grb.quicksum(psh0_pump[j]*PSHefficiency[PSHname.index(j)] for j in PSHname) - float(Estart)
        RHS = 0
        print(LHS)
        ###if we calculate the first one, we use 'SOC0', and the last we use 'End'; or we choose the SOC0 to "beginning", at the same time the last we use 'SOC'. 
        model.addConstr(LHS == RHS, name='%s_%s' % ('SOC0', k))
        # model.addConstr(LHS == RHS, name='%s_%s' % ('Beginning', j))
    # state of charge

    #################rolling constaint############################

    # Upper and lower constraint
    
    for j in PSHname: #all are lists
        model.addConstr(psh0_gen[j] <= PSHmax_g, name='%s_%s' % ('psh_gen_max0', j))
        model.addConstr(psh0_gen[j] >= PSHmin_g, name='%s_%s' % ('psh_gen_min0', j))
        model.addConstr(psh0_pump[j] <= PSHmax_p, name='%s_%s' % ('psh_pump_max0', j))
        model.addConstr(psh0_pump[j] >= PSHmin_p, name='%s_%s' % ('psh_pump_min0', j))
    for k in Ename:
        model.addConstr(e0[k] <= Emax, name='%s_%s' % ('e_max0', k))
        model.addConstr(e0[k] >= Emin, name='%s_%s' % ('e_min0', k))



    
    ############## how to constraint for  SOC_t+1=SOC_min+SOC_1+SOC_2+SOC_3###########


    for k in Ename:
        _temp_sum=0
        for i in range(len_var):     
            _temp_sum += soc[i][k]
        LHS = e0[k]
        RHS = _temp_sum   #RHS=soc[0][k]+soc[1][k]+soc[2][k]+soc[3][k]+soc[4][k]
        model.addConstr(LHS==RHS, name='%s_%s' % ('shadow_part', k))

        
    #############################################################################

    ### how to constraint for  d_1I_2 <= soc_1 <=d_1I_1?############################
    for k in Ename:
        for i in range(len_var):
            name_num = str(i+1)
            bench_num = i
            if bench_num==0:
                model.addConstr(soc[bench_num][k] <= str(d[bench_num])*I[bench_num][k], name='%s_%s' % ('soc_'+name_num+'_max', k))
                model.addConstr(str(d[bench_num])*I[bench_num+1][k]<= soc[bench_num][k] , name='%s_%s' % ('soc_'+name_num+'_min', k))
            elif bench_num==len_var-1:
                model.addConstr(soc[bench_num][k] <= str(d[bench_num])*I[bench_num][k] , name='%s_%s' % ('soc_'+name_num+'_max', k))
                model.addConstr(0 <= soc[bench_num][k],       name='%s_%s' % ('soc_'+name_num+'_min', k))
            else:
                model.addConstr(soc[bench_num][k] <= str(d[bench_num])*I[bench_num][k], name='%s_%s' % ('soc_'+name_num+'_max', k))
                model.addConstr(str(d[bench_num])*I[bench_num+1][k]<= soc[bench_num][k] , name='%s_%s' % ('soc_'+name_num+'_min', k))


        
    #############################################################################


    #######the constraint I_1<=I_2<=I_3#############################################
    for s in range(Nlmp_s):
        for k in Ename:
            for i in range(len_var-1):
                name_num = str(i+1)
                name_num_next =str(i+2)
                bench_num = i
                model.addConstr(I[bench_num+1][k]<= I[bench_num][k], name='%s_%s' % ('I_'+name_num_next+'_'+name_num,k))

    #############################################################################

    #######the constraint for the last -N(t)Pump_max <= SOC-soc_terminal<= Pgen_max*1.1111############################################
    # for k in Ename:
    #     LHS = e0[k]-Edayend
    #     RHS = (len(e_time_periods)+1)*PSHmax_g[0]/PSHefficiency[0]
    #     #RHS = (len(e_time_periods))*PSHmax_p[0]*PSHefficiency[0] #这个是特别的是改过不知道对错的
    #     #print('e0[k]-Edayend=',  e0[k]-Edayend)
    #     print('PSHmax_g is equal ',  PSHmax_p[0])
    #     print('Upper Bound ', (len(e_time_periods)+1)*PSHmax_g[0]/PSHefficiency[0])
    #     model.addConstr(LHS <= RHS, name='%s_%s' % ('final_upper', k))
    # for k in Ename:
    #     LHS = e0[k]-Edayend
    #     RHS = -(len(e_time_periods)+1)*PSHmax_p[0]*PSHefficiency[0]
    #     #RHS = -(len(e_time_periods))*PSHmax_g[0]/PSHefficiency[0] #特别的`
    #     print('PSHmax_p is equal ', PSHmax_p[0])
    #     print('Lower Bound ',  -(len(e_time_periods)+1)*PSHmax_p[0]*PSHefficiency[0])
    #     model.addConstr(LHS >= RHS, name='%s_%s' % ('final_lower', k))
    #############################################################################








###############################Objective function##############################################
    psh_max=[]
    for s in range(Nlmp_s):
        p_s = lmp_quantiles[s]
        for j in PSHname:
            psh_max.append((psh0_gen[j] - psh0_pump[j]) * lmp_scenarios[s][0] * p_s)
    
    for k in Ename:
        for i in range(len_var):
            bench_num = i
            psh_max.append(point_Y[bench_num]*soc[bench_num][k])
    print(psh_max)          
    obj = quicksum(psh_max)
##########################################################################################


################################### Solve Model ####################################
    model.setObjective(obj, GRB.MAXIMIZE)
    model.optimize()

    # print results for variables
    for v in model.getVars():
        print("%s %f" % (v.Varname, v.X))
        # print("%s %f %f" % (v.Varname, v.X, v.Pi))
##########################################################################################








################################### return solutions ####################################

    #Sprice_E_curve_method()
    SOC0=[]
    filename=Output_folder+'/LAC_Solution_System_SOC_'+str(LAC_bhour)+'.csv'
    with open(filename, 'w') as wf:
        wf.write('Num_Period,Reservoir_Name,SOC\n')
        for v in [v for v in model.getVars() if ('Reservoir' in v.Varname and 'e0' in v.Varname)]:
            if 'Reservoir' in v.Varname:
                soc=v.X
                SOC0.append(soc)
                time='T'+str(LAC_bhour)
                name=v.Varname[3:13]
                st = time + ',' + '%s,%.1f' % (name,soc) + '\n'
                wf.write(st)

        ############
    psh0=[]
    PSH0=[]

    for v in [v for v in model.getVars() if 'psh0_gen' in v.Varname]:
        psh = v.X
        psh0.append(psh)
    for v in [v for v in model.getVars() if 'psh0_pump' in v.Varname]:
        psh = v.X
        psh0.append(-psh)
    PSH0.append(sum(psh0))



    if LAC_last_windows:
        psh_last_window_gen=[]
        psh_last_window_pump=[]
        PSH=[PSH0[0]]
        SOC=[]
        E_shadow_price=[]
        Dual_SOC_max=[]
        Dual_SOC_min=[]
        for v in [v for v in model.getVars() if 'PSH_gen' in v.Varname]:
            psh = v.X
            psh_last_window_gen.append(psh)
        for v in [v for v in model.getVars() if 'PSH_pump' in v.Varname]:
            psh = v.X
            psh_last_window_pump.append(psh)
        for i in range(len(psh_last_window_gen)):
            PSH.append(psh_last_window_gen[i]-psh_last_window_pump[i])
        for v in [v for v in model.getVars() if 'E' in v.Varname]:
            soc = v.X
            SOC.append(soc)

        return SOC, PSH
    else:
        return SOC0, PSH0



##########################################################################################