import pandas as pd
from gurobipy import *
import gurobipy as grb
import matplotlib.pyplot as plt
import numpy as np
#from LAC_PSH_profit_max import LAC_PSH_Profitmax
from Any_Sprice_E_curve_method import *

from get_benchmark_dict import *



class initial_input():
    def __init__(self, date):
        self.date = date
    
    def