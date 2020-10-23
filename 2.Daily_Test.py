# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 19:05:42 2020

@author: ruleb
"""
import pandas as pd
import glob
import re
import datetime
import os
import glob
import shutil

def isoStrat(text):
    return str(re.split(" ",str(text))[-1:]).replace("['",'').replace("']",'')
        
def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))
        
        
DailyHist = "C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/BF17AE6EAAB059EEBF7223939EC084E3/MQL4/Files/AccountHistory.csv"
perf_per_strat = "./DailyMatch/exp"
dfxxx = "./DailyMatch"
perf_per_strat_to_del = "./DailyMatch/exp/*"
path_remove_underperforming = glob.glob("./0.DatabaseIn/*")

def remove_used_chr(perf_per_strat_to_del):
    files = glob.glob(perf_per_strat_to_del)
    for f in files:
        os.remove(f)
        
def daily_check(DailyHist,perf_per_strat):
    hist = pd.read_csv(DailyHist, delimiter =";")    
    hist['Strategy'] = hist['Comment'].apply(isoStrat)
    history = hist.sort_values('Ticket')
    
    for i, g in history.groupby(hist['Strategy']):
        globals()['df_' + str(i)] =  g
        g.to_csv(perf_per_strat + '/df_' + str(i) +'.csv')
    
    all_files = glob.glob(perf_per_strat + "/*.csv")
    stats =[]
    dfxx =[]
    
    for filename in all_files:
        df = pd.read_csv(filename)
        df['Strategy'] = filename.split("_")[1].split(".csv")[0]
        df.sort_values('Ticket')
        df['CumProf'] = df['Profit'].cumsum()
        df['DD']= df['CumProf'].cummin()
        df['RetDD'] = df['CumProf']/(-df['DD'])
        date_format='%Y.%m.%d'
        d1 = datetime.datetime.strptime(df.iloc[0]['Open Date'],date_format)
        d2 = datetime.datetime.today()
        difference = d2 - d1
        df['Days'] = difference.days
        df['Count'] = df.Days.count()
        df['Status'] = df['Days'].apply(lambda x : 'FAIL' if (df['RetDD'].iloc[-1] < 0.8) & (df['Count'].iloc[-1]>15) else 'PASS')
        dfx = df[['Strategy','RetDD','Count','Status']].iloc[-1]
        # print(dfx)
        stats.append(dfx.to_list())
    
    today = datetime.datetime.today().strftime("%d%m%Y")
    
    pd.DataFrame(stats).to_csv(('./DailyMatch/database_'+ today + '.csv').format(today))
    return(stats)
    
#posso usare stats come input della prossima funzione      
    
def remove_underperforming_strat(statistics, path_remove_underperforming):    
    for k in statistics:
        if k[3] == 'FAIL':
            for h in statistics:
                if k[0] in h:
                   remove(h)
            
    
