#################################################################################
#### This script writes a plot of position-velocity slices of model and data ####
#################################################################################
import numpy as np 
import os 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from astropy.io import fits 
from astropy.visualization import PowerStretch 
from astropy.visualization.mpl_normalize import ImageNormalize 
from astropy.visualization import PercentileInterval 
mpl.rc('xtick',direction='in') 
mpl.rc('ytick',direction='in') 
mpl.rcParams['contour.negative_linestyle'] = 'solid' 
plt.rc('font',family='sans-serif',serif='Helvetica',size=10) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular'} 
plt.rcParams.update(params) 

gname = 'r431' 
outfolder = 'output_data/r431.hi_barolocentered/0/' 
twostage = 1 
plotmask = 0 
zmin, zmax = 26, 121

if twostage: rad,vrot,inc,pa,vsys = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(1,2,4,5,11),unpack=True) 
else: rad,vrot,inc,pa,vsys = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(1,2,4,5,11),unpack=True) 

files_pva_mod, files_pvb_mod = [], [] 
for thisFile in sorted(os.listdir(outfolder+'pvs/')): 
	if 'pv_a_azim.fits' in thisFile: files_pva_mod.append(thisFile) 
	if 'pv_b_azim.fits' in thisFile: files_pvb_mod.append(thisFile) 
	if 'pv_a_local.fits' in thisFile: files_pva_mod.append(thisFile) 
	if 'pv_b_local.fits' in thisFile: files_pvb_mod.append(thisFile) 

image_maj     = fits.open(outfolder+'pvs/'+gname+'_pv_a.fits') 
image_min     = fits.open(outfolder+'pvs/'+gname+'_pv_b.fits') 
image_mas_maj = fits.open(outfolder+'pvs/'+gname+'mask_pv_a.fits') 
image_mas_min = fits.open(outfolder+'pvs/'+gname+'mask_pv_b.fits') 
head = [image_maj[0].header,image_min[0].header] 
crpixpv = np.array([head[0]['CRPIX1'],head[1]['CRPIX1']]) 
cdeltpv = np.array([head[0]['CDELT1'],head[1]['CDELT1']]) 
crvalpv = np.array([head[0]['CRVAL1'],head[1]['CRVAL1']]) 
xminpv, xmaxpv = np.floor(crpixpv-1-108), np.ceil(crpixpv-1 +108) 
if xminpv[0]<0: xminpv[0]=0 
if xminpv[1]<0: xminpv[1]=0 
if xmaxpv[0]>=head[0]['NAXIS1']: xmaxpv[0]=head[0]['NAXIS1']-1 
if xmaxpv[1]>=head[1]['NAXIS1']: xmaxpv[1]=head[1]['NAXIS1']-1 
data_maj = image_maj[0].data[zmin:zmax+1,int(xminpv[0]):int(xmaxpv[0])+1] 
data_min = image_min[0].data[zmin:zmax+1,int(xminpv[1]):int(xmaxpv[1])+1] 
data_mas_maj = image_mas_maj[0].data[zmin:zmax+1,int(xminpv[0]):int(xmaxpv[0])+1] 
data_mas_min = image_mas_min[0].data[zmin:zmax+1,int(xminpv[1]):int(xmaxpv[1])+1] 
xmin_wcs = ((xminpv+1-0.5-crpixpv)*cdeltpv+crvalpv)*3600
xmax_wcs = ((xmaxpv+1+0.5-crpixpv)*cdeltpv+crvalpv)*3600
zmin_wcs, zmax_wcs = -132.4, 117.2
cont = 0
v = np.array([1,2,4,8,16,32,64])*cont 
v_neg = [-cont] 
interval = PercentileInterval(99.5) 
vmax = interval.get_limits(data_maj)[1] 
norm = ImageNormalize(vmin=cont, vmax=vmax, stretch=PowerStretch(0.5)) 

