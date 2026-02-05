import rasterio
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# PART 4: QUANTITATIVE AND QUALITATIVE COMPARISONS
# Sentinel-2 vs NAIP (FIXED VERSION)
# ============================================

# File paths
s2_red_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B04_10m.jp2"
s2_green_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B03_10m.jp2"
s2_blue_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B02_10m.jp2"
s2_nir_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B08_10m.jp2"

naip_path = r"C:\Users\ashy\Documents\lab1\DATA\NAIP\m_3508050_nw_17_060_20220602.tif"

# ============================================
# LOAD SENTINEL-2 DATA
# ============================================
print("Loading Sentinel-2 data...")
with rasterio.open(s2_red_path) as src:
    s2_red = src.read(1).astype(np.float32)
    s2_shape = s2_red.shape
    
with rasterio.open(s2_green_path) as src:
    s2_green = src.read(1).astype(np.float32)
    
with rasterio.open(s2_blue_path) as src:
    s2_blue = src.read(1).astype(np.float32)
    
with rasterio.open(s2_nir_path) as src:
    s2_nir = src.read(1).astype(np.float32)

print(f"Sentinel-2 shape: {s2_shape}")

# ============================================
# LOAD NAIP DATA
# ============================================
print("Loading NAIP data...")
with rasterio.open(naip_path) as src:
    naip_red = src.read(1).astype(np.float32)
    naip_green = src.read(2).astype(np.float32)
    naip_blue = src.read(3).astype(np.float32)
    naip_nir = src.read(4).astype(np.float32)
    naip_shape = naip_red.shape
    
    # Normalize NAIP (8-bit to 0-1 range)
    if naip_red.max() > 1:
        naip_red = naip_red / 255.0
        naip_green = naip_green / 255.0
        naip_blue = naip_blue / 255.0
        naip_nir = naip_nir / 255.0

print(f"NAIP shape: {naip_shape}")
print("Data loaded successfully!\n")

# ============================================
# COMPARISON 1: HISTOGRAM COMPARISON
# ============================================
print("Creating histogram comparisons...")

# Filter out zeros for Sentinel-2
s2_red_valid = s2_red[s2_red > 0]
s2_nir_valid = s2_nir[s2_nir > 0]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Sentinel-2 Red
axes[0, 0].hist(s2_red_valid.flatten(), bins=100, color='red', alpha=0.7, edgecolor='black')
axes[0, 0].set_title('Sentinel-2 Red Band Histogram (10m)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Pixel Value')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].grid(True, alpha=0.3)

# NAIP Red
axes[0, 1].hist(naip_red.flatten(), bins=100, color='red', alpha=0.7, edgecolor='black')
axes[0, 1].set_title('NAIP Red Band Histogram (0.6m)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Pixel Value')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].grid(True, alpha=0.3)

# Sentinel-2 NIR
axes[1, 0].hist(s2_nir_valid.flatten(), bins=100, color='darkred', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('Sentinel-2 NIR Band Histogram (10m)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Pixel Value')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].grid(True, alpha=0.3)

