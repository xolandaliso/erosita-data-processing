#######################################################################
#### This script writes a plot of kinematic maps of model and data ####
#######################################################################
import numpy as np 
import os 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib.colorbar import ColorbarBase 
from astropy.io import fits 
from astropy.visualization import PercentileInterval 
from copy import copy 
mpl.rc('xtick',direction='in') 
mpl.rc('ytick',direction='in') 
plt.rc('font',family='sans-serif',serif='Helvetica',size=10) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular'} 
plt.rcParams.update(params) 

gname = 'r431' 
outfolder = 'output_data/r431.hi_barolocentered/0/' 
twostage = 1 
xmin, xmax = 0, 199
ymin, ymax = 0, 199

if twostage: rad,inc,pa,xpos,ypos,vsys = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(1,4,5,9,10,11),unpack=True) 
else: rad,inc,pa,xpos,ypos,vsys = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(1,4,5,9,10,11),unpack=True) 
xcen_m,ycen_m,inc_m,pa_m,vsys_m=np.nanmean((xpos,ypos,inc,pa,vsys),axis=1) 
xcen, ycen = xcen_m-xmin, ycen_m-ymin 

# Opening maps and retrieving intensity map units
f0 = fits.open(outfolder+'/maps/'+gname+'_0mom.fits') 
f1 = fits.open(outfolder+'/maps/'+gname+'_1mom.fits') 
f2 = fits.open(outfolder+'/maps/'+gname+'_2mom.fits') 
bunit = f0[0].header['BUNIT'] 
bunit = bunit.replace(' ', '').lower() 
# Now plotting moment maps 
mom0 = f0[0].data[ymin:ymax+1,xmin:xmax+1] 
mom1 = f1[0].data[ymin:ymax+1,xmin:xmax+1] 
mom2 = f2[0].data[ymin:ymax+1,xmin:xmax+1] 
maskmap = np.copy(mom1) 
maskmap[mom1==mom1] = 1 

files_mod0, files_mod1, files_mod2 = [], [], [] 
for thisFile in sorted(os.listdir(outfolder+'/maps/')): 
	if 'azim_0mom.fits' in thisFile: files_mod0.append(thisFile) 
	if 'azim_1mom.fits' in thisFile: files_mod1.append(thisFile) 
	if 'azim_2mom.fits' in thisFile: files_mod2.append(thisFile) 
	if 'local_0mom.fits' in thisFile: files_mod0.append(thisFile) 
	if 'local_1mom.fits' in thisFile: files_mod1.append(thisFile) 
	if 'local_2mom.fits' in thisFile: files_mod2.append(thisFile) 

cmaps = [plt.get_cmap('Spectral_r'),plt.get_cmap('RdBu_r',25),plt.get_cmap('PuOr_r')] 
barlab = ['Intensity ('+bunit+')', 'V$_\mathrm{LOS}$ (km/s)', '$\sigma$ (km/s)'] 
barlab2 = ['I$_\mathrm{res}$ ('+bunit+')', 'V$_\mathrm{res}$ (km/s)', '$\sigma_\mathrm{res}$ (km/s)'] 
titles = ['DATA', 'MODEL','RESIDUAL'] 
mapname = ['INTENSITY', 'VELOCITY', 'DISPERSION'] 
x = np.arange(0,xmax-xmin,0.1) 
y = np.tan(np.radians(pa_m-90))*(x-xcen)+ycen 
ext = [0,xmax-xmin,0, ymax-ymin] 
rad_pix = rad/2
try: nr = len(rad_pix) 
except: nr = 1 
interval = PercentileInterval(99.5) 

