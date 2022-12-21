#!/usr/bin/python
#
# WAVEWATCH3 30-Year Hindcast IEC Wave Resource Parameter Calculations
# 
#
# Project: C3440
#
# Revision Log
# -----------------------------------------------------------------------------
# 11/22/2021 Chris Flanary - created script


import numpy as np
import math 


#%% Compute Wave Energy Period for each partition
# Ahn et al. 2022 Section 3.1 PDF p. 3

if Tp_n < 6.0:
    C = 0.86 # Wind sea
    Te_n = C * Tp_n # Wave energy period (s)
    
elif Tp_n >= 6.0:
    C = 1.0  # Swell
    Te_n = C * Tp_n # Wave energy period (s)



#%% Compute Wave Power for each partition

# Setup constants
rho = 1025 # Water density (kg/m3)
g = 9.81 # Gravity (m/s2)

# Partitioned group velocity
# Ahn et al. 2019 eqs. 3 PDF p. 6
k_n = 2*np.pi/L_n  # Wave number #replace this k with solving the dispersion relationship
Cg_n = (2*np.pi/k_n)*(1 + (2*k_n*depth/math.sinh(2*k_n*depth)))*1/Te_n # Wave group velocity (m/s)

# Partitioned wave power
# Ahn et al. 2022 eq. 1 PDF p. 3
J_n = (rho*g/16) * Hs_n**2 * Cg_n  # Wave power (kW/m [kilowatts per unit wave crest length])



# Frequency-Directionally resolved wave power
# Ahn et al. 2022 eq. 2 PDF p. 3

# T = # of hours in averaging period
J_Tb_thetab = sum(J_n)/T



# Omni-directional wave power or total wave power 
# Ahn et al. 2022 eq. 3 PDF p. 4
J = sum(J_Tb_thetab) # (kW/m [kilowatts per unit wave crest length])



#%% Compute Maximum Energy Direction
# IEC 101 Wave Resource Characterization Section 9.2.6.2, PDF p. 35

# theta_max = direction corresponding to the maximum wave power



#%% Compute Directionality Coefficient
# IEC 101 Wave Resource Characterization Section 9.2.6.3, eq. 18, PDF p. 35

# J_max = max time averaged wave power propagating in a single direction
# J = omni-direction wave power (kW/m)

d = J_max/J



#%% Compute Spectral Width
# IEC 101 Wave Resource Characterization Section 9.2.5, eq. 16, PDF p. 34

# eps0 = standard deviation of the period variance density, normalized by the energy perid


