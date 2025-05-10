#!/bin/bash
inp_dir="data/full_eband/"
gti_dir="data/full_eband/gti_files"
curves_dir="data/full_eband/light_curves"
out_dir="data/full_eband/"
mask_dir="data/full_eband/masks"

"""
    -hard band light curve
"""

flaregti eventfile="$inp_dir/tm0_eventfile.fits" gtifile="$gti_dir/tm0_gti.fits" lightcurve="$curves_dir/tm0_light_curve.fits" mask="$mask_dir/tm0_mask.fits" timebin=100 pimin=5000 pimax=10000  #10 keV