radius = np.concatenate((rad,-rad)) 
pamaj_av = 95.2895
pamin_av = 185.289
costh = np.cos(np.deg2rad(np.abs(pa-pamaj_av))) 
vlos1 = vsys+vrot*np.sin(np.deg2rad(inc))*costh 
vlos2 = vsys-vrot*np.sin(np.deg2rad(inc))*costh 
reverse = True 
if reverse: vlos1, vlos2 = vlos2, vlos1 
vlos = np.concatenate((vlos1,vlos2)) 
vsys_m = np.nanmean(vsys) 
ext = [[xmin_wcs[0],xmax_wcs[0],zmin_wcs-vsys_m,zmax_wcs-vsys_m],\
       [xmin_wcs[1],xmax_wcs[1],zmin_wcs-vsys_m,zmax_wcs-vsys_m]] 
labsize = 14 
palab = ['$\phi = $%i$^\circ$'%np.round(pamaj_av), '$\phi = $%i$^\circ$'%np.round(pamin_av)] 

# Beginning PV plot 
for k in range (len(files_pva_mod)): 
	image_mod_maj = fits.open(outfolder+'pvs/'+files_pva_mod[k]) 
	image_mod_min = fits.open(outfolder+'pvs/'+files_pvb_mod[k]) 
	data_mod_maj = image_mod_maj[0].data[zmin:zmax+1,int(xminpv[0]):int(xmaxpv[0])+1] 
	data_mod_min = image_mod_min[0].data[zmin:zmax+1,int(xminpv[1]):int(xmaxpv[1])+1] 
	toplot = [[data_maj,data_min],[data_mod_maj,data_mod_min],[data_mas_maj,data_mas_min]] 

	fig = plt.figure(figsize=(10,10), dpi=150) 
	x_len, y_len, y_sep = 0.6, 0.42, 0.08 
	ax, bottom_corner = [], [0.1,0.7] 
	for i in range (2): 
		bottom_corner[0], axcol = 0.1, [] 
		ax.append(fig.add_axes([bottom_corner[0],bottom_corner[1],x_len,y_len])) 
		bottom_corner[1]-=(y_len+y_sep) 

	for i in range (2): 
		axis = ax[i] 
		axis.tick_params(which='major',length=8, labelsize=labsize) 
		axis.set_xlabel('Offset (arcsec)',fontsize=labsize+2) 
		axis.set_ylabel('$\mathrm{\Delta V_{LOS}}$ (km/s)',fontsize=labsize+2) 
		axis.text(1, 1.02,palab[i],ha='right',transform=axis.transAxes,fontsize=labsize+4) 
		axis2 = axis.twinx() 
		axis2.set_xlim([ext[i][0],ext[i][1]]) 
		axis2.set_ylim([ext[i][2]+vsys_m,ext[i][3]+vsys_m]) 
		axis2.tick_params(which='major',length=8, labelsize=labsize) 
		axis2.set_ylabel('$\mathrm{V_{LOS}}$ (km/s)',fontsize=labsize+2) 
		axis.imshow(toplot[0][i],origin='lower',cmap = mpl.cm.Greys,norm=norm,extent=ext[i],aspect='auto') 
		axis.contour(toplot[0][i],v,origin='lower',linewidths=0.7,colors='#00008B',extent=ext[i]) 
		axis.contour(toplot[0][i],v_neg,origin='lower',linewidths=0.1,colors='gray',extent=ext[i]) 
		axis.contour(toplot[1][i],v,origin='lower',linewidths=1,colors='#B22222',extent=ext[i]) 
		axis.axhline(y=0,color='black') 
		axis.axvline(x=0,color='black') 
		axis.grid(color='gray', linestyle='--', linewidth=0.3) 
		if plotmask: 
			axis.contour(toplot[2][i],[1],origin='lower',linewidths=2,colors='k',extent=ext[i]) 
		if i==0 : 
			axis2.plot(radius,vlos,'yo') 
			axis.text(0, 1.1, gname, transform=axis.transAxes,fontsize=22) 

	outfile = '%s_pv'%gname 
	if ('azim' in files_pva_mod[k]): outfile += '_azim' 
	elif ('local' in files_pva_mod[k]): outfile += '_local' 
	fig.savefig(outfolder+outfile+'.pdf', bbox_inches='tight') 
	image_mod_maj.close() 
	image_mod_min.close() 

image_maj.close() 
image_min.close() 
