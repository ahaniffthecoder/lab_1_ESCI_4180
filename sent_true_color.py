import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Paths to bands
blue_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B02_10m.jp2"
green_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B03_10m.jp2"
red_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B04_10m.jp2"

# Open bands
with rasterio.open(red_path) as red_src:
    red = red_src.read(1)

with rasterio.open(green_path) as green_src:
    green = green_src.read(1)

with rasterio.open(blue_path) as blue_src:
    blue = blue_src.read(1)

# Stack bands (RGB)
rgb = np.dstack((red, green, blue))

# Convert to float
rgb = rgb.astype(np.float32)

# Percentile stretch (2–98%)
p2 = np.percentile(rgb, 2)
p98 = np.percentile(rgb, 98)

rgb_stretched = np.clip((rgb - p2) / (p98 - p2), 0, 1)


# Plot #Figure 1 True Color Composite\
# Sentinel-2 MSI Level-2A surface reflectance
plt.figure(figsize=(8, 8))
plt.imshow(rgb_stretched)
plt.title("Sentinel-2 True Color (RGB, 2-98% stretch)")
plt.axis("off")

plt.savefig("sentinel2_true_color.png", dpi=300, bbox_inches="tight")
plt.show()

