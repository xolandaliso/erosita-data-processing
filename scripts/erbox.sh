#!/bin/bash
#source eSASS software

erbackmap image=data/science_imgs/TM0_science_image.fits \
              expimage=data/science_imgs/expmap_TM0_image.fits\
              boxlist=data/catalogs/catalog_TM0.fits \
              detmask=data/detmasks/TM0_detmask.fits \
              emin=200. \
              emax=2000 \
              bkgimage=data/backG_image.fits \
              cheesemask=data/cheese_mask.fits \
              scut=0.0001 \
              mlmin=6 \
              maxcut=0.5 \
              fitmethod=smooth \
              snr=30.  \
              smoothval=15.0 \
              cheesemask_flag='Y'
