import rasterio
import pandas as pd
from datetime import datetime

# ============================================
# METADATA EXTRACTION FOR ALL DATASETS
# ============================================

# File paths
sentinel2_path = r"C:\Users\ashy\Documents\lab1\DATA\SENTINEL_2\S2B_MSIL2A_20260120T161509_N0511_R140_T17SNV_20260120T182204.SAFE\GRANULE\L2A_T17SNV_A046355_20260120T161812\IMG_DATA\R10m\needed bands\B04_10m.jp2"
naip_path = r"C:\Users\ashy\Documents\lab1\DATA\NAIP\m_3508050_nw_17_060_20220602.tif"
landsat_path = r"C:\Users\ashy\Documents\lab1\DATA\LANDSAT\LC08_L1TP_017036_20260101_20260106_02_T1_B4.TIF"

# ============================================
# SENTINEL-2 METADATA
# ============================================
print("=" * 60)
print("SENTINEL-2 METADATA")
print("=" * 60)

with rasterio.open(sentinel2_path) as src:
    # Acquisition date (from filename)
    s2_date = "2026-01-20"
    
    # Spatial resolution
    s2_res = src.res[0]  # meters
    
    # Spectral bands
    s2_bands = "13 bands (B1-B12, B8A)"
    s2_bands_used = "B2 (Blue), B3 (Green), B4 (Red), B8 (NIR)"
    
    # Radiometric resolution
    s2_bit_depth = "12-bit"  # Sentinel-2 Level-2A
    
    # CRS
    s2_crs = src.crs
    
    # Temporal resolution
    s2_temporal = "5 days (with both satellites)"
    
    print(f"Acquisition Date: {s2_date}")
    print(f"Spatial Resolution: {s2_res} m")
    print(f"Total Bands: {s2_bands}")
    print(f"Bands Used: {s2_bands_used}")
    print(f"Bit Depth: {s2_bit_depth}")
    print(f"CRS: {s2_crs}")
    print(f"Temporal Resolution: {s2_temporal}")
    print(f"Image Dimensions: {src.width} x {src.height} pixels")
    print(f"Data Type: {src.dtypes[0]}")

# ============================================
# NAIP METADATA
# ============================================
print("\n" + "=" * 60)
print("NAIP METADATA")
print("=" * 60)

with rasterio.open(naip_path) as src:
    # Acquisition date (from filename: 20220602)
    naip_date = "2022-06-02"
    
    # Spatial resolution
    naip_res = src.res[0]
    
    # Spectral bands
    naip_bands = f"{src.count} bands"
    if src.count == 4:
        naip_bands_used = "Red, Green, Blue, NIR"
    else:
        naip_bands_used = "Red, Green, Blue"
    
    # Radiometric resolution
    naip_bit_depth = "8-bit"  # NAIP is typically 8-bit
    
    # CRS
    naip_crs = src.crs
    
    # Temporal resolution
    naip_temporal = "730-1095 days (2-3 years)"
    
    print(f"Acquisition Date: {naip_date}")
    print(f"Spatial Resolution: {naip_res} m")
    print(f"Total Bands: {naip_bands}")
    print(f"Bands Used: {naip_bands_used}")
    print(f"Bit Depth: {naip_bit_depth}")
    print(f"CRS: {naip_crs}")
    print(f"Temporal Resolution: {naip_temporal}")
    print(f"Image Dimensions: {src.width} x {src.height} pixels")
    print(f"Data Type: {src.dtypes[0]}")

# ============================================
# LANDSAT 8 METADATA
# ============================================
print("\n" + "=" * 60)
print("LANDSAT 8 OLI METADATA")
print("=" * 60)

with rasterio.open(landsat_path) as src:
    # Acquisition date (from filename: 20260101)
    landsat_date = "2026-01-01"
    
    # Spatial resolution
    landsat_res = src.res[0]
    
    # Spectral bands
    landsat_bands = "11 bands (B1-B11)"
    landsat_bands_used = "B2 (Blue), B3 (Green), B4 (Red), B5 (NIR)"
    
    # Radiometric resolution
    landsat_bit_depth = "16-bit"  # Landsat Level-1 is 16-bit
    
    # CRS
    landsat_crs = src.crs
    
    # Temporal resolution
    landsat_temporal = "16 days"
    
    print(f"Acquisition Date: {landsat_date}")
    print(f"Spatial Resolution: {landsat_res} m")
    print(f"Total Bands: {landsat_bands}")
    print(f"Bands Used: {landsat_bands_used}")
    print(f"Bit Depth: {landsat_bit_depth}")
    print(f"CRS: {landsat_crs}")
    print(f"Temporal Resolution: {landsat_temporal}")
    print(f"Image Dimensions: {src.width} x {src.height} pixels")
    print(f"Data Type: {src.dtypes[0]}")

# ============================================
# CREATE METADATA TABLE
# ============================================
metadata = {
    'Sensor': ['Sentinel-2 MSI', 'NAIP', 'Landsat 8 OLI'],
    'Date': ['2026-01-20', '2022-06-02', '2026-01-01'],
    'Spatial Res (m)': [10, 0.6, 30],
    'Bands Used': ['B2, B3, B4, B8', 'R, G, B, NIR', 'B2, B3, B4, B5'],
    'Bit Depth': ['12-bit', '8-bit', '16-bit'],
    'CRS': [str(s2_crs), str(naip_crs), str(landsat_crs)],
    'Temporal Res (days)': [5, '730-1095', 16]
}

df = pd.DataFrame(metadata)

print("\n" + "=" * 60)
print("METADATA COMPARISON TABLE")
print("=" * 60)
print(df.to_string(index=False))

# Save to CSV
df.to_csv('metadata_table.csv', index=False)
print("\nMetadata table saved to 'metadata_table.csv'")

# ============================================
# DETAILED BAND INFORMATION
# ============================================
print("\n" + "=" * 60)
print("DETAILED SPECTRAL BAND INFORMATION")
print("=" * 60)

print("\nSentinel-2 MSI Bands Used:")
print("  B2 (Blue): 490 nm, 10m resolution")
print("  B3 (Green): 560 nm, 10m resolution")
print("  B4 (Red): 665 nm, 10m resolution")
print("  B8 (NIR): 842 nm, 10m resolution")

print("\nNAIP Bands:")
print("  Band 1 (Red): ~630-680 nm, 0.6m resolution")
print("  Band 2 (Green): ~510-590 nm, 0.6m resolution")
print("  Band 3 (Blue): ~450-520 nm, 0.6m resolution")
print("  Band 4 (NIR): ~760-900 nm, 0.6m resolution")

print("\nLandsat 8 OLI Bands Used:")
print("  B2 (Blue): 450-510 nm, 30m resolution")
print("  B3 (Green): 530-590 nm, 30m resolution")
print("  B4 (Red): 640-670 nm, 30m resolution")
print("  B5 (NIR): 850-880 nm, 30m resolution")