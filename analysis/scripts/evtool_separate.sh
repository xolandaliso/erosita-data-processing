#!/bin/bash

echo "creating individual TMs for soft band"

inp_dir="data/full_eband"
out_dir="data/indiv_TMs/soft_band"
GTIs="data/indiv_TMs/gti_files"
TMs=(1 2 6)  #telescope modules 

len=${#TMs[@]}

echo " creating TMs at 0.2 - 2.3 keV for TMs 1 2 & 6 - softband images"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/tm0_eventfile_cleaned.fits" outfile="$out_dir/tm${TMs[$i]}.fits" telid=${TMs[$i]} flag=0xc00fff30 pattern=15 gti="GTI" emin=0.2 emax=2.3 image=yes size=1250 center_position=auto
done

TMs=(5 7)  # telescope modules 

len=${#TMs[@]}

echo "creating TMs at soft-band 0.8 - 2.3 keV for TMs 5 & 7"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/tm0_eventfile_cleaned.fits" outfile="$out_dir/tm${TMs[$i]}.fits" telid=${TMs[$i]} flag=0xc00fff30 pattern=15 gti="GTI" emin=0.8 emax=2.3 image=yes size=1250 center_position=auto 
done