import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# NAIP FALSE COLOR COMPOSITE (NIR-Red-Green)
# ============================================

naip_path = r"C:\Users\ashy\Documents\lab1\DATA\NAIP\m_3508050_nw_17_060_20220602.tif"

# Open and read bands
with rasterio.open(naip_path) as src:
    # NAIP band order: Red(1), Green(2), Blue(3), NIR(4)
    red = src.read(1).astype(np.float32)
    green = src.read(2).astype(np.float32)
    nir = src.read(4).astype(np.float32)  # NIR is band 4

# Stack as NIR-Red-Green for false color
false_color = np.dstack((nir, red, green))

# Normalize if needed
if false_color.max() > 1:
    false_color = false_color / 255.0

# Percentile stretch (2–98%)
p2 = np.percentile(false_color, 2)
p98 = np.percentile(false_color, 98)

false_color_stretched = np.clip((false_color - p2) / (p98 - p2), 0, 1)

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(false_color_stretched)
plt.title("NAIP False Color (NIR-Red-Green, 2-98% stretch)\n0.6m resolution, June 2022")
plt.axis("off")

plt.savefig("naip_false_color.png", dpi=300, bbox_inches="tight")
plt.show()