 #!/bin/bash

inp_dir="data/full_eband/"
gti_dir="data/full_eband/gti_files"
curves_dir="data/full_eband/light_curves"
out_dir="data/full_eband/"
mask_dir="data/full_eband/masks"

 
 evtool eventfiles="$inp_dir/tm0_eventfile.fits" outfile="$out_dir/tm0_eventfile_cleaned.fits" flag=0xc00fff30 pattern=15 gti="FLAREGTI" emin=0.2 emax=10. image=yes size=1250 center_position=auto 