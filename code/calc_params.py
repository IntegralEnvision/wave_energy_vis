#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 09:56:41 2022

@author: ashley-integral
"""

import xarray as xr
import datetime as dt 
import numpy as np
import pandas as pd
from utils import IECParams 
#
#Questions - do we need to check that all the model runs have the same discretizations?


#load_data here, run client and get data to local directory 
#if month, get month, if year, get annual, --- see how many months and years you need

def load_param(filedir, filename, date, param):
    '''
    loads parameters from grib files

    Parameters
    ----------
    filedir : str : directory housing data files
    filename : str : file name
    date : datetime obj : month, year desired
    param : str : parameter name

    Returns
    -------
    parameter array t x m x n

    '''
    paramdict = {'hs':'swh', 'tp':'perpw','dp':'dirpw'}
    filename = 'multi_reanal.glo_30m_ext.{}.{}.grb2'.format(param,date.strftime('%Y%m'))
    dset = xr.open_dataset(filedir + filename,engine='cfgrib')
    paramarray = dset[paramdict[param]].values
    
    return paramarray
    

def load_all_params(year, month):
    
    
    '''
    load data from directory. this will be replaced with connecting to client, downloading from bucket, etc.

    Parameters
    ----------
    year :int: year desired
    month :int: month desired - future usage this could be a list of months
    param :str: hs, tp, or dp

    Returns
    -------
    time: t, array of n64 time
    lat : m, array of latitude values
    lon : n, array of longitude values
    hs_array: t x m x n array of hs values
    tp_array: t x m x n array of peak wave period values
    dp_array: t x m x n array of peak direction values    

    '''
    date = dt.datetime(year,month,1)
    
    
    #maps the file parameter name to the name in the netcdf
    filedir = '../data/full/'
    
    filename = 'multi_reanal.glo_30m_ext.hs.{}.grb2'.format(date.strftime('%Y%m'))
    dset = xr.open_dataset(filedir + filename,engine='cfgrib')
    time = np.array([pd.to_datetime(dset['time'].values + x) for x in dset['step'].values]) #Should we check to make sure the lat, lon and time are all aligned? 
    lat = dset['latitude'].values
    lon = dset['longitude'].values
        
    hs_array = load_param(filedir, filename, date, 'hs')
    tp_array = load_param(filedir, filename, date, 'tp')
    dp_array = load_param(filedir, filename, date, 'dp')
    
    return time, lat, lon, hs_array, tp_array, dp_array
        
def load_bathy(gridname):
    
    bathy_dir = '../data/'
    bathyset = xr.open_dataset(bathy_dir + gridname + '.nc')
    bathy = bathyset['depth'].values
    
    return bathy
    
time, lat, lon, hs, tp, dp = load_all_params(2009, 12)
depth = load_bathy('glo_30m')
iec = IECParams(hs, tp, dp, depth, time)
J = iec.total_power()

    
    
