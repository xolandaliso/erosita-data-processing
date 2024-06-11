#!/usr/bin/python3
#
# Copyright (C) 2019-2021:
#   C. Grossberger, A Gueguen, M. Ramos Ceja
#   Max Planck Institute for Extraterrestrial Physics
#This file is part of eRosita's Science Analysis Software System (eSASS) 
#It is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License as
#published by the Free Software Foundation; either version 2 of the
#License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this library; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
#USA.
############
# This program run a set of tests on the input file ,
# each test consist of the execution of an eSASS task on theinput fole or the ouput file of the previous task 
# the initial goal is to check eSASS is correctly installed but it is also used to validate, in this version of the script,
# the data  of the EDR 
# Authors: C.Grossberger, A.Gueguen, M.Ramos (MPE)
############

import os, os.path, time, subprocess
import sys
from datetime import datetime
import distutils.spawn
infile=""
subdir="./"
prefix=""
suffix=".fits.gz" 
srctool_suffix="" # srctool does add .fits internally
template_evtool="EventList"
template_srcmap="SrcMap"
template_apesensmap="ApeSensMap"
template_psfmap="PSFMap"
template_expmap="ExposureMap"
template_detmask="DetMask"
template_boxlist_l="BoxDetSourceListL"
template_cheesemask="CheeseMask"
template_bkgimage="BackgrImage"
template_boxlist_m="BoxDetSourceListM"
template_mllist="MaxLikSourceList"
template_catprep="SourceCatalog"
template_ersensmap="ErSensMap"
template_areatable="AreaTable"
template_srctool="SrcTool"
srctool_dir="srctool_products/"
extended_fname_srctool="[ID_SRC < 5]"


# run evtool for energy bands and gti
#emin_ev=[200, 600, 2300]
#emax_ev=[600, 2300, 5000]
#emin_kev=[0.2, 0.6, 2.3]
#emax_kev=[0.6, 2.3, 5.0]
#eband=["1", "2", "3"]
#ccd=[1, 2, 3, 4, 5, 6, 7]
emin_ev=[200, 500, 1000, 2200]
emax_ev=[500, 1000, 2200, 10000]
emin_kev=[0.2, 0.5, 1.0, 2.2]
emax_kev=[0.5, 1.0, 2.2, 10.0]
eband=["1", "2", "3", "4"]
ccd=[1, 2, 3, 4, 5, 6, 7]

#ccd=[1]
# select the energy bands index
# start with 0
#eband_selected=[0, 1, 2]
eband_selected=[0, 1, 2, 3]
do_evtool=True
do_expmap=True
do_ermask=True
do_erbox_local=True
do_erbackmap=True
do_erbox_m=True
do_ermldet=True
do_catprep=True
do_srctool=True
do_apetool=True
do_ersensmap=True

enable_photon_mode=True

