#!/bin/bash

inp_dir="data/full_eband"

ermask expimage="$inp_dir/tm0_vign_exposure_map.fits" detmask="$inp_dir/tm0_detmask_backup.fits"

erbox images="$inp_dir/tm0_wavelet_filtered.fits" boxlist="$inp_dir/tm0_boxlist_local_backup.fits" emin=200 emax=2300 \
	 expimages="$inp_dir/tm0_vign_exposure_map.fits" detmasks="$inp_dir/tm0_detmask_backup.fits" bkgima_flag=N ecf=1

erbackmap image="$inp_dir/tm0_sband_eventfile_cleaned.fits" expimage="$inp_dir/tm0_vign_exposure_map.fits" \
	     boxlist="$inp_dir/backup.cat" detmask="$inp_dir/tm0_detmask_backup.fits" bkgimage="$inp_dir/tm0_background_backup.fits" emin=200 \
	     emax=2300 cheesemask="$inp_dir/tm0_cheesemask_backup.fits" scut=0.03 mlmin=3 maxcut=0.09 fitmethod=smooth snr=20 smoothval=15.0

erbox images="$inp_dir/tm0_sband_eventfile_cleaned.fits" boxlist="$inp_dir/backup.cat" expimages="$inp_dir/tm0_vign_exposure_map.fits" \
         detmasks="$inp_dir/tm0_detmask_backup.fits" bkgimages="$inp_dir/tm0_background_backup.fits" emin=200 emax=2300 ecf=1