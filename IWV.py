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

#读取时间序列
Data_time=data[::7][1]

#int_Vapor=data[5:][::7][3]
int_Vapor=data.iloc[5:,3][::7]
int_Vapor=int_Vapor.astype(float).values
#读取液态水积分
int_Liquid=data.iloc[5:,4][::7]
int_Liquid=int_Liquid.astype(float).values
#读取云底高度
Cloud_base=data.iloc[5:,5][::7]
Cloud_base=Cloud_base.astype(float).values
#读取雨状态
Rain=data[::7][7]
Ra=Rain.astype(int).values

#X轴取值时间
timeaxs=[]
if len(Data_time.values[0].split('/')[0])==4:
    title = ('20' + Data_time.values[0][8:10] + '-' + Data_time.values[0][2:7]).replace('/', '-')
    for i in range(len(Data_time)):
        timeaxs.append(Data_time.values[i][-5:])
else:
    title = ('20' + Data_time.values[0][6:8] + '-' + Data_time.values[0][:5]).replace('/', '-')
    for i in range(len(Data_time)):
        timeaxs.append(Data_time.values[i][-8:-3])

#获妈时间序列
time=np.linspace(0,24,len(Data_time))  #时间转为一维

plt.figure(figsize=(12,8),dpi=80)

#设置X轴范围
t0=0  #设置起启显示范围int (0至，len(time)-1
t1=len(time)-1  #设置终止显示范围,最大为len(time)-1
if t1>len(time)-1:
    t1=len(time)-1

#绘第一个图
plt.subplot(411)
plt.plot(time,int_Vapor,color='r',linewidth=1.0)
plt.ylabel('int_Vapor(cm)')
plt.xlim(time[t0],time[t1]) #设置PLT的显示范围
plt.xticks(time[t0:t1][::30],[])
plt.title(title)

plt.subplot(412)
plt.plot(time,int_Liquid,color='r',linewidth=1.0)
plt.ylabel('int-Liquid(mm)')
plt.xlim(time[t0],time[t1]) #设置PLT的显示范围
plt.xticks(time[t0:t1][::30],[])

plt.subplot(413)
plt.plot(time,Cloud_base,color='r',linewidth=1.0)
plt.ylabel('Cloud_base(km)')
plt.xlim(time[t0],time[t1]) #设置PLT的显示范围
plt.xticks(time[t0:t1][::30],[])

ax=plt.subplot(414)
plt.bar(time,Ra,color='r',linewidth=1.0)
plt.ylabel('Rain')
plt.yticks([0,1])
pos=ax.get_position()
ax.set_position([pos.x0,pos.y0+0.15,pos.width,0.02])
plt.xlim(time[t0],time[t1]) #设置PLT的显示范围
plt.xticks(time[t0:t1][::30],rotation=60)
plt.show()
