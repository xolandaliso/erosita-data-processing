#!/bin/bash

#!/bin/bash

'''
    this script creates a cleaned event file in the soft band (0.8 - 2.3 keV)
'''

echo "cleaning and creating lightcurves"

event_file='../data/full_eband/tm0_eventfile.fits'

out_dir="../data/full_eband/"


'''
block comments 
'''
evtool eventfiles="$event_file" outfile="$out_dir/tm0_soft_band_8_23eV.fits" telid="1 2 5 6 7" flag=0xc00fff30 pattern=15 gti="GTI" emin=0.8 emax=2.3 image=yes size=1250 center_position=auto
