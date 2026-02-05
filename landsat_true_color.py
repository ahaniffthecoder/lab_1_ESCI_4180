import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# LANDSAT 8 TRUE COLOR COMPOSITE - IMPROVED
# ============================================

# Paths to RGB bands
blue_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B2.TIF"
green_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B3.TIF"
red_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B4.TIF"

# Open bands
with rasterio.open(red_path) as src:
    red = src.read(1).astype(np.float32)
    print(f"Red - min: {red.min()}, max: {red.max()}, mean: {red.mean()}")

with rasterio.open(green_path) as src:
    green = src.read(1).astype(np.float32)
    print(f"Green - min: {green.min()}, max: {green.max()}, mean: {green.mean()}")

with rasterio.open(blue_path) as src:
    blue = src.read(1).astype(np.float32)
    print(f"Blue - min: {blue.min()}, max: {blue.max()}, mean: {blue.mean()}")

# Stack bands (RGB)
rgb = np.dstack((red, green, blue))

# Method 1: Stretch each band independently (better color balance)
def stretch_band(band):
    """Stretch individual band using percentiles on valid data"""
    valid = band[band > 0]
    if len(valid) > 0:
        p2 = np.percentile(valid, 2)
        p98 = np.percentile(valid, 98)
        stretched = np.clip((band - p2) / (p98 - p2 + 1e-8), 0, 1)
        return stretched
    else:
        return band / (band.max() + 1e-8)

# Stretch each band independently
red_stretched = stretch_band(red)
green_stretched = stretch_band(green)
blue_stretched = stretch_band(blue)

# Stack stretched bands
rgb_stretched = np.dstack((red_stretched, green_stretched, blue_stretched))

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(rgb_stretched)
plt.title("Landsat 8 OLI True Color (RGB, per-band 2-98% stretch)\n30m resolution, January 1, 2026")
plt.axis("off")

plt.savefig("landsat8_true_color.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nLandsat 8 true color composite saved!")