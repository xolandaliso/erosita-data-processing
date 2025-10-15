#/bin/bash

#!/bin/bash

'''
    this script attempts to apply manual GTI filters
    based on visual inspection of the hard-band light curve
'''

echo "cleaning and creating lightcurves"

event_file='../data/pm00_300003_020_EventList_c001.fits'

mkdir -p ../data/full_eband && mkdir -p ../data/full_eband/gti_files\
    && mkdir -p ../data/full_eband/light_curves && mkdir -p ../data/full_eband/masks

gti_dir="../data/full_eband/gti_files"
curves_dir="../data/full_eband/light_curves"
out_dir="../data/full_eband/"
mask_dir="../data/full_eband/masks"

'''
block comments 
'''
evtool eventfiles="$event_file" outfile="$out_dir/tm0_eventfile.fits" telid="1 2 5 6 7" flag=0xc00fff30 pattern=15 gti="../custom_flaregti.fits" emin=0.2 emax=10 image=yes size=1250 center_position=auto  
