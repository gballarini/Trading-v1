# -*- coding: utf-8 -*-

import re
import pandas as pd
import glob
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
import shutil
import os

#cartella con le strategie in csv
database_in = "./DatabaseIn/"
path_databank = "./DataBank/DatabankExport.csv"
path_incubazione = "./Incubazione"
all_csv = glob.glob(database_in + "/*.csv")



def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


def decorr(strat_to_decorrelate,path_databank,path_incubazione,all_csv):
    li = []
#modOpen è la colonna con la data dei trade, successivamente verranno combinati i trade su base data
    frame = pd.DataFrame(columns=['modOpen'])
    for filename in all_csv:
    
        #isolare numero strategia
        x = str(re.split(" ",str(filename))[1:][0])
        # print(x)
        xs = x.replace('[','').replace(']','').replace('.csv','')             
        #aggiungere ai csv colonna con i numeri strategia
        csv_input = pd.read_csv(filename, index_col=None, header=0, sep = ';', usecols = ['Balance', 'Open time','MAE ($)', 'MFE ($)'])
        csv_input['Strategy'] = xs
        csv_input['modOpen'] = csv_input['Open time'].str.split(' ').str[0]    
        # #con balance
        csv_input["Profit"] = (csv_input['Balance']-csv_input['Balance'].min())/(csv_input['Balance'].max()-csv_input['Balance'].min())
        csv_input["MAE1"] = (csv_input['MAE ($)']-csv_input['MAE ($)'].min())/(csv_input['MAE ($)'].max()-csv_input['MAE ($)'].min())
        csv_input["MFE1"] = (csv_input['MFE ($)']-csv_input['MFE ($)'].min())/(csv_input['MFE ($)'].max()-csv_input['MFE ($)'].min())
        csv_input[xs] = (csv_input['Profit']+csv_input['MAE1']+csv_input['MFE1'])/3
        csv_input[xs] = csv_input['Profit']
        csv_input = csv_input.drop(["Balance","Profit",'Strategy','Open time','MAE ($)', 'MFE ($)',"MAE1","MFE1"], axis=1)
        csv_inp =csv_input.groupby('modOpen').tail(1)
        csv_in = csv_inp[(csv_inp['modOpen'] != 0)]
        csv_out = csv_in.set_index('modOpen')    
        frame = frame.merge(csv_out,on='modOpen',how='outer')
   
    frame.fillna(method='ffill', inplace = True)      
    frame = frame.set_index('modOpen')
    frame.sort_index(inplace=True)

    #Unire in un database le statistiche delle strategie
    Z= frame.corr() 
    Zlista = Z.index.values.tolist()
    linked = linkage(Z, 'centroid')
    labelList = Zlista
    plt.figure(figsize=(20, 10), dpi = 150)
    den = dendrogram(linked,
                orientation='top',
                labels=labelList,
                distance_sort='descending',
                color_threshold=2,
                truncate_mode='level',#'lastp'
                p=25 ,
                leaf_rotation=80 ,
                show_leaf_counts=False
                )
    
    labels = fcluster(linked,2,criterion ='distance')
    clus = pd.DataFrame({'Cluster':labels,'Strategy':labelList})
    clus['Strategies'] = clus['Strategy'].str.replace("'", "")
    clus.set_index('Strategies', inplace = True)
    clus.drop(axis = 1, labels = ['Strategy'], inplace = True)

    db_input = pd.read_csv(path_databank, index_col=None, header=0, sep = ';',usecols = ['Strategy Name', 'Fitness' ])
    db_input['Strategy Name'] = db_input['Strategy Name'].str.replace('Strategy ', '')
    db_input.set_index('Strategy Name', inplace = True)
    mer = clus.join(db_input)
    mer['Strategy'] = mer.index 
    mer.sort_values(by = ['Cluster','Fitness'], inplace = True,ascending=True)
    finDb = mer.loc[mer.groupby(['Cluster'])['Fitness'].idxmax()]
    return(finDb)


#scansiona i cluster e sposta le strategie nella output folder. L'output della funzione decorr() è l'input database.
#gen_path è il path generale, per rimuovere le strategie da tutte le cartelle 
def move_strat_clusters(database,database_in,path_incubazione):
    for v in database.iterrows():
        x = v[1]['Strategy']
        # print(x)
        for k in database_in:
            if x in k:
                shutil.move(k,path_incubazione)
            else:
                remove(k)
            



