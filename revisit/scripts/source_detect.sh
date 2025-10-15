#!/bin/bash

inp_dir="../data/full_eband"

ermask expimage="$inp_dir/tm0_vignetted_expmap.fits" detmask="$inp_dir/tm0_detmask.fits"

erbox images="$inp_dir/tm0_soft_band_8_23eV.fits" boxlist="$inp_dir/tm0_boxlist.fits" emin=800 emax=2300 \
	 expimages="$inp_dir/tm0_vignetted_expmap.fits" detmasks="$inp_dir/tm0_detmask.fits" bkgima_flag=N ecf=1

erbackmap image="$inp_dir/tm0_soft_band_8_23eV_wcs_corrected.fits" expimage="$inp_dir/tm0_vignetted_expmap.fits" \
	     boxlist="$inp_dir/tm0_boxlist.fits" detmask="$inp_dir/tm0_detmask.fits" bkgimage="$inp_dir/tm0_background.fits" emin=800 \
	     emax=2300 cheesemask="$inp_dir/tm0_cheesemask.fits" scut=0.03 mlmin=3 maxcut=0.09 fitmethod=smooth snr=20 smoothval=15.0

erbox images="$inp_dir/tm0_soft_band_8_23eV_wcs_corrected.fits" boxlist="$inp_dir/tm0_boxlist.fits" expimages="$inp_dir/tm0_vignetted_expmap.fits" \
         detmasks="$inp_dir/tm0_detmask.fits" bkgimages="$inp_dir/tm0_background.fits" emin=800 emax=2300 ecf=1