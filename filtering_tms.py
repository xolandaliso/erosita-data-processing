import os, os.path, time, subprocess
import sys
from datetime import datetime
import distutils.spawn

mask_dir="masks/"
gti_dir="gti_files/"
curves_dir="light_curves/"
out_dir="full_eband/"
event_file='/home/idies/erdata/pm00_300003_020_EventList_c001.fits'

do_evtool, do_flaregti = True, True

TMs=[1, 2, 5, 6, 7]  #telescope modules 

for i in TMs:

    cmd=["evtool",
            "eventfiles=%s" %(event_file),
            "outfile=%s" %(out_dir+"reduced_TM"+str(i)+'_evlist.fits'),
            "emin=0.2", #
            "emax=10",
            "telid=%i" %(i),
            "image=yes",
            "rebin=80",
            "size=1250",
            "center_position=625",
            "pattern=15",
            "flag=0xc00fff30"
        ]

    # run the command

    if(do_evtool==True):
        subprocess.check_call(cmd)

    #---lightcurves at high energy band

    cmd = ["flaregti",
                "eventfile=%s" %(out_dir + "reduced_TM" + str(i) + "_evlist.fits"),
                "gtifile=%s" %(gti_dir + "gti_6_10_keV_TM" + str(i) + ".fits"),
                "lightcurve=%s" %(curves_dir + "lightcurve_6_10_keV_TM" + str(i) + ".fits"),
                "mask=%s" %(mask_dir + "lightcurve_6_10_keV_TM" + str(i) + ".fits"),
                "timebin=100",
                "pimin=6000",           
                "pimax=10000" 
            ]
    if(do_flaregti==True):
        subprocess.check_call(cmd)