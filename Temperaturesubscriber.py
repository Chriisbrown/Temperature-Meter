# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 14:46:47 2018

@author: chris
"""

import paho.mqtt.subscribe as subscribe
import matplotlib.pyplot as plt
import pandas as pd
    
df = pd.DataFrame(columns=['Time','Temperature 1','Temperature 2','Temperature 3'])
with open('hometempdata.csv', 'w+') as f:
        df.to_csv(f, header=True,index=False)
        
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
f.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

def plotting(axes,x,y,colour,label,ylabel):
    axes.clear()
    axes.plot(x,y,color=colour,label=label)
    axes.legend()
    axes.grid()
    axes.set_ylabel(ylabel)
    
           
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
        
    if i < 100:
        plotting(ax1,df['Time'], df['Temperature 1'],colour='red',label='Temperature 1',ylabel='$^\circ$C')
        plotting(ax2,df['Time'],df['Temperature 2'],colour='green',label='Temperature 2',ylabel='$^\circ$C')
        plotting(ax3,df['Time'],df['Temperature 3'],colour='blue',label='Temperature 3',ylabel='$^\circ$C')    
        ax3.set_xlabel('Time (s)')
        plt.pause(0.01)
        plt.show()
    else:
        plotting(ax1,df['Time'][i-100:i], df['Temperature 1'][i-100:i],colour='red',label='Temperature 1',ylabel='$^\circ$C')
        plotting(ax2,df['Time'][i-100:i],df['Temperature 2'][i-100:i],colour='green',label='Temperature 2',ylabel='$^\circ$C')
        plotting(ax3,df['Time'][i-100:i],df['Temperature 3'][i-100:i],colour='blue',label='Temperature 3',ylabel='$^\circ$C')    
        ax3.set_xlabel('Time (s)')
        plt.pause(0.01)
        plt.show()
    i += 1
    
print(df)
