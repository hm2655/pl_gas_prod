# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 13:15:31 2020

@author: harshit.mahajan
"""

#PointLogic Prod Module 
import os
import pandas as pd 
from datetime import date 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

mapping_file_path = 'XXXX'
excelFile = pd.ExcelFile(mapping_file_path)
sheetList = excelFile.sheet_names
region_mapping = excelFile.parse('Sheet1', header = None).iloc[0:].reset_index(drop=True) 
region_mapping.columns = region_mapping.iloc[0]
region_mapping = region_mapping.drop(region_mapping.index[0])[['Producing Area','Basin']]


today = date.today()

if today.day<10:
    path = 'XXXX'
    name = 'Gas_Lower48 Daily_ProducingArea_Volume_Sample ' + '0' + str(today.month) + '-0'+ str(today.day) + '-' + str(today.year) +'.csv' 

    flowData = pd.DataFrame()
    filepath = path + name
    df = pd.read_csv(filepath)
    meltedDf = pd.melt(df, id_vars = ['Region','State','Producing Area'], var_name = 'Date_id',value_name = 'flows').dropna()
    meltedDf= meltedDf[meltedDf['Date_id'] != '30 Day Average']
    meltedDf['Date_id'] = meltedDf.Date_id.astype('datetime64[ns]') 
    
    meltedDf = pd.merge(meltedDf, region_mapping, how = 'left', left_on = 'Producing Area', right_on='Producing Area', suffixes=('_left','_right'))
    
    meltedDf = meltedDf[['Region','State','Basin','Producing Area', 'Date_id','flows']]
    
    sum_region = meltedDf.groupby(['Region', 'Date_id']).sum().reset_index()
    sum_region['7dayMean'] = sum_region['flows'].rolling(7).mean()
    
    sum_state = meltedDf.groupby(['State', 'Date_id']).sum().reset_index()
    sum_state['7dayMean'] = sum_state['flows'].rolling(7).mean()
        
    sum_producingarea= meltedDf.groupby(['Producing Area', 'Date_id']).sum().reset_index()
    sum_producingarea['7dayMean'] = sum_producingarea['flows'].rolling(7).mean()
    
    sum_basin= meltedDf.groupby(['Basin', 'Date_id']).sum().reset_index()
    sum_basin['7dayMean'] = sum_basin['flows'].rolling(7).mean()
    
    daily_sum = meltedDf[['Date_id','flows']].groupby(['Date_id']).sum().reset_index()        
    daily_sum['7dayMean'] =  daily_sum['flows'].rolling(7).mean()
    
    
    path = 'XXXX'
    name = 'ple_gas_sampleprod_' + str(today) + '.xlsx'
    filepath = path + name 
    
    dfs = {'daily_prod': daily_sum, 'regional_prod':sum_region, 'state_prod': sum_state, 'producing_area':sum_producingarea, 'basin_level':sum_basin}
    writer = pd.ExcelWriter(filepath, engine = 'xlsxwriter')
    
    for sheetname in dfs.keys():
        print(sheetname)
        dfs[sheetname].to_excel(writer, sheet_name=sheetname, index = False)
    writer.save()            
        
else:

    path = 'XXXX'
    name = 'Gas_Lower48 Daily_ProducingArea_Volume_Sample ' + '0'+ str(today.month) + '-'+ str(today.day) + '-' + str(today.year) +'.csv' 

    flowData = pd.DataFrame()
    filepath = path + name
    df = pd.read_csv(filepath)
    df.columns
    meltedDf = pd.melt(df, id_vars = ['Region','State','Producing Area'], var_name = 'Date_id',value_name = 'flows').dropna()
    meltedDf= meltedDf[meltedDf['Date_id'] != '30 Day Average']
    meltedDf['Date_id'] = meltedDf.Date_id.astype('datetime64[ns]') 
    meltedDf = pd.merge(meltedDf, region_mapping, how = 'left', left_on = 'Producing Area', right_on='Producing Area')
    meltedDf = meltedDf[['Region','State','Basin','Producing Area', 'Date_id','flows']]
    
    sum_region = meltedDf.groupby(['Region', 'Date_id']).sum().reset_index()
    sum_region['7dayMean'] = sum_region['flows'].rolling(7).mean()
    
    sum_state = meltedDf.groupby(['State', 'Date_id']).sum().reset_index()
    sum_state['7dayMean'] = sum_state['flows'].rolling(7).mean()
        
    sum_producingarea= meltedDf.groupby(['Producing Area', 'Date_id']).sum().reset_index()
    sum_producingarea['7dayMean'] = sum_producingarea['flows'].rolling(7).mean()
    
    sum_basin= meltedDf.groupby(['Basin', 'Date_id']).sum().reset_index()
    sum_basin['7dayMean'] = sum_basin['flows'].rolling(7).mean()
    
    daily_sum = meltedDf[['Date_id','flows']].groupby(['Date_id']).sum().reset_index()        
    daily_sum['7dayMean'] =  daily_sum['flows'].rolling(7).mean()
    
    path = 'XXXX'
    name = 'ple_gas_sampleprod_' + str(today) + '.xlsx'
    filepath = path + name 
    
    dfs = {'daily_prod': daily_sum, 'regional_prod':sum_region, 'state_prod': sum_state, 'producing_area':sum_producingarea, 'basin_level':sum_basin}
    writer = pd.ExcelWriter(filepath, engine = 'xlsxwriter')
    
    for sheetname in dfs.keys():
        print(sheetname)
        dfs[sheetname].to_excel(writer, sheet_name=sheetname, index = False)
    writer.save()            
        
fig, ax= plt.subplots(figsize=(12,8))
groups = sum_basin.groupby('Basin')
        
for i, (key, grp) in enumerate(groups):
    grp.plot(linestyle= 'solid' , x = 'Date_id',y='7dayMean',label= key, ax=ax)     
    
plt.plot(daily_sum['Date_id'], daily_sum['flows'])
