# -*- coding: utf-8 -*-

import numpy 
import pandas 
from mhkit.wave.resource import wave_number, wave_celerity
import time

class IECParams:
    
    def __init__(self, hs, tp, dp, depth, time_vec):

        self.hs = hs
        self.tp = tp
        self.dp = dp
        self.depth = depth
        self.time = time_vec
        
        self.total_hours = (self.time[-1] - self.time[0]).total_seconds()/3600

    def energy_period(self,wind_sea_cutoff = 6):
        '''
        Calculate energy period following Ahn et al, 2022
        
        Te = C * Tp where the value of C depends on Tp.
        
        wind_sea_cutoff is the cut off period; peak wave period values less 
        than the cutoff value are considered wind sea
        
        Attributes:
        --------------------
        te: time x lat x lon: energy period (s)
        
        >>> 10 = energy_period(10, wind_sea_cutoff=6)
        >>> 4.3 = energy_period(5, wind_sea_cutoff=6)
        
        '''
        C_wind = 0.86
        C_swell = 1
        self.te = C_swell * self.tp
        windsea_mask = self.te<wind_sea_cutoff
        self.te[windsea_mask] = C_wind * self.te[windsea_mask] 


    def total_power(self, rho = 1025, g = 9.80665):
        '''
        Calculates the total power following Eq.1 in Ahn et al, 2022
        Uses MHKit for group velocity and energy period
        
        Attributes:
        ----------------------------
        J:float: time x lat x lon: wave power (units)
        
    
        
        '''
        
        self.energy_period()
        k = wave_number(self.energy_period, self.depth)
        Cn = wave_celerity(k, self.depth, g=9.80665, depth_check=True, ratio=2)#check this ratio
        J = (rho * g)/16 * self.Hs**2 * Cn
        
        return J
        
        
        
        
        
    
        
    
    