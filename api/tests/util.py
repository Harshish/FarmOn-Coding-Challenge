import geopandas as gpd
from pathlib import Path
import rasterio

parcels_df = None
raw_data = None

def load_parcels_data():
    global parcels_df, raw_data
    raw_data = Path("../data/raw_data/")
    parcels_df = gpd.read_file(raw_data / "nl_parcels_subset_small.gpkg")

def add_centroid():
    parcels_df["centroid"] = parcels_df.apply(lambda row : row['geometry'].centroid , axis=1)

def add_soc_and_centroid():
    carbon_tif_path = raw_data / "soil_log_organic_carbon_content_2020.tif"
    with rasterio.open(carbon_tif_path) as f:
        raster_stats = f.statistics(bidx=1)

        add_centroid()
        centroid_list = parcels_df["centroid"]

        new_df = gpd.GeoDataFrame(geometry = centroid_list,crs=parcels_df.crs)
        new_df = new_df.to_crs(f.crs)

        coord_list = [(x, y) for x, y in zip(new_df["geometry"].x, new_df["geometry"].y)]
        parcels_df["soc"] = [raster_stats.max - x for x in f.sample(coord_list)]

def get_in_batch(st, end):
    if parcels_df is None:
        return None
    return parcels_df[st:end]