#!/bin/bash
#source eSASS software

mkdir -p data/spectra

echo "created dir for storing spectra"

inp_dir="data/"
out_dir="data/tm_spectra"

srctool eventfiles="$inp_dir/pm00_300003_020_EventList_c001.fits"\
        srccoord="fk5; 7:08:31.7000, -49:12:52.000" \
        prefix="$out_dir/tm8_" \
        suffix="circle_annul_src.fits" \
        todo="SPEC ARF RMF" \
        insts="1 2 6" \
        gtitype="FLAREGTI" \
        lcemin=0.2 lcemax=9 \
        srcreg='fk5; circle (7:08:31.7000, -49:12:52.000, 911.695")' \
        backreg='fk5; annulus (7:10:35.6973, -49:42:37.436, 204.545", 314.953")'
