
#!/bin/bash

echo "cleaning and creating lightcurves"

event_file='/home/idies/erdata/pm00_300003_020_EventList_c001.fits'

mkdir -p full_eband && mkdir -p gti_files\
    && mkdir -p light_curves && mkdir -p masks

gti_dir="gti_files/"
curves_dir="light_curves"
out_dir="full_eband/"
mask_dir="masks"

TMs=(1 2 5 6 7)  #telescope modules 
thresh=(0.3 0.23 0.33 0.25 0.31)  #3sigma thresholds for flares 

len=${#TMs[@]}

for ((i = 0; i < len; i++)); do
    '''
    block comments 
    '''
    evtool eventfiles="$event_file" \
            outfile="$out_dir/reduced_TM${TMs[$i]}.fits" \
            telid=${TMs[$i]} \
            flag=0xc00fff30 \
            pattern=15 \
            gti="GTI" \
            region="fk5; circle(7:09:13.004, -49:23:02.832, 0.532)" \
            emin=0.2 \
            emax=10. \
            image=yes \
            size=1250 \
            center_position=auto   
done


////


              
    '''
    block comments
    '''
    flaregti eventfile="$out_dir/reduced_TM${TMs[$i]}.fits" \
              gtifile="$gti_dir/gti_6_10_keV_TM${TMs[$i]}.fits" \
              lightcurve="$curves_dir/lightcurve_6_10keV_TM${TMs[$i]}.fits" \
              mask="$mask_dir/mask_6_9keV_TM${TMs[$i]}.fits" \
              threshold="${thresh[$i]}" \
              timebin=100 \
              pimin=6000 \
              pimax=10000 \
              gridsize=26 \
              source_size=150

    '''
    block comments
    '''
    evtool eventfiles="$out_dir/reduced_TM${TMs[$i]}.fits" \
            outfile="$out_dir/reduced_TM${TMs[$i]}.fits" \
            flag=0xc00fff30 \
            pattern=15 \
            gti="FLAREGTI" \
            region="fk5; circle(7:09:13.004, -49:23:02.832, 0.532)" \
            emin=0.2 emax=10. \
            image=yes \
            size=1250 \
            center_position=auto 
        
done


mkdir  -p filtered_ev

echo "created dir for filtered event files"


inp_dir="full_eband"
out_dir="filtered_ev"
GTIs="gti_files"
TMs=(1 2 6)  #telescope modules 

len=${#TMs[@]}

echo "applying GTIs in 0.2 - 2.3 keV for TMs 1 2 & 6 - softband images"

for ((i = 0; i < len; i++)); do
    '''
    block comments 
    '''
    evtool eventfiles="$inp_dir/reduced_TM${TMs[$i]}.fits" \
            outfile="$out_dir/filtered_TM${TMs[$i]}.fits" \
            telid=${TMs[$i]} \
            flag=0xc00fff30 \
            pattern=15 \
            gti="FLAREGTI" \
            emin=0.3 emax=2. \
            image=yes \
            size=1250 \
            center_position=auto
done

TMs=(5 7)  #telescope modules 

len=${#TMs[@]}

echo "applying GTIs in the 1.0 - 2.3 keV for TMs 5 & 7 with flares - hard band images"

for ((i = 0; i < len; i++)); do
    '''
    block comments 
    '''
    evtool eventfiles="$inp_dir/reduced_TM${TMs[$i]}.fits" \
            outfile="$out_dir/filtered_TM${TMs[$i]}.fits" \
            telid=${TMs[$i]} \
            flag=0xc00fff30 \
            pattern=15 \
            gti="FLAREGTI" \
            emin=1. emax=2. \
            image=yes \
            size=1250 \
            center_position=auto 
done