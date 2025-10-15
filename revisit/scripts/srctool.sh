#!/bin/bash
# source /path/to/eSASS/setup.sh

echo "created directory for storing spectra"

inp_dir="../data/"
out_dir="../data/tm_spectra"

srctool eventfiles="$inp_dir/pm00_300003_020_EventList_c001.fits" \
        srccoord="fk5; 7:08:31.7000,-49:12:52.000, 911.695" \
        srcreg="fk5; mask $inp_dir/full_eband/catalog_cheesemask.fits" \
        backreg="$inp_dir/full_eband/background.reg" \
        prefix="$out_dir/masked_tm_" \
        suffix="cluster_clean.fits" \
        todo="SPEC ARF RMF" \
        insts="1 2 5 6 7" \
        gtitype="GTI" \
        lcemin=0.2 lcemax=9.0 \
        exttype="BETA" \
        extpars="60.0 5" \
        clobber="yes"
