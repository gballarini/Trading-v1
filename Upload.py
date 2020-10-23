# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 08:23:17 2020

@author: ruleb
"""
from IPython import get_ipython
import os 
import sys
import inspect
import glob
import shutil

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def file_name(idxx):
    if idxx < 10:
        return('Chart0' + str(idxx))
    else: return('Chart'+ str(idxx))

ExportMQL = "C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/BF17AE6EAAB059EEBF7223939EC084E3/MQL4/Experts/"
ExportCHR= "C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/BF17AE6EAAB059EEBF7223939EC084E3/profiles/default/"
RemoveMQL = "C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/BF17AE6EAAB059EEBF7223939EC084E3/MQL4/Experts/*"
RemoveCHR= "C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/BF17AE6EAAB059EEBF7223939EC084E3/profiles/default/*"

path = get_script_dir()
allMQL = glob.glob(path + "./Incubazione/*.mq4")
# all_chr = glob.glob(path + "/Incubazione/*.chr")



def prod_chr(ExportMQL,ExportCHR,RemoveMQL,RemoveCHR,allMQL,allCHR):
    inst='EURUSD'
    files = glob.glob(RemoveMQL)
    for f in files:
        os.remove(f)
    
    files = glob.glob(RemoveCHR)
    for f in files:
        os.remove(f)
    
    var = {}
    idxx = 0
            
    text = '<chart>\n\
    id={idx}\n\
    symbol={instrument}\n\
    period={timeframe}\n\
    leftpos=141124\n\
    digits=5\n\
    scale=2\n\
    graph=0\n\
    fore=0\n\
    grid=1\n\
    volume=0\n\
    scroll=1\n\
    shift=0\n\
    ohlc=1\n\
    one_click=0\n\
    one_click_btn=1\n\
    askline=0\n\
    days=0\n\
    descriptions=0\n\
    shift_size=20\n\
    fixed_pos=0\n\
    window_left=195\n\
    window_top=160\n\
    window_right=1642\n\
    window_bottom=701\n\
    window_type=1\n\
    background_color=0\n\
    foreground_color=16777215\n\
    barup_color=65280\n\
    bardown_color=65280\n\
    bullcandle_color=0\n\
    bearcandle_color=16777215\n\
    chartline_color=65280\n\
    volumes_color=3329330\n\
    grid_color=10061943\n\
    askline_color=255\n\
    stops_color=255\n\
    <window>\n\
    height=100\n\
    fixed_height=0\n\
    <indicator>\n\
    name=main\n\
    </indicator>\n\
    </window>\n\
    <expert>\n\
    name={eaname}\n\
    flags = 339\n\
    window_num=0\n\
    <inputs>\n\
       '
    
    text2 = "</inputs>\n\
    </expert>\n\
    </chart>"

    for filename in allMQL:
        par = []
        idxx +=1
        g = str(idxx)
        eaname = os.path.basename(filename)[:-4] 
        timeframe = 60
        var = {'idx' : g, 'instrument' : inst, 'timeframe' : '60', 'eaname' : eaname}
        with open('temp.txt','a+') as obj:
            obj.write(text.format(**var))
            obj.close()
        with open(filename,'r') as file:
            for line in file:
                if 'extern' in line:
                   with open('temp.txt','a+') as obj:
                       obj.seek(0)
                       data = obj.read(100)
                       obj.write(line)
                       obj.close()   
        file.close()
        with open('temp.txt','a+') as obj:
            obj.write(text2)
            obj.close()
        fin = open('temp.txt','r')
        fout = open("%s.chr" % file_name(idxx), "wt")
        # print('%s.chr' % file_name(idxx))
        for line in fin:
            fout.write(line.replace('extern ','').replace('int ','').replace('string ','').replace('bool ','').replace(';','').replace('double ','')\
                        .replace('//Minimum SL in pips','').replace('//Minimum PT in pips','').replace('//Maximum SL in pips','').replace('//Maximum PT in pips','')\
                        .replace('// add word "" in front of the variable you want','').replace('// open bar delay in minutes','').replace('"','')\
                            .replace('1.0E-4','0.0001'))
        fin.close()
        fout.close()
        shutil.copy(filename,ExportMQL)
        os.remove('temp.txt')
        get_ipython().magic('reset -sf')
    
    # limit to 99 chr
    k=0
    for file in glob.glob('*.chr'):
        if k<100:
            shutil.move(file,ExportCHR)
            k +=1
        else: break
    


