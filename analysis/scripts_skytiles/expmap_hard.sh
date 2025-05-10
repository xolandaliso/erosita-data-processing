#!/bin/bash

echo "created dir for exposure maps"


inp_dir="data/indiv_TMs/hard_band"
out_dir="data/indiv_TMs/hard_band/exposure_maps"
GTIs="data/gti_files"
TMs=(1 2 5 6 7)  #telescope modules 

len=${#TMs[@]}

echo "exposure maps in 6 - 9 keV for all TMs"

for ((i = 0; i < len; i++)); do

        echo "creating vign corrected exposure map for TM${TMs[$i]}" 

        expmap inputdatasets="$inp_dir/tm${TMs[$i]}.fits" templateimage="$inp_dir/tm${TMs[$i]}.fits" mergedmaps="$out_dir/vign/tm${TMs[$i]}_vignetted.fits" gtitype=FLAREGTI emin=6 emax=9 withdetmaps=yes withvignetting=yes
        
        echo "creating non-vign corrected exposure map for TM${TMs[$i]}" 

        expmap inputdatasets="$inp_dir/tm${TMs[$i]}.fits" templateimage="$inp_dir/tm${TMs[$i]}.fits" mergedmaps="$out_dir/non_vign/tm${TMs[$i]}_nonvignetted.fits" gtitype=FLAREGTI emin=6 emax=9 withdetmaps=yes withvignetting=no
done

