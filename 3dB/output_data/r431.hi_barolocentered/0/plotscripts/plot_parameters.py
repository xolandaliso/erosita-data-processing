###############################################################
#### This script produces plots of the best-fit parameters ####
###############################################################
import numpy as np 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
lsize = 11 
mpl.rc('xtick',direction='in',top=True) 
mpl.rc('ytick',direction='in',right=True) 
mpl.rcParams['contour.negative_linestyle'] = 'solid' 
plt.rc('font',family='sans-serif',serif='Helvetica',size=10) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular', 'errorbar.capsize': 0} 
plt.rcParams.update(params) 

gname = 'r431' 
outfolder = 'output_data/r431.hi_barolocentered/0/' 
twostage = 1 

# Reading in best-fit parameters 
rad_sd, surfdens, sd_err = np.genfromtxt(outfolder+'densprof.txt', usecols=(0,3,4),unpack=True) 
rad,vrot,disp,inc,pa,z0,xpos,ypos,vsys,vrad = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(1,2,3,4,5,7,9,10,11,12),unpack=True) 
try: err1_l, err1_h = np.zeros(shape=(10,len(rad))), np.zeros(shape=(10,len(rad)))
except: err1_l, err1_h = np.zeros(shape=(10,1)), np.zeros(shape=(10,1))
color=color2='#B22222' 
max_vrot,max_vdisp = np.nanmax(vrot),np.nanmax(disp) 
max_rad = 1.1*np.nanmax(rad) 
err1_l[0], err1_h[0] = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(13,14),unpack=True) 
err1_l[1], err1_h[1] = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(15,16),unpack=True) 
err1_l[4], err1_h[4] = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(17,18),unpack=True) 
err1_l[5], err1_h[5] = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(19,20),unpack=True) 
err1_l[8], err1_h[8] = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(21,22),unpack=True) 

if twostage: 
	rad2, vrot2,disp2,inc2,pa2,z02,xpos2,ypos2,vsys2, vrad2 = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(1,2,3,4,5,7,9,10,11,12),unpack=True)
	err2_l, err2_h = np.zeros(shape=(10,len(rad2))), np.zeros(shape=(10,len(rad2)))
	color='#A0A0A0' 
	max_rad = 1.1*np.nanmax(rad2) 
	max_vrot,max_vdisp = np.maximum(max_vrot,np.nanmax(vrot2)),np.maximum(max_vdisp,np.nanmax(disp2)) 
	err2_l[0], err2_h[0] = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(13,14),unpack=True) 
	err2_l[1], err2_h[1] = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(15,16),unpack=True) 

# Defining figure and axes 
fig=plt.figure(figsize=(11,11),dpi=150) 
nrows, ncols = 3,3 
xlen, ylen = 0.27, 0.13 
x_sep, y_sep = 0.07,0.015 
bottom_corner = [0.1,0.7] 
for i in range (nrows): 
	bottom_corner[0], yl = 0.1, ylen 
	if i==0: yl *= 1.8 
	for j in range (ncols): 
		fig.add_axes([bottom_corner[0],bottom_corner[1],xlen,yl]) 
		fig.axes[-1].set_xlim(0,max_rad) 
		if i==nrows-1: fig.axes[-1].tick_params(labelbottom=True) 
		else: fig.axes[-1].tick_params(labelbottom=False) 
		bottom_corner[0]+=xlen+x_sep 
	bottom_corner[1]-=(ylen+y_sep) 

ax = fig.axes 

# Plotting rotation velocity 
ax[0].set_ylim(0,1.2*max_vrot) 
ax[0].set_ylabel('V$_\mathrm{rot}$ (km/s)', fontsize=lsize) 
ax[0].errorbar(rad,vrot, yerr=[-err1_l[0],err1_h[0]],fmt='o', color=color) 
if twostage: ax[0].errorbar(rad2,vrot2, yerr=[-err2_l[0],err2_h[0]],fmt='o', color=color2) 

# Plotting velocity dispersion 
ax[1].set_ylim(0,1.2*max_vdisp) 
ax[1].set_ylabel('$\sigma_\mathrm{gas}$  (km/s)', fontsize=lsize) 
ax[1].errorbar(rad,disp, yerr=[-err1_l[1],err1_h[1]],fmt='o', color=color) 
if twostage: ax[1].errorbar(rad2,disp2, yerr=[-err2_l[1],err2_h[1]],fmt='o', color=color2) 

# Plotting surface density 
ax[2].set_xlim(0,max_rad) 
ax[2].set_ylabel('$\Sigma}$ (JY * KM/S)', fontsize=lsize) 
ax[2].errorbar(rad_sd,surfdens, yerr=sd_err,fmt='o', color=color2) 

# Plotting inclination angle 
ax[3].set_ylabel('i (deg)', fontsize=lsize) 
ax[3].errorbar(rad,inc, yerr=[-err1_l[4],err1_h[4]],fmt='o', color=color) 
if twostage: ax[3].errorbar(rad2,inc2,yerr=[-err2_l[4],err2_h[4]], fmt='o-', color=color2) 

# Plotting x-center 
ax[4].set_ylabel('x$_0$ (pix)', fontsize=lsize) 
ax[4].errorbar(rad,xpos, yerr=[-err1_l[6],err1_h[6]],fmt='o', color=color) 
if twostage: ax[4].errorbar(rad2,xpos2,yerr=[-err2_l[6],err2_h[6]],fmt='o-', color=color2) 

# Plotting radial velocity 
ax[5].set_xlim(0,max_rad) 
ax[5].set_ylabel('V$_\mathrm{rad}$ (km/s)', fontsize=lsize) 
ax[5].errorbar(rad,vrad, yerr=[-err1_l[9],err1_h[9]],fmt='o', color=color) 
if twostage==True: ax[5].errorbar(rad2,vrad2,yerr=[-err2_l[9],err2_h[9]],fmt='o', color=color2) 

# Plotting position angle 
ax[6].set_ylabel('$\phi$ (deg)', fontsize=lsize) 
ax[6].set_xlabel('Radius (arcsec)', fontsize=lsize, labelpad=10) 
ax[6].errorbar(rad,pa, yerr=[-err1_l[5],err1_h[5]],fmt='o', color=color) 
if twostage: ax[6].errorbar(rad2,pa2,yerr=[-err2_l[5],err2_h[5]], fmt='o-', color=color2) 

# Plotting y-center 
ax[7].set_ylabel('y$_0$ (pix)', fontsize=lsize) 
ax[7].set_xlabel('Radius (arcsec)', fontsize=lsize, labelpad=10) 
ax[7].errorbar(rad,ypos, yerr=[-err1_l[7],err1_h[7]],fmt='o', color=color) 
if twostage: ax[7].errorbar(rad2,ypos2, yerr=[-err2_l[7],err2_h[7]],fmt='o-', color=color2) 

# Plotting systemic velocity 
ax[8].set_ylabel('v$_\mathrm{sys}$ (km/s)', fontsize=lsize) 
ax[8].set_xlabel('Radius (arcsec)', fontsize=lsize, labelpad=10) 
ax[8].errorbar(rad,vsys, yerr=[-err1_l[8],err1_h[8]],fmt='o', color=color) 
if twostage==True: ax[8].errorbar(rad2,vsys2,yerr=[-err2_l[8],err2_h[8]],fmt='o', color=color2) 

fig.savefig(outfolder+'%s_parameters.pdf'%gname,bbox_inches='tight') 
