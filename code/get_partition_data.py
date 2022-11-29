# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:46:39 2022

@author: aellenson
"""
import shutil
import urllib.request
import requests 
import datetime as dt
from contextlib import closing
import xarray as xr
import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import os
import time
import netCDF4 as nc
import dask

def to_datetime(timesecs):
    t = dt.datetime(1970,1,1) + dt.timedelta(days = timesecs)
    return t
    
def download_file(url, local_fname):
    # NOTE the stream=True parameter below
    chunknum = 1
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=500000000000): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
                print('Chunk number {}'.format(chunknum))
                chunknum+=1

def select_partition_parameter(dset, paramname, partitionnum):
    param = dset[paramname].sel(partition=partitionnum).values
    return param

def reshape_param(param):
    param = param.reshape(param.size,)
    return param

date = dt.datetime(2009,12,1)
spectype = 'partition'

ftproot = 'https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2/{}/partitions/'.format(date.strftime('%Y%m'))
outroot = '../data/{}/'.format(spectype)
grid = 'multi_reanal.partition.glo_30m'
fname = grid + '.{}'.format(date.strftime('%Y%m'))
local_netcdf = outroot + fname + '.nc'
url = ftproot + fname + '.nc'


# download_file(url, local_fname)
dset = xr.open_dataset(local_netcdf,engine='netcdf4')
time_vec = dset['date'].values
lat = dset['latitude'].values
lon = dset['longitude'].values
hs = dset['significant_wave_height'].sel(partition=1).values
partitions = [int(xx) for xx in dset['partition'].values]

#develop dataframes

#reshape lat and lon 
lat_tiled = np.tile(lat,int(hs.size/lat.shape[0]))
lon_tiled = np.tile(lon,int(hs.size/lon.shape[0]))

#reshape time
time_tiled = np.tile(np.array(time_vec),int(hs.size/len(time_vec)))

t1 = time.time()
for partitionnum in partitions:
    local_pqt = fname + '.part{0:d}.parquet'.format(partitionnum)
    hs = dask.delayed(select_partition_parameter(dset, 'significant_wave_height', partitionnum))
    k = dask.delayed(select_partition_parameter(dset, 'wavelength', partitionnum))
    tp = dask.delayed(select_partition_parameter(dset, 'peak_period', partitionnum))
    dp = dask.delayed(select_partition_parameter(dset, 'wave_direction', partitionnum))
    
    #reshape into columns
    hs = dask.delayed(reshape_param(hs))
    tp = dask.delayed(reshape_param(tp))
    dp = dask.delayed(reshape_param(dp))
    k = dask.delayed(reshape_param(k))

    #save into a pandas dataframe
    df_out = pd.DataFrame({'hs':hs.compute(), 'tp':tp.compute(), 'dp':dp.compute(), 'time':time_tiled, 'lat':lat_tiled, 'lon':lon_tiled})

    df_out.to_parquet(outroot + local_pqt)

t2 = time.time()
print('time took {0:.2f} secs'.format(t2-t1))
