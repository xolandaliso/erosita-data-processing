#!/bin/bash

echo "creating individual TMs for hard band for all TMs"

inp_dir="data/full_eband"
out_dir="data/indiv_TMs/hard_band"
GTIs="data/indiv_TMs/gti_files"
TMs=(1 2 5 6 7)  #telescope modules 

len=${#TMs[@]}

echo " creating TMs at 6 - 9 keV for TMs - hardband images"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/tm0_eventfile_cleaned.fits" outfile="$out_dir/tm${TMs[$i]}.fits" telid=${TMs[$i]} flag=0xc00fff30 pattern=15 gti="FLAREGTI" emin=6 emax=9 image=yes size=1250 center_position=auto
done
