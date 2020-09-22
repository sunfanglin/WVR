from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pylab import *
import tkinter.filedialog

# 设置微波辐射数据路径选择要读取的_lv2.CSV文件
# wbfs_file_path='/home/python/Desktop/data/wbfs/2018-07-02_00-04-11_lv2.csv'
wbfs_file_path = tkinter.filedialog.askopenfilename()

# 若没有选则退出
if wbfs_file_path == ():
    exit()

#读取廓线数据
skip_rows=21                           #设置始读行
use_cols=tuple(i for i in range(0,62)) #设置使用的列数
cols_name=list(range(0,62))            #设置使用的列名（数据列）

#使用pandas_read_csv读取数据
data=pd.read_csv(wbfs_file_path,skiprows=skip_rows,dtype=str,delimiter=',',usecols=use_cols,names=cols_name)

#读取温度廓线数据Temperature (K)
#Tprof_data=data[1:][::7].iloc[:,4:]    #iloc对dataFrame数组的操作
Tprof_data=data.iloc[1:,4:][::7]
#读取水汽廓线数据Vapor
Vprof_data=data.iloc[2:,4:][::7]
#读取液态水廓线数据Liquid
Lprof_data=data.iloc[3:,4:][::7]
#读取相对温度廓线数据Relative Humidity
RHprof_data=data.iloc[4:,4:][::7]

#转置成x,y轴后的数据
T_data=Tprof_data.astype(float).values
V_data=Vprof_data.astype(float).values
L_data=Lprof_data.astype(float).values
RH_data=RHprof_data.astype(float).values

#高度取值按层数
hight=np.array([i/20 for i in range(0,11)]+[i/10 for i in range(6,21)]+[i/4 for i in range(9,41)])

#取值行数对应时间
#读取时间块
Data_time=data[::7][1]
time=[]
#根据不同格式的时间字符转成YYYY-MM-DD HH:MM:SS
if len(Data_time.values[0].split('/')[0])==4:
    for i in range(len(Data_time)):
        # time.append(Data_time.values[i][-5:])
        time.append(('20'+Data_time.values[i][8:10]+'-'+Data_time.values[i][2:7]).replace('/','-')+Data_time.values[i][-6:]+':00')
else:
    for i in range(len(Data_time)):
        # time.append(Data_time.values[i][-8:-3])
        time.append(('20'+Data_time.values[i][6:8]+'-'+Data_time.values[i][:5]+Data_time.values[i][-9:]).replace('/','-'))

#取某条时间值
n=60
if n>len(time):
    n=len(time)

timelabel=time[n-1]

plt.figure(figsize=(12,8),dpi=80)

plt.subplot(1,3,1)
plt.plot(T_data[n,:],hight,color='r')
plt.ylim(0,10)
plt.xlabel('temperature(K)')
plt.ylabel('Height/km')
plt.grid()

plt.subplot(1,3,2)
plt.plot(V_data[n,:],hight,color='r')
plt.xlabel('Vapor(g/m^3)')
plt.grid()
plt.ylim(0,10)
plt.title(timelabel)

plt.subplot(1,3,3)
plt.plot(L_data[n,:],hight,color='r')
plt.xlabel('Liquid(g/m^3)')
plt.ylim(0,10)
plt.grid()

plt.tight_layout()
plt.show()
