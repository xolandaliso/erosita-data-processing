#!/bin/bash

# merging 3 event files in the soft band 0.2 - 2.3 keV

evtool eventfiles="data/indiv_TMs/soft_band/tm1.fits data/indiv_TMs/soft_band/tm2.fits data/indiv_TMs/soft_band/tm6.fits"\
    outfile="data/indiv_TMs/soft_band/tm8.fits"\
    emin=0.2 emax=2.3 image=yes size=1250

# this script does NOT run see error below and check if you can fix it

"""
    evtool/write_tEventFile: Writing events.
    evtool/write_tEventFile: Writing events-extension extras.
    evtool/write_tBinTable: **STOP** Column TIME is not allocated.
    evtool: FAILED
 """