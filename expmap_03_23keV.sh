#!/bin/bash
#source eSASS software


mkdir -p expmaps

echo "created dir for exposure maps"


inp_dir="filtered_ev"
out_dir="expmaps"
GTIs="gti_files"
TMs=(1 2 6)  #telescope modules 

len=${#TMs[@]}

echo "exposure maps in 0.2 - 2.3 keV for TMs 1 2 & 6"

for ((i = 0; i < len; i++)); do

        #creating vignetting maps 

        expmap inputdatasets="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                templateimage="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                mergedmaps="$out_dir/vignetted_TM${TMs[$i]}.fits"\
                gtitype=FLAREGTI \
                emin=0.3 emax=2. withdetmaps=yes withvignetting=yes

        #nonvegnetted maps
        expmap inputdatasets="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                templateimage="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                mergedmaps="$out_dir/nonvignetted_TM${TMs[$i]}.fits"\
                gtitype=FLAREGTI \
                emin=0.3 emax=2. withdetmaps=yes withvignetting=no

done

TMs=(5 7)  #telescope modules 

len=${#TMs[@]}

echo "exposure maps in 1.0 - 2.3 keV for TMs 5 & 7"

for ((i = 0; i < len; i++)); do

        #creating vignetting maps

        expmap inputdatasets="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                templateimage="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                mergedmaps="$out_dir/vignetted_TM${TMs[$i]}.fits"\
                gtitype=FLAREGTI \
                emin=1. emax=2. withdetmaps=yes withvignetting=yes

        #nonvignetted maps

        expmap inputdatasets="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                templateimage="$inp_dir/filtered_TM${TMs[$i]}.fits"\
                mergedmaps="$out_dir/nonvignetted_TM${TMs[$i]}.fits"\
                gtitype=FLAREGTI \
                emin=1. emax=2. withdetmaps=yes withvignetting=no
done