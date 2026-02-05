import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# LANDSAT 8 FALSE COLOR COMPOSITE (NIR-Red-Green)
# ============================================

# Paths to NIR, Red, Green bands
green_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B3.TIF"
red_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B4.TIF"
nir_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B5.TIF"

# Open bands
with rasterio.open(nir_path) as src:
    nir = src.read(1).astype(np.float32)

with rasterio.open(red_path) as src:
    red = src.read(1).astype(np.float32)

with rasterio.open(green_path) as src:
    green = src.read(1).astype(np.float32)

# Stack bands as NIR-Red-Green for false color
false_color = np.dstack((nir, red, green))

# Percentile stretch on valid data
valid_pixels = false_color[false_color > 0]

if len(valid_pixels) > 0:
    # Percentile stretch (2–98%)
    p2 = np.percentile(valid_pixels, 2)
    p98 = np.percentile(valid_pixels, 98)
    
    print(f"Landsat false color percentiles: p2={p2:.1f}, p98={p98:.1f}")
    
    false_color_stretched = np.clip((false_color - p2) / (p98 - p2 + 1e-8), 0, 1)
else:
    # Fallback
    false_color_stretched = false_color / false_color.max()

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(false_color_stretched)
plt.title("Landsat 8 OLI False Color (NIR-Red-Green, 2-98% stretch)\n30m resolution, January 1, 2026")
plt.axis("off")

plt.savefig("landsat8_false_color.png", dpi=300, bbox_inches="tight")
plt.show()

print("Landsat 8 false color composite saved!")