expmaps=[]
expmap_all=[]
infile_expmap=[]
emin=[]
emax=[]
emin_ev_str=[]
emax_ev_str=[]
outfile_evtool=[]
cheesemask=[]
bkgimage=[]
srcmaps=[]
psfmaps=[]
apesensmap=[]
eindex=[]
def RunTasks():
    for ii in range(len(eband_selected)):
      index=eband_selected[ii]
      outfile_evtool.append("%s_02%s%s" %(os.path.join(subdir,template_evtool), eband[index], suffix))
      srcmaps.append("%s_02%s%s" %(os.path.join(subdir,template_srcmap), eband[index], suffix))
      psfmaps.append("%s_02%s%s" %(os.path.join(subdir,template_psfmap), eband[index], suffix))
      apesensmap.append("%s_02%s%s" %(os.path.join(subdir,template_apesensmap), eband[index], suffix))
      eindex.append("%i" % (ii+1))
      cmd=["evtool",
          "eventfiles=%s" %(infile),
          "outfile=%s" %(outfile_evtool[ii]),
          "emin=%f" %(emin_kev[index]),
          "emax=%f" %(emax_kev[index]),
          "image=yes",
          "rebin=80",
          "size=3240",
          "pattern=15"
          ]
      # run the command
      if(do_evtool==True):
        subprocess.check_call(cmd)
        
      infile_expmap.append(outfile_evtool[ii])
      expmap_all.append("%s_02%s%s" %(os.path.join(subdir,template_expmap), eband[index], suffix))
      emin.append("%f" %(emin_kev[index]))
      emax.append("%f" %(emax_kev[index]))
      emin_ev_str.append("%ld" %(emin_ev[index]))
      emax_ev_str.append("%ld" %(emax_ev[index]))
    
    if(do_expmap==True):
      cmd=["expmap",
           "inputdatasets=%s"  %(infile),
           "emin=%s" %((" ").join(emin)),
           "emax=%s" %((" ").join(emax)),
           "templateimage=%s" %(infile_expmap[0]),
           "withvignetting=yes",
           "withmergedmaps=yes",
           "withdetmaps=yes",
           "withfilebadpix=no",
           #"withcalbadpix=no",
           "mergedmaps=%s" %((" ").join(expmap_all))
           ]
      print(cmd)
      subprocess.check_call(cmd)
    
    # ------------------------------------------------------------------------------
    
    detmask="%s%s" %(os.path.join(subdir,template_detmask), suffix)
    cmd=["ermask",
         "expimage=%s" %(expmap_all[0]),
         "detmask=%s" %(detmask),
         "threshold1=0.2",
         "threshold2=1.0",
         "regionfile_flag=no"
         ]
    if(do_ermask==True):
      if(os.path.isfile(detmask)==True):
        os.remove(detmask)
      print(cmd)
      subprocess.check_call(cmd)
    
    boxlist_l="%s%s" %(os.path.join(subdir,template_boxlist_l), suffix)
    
    cmd=["erbox",
        "images=%s" %((" ").join(outfile_evtool)),
        "boxlist=%s" %(boxlist_l),
        "expimages=%s" %((" ").join(expmap_all)),
        "detmasks=%s" %(detmask),
        "emin=%s" %((" ").join(emin_ev_str)),
        "emax=%s" %((" ").join(emax_ev_str)),
        "hrdef=",
        "ecf=1.0 1.0 1.0 1.0",  #"ecf=1.0 1.0 1.0",
        "nruns=3",
        "likemin=6.0",
        "boxsize=4",
        "compress_flag=N",
        "bkgima_flag=N",
        "expima_flag=Y",
        "detmask_flag=Y"
        ]
    
    if(do_erbox_local==True):
      if(os.path.isfile(boxlist_l)==True):
        os.remove(boxlist_l)
      print(cmd)
      subprocess.check_call(cmd)
    
    #------------------------------------------------------------------
    
    for ii in range(len(eband_selected)):
      index=eband_selected[ii]
      cheesemask.append("%s_02%s%s" %(os.path.join(subdir,template_cheesemask), eband[index], suffix))
      bkgimage.append("%s_02%s%s" %(os.path.join(subdir,template_bkgimage), eband[index], suffix))
      # one command per energy band
      cmd=["erbackmap",
          "image=%s" %(outfile_evtool[ii]),
          "expimage=%s" %(expmap_all[ii]),
          "boxlist=%s" %(boxlist_l),
          "detmask=%s" %(detmask),
          "cheesemask=%s" %(cheesemask[ii]),
          "bkgimage=%s" %(bkgimage[ii]),
          "idband=%s" %(eband_selected[ii]),
          "scut=0.0001",
          "mlmin=0.0",
          "maxcut=0.5",
          "fitmethod=smooth",
          "degree=2",
          "smoothflag=yes",
          "smoothval=15.",
          "snr=40.0",
          "excesssigma=1000.",
          "nfitrun=1",
          "cheesemask_flag=N"
          ]
      if(do_erbackmap==True):
        if(os.path.isfile(cheesemask[ii])==True):
          os.remove(cheesemask[ii])
        if(os.path.isfile(bkgimage[ii])==True):
          os.remove(bkgimage[ii])
        print(cmd)
        subprocess.check_call(cmd)
    
    # --------------------------------------------------------------------------
    
    # erbox m mode
    
    boxlist_m="%s%s" %(os.path.join(subdir,template_boxlist_m), suffix)
    cmd=["erbox",
        "images=%s" %((" ").join(outfile_evtool)),
        "boxlist=%s" %(boxlist_m),
        "expimages=%s" %((" ").join(expmap_all)),
        "detmasks=%s" %(detmask),
        "bkgimages=%s" %((" ").join(bkgimage)),
        "emin=%s" %((" ").join(emin_ev_str)),
        "emax=%s" %((" ").join(emax_ev_str)),
        "hrdef=1 2 3 4",
        "ecf=1.0 1.0 1.0 1.0",
        #"hrdef=1 2 3",
        #"ecf=1.0 1.0 1.0",
        "nruns=3",
        "likemin=4.",
        "boxsize=4",
        "compress_flag=N",
        "bkgima_flag=Y",
        "expima_flag=Y",
        "detmask_flag=Y"
        ]
    if(do_erbox_m==True):
      if(os.path.isfile(boxlist_m)==True):
        os.remove(boxlist_m)
      print(cmd)
      subprocess.check_call(cmd)
    
    # ----------------------------------------------------------------------------
    # proceed with ermldet
    
    mllist="%s%s" %(os.path.join(subdir,template_mllist), suffix)
    cmd=["ermldet",
        "mllist=%s" %(mllist),
        "boxlist=%s" %(boxlist_m),
        "images=%s" %((" ").join(outfile_evtool)),
        "expimages=%s" %((" ").join(expmap_all)),
        "detmasks=%s" %(detmask),
        "bkgimages=%s" %((" ").join(bkgimage)),
        "emin=%s" %((" ").join(emin_ev_str)),
        "emax=%s" %((" ").join(emax_ev_str)),
        "hrdef=1 2 3 4",
        "ecf=1.0 1.0 1.0 1.0",        
        #"hrdef=1 2 3",
        #"ecf=1.0 1.0 1.0",
        "likemin=5.",
        "extlikemin=3.",
        "compress_flag=N",
        "cutrad=15.",
        "multrad=15.",
        "extmin=1.5",
        "extmax=30.0",
        "expima_flag=Y",
        "detmask_flag=Y",
        "extentmodel=beta",
        "thres_flag=N",
        "thres_col=like",
        "thres_val=30.",
        "nmaxfit=3",
        "nmulsou=2",
        "fitext_flag=yes",
        "srcima_flag=yes",
        "srcimages=%s" %((" ").join(srcmaps)),
        "shapelet_flag=yes",
        "photon_flag=no"
        ]
    
    if(enable_photon_mode==True):
    	cmd=["ermldet",
        "mllist=%s" %(mllist),
        "boxlist=%s" %(boxlist_m),
        "images=%s" %((" ").join(outfile_evtool)),
        "expimages=%s" %((" ").join(expmap_all)),
        "detmasks=%s" %(detmask),
        "bkgimages=%s" %((" ").join(bkgimage)),
        "emin=%s" %((" ").join(emin_ev_str)),
        "emax=%s" %((" ").join(emax_ev_str)),
        "hrdef=1",
        "ecf=1.0",
        #"hrdef=1 2 3",
        #"ecf=1.0 1.0 1.0",
        "likemin=5.",
        "extlikemin=3.",
        "compress_flag=N",
        "cutrad=15.",
        "multrad=15.",
        "extmin=1.5",
        "extmax=30.0",
        "expima_flag=Y",
        "detmask_flag=Y",
        "extentmodel=beta",
        "thres_flag=N",
        "thres_col=like",
        "thres_val=30.",
        "nmaxfit=3",
        "nmulsou=2",
        "fitext_flag=yes",
        "srcima_flag=yes",
        "srcimages=%s" %((" ").join(srcmaps)),
        "shapelet_flag=yes",
        "photon_flag=yes"
        ]
    
    if(do_ermldet==True):
      if(os.path.isfile(mllist)==True):
        os.remove(mllist)
      for ii in range(len(srcmaps)):
        if(os.path.isfile(srcmaps[ii])==True):
          os.remove(srcmaps[ii])
      print(cmd)
      subprocess.check_call(cmd)
    
    
    # -------------------------------------------------------------------------
    #catprep="%s" %(os.path.join(subdir,outfile +"_catprep" +  suffix))
    catprep="%s%s" %(os.path.join(subdir, template_catprep), suffix)
    cmd=["catprep",
         "infile=%s" %(mllist),
         "outfile=%s" %(catprep)
        ]
    if(do_catprep==True):
        if(os.path.isfile(catprep)==True):
            os.remove(catprep)
        print(cmd)
        subprocess.check_call(cmd)
    
    # ----------------------------------------------------------------
    
    cmd=['srctool',
         'eventfiles=%s' %(infile),
         'prefix=%s' %(os.path.join(subdir,srctool_dir,template_srctool)),
         'suffix=%s' %(srctool_suffix),
         'srccoord=%s%s' %(catprep, extended_fname_srctool),
         'srcreg=fk5;circle * * 60"',
         'backreg=fk5;annulus * * 90" 120"',
         "clobber=yes"
         ]
    
    if(do_srctool==True):
        if(os.path.isdir(os.path.join(subdir, srctool_dir))==True):
          os.mkdir(os.path.join(subdir, srctool_dir))  
        print(cmd)
        subprocess.check_call(cmd)
    
    cmd=["apetool",
         #"mllist=%s" %(mllist),
         #"apelist="",
         "mllist=%s" %(mllist),
         "apelist=%s" %(mllist),
         "apelistout=%s" %(mllist),
         "images=%s" %((" ").join(outfile_evtool)),
         "psfmaps=%s" %((" ").join(psfmaps)),
         "apesenseimages=%s" %((" ").join(apesensmap)),
         "expimages=%s" %((" ").join(expmap_all)),
         "detmasks=%s" %(detmask),
         "bkgimages=%s" %((" ").join(bkgimage)),
         "srcimages=%s" % ((" ").join(srcmaps)),
         "emin=%s" %((" ").join(emin_ev_str)),
         "emax=%s" %((" ").join(emax_ev_str)),
         "eefextract=0.65",
         "stackflag=no",
         "apexflag=yes",
         "psfmapflag=yes",
         "apesenseflag=yes",
         "shapepsf=yes"
         ]
    
    if(do_apetool==True):
      for ii in range(len(psfmaps)):
        if(os.path.isfile(psfmaps[ii])==True):
          os.remove(psfmaps[ii]) 
      for ii in range(len(apesensmap)):
        if(os.path.isfile(apesensmap[ii])==True):
          os.remove(apesensmap[ii])
      print(cmd)
      subprocess.check_call(cmd)
    
    # ------------------------------------------------------------------------
    
    # experimental ersensmap
    ersensmap="%s%s" %(os.path.join(subdir,template_ersensmap), suffix)
    areatable="%s%s" %(os.path.join(subdir,template_areatable), suffix)
    cmd=["ersensmap",
    	"sensimage=%s" %(ersensmap),
        "expimages=%s" %((" ").join(expmap_all)),
        "detmasks=%s" %(detmask),
        "bkgimages=%s" %((" ").join(bkgimage)),
        "emin=%s" %((" ").join(emin_ev_str)),
        "emax=%s" %((" ").join(emax_ev_str)),
        "ecf=2.57027e+11 3.69588e+11 2.47685e+11 4.26585e+10",
    	"method=aper",
    	"aper_type=BOX",
    	"aper_size=4.5",
    	"likemin=8.",
    	"detmask_flag=Y",
    	"shapelet_flag=N",
    	"photon_flag=N",
    	"area_table=%s" %(areatable),
    	"area_flag=Y"
        ]
        
    if(do_ersensmap==True):
      if(os.path.isfile(ersensmap)==True):
        os.remove(ersensmap)
      if(os.path.isfile(areatable)==True):
        os.remove(areatable)
      print(cmd)
      subprocess.check_call(cmd)
    
