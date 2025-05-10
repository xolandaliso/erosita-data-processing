#!/bin/bash
inp_dir="data/skytiles"
gti_dir="$inp_dir/gti_files"
curves_dir="$inp_dir/light_curves"
out_dir="$inp_dir/cleaned"
mask_dir="$inp_dir/masks"

"""
    -hard band light curve
"""

flaregti eventfile="$inp_dir/cleaned/tm0_skytiles_full_eband.fits" gtifile="$gti_dir/tm0_skytiles_gti.fits" lightcurve="$curves_dir/tm0_skytiles_light_curve.fits" mask="$mask_dir/tm0_skytiles_mask.fits" timebin=100 pimin=5000 pimax=10000  #10 keV