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

#Input Variables
#=====================
date = dt.datetime(2009,12,1)
param = 'hs'
spectype = 'full'

ftproot = 'https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2/{}/gribs/'.format(date.strftime('%Y%m'))
outroot = '../data/{}/'.format(spectype)

fname = 'multi_reanal.glo_30m_ext.{}.{}.grb2'.format(param,date.strftime('%Y%m'))


# with closing(urllib.request.urlopen(ftproot + fname)) as r:
#     with open(outroot + fname, 'wb') as f:
#         shutil.copyfileobj(r, f)

hsdataset = xr.open_dataset(outroot+fname,engine='cfgrib')