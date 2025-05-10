
#!/bin/bash

#script from grok edited
# i need to re-look this and understand it better

for tm in 1 2 6; do
    flaregti eventfile="data/indiv_TMs/soft_band/tm${tm}.fits" gtifile= "data/indiv_TMs/soft_band/tm${tm}_gti.fits" lightcurve="data/indiv_TMs/soft_band/tm${tm}_light_curve.fits" mask="data/indiv_TMs/soft_band/tm${tm}_mask.fits" threshold=1.03 timebin=100 pimin=200 pimax=2300

    evtool eventfiles="data/indiv_TMs/soft_band/tm${tm}.fits" outfile="data/indiv_TMs/soft_band/tm${tm}.fits" flag=0xc00fff30 pattern=15 gti="FLAREGTI" emin=0.2 emax=2.3 image=yes size=1250 center_position=auto

done


for tm in 5 7; do
    flaregti eventfile="data/indiv_TMs/soft_band/tm${tm}.fits" gtifile= "data/indiv_TMs/soft_band/tm${tm}_gti.fits" lightcurve="data/indiv_TMs/soft_band/tm${tm}_light_curve.fits" mask="data/indiv_TMs/soft_band/tm${tm}_mask.fits" threshold=1.03 timebin=100 pimin=800 pimax=2300
            
    evtool eventfiles="data/indiv_TMs/soft_band/tm${tm}.fits" outfile="data/indiv_TMs/soft_band/tm${tm}.fits" flag=0xc00fff30 pattern=15 gti="FLAREGTI" emin=0.8 emax=2.3 image=yes size=1250 center_position=auto

done
