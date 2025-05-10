#!/bin/bash
#defining path for 
#and running python script

echo "cleaning and creating lightcurves"

mkdir -p data/full_eband && mkdir -p images/gti_files\
    && mkdir -p images/light_curves && mkdir -p images/masks

gti_dir="images/gti_files"
curves_dir="images/light_curves"
out_dir="images/soft_band"
mask_dir="images/masks"
inp_dir="data/full_eband"

event_file='data/pm00_300003_020_EventList_c001.fits'
TMs=(1 2 5 6 7)  # telescope modules 

len=${#TMs[@]}

for ((i = 0; i < len; i++)); do
    '''
     block comments f
    '''
     evtool eventfiles="$event_file"\
            outfile="$inp_dir/tm${TMs[$i]}.fits"\
            telid=${TMs[$i]} flag=0xc00fff30 pattern=15 gti="GTI" \
            region="fk5; circle(7:09:13.004, -49:23:02.832, 0.532)" \
            emin=0.2 emax=10.0 image=yes size=1250 center_position=auto   

    echo -e "\n first evtool done for TM${TMs[$i]} \n"

    '''
    block comments
    '''

    flaregti eventfile="$inp_dir/tm${TMs[$i]}.fits"\
        gtifile="$gti_dir/gti_tm${TMs[$i]}.fits" \
        lightcurve="$curves_dir/lightcurve_tm${TMs[$i]}.fits" \
        mask="$mask_dir/mask_tm${TMs[$i]}.fits" \
        timebin=100 pimin=5000 pimax=10000  #10 keV

    echo -e "\n first flaregti done for TM${TMs[$i]} \n"

    '''
    block comments
    '''

    flaregti eventfile="$inp_dir/tm${TMs[$i]}.fits"\
        gtifile="$gti_dir/gti_thresh_tm${TMs[$i]}.fits" \
        lightcurve="$curves_dir/lightcurve_thresh_tm${TMs[$i]}.fits" \
        mask="$mask_dir/mask_thresh_tm${TMs[$i]}.fits" \
        threshold=1.03 timebin=100 pimin=5000 pimax=10000 \
        gridsize=26 source_size=150

    echo -e "\n second flaregti done for TM${TMs[$i]} \n"


     '''
    block comments
    '''

    evtool  eventfiles="$inp_dir/tm${TMs[$i]}.fits"\
            outfile="$inp_dir/tm${TMs[$i]}.fits"\
            flag=0xc00fff30 pattern=15 gti="FLAREGTI" \
            region="fk5; circle(7:09:13.004, -49:23:02.832, 0.532)" \
            emin=0.2 emax=10.0 image=yes size=1250 center_position=auto 

    echo -e "\n second evtool done for TM${TMs[$i]} \n"

echo -e "\n all TMs processed for full energy band \n"

done


mkdir  -p data/filtered_ev

echo -e "\n created dir for filtered event files \n"


inp_dir="data/full_eband"
out_dir="images/soft_band"
TMs=(1 2 6)  #telescope modules 

len=${#TMs[@]}

echo -e "\n applying GTIs in 0.2 - 2.3 keV for TMs 1 2 & 6 - softband images \n"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/tm${TMs[$i]}.fits"\
                outfile="$out_dir/tm${TMs[$i]}_cleaned.fits"\
                telid=${TMs[$i]} flag=0xc00fff30 pattern=15 gti="FLAREGTI" \
                emin=0.2 emax=2.3 image=yes size=1250 center_position=auto
done

TMs=(5 7)  # telescope modules 

len=${#TMs[@]}

echo -e "\n applying GTIs in the 1.0 - 2.3 keV for TMs 5 & 7 with flares - hard band images \n"

for ((i = 0; i < len; i++)); do
        evtool eventfiles="$inp_dir/tm${TMs[$i]}.fits"\
                outfile="$out_dir/tm${TMs[$i]}_cleaned.fits"\
                telid=${TMs[$i]} flag=0xc00fff30 pattern=15 gti="FLAREGTI" \
                emin=0.8 emax=2.3 image=yes size=1250 center_position=auto 
done