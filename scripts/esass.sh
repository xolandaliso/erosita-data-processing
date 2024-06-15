#!/bin/bash
#source eSASS software


mkdir  -p filtered_ev

echo "created dir for filtered event files"


inp_dir="full_eband"
out_dir="filtered_ev"
GTIs="gti_files"
TMs=(1 2 6)  #telescope modules 

len=${#TMs[@]}

echo "applying GTIs in 0.2 - 2.3 keV for TMs 1 2 & 6 - softband images"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/reduced_TM${TMs[$i]}.fits"\
                outfile="$out_dir/filtered_TM${TMs[$i]}_03_20keV_flaregti.fits"\
                flag=0xc00fff30\
                gti="FLAREGTI"\
                pattern=15\
                image=yes\
                emin=.3 emax=2.\
                size=1250\                #size of the image
                center_position=625\      #center the image at x, y = 625
                telid=${TMs[$i]}
done

TMs=(5 7)  #telescope modules 

len=${#TMs[@]}

echo "applying GTIs in the 1.0 - 2.3 keV for TMs 5 & 7 with flares - hard band images"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/reduced_TM${TMs[$i]}.fits"\
                outfile="$out_dir/filtered_TM${TMs[$i]}_1_20keV_flaregti.fits"\
                flag=0xc00fff30\
                gti="FLAREGTI"\
                pattern=15\
                image=yes\
                emin=1. emax=2.\
                size=1250\                #size of the image
                center_position=625\      #center the image at x, y = 625
                telid=${TMs[$i]}
done





