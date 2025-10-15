import numpy as np
from astropy.io import fits
from astropy.table import Table

def create_gti_file(total_start, total_stop, bad_intervals, output_filename, telid=None):
    '''
        creates a GTI fits file by excluding bad time intervals.
        
        params:
        -----------
        total_start : float
            start time of the entire observation 
        total_stop : float
            stop time of the entire observation 
        bad_intervals : list of tuples
            list of (start, stop) tuples defining time intervals to EXCLUDE
            example: [(1000, 1500), (2000, 2300)]
        output_filename : str
            mame of output GTI FITS file
        telid : int or list of int, optional
            TMs to create GTI for. If None, creates STDGTI extension.
            if int or list, creates FLAREGTIn extensions for each TM.
    '''
    
    bad_intervals = sorted(bad_intervals, key=lambda x: x[0])
    
    good_intervals = []
    current_time = total_start
    
    for bad_start, bad_stop in bad_intervals:
        
        if current_time < bad_start:
            good_intervals.append((current_time, bad_start))
        current_time = max(current_time, bad_stop)
    
    if current_time < total_stop:
        good_intervals.append((current_time, total_stop))
    
    if len(good_intervals) == 0:
        print("WARNING: No good time intervals remaining!")
        start_times = np.array([])
        stop_times = np.array([])
    else:
        start_times = np.array([interval[0] for interval in good_intervals])
        stop_times = np.array([interval[1] for interval in good_intervals])
    
    total_exposure = np.sum(stop_times - start_times) if len(good_intervals) > 0 else 0.0
    
    print(f"\nGTI Summary:")
    print(f"exposure time: {total_start} to {total_stop} ({total_stop - total_start:.2f} s)")
    print(f"bad time intervals given: {len(bad_intervals)}")
    print(f"gtis: {len(good_intervals)}")
    print(f"total good exp time: {total_exposure:.2f} s")
    print(f"fraction retained: {100*total_exposure/(total_stop - total_start):.1f}%")
    
    primary = fits.PrimaryHDU()
    hdul = fits.HDUList([primary])
    
    if telid is None:
        extnames = ['STDGTI']
    else:
        if isinstance(telid, int):
            telid = [telid]
        extnames = [f'FLAREGTI{tm}' for tm in telid]
    
    for extname in extnames:
        gti_table = Table()
        gti_table['START'] = start_times
        gti_table['STOP'] = stop_times
        
        gti_hdu = fits.BinTableHDU(gti_table)
        gti_hdu.name = extname
        
        gti_hdu.header['EXTNAME'] = extname
        gti_hdu.header['HDUCLASS'] = 'OGIP'
        gti_hdu.header['HDUCLAS1'] = 'GTI'
        gti_hdu.header['HDUCLAS2'] = 'STANDARD'
        gti_hdu.header['ONTIME'] = (total_exposure, 'Total good time (s)')
        gti_hdu.header['TSTART'] = (total_start, 'Start time')
        gti_hdu.header['TSTOP'] = (total_stop, 'Stop time')
        
        hdul.append(gti_hdu)
    
    hdul.writeto(output_filename, overwrite=True)
    print(f"\nGTI file written to: {output_filename}")
    print(f"Extensions created: {', '.join(extnames)}")
    
    return output_filename

if __name__ == "__main__":
    
    print("="*60)
    print("Custom GTI File Creator for eROSITA Data")
    print("="*60)

    obs_start = 6.241104526425600e+08
    obs_stop = 6.241607576061440e+08
    
    flare_intervals = [
        (6.241225e+08, 6.241240e+08),   # 1st flare
        (6.241265e+08, 6.241275e+08),   # 2nf flare
        (6.241540e+08, 6.241570e+08),   # 3rd flare
    ]
    
    create_gti_file(obs_start, obs_stop, flare_intervals, 
                    'custom_flaregti.fits', telid=None)