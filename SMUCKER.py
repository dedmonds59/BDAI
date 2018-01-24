
# coding: utf-8

# # Smuckers Stock Analysis
# ##     I'm gonna visualizing stock prices
# ###          Author: Quinn McLaughlin
# 

# In[1]:

import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

get_ipython().magic('matplotlib inline')

# allows inline plots to be interactive
import mpld3
mpld3.enable_notebook()
plt.style.use('ggplot')


# In[2]:

#January 1st, 2000
startTime = dt.datetime(2000,1,1)
#December 9th, 2017
endTime = dt.datetime(2017,12,9)
#Grabs data from Yahoo 
SJM = web.DataReader('SJM', 'yahoo', startTime, endTime)


# In[3]:

SJM.head()


# In[4]:

SJM.tail()


# In[5]:

SJM['Volume'].plot(color='purple', title ='SJM Trade Volume')


# In[6]:

SJM['Open'].plot(title = ' Opening Prices')


# In[7]:

SJM_ohlc = SJM['Adj Close'].resample('7D').ohlc()
SJM_volume = SJM['Volume'].resample('7D').sum()


# In[8]:

SJM_ohlc.head()


# In[9]:

SJM_volume.head()


# In[ ]:

SJM_ohlc.reset_index(inplace=True)
SJM_ohlc['Date'] = SJM_ohlc['Date'].map(mdates.date2num)


# In[ ]:

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
candlestick_ohlc(ax1, SJM_ohlc.values, width=2, colorup='purple',colordown='brown')
ax2.fill_between(SJM_volume.index.map(mdates.date2num), SJM_volume.values, 0)


# New Cell for Closer candle

# In[ ]:

narrowAx1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
narrowAx2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
candlestick_ohlc(narrowAx1, SJM_ohlc.values, width=2, colorup='purple',colordown='brown')
narrowAx2.fill_between(SJM_volume.index.map(mdates.date2num), SJM_volume.values, 0)


# In[ ]:




# In[ ]:



