#! /bin/bash

inp_dir="data/skytiles/cleaned"

cleaned_suffix="_cleaned.fits"

# Set RA and DEC values
ra0=107.13208333333333
dec0=-49.214444444444446

# Loop through all cleaned FITS files
for cleaned_file in "${inp_dir}"/*"${cleaned_suffix}"; do
  echo "Running radec2xy on $(basename "$cleaned_file")..."
  
  radec2xy file="$cleaned_file" ra0="$ra0" dec0="$dec0"
  
done