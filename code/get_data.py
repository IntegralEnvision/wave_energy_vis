# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 11:20:38 2022

@author: aellenson
"""
import shutil
import urllib.request
import datetime
import datetime as dt
from contextlib import closing
import xarray as xr
import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import os
import time

t0 = time.time()

#Input Variables
#=====================
date = dt.datetime(2009,12,1)
spectype = 'full'

ftproot = 'https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2/{}/gribs/'.format(date.strftime('%Y%m'))
outroot = '../data/{}/'.format(spectype)
grid = 'multi_reanal.glo_30m_ext'
#====================================

param_dict = {}
paramnamedict = {'hs':'swh','tp':'perpw','dp':'dirpw'}
outfname = grid + '.{}.hs.tp.dp.pickle'.format(date.strftime('%Y%m'))
gribnames = []

for paramname in ['hs','tp','dp']:
    fname = grid + '.{}.{}.grb2'.format(paramname,date.strftime('%Y%m'))
    gribnames.append(outroot + fname)
    #Download a file
    with closing(urllib.request.urlopen(ftproot + fname)) as r:
        with open(outroot + fname, 'wb') as f:
            shutil.copyfileobj(r, f)
    
    dataset = xr.open_dataset(outroot+fname,engine='cfgrib')
    paramname = paramnamedict[paramname]
    param = dataset[paramname].values
    param_dict.update({paramname:param})


tdataset = dataset['time'].values
tstep = dataset['step'].values
lat = dataset['latitude'].values
lon = dataset['longitude'].values
time_vec = [tdataset + tt for tt in tstep]

hs = param_dict['swh']
tp = param_dict['perpw']
dp = param_dict['dirpw']

#reshape into columns
hs = hs.reshape(hs.size,)
tp = tp.reshape(tp.size,)
dp = dp.reshape(dp.size,)

#reshape lat and lon 
lat = np.tile(lat,int(hs.size/lat.shape[0]))
lon = np.tile(lon,int(hs.size/lon.shape[0]))

#reshape time
global_t = np.tile(np.array(time_vec),int(hs.size/len(time_vec)))

#save into a pandas dataframe
df_out = pd.DataFrame({'hs':hs, 'tp':tp, 'dp':dp, 'time':global_t, 'lat':lat, 'lon':lon})

df_out.to_pickle(outroot + outfname)

#clean up
allfiles = os.listdir(outroot)
allfiles = [aa for aa in allfiles if 'pickle' not in aa]
for file in allfiles:
    os.remove(outroot + file)

t1 = time.time()
total_time = t1-t0
print('Total time took {0:.2f} s'.format(total_time))

