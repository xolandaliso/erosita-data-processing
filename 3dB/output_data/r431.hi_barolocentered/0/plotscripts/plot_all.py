########################################################################
#### This script simply calls all other python scripts for plotting ####
########################################################################
import os 

scriptdir = 'output_data/r431.hi_barolocentered/0/plotscripts/' 
cmd = '' 

for f in os.listdir(scriptdir): 
	if '.py' in f and f!='plot_all.py': 
		cmd += 'python "%s/%s" & '%(scriptdir,f) 

os.system(cmd[:-2]) 
