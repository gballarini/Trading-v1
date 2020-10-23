import re
import pandas as pd
import glob
import inspect
import os
import sys
from datetime import date


toRename ="./DatabaseIn"

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def gen_id():
    today = date.today()
    day = today.strftime('%d')
    month = today.strftime('%m')
    year = today.strftime('%y')
    return(day+month+year)


def rename(toRename):
    str_list=[]
    with os.scandir(toRename) as it:
        for entry in it:
            if entry.name.endswith(".sqx") and entry.is_file():
                str_list.append(entry.name)
    mql_list=[]
    with os.scandir(toRename) as it:
        for entry in it:
            if entry.name.endswith(".mq4") and entry.is_file():
                mql_list.append(entry.name)   
    csv_list=[]
    with os.scandir(toRename) as it:
        for entry in it:
            if entry.name.endswith(".csv") and entry.is_file():
                csv_list.append(entry.name)
    mylines=[]
    oldFileName = []
    newFileName = []
    newPathAndFileName =[]
    newPathAndFileNameSQX=[]
    oldPathAndFileNameSQX=[]
    for file in os.listdir(toRename):
        if file.endswith(".mq4"):
            oldFileName = toRename+str('/')+file
            oldFileNameSQX = toRename+str('/')+file[:-3]+str('sqx')
            oldFileNameCSV = toRename+str('/')+file[:-3]+str('csv')
    
    
            file_name = file[:-4]
            newFileName = (file_name+str(' ')+str(gen_id()))
            newPathAndFileName = toRename+str('/')+newFileName+str('.mq4')
            newPathAndFileNameSQX = toRename+str('/')+newFileName+str('.sqx')
            newPathAndFileNameCSV = toRename+str('/')+newFileName+str('.csv')
            os.rename(oldFileName,newPathAndFileName)
            os.rename(oldFileNameCSV,newPathAndFileNameCSV)
            os.rename(oldFileNameSQX,newPathAndFileNameSQX)
    return 


        # Vecchio per estrarre il magic number
        # with open(toRename+str('/')+file, 'rt') as myfile:
        #     for myline in myfile:
        #         if keyword in myline:
        #             # MagigNumber = int(filter(str.isdigit, myline))
        #             MagicNumber=int(re.search(r'\d+',myline).group(0))