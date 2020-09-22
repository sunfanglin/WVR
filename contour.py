#Author:Wu Dongqiao
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pylab import *
import tkinter.filedialog

#设置微波辐射数据路径选择要读取的_lv2.CSV文件
#wbfs_file_path='/home/python/Desktop/data/wbfs/2018-07-02_00-04-11_lv2.csv'
wbfs_file_path=tkinter.filedialog.askopenfilename()

#若没有选则退出
if wbfs_file_path==():
    exit()

#读取廓线数据
skip_rows=21                           #设置始读行
use_cols=tuple(i for i in range(0,62)) #设置使用的列数
cols_name=list(range(0,62))            #设置使用的列名（数据列）

#使用pandas_read_csv读取数据
data=pd.read_csv(wbfs_file_path,skiprows=skip_rows,dtype=str,delimiter=',',usecols=use_cols,names=cols_name)

#读取时间序列
Data_time=data[::7][1]
#读取雨状态
Rain=data[::7][7]
#读取温度廓线数据Temperature (K)
Tprof_data=data.iloc[1:,4:][::7]
#读取水汽廓线数据Vapor
Vprof_data=data.iloc[2:,4:][::7]
#读取液态水廓线数据Liquid
Lprof_data=data.iloc[3:,4:][::7]
#读取相对温度廓线数据Relative Humidity
RHprof_data=data.iloc[4:,4:][::7]

#转置成x,y轴后的数据
T_data=Tprof_data.astype(float).T.values
V_data=Vprof_data.astype(float).T.values
L_data=Lprof_data.astype(float).T.values
RH_data=RHprof_data.astype(float).T.values
Ra=Rain.astype(int).values    #由serise转成arrays(np)

#X轴取值时间
timeaxs=[]
if len(Data_time.values[0].split('/')[0])==4:
    title=('20'+Data_time.values[0][8:10]+'-'+Data_time.values[0][2:7]).replace('/','-')
    for i in range(len(Data_time)):
        timeaxs.append(Data_time.values[i][-5:])
else:
    title=('20' + Data_time.values[0][6:8] + '-' + Data_time.values[0][:5]).replace('/','-')
    for i in range(len(Data_time)):
        timeaxs.append(Data_time.values[i][-8:-3])

#高度取值按层数
hight=np.array([i/20 for i in range(0,11)]+[i/10 for i in range(6,21)]+[i/4 for i in range(9,41)])
time=np.linspace(0,24,T_data.shape[1])  #时间转为一维
x,y=np.meshgrid(time,hight)

#设置窗体
fig1,axes=plt.subplots(nrows=5,figsize=(12,10),sharex=True)

#设置颜色条
cm=plt.cm.get_cmap('rainbow')

#绘单个图的方法，温度廓线及设置
ax0=axes[0].pcolormesh(x,y,T_data,cmap=cm,vmin=np.min(T_data),vmax=np.max(T_data))
C=axes[0].contour(x,y,T_data,6,colors='black',linewidths=0.5) #画等值线
axes[0].clabel(C,inline=True,fontsize=8,fmt='%.0f')
axes[0].set_ylabel('temperature(K)')
fig1.colorbar(ax0,ax=axes[0])
axes[0].set_title(title)

#水气廓线及设置
ax1=axes[1].pcolormesh(x,y,V_data,cmap=cm,vmin=np.min(V_data),vmax=np.max(V_data))
C=axes[1].contour(x,y,V_data,6,colors='black',linewidths=0.5) #画等值线
axes[1].clabel(C,inline=True,fontsize=8,fmt='%.1f')
axes[1].set_ylabel('Vapor(g/m^3)')
fig1.colorbar(ax1,ax=axes[1])

#液态水廓线及设置
ax2=axes[2].pcolormesh(x,y,L_data,cmap=cm,vmin=np.min(L_data),vmax=np.max(L_data))
axes[2].set_ylabel('Liquid(g/m^3)')
C=axes[2].contour(x,y,L_data,4,colors='black',linewidths=0.5) #画等值线
axes[2].clabel(C,inline=True,fontsize=8,fmt='%.1f')
fig1.colorbar(ax2,ax=axes[2])

#相对湿度廓线及设置
ax3=axes[3].pcolormesh(x,y,RH_data,cmap=cm,vmin=np.min(RH_data),vmax=np.max(RH_data))
axes[3].set_ylabel('Relative Humidity(%)')
C=axes[3].contour(x,y,RH_data,4,colors='black',linewidths=0.5) #画等值线
axes[3].clabel(C,inline=True,fontsize=8,fmt='%.0f')
fig1.colorbar(ax3,ax=axes[3])

#画雨线及设置
axes[4].bar(time,Ra,color='r')
axes[4].set_ylabel('Rain')
axes[4].set_yticks([0,1])
axes[4].set_ylim(0,1)

#重点哦，将雨线与上对齐的方法get_position
pos3=axes[3].get_position()
pos4=[pos3.x0,pos3.y0-0.05,pos3.width-0.002,0.02]
axes[4].set_position(pos4)

#设置X轴范围
t0=0  #设置起启显示范围int (0至，len(time)-1
t1=len(time)-1  #设置终止显示范围,最大为len(time)-1
if t1>len(time)-1:
    t1=len(time)-1
plt.xlim(time[t0],time[t1]) #设置PLT的显示范围
plt.xticks(time[t0:t1][::30],timeaxs[t0:t1][::30],rotation=60)
plt.show()
