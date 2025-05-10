#!/bin/bash

inp_dir="data/skytile_data"
gti_dir="$inp_dir/gti_files"
curves_dir="$inp_dir/light_curves"
out_dir="$inp_dir/cleaned"
mask_dir="$inp_dir/masks"


for infile in "${inp_dir}"/em01_*_020_EventList_c010.fits; do
  # extract just the base name of the file (no directory)
  filename=$(basename "$infile")
  # define output file name
  outfile="${out_dir}/${filename%.fits}_cleaned.fits"

  echo "Processing $filename..."

  evtool eventfiles="$infile" \
         outfile="$outfile" \
         flag=0xc00fff30 \
         pattern=15 \
         gti="FLAREGTI" \
         emin=0.2 \
         emax=10.0 \
         image=yes \
         size=1250 \
         center_position=auto
done