# ------------------------------------------------------------------------
def HelpErrmessage(scriptname):
    print ("%s demo script for eSASS4EDR"%scriptname)
    print ("by A.Gueguen M.Ramos & C.Grossberger")
    print ("current version : April 2021")
    print ("This script must be called with 1 or 2 parameters")
    print ("%s --help or %s -H, print this message "%(os.path.basename(scriptname),os.path.basename(scriptname)))
    print ("")
    print ("\t*\tFirst parameter, Mandatory, is the input file, with absolute or relative path")
    print ("\t*\tSecond parameter, Optional, is the result folder, with absolute or relative path")
    print ("                                 if given, and not existing, the folder is created by the script")
    print (" EXAMPLES")
    print ("")
    print (" ./%s ./em01_237171_020_EventList_003_c946.fits  ./MyResults"%os.path.basename(scriptname))
    print ("    This call will run the script on a local file em01_237171_020_EventList_003_c946.fits ")
    print ("    and save the results in a subfolder of the current working directory named MyResults")
    print ("")
    print (" ./%s ./em01_237171_020_EventList_003_c946.fits  "%os.path.basename(scriptname))
    print ("    This call will run the script on a local file em01_237171_020_EventList_003_c946.fits ")
    print ("    and save the results the current working directory")
    print ("")
    print ("this program needs python3")
    
    
