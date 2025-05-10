#!/bin/bash

echo "created dir for exposure maps"


inp_dir="data/indiv_TMs/soft_band"
out_dir="data/indiv_TMs/soft_band/exposure_maps"
GTIs="data/gti_files"
TMs=(1 2 6)  #telescope modules 

len=${#TMs[@]}

echo "exposure maps in 0.2 - 2.3 keV for TMs 1 2 & 6"

for ((i = 0; i < len; i++)); do

        echo "creating vign corrected exposure map for TM${TMs[$i]}" 

        expmap inputdatasets="$inp_dir/tm${TMs[$i]}.fits" templateimage="$inp_dir/tm${TMs[$i]}.fits" mergedmaps="$out_dir/vign/tm${TMs[$i]}_vignetted.fits" gtitype=FLAREGTI emin=0.2 emax=2.3 withdetmaps=yes withvignetting=yes
        
        echo "creating non-vign corrected exposure map for TM${TMs[$i]}" 

        expmap inputdatasets="$inp_dir/tm${TMs[$i]}.fits" templateimage="$inp_dir/tm${TMs[$i]}.fits" mergedmaps="$out_dir/non_vign/tm${TMs[$i]}_nonvignetted.fits" gtitype=FLAREGTI emin=0.2 emax=2.3 withdetmaps=yes withvignetting=no
done

TMs=(5 7)  #telescope modules 

len=${#TMs[@]}

echo "exposure maps in 0.8 - 2.3 keV for TMs 5 & 7"

for ((i = 0; i < len; i++)); do

        #creating vignetting maps
        echo "creating vign corrected exposure map for TM${TMs[$i]}"

        expmap inputdatasets="$inp_dir/tm${TMs[$i]}.fits" templateimage="$inp_dir/tm${TMs[$i]}.fits" mergedmaps="$out_dir/vign/tm${TMs[$i]}_vignetted.fits" gtitype=FLAREGTI emin=0.8 emax=2.3 withdetmaps=yes withvignetting=yes

        echo "creating non-vign corrected exposure map for TM${TMs[$i]}"
        #nonvignetted maps
        
        expmap inputdatasets="$inp_dir/tm${TMs[$i]}.fits" templateimage="$inp_dir/tm${TMs[$i]}.fits" mergedmaps="$out_dir/non_vign/tm${TMs[$i]}_nonvignetted.fits" gtitype=FLAREGTI emin=0.8 emax=2.3 withdetmaps=yes withvignetting=no

done