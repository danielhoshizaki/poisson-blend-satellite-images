"""
Author: Daniel Hoshizaki
"""

import os
from pathlib import Path
import numpy as np
import rasterio
from scipy.ndimage import binary_dilation, binary_erosion


def gather_inputs(path: Path) -> list:
    """Get a dictionary where the key is the folder name and the value is a tuple of
    the source and target file paths"""
    collected_inputs = {}
    for directory in os.listdir(path):

        target_path = path / directory / "target.tif"
        source_path = path / directory / "source.tif"

        if target_path.exists() and source_path.exists():
            collected_inputs[directory] = (source_path, target_path)

    assert len(collected_inputs) > 0, "Provide target and source files in the input directory"

    return collected_inputs


def read_data(path: Path) -> np.ndarray:
    """Open the GeoTIFF and read the RGB data"""
    with rasterio.open(path) as src:
        data = src.read()
    return data


def get_nodata_value(path: Path) -> int:
    """Read the target files metadata and get the nodata value"""
    with rasterio.open(path) as src:
        nodata_value = src.profile['nodata']
    return nodata_value


def format_mask(mask: np.ndarray) -> np.ndarray:
    """Get rid of holes in the mask and step the mask away from the boundary of the image"""
    mask = binary_dilation(mask, iterations=1)  # remove any 'holes' in the mask
    mask = binary_erosion(mask, iterations=2)  # step the mask away from the image boundary

    return mask