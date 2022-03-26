"""
Author: Daniel Hoshizaki

Blend two satellite images together using poisson image editing
"""

import os
from pathlib import Path
import numpy as np
import rasterio
from scikits.umfpack import spsolve
import utils
import poisson


if __name__ == '__main__':

    cwd = Path(__file__).resolve().parent.parent
    base = cwd / 'data'

    input_dir = base / 'inputs'
    output_dir = base / 'outputs'
    NODATA = 0

    # Collect pairs of inputs
    inputs = utils.gather_inputs(input_dir)

    for dir_name, (source_path, target_path) in inputs.items():
        print(f"Processing images in folder {dir_name}")

        # Read the image data to a Numpy array
        source_img = utils.read_data(source_path)
        target_img = utils.read_data(target_path)

        # Get the image dimensions
        channels, height, width = source_img.shape

        # Get the sources nodata value to compute a mask
        nodata = utils.get_nodata_value(source_path)

        # Generate a mask form the source file
        # Use one band and create a mask from areas that are nodata
        mask = np.where(source_img[0] == nodata, 0, 1)

        # Format the mask so that it can be used successfully during the blending step
        mask = utils.format_mask(mask)

        # Get all non-zero elements and their index locations of the mask, 
        # these points will be used to create the sparse matrix A
        nonzero = np.nonzero(mask)
        target_points = {(i,j):k for k, (i,j) in enumerate(zip(nonzero[0], nonzero[1]))}

        # Create the Laplacian operator
        # Matrix A in Ax = b
        A = poisson.laplacian_operator(target_points)
        
        # Solve for x in Ax = b for each band
        blended_bands = []
        for band in range(channels):
            print(f"Blending band {band}")

            # Collect the data for the source and target band
            target = target_img[band]
            source = source_img[band]

            b = poisson.compute_gradient(target_points, source, target)

            # NOTE
            # If `A` is very large the solver uses too much memory
            x = spsolve(A, b)

            # Insert the new intensities into the target image
            blended_band = poisson.insert_values(x, target, target_points)
            blended_bands.append(blended_band)
        
        result = np.array(blended_bands).astype(np.uint8)

        # Save the output as GeoTIFF
        os.makedirs(output_dir / dir_name, exist_ok=True)
        destination = output_dir / dir_name / 'result.tif'
        with rasterio.open(target_path) as src:
            with rasterio.open(destination, 'w', **src.profile) as dst:
                dst.write(result)

        print(f"Blended result saved\n")


