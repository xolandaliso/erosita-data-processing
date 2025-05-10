#####################################################################
#### This script writes a plot of channel maps of model and data ####
#####################################################################
import numpy as np 
import os 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec 
from astropy.io import fits 
from astropy.visualization import PowerStretch 
from astropy.visualization.mpl_normalize import ImageNormalize 
from astropy.visualization import PercentileInterval 
mpl.rc('xtick',direction='in',top=True,labelbottom=False) 
mpl.rc('ytick',direction='in',right=True,labelleft=False) 
mpl.rcParams['contour.negative_linestyle'] = 'solid' 
plt.rc('font',family='sans-serif',serif='Helvetica',size=10) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular'} 
plt.rcParams.update(params) 

gname = 'r431' 
outfolder = 'output_data/r431.hi_barolocentered/0/' 
twostage = 1 
plotmask = 0 

if twostage: xpos,ypos,vsys = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(9,10,11),unpack=True) 
else: xpos,ypos,vsys = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(9,10,11),unpack=True) 
xcen_m,ycen_m,vsys_m = np.nanmean((xpos,ypos,vsys),axis=1) 

# CHANNEL MAPS: Setting all the needed variables 
image = fits.open('simulated//r431.hi_barolocentered.fits') 
image_mas = fits.open(outfolder+'mask.fits') 
xmin, xmax = 0, 199
ymin, ymax = 0, 199
zmin, zmax = 26, 121
data = image[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
data_mas = image_mas[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
head = image[0].header 
zsize= data.shape[0] 
cdeltsp=2
cont = 0
v = np.array([1,2,4,8,16,32,64])*cont 
v_neg = [-cont] 
interval = PercentileInterval(99.5) 
vmax = interval.get_limits(data)[1] 
norm = ImageNormalize(vmin=cont, vmax=vmax, stretch=PowerStretch(0.5)) 
xcen, ycen = xcen_m-xmin, ycen_m-ymin  

files_mod = [] 
for thisFile in sorted(os.listdir(outfolder)): 
	if 'mod_azim.fits'  in thisFile: files_mod.append(thisFile) 
	if 'mod_local.fits' in thisFile: files_mod.append(thisFile) 
if len(files_mod)==0: exit('ERROR: no model in output directory') 

# Beginning channel map plot 
for k in range (len(files_mod)): 
	image_mod = fits.open(outfolder+files_mod[k]) 
	data_mod = image_mod[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
	fig = plt.figure(figsize=(8.27, 11.69), dpi=150) 
	grid = [gridspec.GridSpec(2,5),gridspec.GridSpec(2,5),gridspec.GridSpec(2,5)] 
	grid[0].update(top=0.90, bottom=0.645, left=0.05, right=0.95, wspace=0.0, hspace=0.0) 
	grid[1].update(top=0.60, bottom=0.345, left=0.05, right=0.95, wspace=0.0, hspace=0.0) 
	grid[2].update(top=0.30, bottom=0.045, left=0.05, right=0.95, wspace=0.0, hspace=0.0) 

	num = 0 
	for j in range (0,3): 
		for i in range (0,5): 
			chan = int(num*(zsize)/15) 
			z = data[chan,:,:] 
			z_mod = data_mod[chan,:,:] 
			#New matplotlib draws wrong contours when no contours are found. This is a workaround.
			if np.all(z_mod<v[0]): z_mod[:,:] =0
			velo_kms = (chan+1--25)*2.6+-198.7
			velo = ' v = ' + str(int(velo_kms-vsys_m)) + ' km/s' 
			ax = plt.subplot(grid[j][0,i]) 
			ax.set_title(velo, fontsize=10,loc='left') 
			ax.imshow(z,origin='lower',cmap = mpl.cm.Greys,norm=norm,aspect='auto',interpolation='none') 
			ax.contour(z,v,origin='lower',linewidths=0.7,colors='#00008B') 
			ax.contour(z,v_neg,origin='lower',linewidths=0.1,colors='gray') 
			ax.plot(xcen,ycen,'x',color='#0FB05A',markersize=7,mew=2) 
			if plotmask: 
				ax.contour(data_mas[chan],[1],origin='lower',linewidths=2,colors='k') 
			if (j==i==0): 
				ax.text(0, 1.4, gname, transform=ax.transAxes,fontsize=15,va='center') 
				lbar = 0.5*(xmax-xmin)*cdeltsp 
				ltex = "%.0f'' "%lbar if lbar>10 else "%.2f'' "%lbar 
				if lbar>600: ltex = "%.0f' "%(lbar/60.) 
				ax.annotate('', xy=(4.5, 1.4), xycoords='axes fraction', xytext=(5, 1.4),arrowprops=dict(arrowstyle='<->', color='k'))
				ax.text(4.75,1.50,ltex,transform=ax.transAxes,fontsize=11, ha='center')
				bmaj, bmin, bpa = 4.14628/float(xmax-xmin), 3.44713/float(ymax-ymin),154.302
				beam = mpl.patches.Ellipse((3.5, 1.4), bmaj, bmin, bpa+90, color='#5605D0', clip_on=False, transform=ax.transAxes, alpha=0.2) 
				ax.add_artist(beam) 
				ax.text(3.6+bmaj/1.8,1.4,'Beam',transform=ax.transAxes,fontsize=11, ha='left',va='center') 
			ax = plt.subplot(grid[j][1,i]) 
			ax.tick_params(axis='both',which='both',bottom=True,top=True,labelbottom=False,labelleft=False) 
			ax.imshow(z_mod,origin='lower',cmap = mpl.cm.Greys,norm=norm,aspect='auto',interpolation='none') 
			ax.contour(z_mod,v,origin='lower',linewidths=0.7,colors='#B22222') 
			ax.plot(xcen,ycen,'x',color='#0FB05A',markersize=7,mew=2) 
			if (i==0 and j==2): 
				clab = 'Contour levels at 2$^n \, c_{min}$, where $c_{min}$ = %s JY/BEAM and n = 0,1,..,8 '%cont 
				ax.text(0.01,-0.16,clab,transform=ax.transAxes,fontsize=11, ha='left',va='center') 
			num = num+1 

	outfile = '%s_chanmaps'%gname 
	if ('azim' in files_mod[k]): outfile += '_azim' 
	elif ('local' in files_mod[k]): outfile += '_local' 
	fig.savefig(outfolder+outfile+'.pdf', orientation = 'portrait', format = 'pdf') 
	image_mod.close() 

image.close() 
