import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon


def clip_with_bbox(
    df: pd.DataFrame,
    longitude_column: str = "lon",
    latitude_column: str = "lat",
    lon_min: float = -76.13660237,
    lon_max: float = -74.3897055,
    lat_min: float = 39.51487271,
    lat_max: float = 40.60855931,
) -> pd.DataFrame:
    """
    Use a non-spatial bounding box filter on a tabular
    dataframe with lat and long columns.
    """

    return df[
        (df[longitude_column].between(lon_min, lon_max))
        & (df[latitude_column].between(lat_min, lat_max))
    ]


def clip_df_to_region(df: pd.DataFrame, clipping_shape: Polygon) -> gpd.GeoDataFrame:
    """
    Turn a non-spatial dataframe with lon/lat columns into a point geodataframe,
    and then clip it to the provided `clipping_shape`.

    Return as a filtered geodataframe
    """
    data_in_bbox = clip_with_bbox(df)

    data_gdf = gpd.GeoDataFrame(
        data_in_bbox,
        geometry=gpd.points_from_xy(data_in_bbox["lon"], data_in_bbox["lat"], crs="EPSG:4326"),
    )
    return data_gdf[data_gdf.intersects(clipping_shape)]
