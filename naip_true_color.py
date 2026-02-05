import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# NAIP TRUE COLOR COMPOSITE
# ============================================

# Path to NAIP file (single multi-band TIF)
naip_path = r"C:\Users\ashy\Documents\lab1\DATA\NAIP\m_3508050_nw_17_060_20220602.tif"

# Open the file and read bands
with rasterio.open(naip_path) as src:
    print(f"NAIP has {src.count} bands")
    print(f"Data type: {src.dtypes[0]}")
    print(f"Image shape: {src.shape}")
    
    # NAIP band order: Red(1), Green(2), Blue(3), NIR(4)
    red = src.read(1).astype(np.float32)
    green = src.read(2).astype(np.float32)
    blue = src.read(3).astype(np.float32)

# Stack bands (RGB)
rgb = np.dstack((red, green, blue))

# NAIP is typically 8-bit (0-255), normalize to 0-1
if rgb.max() > 1:
    rgb = rgb / 255.0

# Percentile stretch (2–98%)
p2 = np.percentile(rgb, 2)
p98 = np.percentile(rgb, 98)

rgb_stretched = np.clip((rgb - p2) / (p98 - p2), 0, 1)

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(rgb_stretched)
plt.title("NAIP True Color (RGB, 2-98% stretch)\n0.6m resolution, June 2022")
plt.axis("off")

plt.savefig("naip_true_color.png", dpi=300, bbox_inches="tight")
plt.show()