# Lab 1 – Remote Sensing Starter Script
# Dataset: Sentinel-2 (example)
# AOI: Charlotte, NC

import rasterio
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Confirm Python + libraries
# -----------------------------
print("Rasterio version:", rasterio.__version__)
print("NumPy version:", np.__version__)

# -----------------------------
# 2. Path to ONE raster band
# (update filename as needed)
# -----------------------------
band_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B02_10m.jp2"
# Sentinel-2 Red band (10 m)

# -----------------------------
# 3. Open raster and read data
# -----------------------------
with rasterio.open(band_path) as src:
    band = src.read(1)
    crs = src.crs
    transform = src.transform
    dtype = band.dtype
    bounds = src.bounds
    res = src.res

# -----------------------------
# 4. Print metadata (Part 2)
# -----------------------------
print("\n--- Metadata ---")
print("CRS:", crs)
print("Resolution (m):", res)
print("Data type:", dtype)
print("Raster shape (rows, cols):", band.shape)
print("Bounds:", bounds)

# -----------------------------
# 5. Simple visualization
# -----------------------------
plt.figure(figsize=(6, 6))
plt.imshow(band, cmap="gray")
plt.colorbar(label="Pixel Value")
plt.title("Sentinel-2 Red Band (B04)")
plt.axis("off")
plt.tight_layout()
plt.show()
