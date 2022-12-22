# -*- coding: utf-8 -*-

import numpy 
import pandas 
from mhkit.wave.resource import wave_number, wave_celerity
import time

class IECParams:
    
    def __init__(self, time_vec):

        self.time = time_vec
        self.total_hours = (self.time[-1] - self.time[0]).total_seconds()/3600

    def energy_period(self, tp, wind_sea_cutoff = 6):
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
        te = C_swell * tp
        windsea_mask = te<wind_sea_cutoff
        te[windsea_mask] = C_wind * te[windsea_mask] 
        
        return te


    def total_power(self, depth, hs, tp, rho = 1025, g = 9.80665):
        '''
        Calculates the total power following Eq.1 in Ahn et al, 2022
        Uses MHKit for group velocity and energy period
        
        Returns:
        ----------------------------
        J:float: 1 x (time x lat x lon): wave power (units)
        k:float: 1 x (time x lat x lon): wave number (units)
        
        >>> 32054.2 = total_power(5287.886, 2.37, 11.64)
        >>> 124245.41.2 = total_power(5572.521, 4.4, 13.09)
        
        '''
        
        te = self.energy_period(tp)
        
        frequency_e = 1/te

        k = wave_number(frequency_e, depth)

        Cn = wave_celerity(frequency_e, k, depth, g=9.80665, depth_check=True, ratio=2)#check this ratio

        J = (rho * g)/16 * hs**2 * Cn
        
        return k, Cn, J
           