for k in range (len(files_mod0)): 
	mom0_mod = fits.open(outfolder+'/maps/'+files_mod0[k])[0].data[ymin:ymax+1,xmin:xmax+1] 
	mom1_mod = fits.open(outfolder+'/maps/'+files_mod1[k])[0].data[ymin:ymax+1,xmin:xmax+1] 
	mom2_mod = fits.open(outfolder+'/maps/'+files_mod2[k])[0].data[ymin:ymax+1,xmin:xmax+1] 
	to_plot = [[mom0,mom1-vsys_m,mom2],[mom0_mod,mom1_mod-vsys_m,mom2_mod],[mom0-mom0_mod,mom1-mom1_mod,mom2-mom2_mod]] 

	fig=plt.figure(figsize=(11,11), dpi=150) 
	nrows, ncols = 3, 3 
	x_len, y_len = 0.2, 0.2 
	x_sep, y_sep = 0.00,0.08 
	ax, bottom_corner = [], [0.1,0.7] 
	for i in range (nrows): 
		bottom_corner[0], axcol = 0.1, [] 
		for j in range (ncols): 
			axcol.append(fig.add_axes([bottom_corner[0],bottom_corner[1],x_len,y_len])) 
			bottom_corner[0]+=x_len+x_sep 
		ax.append(axcol) 
		bottom_corner[1]-=(y_len+y_sep) 

	for i in range (nrows): 
		cmap = copy(cmaps[i]) 
		cmap.set_bad('w',1.) 
		vmin, vmax = interval.get_limits(to_plot[1][i]) 
		vmin, vmax = (-1.1*np.nanmax(vmax),1.1*np.nanmax(vmax)) if i==1 else (vmin,vmax) 
		norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax) 
		cbax = fig.add_axes([ax[i][0].get_position().x0,ax[i][0].get_position().y0-0.025,2*x_len-0.003,0.02]) 
		cb1 = ColorbarBase(cbax, orientation='horizontal', cmap=cmap, norm=norm) 
		cb1.set_label(barlab[i],fontsize=13) 
		for j in range (ncols): 
			axis = ax[i][j] 
			axis.tick_params(labelbottom=False,labelleft=False,right=True,top=True) 
			axis.set_xlim(ext[0],ext[1]) 
			axis.set_ylim(ext[2],ext[3]) 
			if j==2: 
				vmax = np.nanmax(interval.get_limits(to_plot[j][i])) 
				norm = mpl.colors.Normalize(vmin=-vmax, vmax=vmax) 
			axis.imshow(to_plot[j][i]*maskmap,origin='lower',cmap=cmap,norm=norm,aspect='auto',extent=ext,interpolation='nearest') 
			axis.plot(xcen,ycen,'x',color='#000000',markersize=7,mew=1.5) 

			if i==0: 
				axis.text(0.5,1.05,titles[j],ha='center',transform=axis.transAxes,fontsize=15) 
				axis.plot(x,y,'--',color='k',linewidth=1) 
				if j!=2 and nr>3:  
					axmaj = rad_pix[-1] 
					axmin = axmaj*np.cos(np.radians(inc_m))  
					posa = np.radians(pa_m-90)  
					t = np.linspace(0,2*np.pi,100)  
					xt = xcen+axmaj*np.cos(posa)*np.cos(t)-axmin*np.sin(posa)*np.sin(t)  
					yt = ycen+axmaj*np.sin(posa)*np.cos(t)+axmin*np.cos(posa)*np.sin(t)  
					axis.plot(xt,yt,'-',c='k',lw=0.8)  
			elif i==1: 
				axis.plot(x,y,'--',color='k',linewidth=1) 
				if nr<10: 
					x_pix = rad_pix*np.cos(np.radians(pa_m-90)) 
					y_pix = rad_pix*np.sin(np.radians(pa_m-90)) 
					axis.scatter(x_pix+xcen,y_pix+ycen,c='grey',s=12) 
					axis.scatter(xcen-x_pix,ycen-y_pix,c='grey',s=12) 
				if nr>5 and not all(np.diff(pa)==0): 
					x_pix = rad_pix*np.cos(np.radians(pa-90)) 
					y_pix = rad_pix*np.sin(np.radians(pa-90)) 
					axis.plot(xcen-x_pix,ycen-y_pix,'-',color='grey',lw=1) 
					axis.plot(x_pix+xcen,y_pix+ycen,'-',color='grey',lw=1) 
				if j!=2: axis.contour(to_plot[j][i]*maskmap,levels=[0],colors='green',origin='lower',extent=ext) 
			if j==0: axis.text(-0.12,0.5,mapname[i],va='center',rotation=90,transform=axis.transAxes,fontsize=15) 

		cbax = fig.add_axes([ax[i][2].get_position().x0+0.003,ax[i][2].get_position().y0-0.025,x_len-0.003,0.02]) 
		cb2 = ColorbarBase(cbax, orientation='horizontal', cmap=cmap, norm=norm) 
		cb2.set_label(barlab2[i],fontsize=13) 
		cb2.ax.locator_params(nbins=3) 
		for c in [cb1,cb2]: 
			c.solids.set_edgecolor('face') 
			c.outline.set_linewidth(0) 

	outfile = '%s_maps'%gname 
	if ('azim' in files_mod0[k]): outfile += '_azim' 
	elif ('local' in files_mod0[k]): outfile += '_local' 
	fig.savefig(outfolder+outfile+'.pdf', bbox_inches = 'tight') 

