#!/bin/bash
inp_dir="data/full_eband/"
gti_dir="data/full_eband/gti_files"
curves_dir="data/full_eband/light_curves"
out_dir="data/full_eband/"
mask_dir="data/full_eband/masks"

"""
    -hard band light curve
"""

flaregti eventfile="$inp_dir/tm0_eventfile.fits" gtifile="$gti_dir/tm0_filtered_gti.fits" lightcurve="$curves_dir/tm0_filtered_light_curve.fits" mask="$mask_dir/tm0_filtered_mask.fits" threshold=1.03 pimin=5000 pimax=10000 gridsize=26 source_size=150  #10 keV  
# 10 keV
# threshold is set to mean + 3 sigma - script breaks if set to 3 sigma
