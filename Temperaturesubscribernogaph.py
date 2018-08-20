# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 14:46:47 2018

@author: chris
"""

import paho.mqtt.subscribe as subscribe

import pandas as pd
    
df = pd.DataFrame(columns=['Time','Temperature 1','Temperature 2','Temperature 3'])
with open('hometempdata.csv', 'w+') as f:
        df.to_csv(f, header=True,index=False)
          
topics = ['#']
i = 0
N = 10000
while i < N:
    df_temp = pd.DataFrame(index=range(0,1), columns=['Time','Temperature 1','Temperature 2','Temperature 3'])
    m = subscribe.simple(topics, hostname="10.0.100.213", retained=False, msg_count=4)
    for a in m:
        y = a.payload
        if a.topic == 'time':
            df_temp['Time'][0] = float(y.decode())
        if a.topic == 'Temperature 1':
            df_temp['Temperature 1'][0] = float(y.decode())
        if a.topic == 'Temperature 2':
            df_temp['Temperature 2'][0] = float(y.decode())
        if a.topic == 'Temperature 3':
            df_temp['Temperature 3'][0] = float(y.decode())
    print('message count:',i)
    df = df.append(df_temp)
    with open('hometempdata.csv', 'a+') as f:
        df_temp.to_csv(f, header=False)
        
    i += 1
    
print(df)
