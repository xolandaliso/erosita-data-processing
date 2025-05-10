#!/bin/bash

# dir structure
inp_dir="data/skytile_data/full_eband"
gti_dir="$inp_dir/gti_files"
curves_dir="$inp_dir/light_curves"
out_dir="$inp_dir"
mask_dir="$inp_dir/masks"

# create directories if they don't exist
mkdir -p "$gti_dir" "$curves_dir" "$out_dir" "$mask_dir"

# logging function
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# declare associative array for threshold mappings
declare -A thresholds
thresholds=(
    ["102138"]="1.2448730055398027"
    ["104141"]="1.2438511876568623"
    ["106135"]="1.2344046657096568"
    ["106138"]="1.2429232583379708"
    ["108141"]="1.2438354511705738"
    ["110135"]="1.317289102404949"
    ["111138"]="1.2558096423711835"
    ["113141"]="1.2494132089315557"
)

# process each file in the input directory
for infile in "${inp_dir}"/em01_*_020_EventList_c010_full_band.fits; do
    # check if file exists (in case the glob doesn't match any files)
    [ -e "$infile" ] || { log_message "No matching files found"; exit 1; }
  
    # extract just the base name of the file (no directory)
    filename=$(basename "$infile")
    
    # Extract the observation identifier (the numeric part)
    obs_id=$(echo "$filename" | grep -o "em01_[0-9]*" | sed 's/em01_//')
    
    # check if obs_id has a corresponding threshold
    if [ -z "${thresholds[$obs_id]}" ]; then
        log_message "Error: No threshold defined for obs_id $obs_id ($filename). Skipping..."
        continue
    fi
    
    threshold="${thresholds[$obs_id]}"
    log_message "Processing $filename (Observation ID: $obs_id) with threshold $threshold..."
    
    # define output file names using the specific filename (no wildcards)
    cleaned_file="$infile"
    gti_file="${gti_dir}/gti_${filename}"
    lightcurve_file="${curves_dir}/light_curve_${filename}"
    mask_file="${mask_dir}/mask_${filename}"
        
    log_message "Running flare detection in hard band (5-10 keV)..."
    flaregti eventfile="$cleaned_file" \
             gtifile="$gti_file" \
             lightcurve="$lightcurve_file" \
             mask="$mask_file" \
             pimin=5000 \
             pimax=10000 \
             threshold="$threshold" \
             gridsize=26 \
             source_size=150

    
    if [ $? -eq 0 ]; then
        log_message "Flare detection completed successfully for $filename"
    else
        log_message "Error: Flare detection failed for $filename"
    fi
    
    echo "------------------------------------------------------"
done

log_message "All files processed"