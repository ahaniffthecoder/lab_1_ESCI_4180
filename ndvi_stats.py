import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# CALCULATE NDVI STATISTICS FOR ALL 3 SENSORS
# ============================================

# File paths
# Sentinel-2
s2_red_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B04_10m.jp2"
s2_nir_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B08_10m.jp2"

# NAIP
naip_path = r"C:\Users\ashy\Documents\lab1\DATA\NAIP\m_3508050_nw_17_060_20220602.tif"

# Landsat 8
landsat_red_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B4.TIF"
landsat_nir_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B5.TIF"

print("=" * 70)
print("NDVI STATISTICS COMPARISON")
print("=" * 70)

# ============================================
# SENTINEL-2 NDVI
# ============================================
print("\n--- SENTINEL-2 MSI (10m, January 20, 2026) ---")

with rasterio.open(s2_red_path) as src:
    s2_red = src.read(1).astype(np.float32)
    
with rasterio.open(s2_nir_path) as src:
    s2_nir = src.read(1).astype(np.float32)

# Calculate NDVI, masking out zeros
s2_ndvi = np.where((s2_nir > 0) & (s2_red > 0), 
                   (s2_nir - s2_red) / (s2_nir + s2_red + 1e-8),
                   np.nan)

# Statistics (ignoring NaN values)
s2_min = np.nanmin(s2_ndvi)
s2_max = np.nanmax(s2_ndvi)
s2_mean = np.nanmean(s2_ndvi)
s2_std = np.nanstd(s2_ndvi)
s2_median = np.nanmedian(s2_ndvi)

print(f"  Minimum NDVI:  {s2_min:.3f}")
print(f"  Maximum NDVI:  {s2_max:.3f}")
print(f"  Mean NDVI:     {s2_mean:.3f}")
print(f"  Median NDVI:   {s2_median:.3f}")
print(f"  Std Deviation: {s2_std:.3f}")
print(f"  Valid pixels:  {np.sum(~np.isnan(s2_ndvi)):,}")

# ============================================
# NAIP NDVI
# ============================================
print("\n--- NAIP (0.6m, June 2, 2022) ---")

with rasterio.open(naip_path) as src:
    naip_red = src.read(1).astype(np.float32)
    naip_nir = src.read(4).astype(np.float32)
    
    # Normalize if 8-bit
    if naip_red.max() > 1:
        naip_red = naip_red / 255.0
        naip_nir = naip_nir / 255.0

# Calculate NDVI
naip_ndvi = (naip_nir - naip_red) / (naip_nir + naip_red + 1e-8)

# Statistics
naip_min = np.nanmin(naip_ndvi)
naip_max = np.nanmax(naip_ndvi)
naip_mean = np.nanmean(naip_ndvi)
naip_std = np.nanstd(naip_ndvi)
naip_median = np.nanmedian(naip_ndvi)

print(f"  Minimum NDVI:  {naip_min:.3f}")
print(f"  Maximum NDVI:  {naip_max:.3f}")
print(f"  Mean NDVI:     {naip_mean:.3f}")
print(f"  Median NDVI:   {naip_median:.3f}")
print(f"  Std Deviation: {naip_std:.3f}")
print(f"  Valid pixels:  {naip_ndvi.size:,}")

# ============================================
# LANDSAT 8 NDVI
# ============================================
print("\n--- LANDSAT 8 OLI (30m, January 1, 2026) ---")

with rasterio.open(landsat_red_path) as src:
    landsat_red = src.read(1).astype(np.float32)
    
with rasterio.open(landsat_nir_path) as src:
    landsat_nir = src.read(1).astype(np.float32)

# Calculate NDVI, masking out zeros
landsat_ndvi = np.where((landsat_nir > 0) & (landsat_red > 0), 
                        (landsat_nir - landsat_red) / (landsat_nir + landsat_red + 1e-8),
                        np.nan)

# Statistics
landsat_min = np.nanmin(landsat_ndvi)
landsat_max = np.nanmax(landsat_ndvi)
landsat_mean = np.nanmean(landsat_ndvi)
landsat_std = np.nanstd(landsat_ndvi)
landsat_median = np.nanmedian(landsat_ndvi)

print(f"  Minimum NDVI:  {landsat_min:.3f}")
print(f"  Maximum NDVI:  {landsat_max:.3f}")
print(f"  Mean NDVI:     {landsat_mean:.3f}")
print(f"  Median NDVI:   {landsat_median:.3f}")
print(f"  Std Deviation: {landsat_std:.3f}")
print(f"  Valid pixels:  {np.sum(~np.isnan(landsat_ndvi)):,}")

# ============================================
# SUMMARY COMPARISON TABLE
# ============================================
print("\n" + "=" * 70)
print("SUMMARY COMPARISON")
print("=" * 70)
print(f"\n{'Sensor':<20} {'Min':<10} {'Max':<10} {'Mean':<10} {'Std Dev':<10}")
print("-" * 70)
print(f"{'Sentinel-2 (10m)':<20} {s2_min:<10.3f} {s2_max:<10.3f} {s2_mean:<10.3f} {s2_std:<10.3f}")
print(f"{'NAIP (0.6m)':<20} {naip_min:<10.3f} {naip_max:<10.3f} {naip_mean:<10.3f} {naip_std:<10.3f}")
print(f"{'Landsat 8 (30m)':<20} {landsat_min:<10.3f} {landsat_max:<10.3f} {landsat_mean:<10.3f} {landsat_std:<10.3f}")

# ============================================
# INTERPRETATION GUIDE
# ============================================
print("\n" + "=" * 70)
print("INTERPRETATION GUIDE")
print("=" * 70)
print("\nNDVI Value Ranges:")
print("  0.6 to 1.0  → Dense, healthy vegetation (forests, crops)")
print("  0.2 to 0.6  → Moderate vegetation (grass, sparse trees)")
print(" -0.1 to 0.2  → Bare soil, urban areas, rocks")
print(" -1.0 to -0.1 → Water, clouds, snow")