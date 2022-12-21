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



#Input Variables
#=====================
date = dt.datetime(2009,12,1)
spectype = 'full'

ftproot = 'https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2/{}/gribs/'.format(date.strftime('%Y%m'))
outroot = '../data/{}/'.format(spectype)
grid = 'multi_reanal.glo_30m_ext'
#====================================

param_dict = {}
params = ['hs', 'dp', 'tp']
gribnames = []

for paramname in params:
    fname = grid + '.{}.{}.grb2'.format(paramname,date.strftime('%Y%m'))
    gribnames.append(outroot + fname)
    #Download a file
    with closing(urllib.request.urlopen(ftproot + fname)) as r:
        with open(outroot + fname, 'wb') as f:
            shutil.copyfileobj(r, f)
    
