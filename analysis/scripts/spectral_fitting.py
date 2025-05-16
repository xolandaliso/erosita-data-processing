import xspec
from xspec import *

Plot.device = "/png"
Plot.xAxis="keV"
Plot.yLog=True
Plot.xLog=False

spectra_dir = '/idia/projects/lensed-hi/xola/xray/tm_spectra/'

spectra = xspec.Spectrum("{spectra_dir}+tm8_020_SourceSpec_00001circle_annul_src.fits")

model = Model("constant*(apec + TBabs*(apec + powerlaw) + TBabs*apec)")
'''
model looks like this:
========================================================================
Model constant<1>(apec<2> + TBabs<3>(apec<4> + powerlaw<5>) + TBabs<6>*apec<7>) Source No.: 1   Active/On
Model Model Component  Parameter  Unit     Value
 par  comp
   1    1   constant   factor              725.350      +/-  0.0          
   2    2   apec       kT         keV      1.00000      +/-  0.0          
   3    2   apec       Abundanc            1.00000      frozen
   4    2   apec       Redshift            0.0          frozen
   5    2   apec       norm                1.00000      +/-  0.0          
   6    3   TBabs      nH         10^22    1.00000      +/-  0.0          
   7    4   apec       kT         keV      1.00000      +/-  0.0          
   8    4   apec       Abundanc            1.00000      frozen
   9    4   apec       Redshift            0.0          frozen
  10    4   apec       norm                1.00000      +/-  0.0          
  11    5   powerlaw   PhoIndex            1.00000      +/-  0.0          
  12    5   powerlaw   norm                1.00000      +/-  0.0          
  13    6   TBabs      nH         10^22    1.00000      +/-  0.0          
  14    7   apec       kT         keV      1.00000      +/-  0.0          
  15    7   apec       Abundanc            1.00000      frozen
  16    7   apec       Redshift            0.0          frozen
  17    7   apec       norm                1.00000      +/-  0.0          
________________________________________________________________________

'''
# component 1 values

constant = model(1)
constant.values = 725.35 # area of the source region
constant.frozen = True

# apec paramters
apec1_kT, apec1_abund, apec1_z, apec1_norm = model(2), model(3), model(4), model(5)

apec1_kT.values = 0.1
apec1_kT.frozen = True
apec1_abund.values = 0.03
apec1_abund.frozen = False # let this vary
apec1_z.values = 0.0
apec1_z.frozen = True
apec1_norm.values = 1.0
apec1_norm.frozen = False # let this vary

# TBabs parameters
TBabs1_nH = model(6)
TBabs1_nH.values = 0.04 # 4e20 cm^-2 -- Milky Way's nH
TBabs1_nH.frozen = True

# apec2 parameters
apec2_kT, apec2_abund, apec2_z, apec2_norm = model(7), model(8), model(9), model(10)
apec2_kT.values = 0.25 # Koribalski et al. 2024
apec2_kT.frozen = True
apec2_abund.values = 0.03
apec2_abund.frozen = False # let this vary
apec2_z.values = 0.0
apec2_z.frozen = True
apec2_norm.values = 1.0
apec2_norm.frozen = False # let this vary

# powerlaw parameters
powerlaw_index, powerlaw_norm = model(11), model(12)
powerlaw_index.values = 1.4
powerlaw_index.frozen = False # let this vary
powerlaw_norm.values = 1.0
powerlaw_norm.frozen = False # let this vary

# TBabs2 parameters
TBabs2_nH = model(13)
TBabs2_nH.values = 0.0385 # 3.85e20 cm^-2 -- A3408 nH from HI4PI
TBabs2_nH.frozen = True

# apec3 parameters
apec3_kT, apec3_abund, apec3_z, apec3_norm = model(14), model(15), model(16), model(17)
apec3_kT.values = 0.25 # Koribalski et al. 2024
apec3_kT.frozen = False # let this vary
apec3_abund.values = 0.03
apec3_abund.frozen = False # let this vary
apec3_z.values = 0.0420
apec3_z.frozen = True
apec3_norm.values = 1.0
apec3_norm.frozen = False # let this vary

# set the fit statistic to Cstat
Fit.nIterations = 100
Fit.statMethod = "cstat"
Fit.statMethod = "chi"
Fit.perform()    # do the fit

Fit.show() # this will perhaps save the plot

Plot.add = True
Plot("data")
Plot("model")
Plot("data chisq")
Plot("data","model","resid")
Plot()
 
