import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon


def clip_df_to_region(df: pd.DataFrame, clipping_shape: Polygon) -> gpd.GeoDataFrame:
    """
    Turn a non-spatial dataframe with lon/lat columns into a point geodataframe,
    and then clip it to the provided `clipping_shape`.

    Return as a filtered geodataframe
    """
    data_gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["lon"], df["lat"], crs="EPSG:4326")
    )
    return data_gdf[data_gdf.intersects(clipping_shape)]
