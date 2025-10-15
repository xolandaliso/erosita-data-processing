#!/bin/bash

'''
    this script creates soft-band exposure maps (non-/vignetted)
'''

echo "creating exposure maps"

event_file='../data/full_eband/tm0_soft_band_8_23eV.fits'

out_dir="../data/full_eband/"

# non-vignetted

expmap inputdatasets="$event_file" templateimage="$event_file" mergedmaps="$out_dir/tm0_nonvignetted_expmap.fits" gtitype=GTI emin=0.8 emax=2.3 withdetmaps=yes withvignetting=no


# vignetted

expmap inputdatasets="$event_file" templateimage="$event_file" mergedmaps="$out_dir/tm0_vignetted_expmap.fits" gtitype=GTI emin=0.8 emax=2.3 withdetmaps=yes withvignetting=yes
