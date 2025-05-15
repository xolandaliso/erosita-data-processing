from astropy.io import fits

# Input and output files
input_file = "mosaic.fits"
output_file = "mosaic_header_corrected.fits"

# Expected TMs for TM8
expected_tms = [1, 2, 5, 6, 7]

# Prefixes of TM-specific extensions
tm_prefixes = ['CORRATT', 'DEADCOR', 'BADPIX', 'GTI', 'FLAREGTI', 'HK1', 'HK2', 'HK3', 'HK5']

# Load the input FITS file
with fits.open(input_file) as hdul:
    # Create a new HDUList for the output
    new_hdul = fits.HDUList()
    
    # Copy non-TM-specific extensions
    for hdu in hdul:
        is_tm_specific = any(hdu.name.startswith(prefix) for prefix in tm_prefixes)
        if not is_tm_specific:
            new_hdul.append(hdu.copy())
    
    # Collect TM-specific extensions
    tm_extensions = {}
    for prefix in tm_prefixes:
        tm_extensions[prefix] = [
            hdu for hdu in hdul
            if hdu.name.startswith(prefix) and hdu.name != prefix
        ]
        # Sort by the TM number in the name (e.g., GTI1, GTI2, GTI5)
        tm_extensions[prefix].sort(key=lambda hdu: int(hdu.name.replace(prefix, '')))
    
    # Check and rename TM-specific extensions
    for prefix in tm_prefixes:
        extensions = tm_extensions[prefix]
        if len(extensions) != len(expected_tms):
            print(f"Warning: Found {len(extensions)} {prefix} extensions, "
                  f"but expected {len(expected_tms)} for TMs {expected_tms}.")
        
        for i, tm in enumerate(expected_tms):
            if i < len(extensions):
                hdu = extensions[i].copy()
                # Rename the extension
                if prefix in ['CORRATT', 'DEADCOR', 'BADPIX', 'GTI', 'FLAREGTI']:
                    new_name = f"{prefix}{tm}"
                else:  # HK1, HK2, HK3, HK5
                    new_name = f"{prefix}{tm}"  # e.g., HK1 + 6 -> HK16
                hdu.name = new_name
                # Update TELID keyword if present
                if 'TELID' in hdu.header:
                    hdu.header['TELID'] = tm
                new_hdul.append(hdu)
            else:
                print(f"Warning: Missing {prefix} extension for TM{tm}")
    
    # Save the corrected FITS file
    new_hdul.writeto(output_file, overwrite=True)
    print(f"Corrected FITS file saved to {output_file}")

# Verify the new file
with fits.open(output_file) as hdul:
    print("\nNew FITS file structure:")
    hdul.info()