# NAIP NIR
axes[1, 1].hist(naip_nir.flatten(), bins=100, color='darkred', alpha=0.7, edgecolor='black')
axes[1, 1].set_title('NAIP NIR Band Histogram (0.6m)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Pixel Value')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('comparison1_histogram.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Histogram comparison saved\n")

# ============================================
# COMPARISON 2: NDVI CALCULATION AND COMPARISON
# ============================================
print("Calculating NDVI for both sensors...")

# Sentinel-2 NDVI (mask out zeros)
s2_ndvi = np.where((s2_nir > 0) & (s2_red > 0), 
                   (s2_nir - s2_red) / (s2_nir + s2_red + 1e-8),
                   np.nan)

# NAIP NDVI
naip_ndvi = (naip_nir - naip_red) / (naip_nir + naip_red + 1e-8)

# Print statistics
print("SENTINEL-2 NDVI Statistics:")
print(f"  Min: {np.nanmin(s2_ndvi):.3f}")
print(f"  Max: {np.nanmax(s2_ndvi):.3f}")
print(f"  Mean: {np.nanmean(s2_ndvi):.3f}")
print(f"  Std Dev: {np.nanstd(s2_ndvi):.3f}\n")

print("NAIP NDVI Statistics:")
print(f"  Min: {np.nanmin(naip_ndvi):.3f}")
print(f"  Max: {np.nanmax(naip_ndvi):.3f}")
print(f"  Mean: {np.nanmean(naip_ndvi):.3f}")
print(f"  Std Dev: {np.nanstd(naip_ndvi):.3f}\n")

# Plot NDVI comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Sentinel-2 NDVI
im1 = axes[0].imshow(s2_ndvi, cmap='RdYlGn', vmin=-0.2, vmax=0.8)
axes[0].set_title('Sentinel-2 NDVI (10m resolution)', fontsize=12, fontweight='bold')
axes[0].axis('off')
plt.colorbar(im1, ax=axes[0], label='NDVI Value', shrink=0.8)

# NAIP NDVI
im2 = axes[1].imshow(naip_ndvi, cmap='RdYlGn', vmin=-0.2, vmax=0.8)
axes[1].set_title('NAIP NDVI (0.6m resolution)', fontsize=12, fontweight='bold')
axes[1].axis('off')
plt.colorbar(im2, ax=axes[1], label='NDVI Value', shrink=0.8)

plt.tight_layout()
plt.savefig('comparison2_ndvi.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ NDVI comparison saved\n")

# ============================================
# COMPARISON 3: SCATTER PLOT (NIR vs RED)
# ============================================
print("Creating scatter plot comparisons...")

# Sample data to avoid overplotting
sample_rate = 20

# Sentinel-2: only use valid pixels
s2_valid_mask = (s2_red > 0) & (s2_nir > 0)
s2_red_sample = s2_red[s2_valid_mask][::sample_rate]
s2_nir_sample = s2_nir[s2_valid_mask][::sample_rate]

naip_red_sample = naip_red[::sample_rate, ::sample_rate].flatten()
naip_nir_sample = naip_nir[::sample_rate, ::sample_rate].flatten()

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Sentinel-2 scatter
axes[0].scatter(s2_red_sample, s2_nir_sample, alpha=0.3, s=1, c='blue')
axes[0].set_xlabel('Red Band Reflectance', fontsize=11)
axes[0].set_ylabel('NIR Band Reflectance', fontsize=11)
axes[0].set_title('Sentinel-2: NIR vs Red (10m)', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)
max_s2 = max(s2_red_sample.max(), s2_nir_sample.max())
axes[0].plot([0, max_s2], [0, max_s2], 'r--', label='NIR = Red', linewidth=2)
axes[0].legend(loc='upper left')

# NAIP scatter
axes[1].scatter(naip_red_sample, naip_nir_sample, alpha=0.3, s=1, c='green')
axes[1].set_xlabel('Red Band Reflectance', fontsize=11)
axes[1].set_ylabel('NIR Band Reflectance', fontsize=11)
axes[1].set_title('NAIP: NIR vs Red (0.6m)', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)
max_naip = max(naip_red_sample.max(), naip_nir_sample.max())
axes[1].plot([0, max_naip], [0, max_naip], 'r--', label='NIR = Red', linewidth=2)
axes[1].legend(loc='upper left')

plt.tight_layout()
plt.savefig('comparison3_scatter.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Scatter plot comparison saved\n")

# ============================================
# COMPARISON 4: SPATIAL DETAIL - AUTO-FIND VALID DATA
# ============================================
print("Creating spatial detail comparison...")

# Find valid data area in Sentinel-2
valid_s2_mask = (s2_red > 0) & (s2_green > 0) & (s2_blue > 0)
valid_rows, valid_cols = np.where(valid_s2_mask)

if len(valid_rows) > 1000:  # Need enough valid pixels
    # Find center of valid data
    s2_center_row = int(np.median(valid_rows))
    s2_center_col = int(np.median(valid_cols))
    
    print(f"Valid Sentinel-2 data center: row {s2_center_row}, col {s2_center_col}")
    
    # Take 400x400 crop around valid center
    s2_crop_size = 400
    s2_row_start = max(0, s2_center_row - s2_crop_size // 2)
    s2_row_end = min(s2_shape[0], s2_center_row + s2_crop_size // 2)
    s2_col_start = max(0, s2_center_col - s2_crop_size // 2)
    s2_col_end = min(s2_shape[1], s2_center_col + s2_crop_size // 2)
    
    # Create Sentinel-2 RGB crop
    s2_rgb_crop = np.dstack((
        s2_red[s2_row_start:s2_row_end, s2_col_start:s2_col_end],
        s2_green[s2_row_start:s2_row_end, s2_col_start:s2_col_end],
        s2_blue[s2_row_start:s2_row_end, s2_col_start:s2_col_end]
    ))
    
    # Stretch using only valid pixels
    valid_crop_pixels = s2_rgb_crop[s2_rgb_crop > 0]
    if len(valid_crop_pixels) > 100:
        p2_s2 = np.percentile(valid_crop_pixels, 2)
        p98_s2 = np.percentile(valid_crop_pixels, 98)
        
        print(f"Sentinel-2 crop percentiles: p2={p2_s2:.1f}, p98={p98_s2:.1f}")
        
        s2_rgb_stretched = np.clip((s2_rgb_crop - p2_s2) / (p98_s2 - p2_s2 + 1e-8), 0, 1)
        
        # NAIP crop from center
        naip_center_row = naip_shape[0] // 2
        naip_center_col = naip_shape[1] // 2
        naip_crop_size = 1500
        
        naip_row_start = max(0, naip_center_row - naip_crop_size // 2)
        naip_row_end = min(naip_shape[0], naip_center_row + naip_crop_size // 2)
        naip_col_start = max(0, naip_center_col - naip_crop_size // 2)
        naip_col_end = min(naip_shape[1], naip_center_col + naip_crop_size // 2)
        
        naip_rgb_crop = np.dstack((
            naip_red[naip_row_start:naip_row_end, naip_col_start:naip_col_end],
            naip_green[naip_row_start:naip_row_end, naip_col_start:naip_col_end],
            naip_blue[naip_row_start:naip_row_end, naip_col_start:naip_col_end]
        ))
        
        p2_naip, p98_naip = np.percentile(naip_rgb_crop, [2, 98])
        naip_rgb_stretched = np.clip((naip_rgb_crop - p2_naip) / (p98_naip - p2_naip + 1e-8), 0, 1)
        
        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        axes[0].imshow(s2_rgb_stretched)
        axes[0].set_title('Sentinel-2 Spatial Detail (10m resolution)\nUrban/vegetation features', 
                          fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        axes[1].imshow(naip_rgb_stretched)
        axes[1].set_title('NAIP Spatial Detail (0.6m resolution)\nIndividual features visible', 
                          fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        plt.tight_layout()
        plt.savefig('comparison4_spatial_detail.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Spatial detail comparison saved\n")
    else:
        print("ERROR: Not enough valid pixels in crop")
else:
    print("ERROR: No valid Sentinel-2 data found")

# ============================================
# SUMMARY
# ============================================
print("=" * 60)
print("PART 4 COMPLETE!")
print("=" * 60)
print("\nGenerated files:")
print("  1. comparison1_histogram.png")
print("  2. comparison2_ndvi.png")
print("  3. comparison3_scatter.png")
print("  4. comparison4_spatial_detail.png")