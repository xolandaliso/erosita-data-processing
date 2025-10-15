import bdsf
# For Chandra (PSF FWHM ~0.5" at 1.5 keV)
# Convert arcseconds to degrees
beam_fwhm = 0.5 / 3600.0  # 0.5 arcsec in degrees

# Specify as (major_axis, minor_axis, position_angle)
img = bdsf.process_image('data/full_eband/tm0_soft_band_8_23eV.fits', 
                         beam=(beam_fwhm, beam_fwhm, 0.0),
			 frequency=2.42e17,
                         thresh_pix=5.0,
                         thresh_isl=3.0)
