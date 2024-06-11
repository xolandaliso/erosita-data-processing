#!/bin/bash
#source eSASS software

mkdir -p tm_spectra

echo "created dir for storing spectra"

inp_dir="full_eband"
out_dir="tm_spectra"

TMs=(1 2 5 6 7)  #telescope modules 

len=${#TMs[@]}

echo "spectra for all the TMs"

for ((i = 0; i < len; i++)); do

    srctool eventfiles="$inp_dir/reduced_TM${TMs[$i]}_evlist.fits"\
            srccoord="fk5; 7:08:31.4822, -49:14:29.115" \
            prefix="$out_dir/observations_TM${TMs[$i]}_"\
            suffix="circle_annul_src.fits" \
            todo="SPEC ARF RMF" \
            insts="${TMs[$i]}" \
            gtitype="FLAREGTI" \
            writeinsts="${TMs[$i]}"\
            lcemin=0.2 lcemax=10.0\
            srcreg="fk5; circle (7:08:31.4822, -49:14:29.115, 0.2272171d)"\
            backreg="fk5; annulus (7:08:30.4142, -49:14:50.003, 0.2645976d, 0.3142628d)" 
done