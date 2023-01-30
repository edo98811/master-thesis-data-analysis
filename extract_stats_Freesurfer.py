# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 09:44:17 2022

@author: Helena
"""

import zipfile
import os
import pandas as pd
import shutil
import csv
import re


# if the folders are not in a zip file:
mainDir = ''
all_path = []
for path, subdirs, files in os.walk(mainDir):
    for name in files:
        all_path.append(os.path.join(path, name))


# if the folders are in a zip file:
# zip file handler  
zip_dir = 'C:\\Users\\helen\\Downloads'
filename = 'subject_output_nifti3_2.zip'
save_dir = 'C:\\Users\\helen\\Downloads\\Nova pasta'
zipf = zipfile.ZipFile(os.path.join(zip_dir,filename),"r")
all_path = zipf.namelist()


##### ASEG STATS
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('aseg.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = ['SegId','NVoxels','Volume_mm3','StructName','normMean','normStdDev','normMin','normMax','normRange']

subjs = []
df_final1 = pd.DataFrame()
df_final2 = pd.DataFrame()

for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()
    
    #1st measures
    ls = stats_aseg.splitlines()
    ls = ls[14:33]
    df1 = dfs.iloc[14:33]
    df1 = dfs.iloc[14:33,3].tolist()
    vals = []
    for i in range(len(ls)):
        if (i < 16):
            vals.append(float(re.findall("\d+\.\d+",ls[i])[0])) # prende i numeri con il punto
        else:
            vals.append(int(re.findall(r"\d+",ls[i])[0])) # prende i numeri senza punto (ci sono tre righe)
    df1 = pd.DataFrame({'Metric':df1,'value':vals}).T

    sub_df = df1.reset_index()
    sub_df.columns = sub_df.iloc[0]
    sub_df2 = sub_df.drop(sub_df.index[0])
    
    
    df_final1 = pd.concat([df_final1,sub_df2])
    
    


    #2nd measures
    df = dfs.iloc[79:,2:11]
    #df = df.iloc[:, 2:11]

    df.columns = cols_aseg
    df['Volume_mm3'] = pd.to_numeric(df['Volume_mm3'])
    sub_df = df[['StructName','Volume_mm3']].T
    sub_df = sub_df.reset_index()
    sub_df.columns = sub_df.iloc[0]
    sub_df = sub_df.drop(sub_df.index[0])
    df_final2 = pd.concat([df_final2, sub_df])
    


df_final1 = df_final1.drop(['Metric'],axis=1)    
new_cols = []
holes = ['lhSurfaceHoles,','rhSurfaceHoles,','SurfaceHoles,']
for c in df_final1.columns.tolist():
    if c not in holes:
        new_cols.append('Volume_'+c.split(',')[0])
    else:
        new_cols.append('Number_'+c.split(',')[0])
df_final1.columns = new_cols  
df_final1.insert(0,'Subjects',subjs)


df_final2 = df_final2.drop(['StructName'],axis=1)    
new_cols = []
for c in df_final2.columns.tolist():
    new_cols.append('Volume_'+c)
df_final2.columns = new_cols  
df_final2.insert(0,'Subjects',subjs)

df_final = pd.merge(df_final2,df_final1, on='Subjects',how='outer')

df_final.to_csv(os.path.join(save_dir,'aseg_measures.csv'),index=False)

##### APARC STATS - Left
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('lh.aparc.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = []


subjs = []
df_final1 = pd.DataFrame()
df_final2 = pd.DataFrame()
dict_data = dict()
for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()


    #1st measures
    ls = stats_aseg.splitlines()
    ls = ls[18:29]
    df1 = dfs.iloc[18:29]
    df1 = dfs.iloc[18:29,4].tolist()
    vals = []
    for i in range(len(ls)):
        if (i == 0):
            vals.append(int(re.findall(r"\d+",ls[i])[0]))
        elif(i == 3):
            vals.append(0)
        else:
            try:
                vals.append(float(re.findall("\d+\.\d+",ls[i])[0]))
            except:
                vals.append(float(re.findall(r"\d+",ls[i])[0]))
    df1 = pd.DataFrame({'Metric':df1,'value':vals}).T  
    sub_df = df1.reset_index()
    sub_df.columns = sub_df.iloc[0]
    sub_df2 = sub_df.drop(sub_df.index[0])
    df_final1 = pd.concat([df_final1,sub_df2])
    
    #2nd measures
    df = dfs.iloc[60:,1:13]
    cols = df.iloc[0].tolist()
    del cols[0:2]
    df = df.iloc[1:,0:10]
    df.columns = cols
    del cols[0]
    if(dict_data):
        for c in cols:
            n = dict_data[c]
            df[c] = pd.to_numeric(df[c])
            sub_dfi = df[['StructName',c]].T
            sub_dfi = sub_dfi.reset_index()
            sub_dfi.columns = sub_dfi.iloc[0]
            sub_dfi = sub_dfi.drop(sub_dfi.index[0])
            sub_dfi = sub_dfi.drop(['StructName'],axis=1) 
            n = pd.concat([n,sub_dfi])
            dict_data.update({c:n})           
    else:
        for c in cols:
            df[c] = pd.to_numeric(df[c])
            sub_dfi = df[['StructName',c]].T
            sub_dfi = sub_dfi.reset_index()
            sub_dfi.columns = sub_dfi.iloc[0]
            sub_dfi = sub_dfi.drop(sub_dfi.index[0])
            sub_dfi = sub_dfi.drop(['StructName'],axis=1) 
            dict_data.update({c:sub_dfi})
            
    
df_final1 = df_final1.drop(['Metric','voxelvolume=1mm3'],axis=1)
new_cols = []
for cc in df_final1.columns.tolist():
    new_cols.append('lh_'+ cc)
df_final1.columns = new_cols  
df_final1.insert(0,'Subjects',subjs)    



for c in cols:
    df_final2 = dict_data [c]
    new_cols = []
    for cc in df_final2.columns.tolist():
        new_cols.append('lh_'+ c +'_'+ cc)
    df_final2.columns = new_cols  
    df_final2.insert(0,'Subjects',subjs)

df_final = pd.merge(df_final2,df_final1, on='Subjects',how='outer')
df_final.to_csv(os.path.join(save_dir,'lh_aparc_measures.csv'),index=False)

##### APARC STATS - Right
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('rh.aparc.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = []


subjs = []
df_final1 = pd.DataFrame()
df_final2 = pd.DataFrame()
dict_data = dict()
for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()


    #1st measures
    ls = stats_aseg.splitlines()
    ls = ls[18:29]
    df1 = dfs.iloc[18:29]
    df1 = dfs.iloc[18:29,4].tolist()
    vals = []
    for i in range(len(ls)):
        if (i == 0):
            vals.append(int(re.findall(r"\d+",ls[i])[0]))
        elif(i == 3):
            vals.append(0)
        else:
            try:
                vals.append(float(re.findall("\d+\.\d+",ls[i])[0]))
            except:
                vals.append(float(re.findall(r"\d+",ls[i])[0]))
            
    df1 = pd.DataFrame({'Metric':df1,'value':vals}).T  
    sub_df = df1.reset_index()
    sub_df.columns = sub_df.iloc[0]
    sub_df2 = sub_df.drop(sub_df.index[0])
    df_final1 = pd.concat([df_final1,sub_df2])
    
    #2nd measures
    df = dfs.iloc[60:,1:13]
    cols = df.iloc[0].tolist()
    del cols[0:2]
    df = df.iloc[1:,0:10]
    df.columns = cols
    del cols[0]
    if(dict_data):
        for c in cols:
            n = dict_data[c]
            df[c] = pd.to_numeric(df[c])
            sub_dfi = df[['StructName',c]].T
            sub_dfi = sub_dfi.reset_index()
            sub_dfi.columns = sub_dfi.iloc[0]
            sub_dfi = sub_dfi.drop(sub_dfi.index[0])
            sub_dfi = sub_dfi.drop(['StructName'],axis=1) 
            n = pd.concat([n,sub_dfi])
            dict_data.update({c:n})           
    else:
        for c in cols:
            df[c] = pd.to_numeric(df[c])
            sub_dfi = df[['StructName',c]].T
            sub_dfi = sub_dfi.reset_index()
            sub_dfi.columns = sub_dfi.iloc[0]
            sub_dfi = sub_dfi.drop(sub_dfi.index[0])
            sub_dfi = sub_dfi.drop(['StructName'],axis=1) 
            dict_data.update({c:sub_dfi})
            
    
df_final1 = df_final1.drop(['Metric','voxelvolume=1mm3'],axis=1)
new_cols = []
for cc in df_final1.columns.tolist():
    new_cols.append('rh_'+ cc)
df_final1.columns = new_cols  
df_final1.insert(0,'Subjects',subjs)    


for c in cols:
    df_final2 = dict_data[c]
    new_cols = []
    for cc in df_final2.columns.tolist():
        new_cols.append('rh_'+ c +'_'+ cc)
    df_final2.columns = new_cols  
    df_final2.insert(0,'Subjects',subjs)

df_final = pd.merge(df_final2,df_final1, on='Subjects',how='outer')
df_final.to_csv(os.path.join(save_dir,'rh_aparc_measures.csv'),index=False)
"""
## Amygdala - left
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('amygdalar-nuclei.lh.T1.v22.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = []


subjs = []
df_final = pd.DataFrame()

dict_data = dict()
for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()
    
    #Measures
    df1 = dfs.iloc[1:,4:6]
    df1 = df1[[4,3]].T
    df1.columns = df1.iloc[0]
    df1 = df1.reset_index()
    df1 = df1.drop(df1.index[0])
    df1 = df1.drop(['index'],axis=1)
    df_final = pd.concat([df_final, df1])


new_cols = []
for cc in df_final.columns.tolist():
    new_cols.append('lh_'+ cc)
df_final.columns = new_cols  
df_final.insert(0,'Subjects',subjs)    

df_final.to_csv(os.path.join(save_dir,'lh_amygdala.csv'),index=False)

# Amygdala - right
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('amygdalar-nuclei.rh.T1.v22.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = []


subjs = []
df_final = pd.DataFrame()

dict_data = dict()
for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()
    
    #Measures
    df1 = dfs.iloc[1:,4:6]
    df1 = df1[[4,3]].T
    df1.columns = df1.iloc[0]
    df1 = df1.reset_index()
    df1 = df1.drop(df1.index[0])
    df1 = df1.drop(['index'],axis=1)
    df_final = pd.concat([df_final, df1])


new_cols = []
for cc in df_final.columns.tolist():
    new_cols.append('rh_'+ cc)
df_final.columns = new_cols  
df_final.insert(0,'Subjects',subjs)    
df_final.to_csv(os.path.join(save_dir,'rh_amygdala.csv'),index=False)



## Hippocampus - left
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('hipposubfields.lh.T1.v22.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = []


subjs = []
df_final = pd.DataFrame()

dict_data = dict()
for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()
    
#     #Measures
    df1 = dfs.iloc[1:,4:6]
    df1 = df1[[4,3]].T
    df1.columns = df1.iloc[0]
    df1 = df1.reset_index()
    df1 = df1.drop(df1.index[0])
    df1 = df1.drop(['index'],axis=1)
    df_final = pd.concat([df_final, df1])


new_cols = []
for cc in df_final.columns.tolist():
    new_cols.append('lh_'+ cc)
df_final.columns = new_cols  
df_final.insert(0,'Subjects',subjs)  
df_final.to_csv(os.path.join(save_dir,'lh_hippocampus.csv'),index=False)


## Hippocampus - right
subjs_path = []
for p in all_path:
    if('/stats/' in p):
        if('hipposubfields.rh.T1.v22.stats' in p):
            subjs_path.append(p)

#subjs_path = subjs_path[:3]
cols_aseg = []


subjs = []
df_final = pd.DataFrame()

dict_data = dict()
for s in subjs_path:
    #print(s)
    subjs.append(s.split("/")[1])
    stats_aseg = zipf.read(s).decode("utf-8")
    f_lines = []
    dfs = pd.DataFrame()
    for line in stats_aseg.splitlines():
        a = line.split(" ")
        str_list = filter(None, a)
        dfl = pd.DataFrame([str_list],index=[0])
        dfs = pd.concat([dfs,dfl])
        #print(df)
    dfs = dfs.reset_index()
    
#     #Measures
    df1 = dfs.iloc[1:,4:6]
    df1 = df1[[4,3]].T
    df1.columns = df1.iloc[0]
    df1 = df1.reset_index()
    df1 = df1.drop(df1.index[0])
    df1 = df1.drop(['index'],axis=1)
    df_final = pd.concat([df_final, df1])


new_cols = []
for cc in df_final.columns.tolist():
    new_cols.append('rh_'+ cc)
df_final.columns = new_cols  
df_final.insert(0,'Subjects',subjs)  
df_final.to_csv(os.path.join(save_dir,'rh_hippocampus.csv'),index=False)
"""