def main(args):
    global subdir ,infile
    
    starttimesecs=datetime.now()
    start_time = starttimesecs.strftime("%H:%M:%S")
    
    if len(args)<2 or args[1].lower().strip()=="--help"  or args[1].lower().strip()=="-h":
        HelpErrmessage(args[0])
        return 
    
    infile=args[1]
    if not os.path.isfile(infile):
        print ("ERROR: Iinput file %s \n\tcan't be found, please check it exist, the path is correct or you have access to it"%infile)
        return 
    
    if (len(args)>2):
        #print ("output dir is %s"%args[2])
        subdir=args[2]
        if not os.path.isdir(subdir):
            try:
                os.makedirs(subdir)
            except Exception as e:
                print ("ERROR: Can't create the output folder %s"%subdir)
    else: 
        currentfolder=os.getcwd()
        print("Results will be saved in the current folder :\n\t%s"%currentfolder)

    #control eSASS was initialised 
    findevtool= distutils.spawn.find_executable("evtool")
    if findevtool == None:
        print ("ERROR: eSASS was not initialised please initialise it (source the esass-init script ) and try again")
        return
    else :
        sasshome=os.getenv("SASS_HOME")
        print ("This script will uses eSASS installed in %s"%sasshome)
        sassbinroot=os.getenv("SASS_BIN_ROOT")
        print ("and the executables in:\n\t%s"%sassbinroot)

    RunTasks()
    
    endtimesec=datetime.now()
    end_time = endtimesec.strftime("%H:%M:%S")
    #print ("execution time ",(endtimesec-starttimesecs))
    statusin=0
    
if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
    
