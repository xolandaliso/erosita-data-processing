import os
import numpy as np
from astropy.io import fits

hdu = fits.open('pm00_300003_020_EventList_c001.fits')

data_table = hdu[1].data  # second extension for data

'''
dict : to store data for different TMs
list : the different TMs for eRosita
'''
tm_data, tm_n = {}, [1, 2, 5, 6, 7]

for tm_number in tm_n:  
    tm_data[tm_number] = data_table[data_table['TM_NR'] == tm_number]

'''
creating different .fits
files for TMs 
'''
for tm_number, tm_events in tm_data.items():
    # Create a new primary HDU (header) for the output FITS file
    primary_hdu = fits.PrimaryHDU()

    # Create a new FITS HDU with the TM data table
    events_hdu = fits.BinTableHDU(data=tm_events)
    events_hdu.name = 'EVENTS'

    # Create a list containing both HDUs (primary and events table)
    output_hdul = fits.HDUList([primary_hdu, events_hdu])

    # Define the output filename (example: tm1_events.fits for TM 1)
    output_filename = f'tm{tm_number}_events.fits'

    # Write the data to the new FITS file
    output_hdul.writeto('tms/'+output_filename, overwrite=True)

    print(f'Created FITS file: {output_filename}')

hdu.close()

print('Successfully separated data by TM and created FITS files.')
