
"""
Author: Daniel Hoshizaki

Blend two images together using gradient domain editing
"""

import os
from pathlib import Path
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.windows import bounds, Window
from rasterio.transform import Affine
import sys
from PIL import Image

if __name__ == '__main__':

    cwd = Path(__file__).resolve().parent.parent
    base = cwd / 'data'
    target = base / "inputs" / "0508.tif"
    target2 = base / "inputs" / "0826.tif"

    out2 = base / "inputs" / "1" / "source.tif"
    out = base / "inputs" / "1" / "target.tif"

    out = base / "outputs" / "1" / "result.tif"
    
    # with rasterio.open(out2) as src, rasterio.open(out) as src2:
    #     data2 = src.read()
    #     data = src2.read()

    #     data = np.where(data2 == 0, data, data2)

    #     img = Image.fromarray(np.moveaxis(data, 0, -1))
    #     img = img.resize((500,500))
    #     img.save(base / "example" / "naive.jpg")
    #     plt.imshow(img)
    #     plt.show()

    with rasterio.open(out) as src:
        data = src.read()


        img = Image.fromarray(np.moveaxis(data, 0, -1))
        img = img.resize((500,500))
        img.save(base / "example" / "result.jpg")
        plt.imshow(img)
        plt.show()


    # sys.exit()
    # with rasterio.open(target) as src, rasterio.open(target2) as src2:

    #     # Iterate over the windows and compute over each window sequentially
    #     for (i, j), window in src.block_windows(1):
    #         if (i, j) == (3, 3):

    #             data2 = src.read(window=window)
    #             data = src2.read(window=window)
                
    #             channels, height, width = data.shape

    #             # data[:, height//2:height, width//2:width] = 0
    #             data2[:, :, :width//2] = 0
    #             # data2[:, :height//2, :] = 0

    #             # calculate the new bounds
    #             profile = src.profile
    #             src_bounds = bounds(window, transform=profile["transform"])

    #             transform = Affine(profile["transform"][0], profile["transform"][1], src_bounds[0], 
    #                                profile["transform"][3], profile["transform"][4], src_bounds[-1])
    #             profile.update(width=width, height=height, transform=transform, tiles=False)

    #             # with rasterio.open(out, 'w', **profile) as dst, rasterio.open(out2, 'w', **profile) as dst2:
    #             #     dst.write(data)
    #             #     dst2.write(data2)

    #             # print(transform)


    #             data = np.where(data2 == 0, data, data2)
                
    #             # plt.imshow(np.moveaxis(data, 0, -1))
    #             # plt.show()

    #             plt.imshow(np.moveaxis(data, 0, -1))
    #             plt.show()