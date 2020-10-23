# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 18:37:04 2020

@author: ruleb
"""
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

# x = os.chdir(get_script_dir())
for file in glob.glob('*.chr'):
    print(file)