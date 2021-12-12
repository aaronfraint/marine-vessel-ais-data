import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon


def get_dvrpc_polygon() -> Polygon:
    """
    Read the US Census' national county shapefile
    Filter out all counties except DVRPC's 9 counties
    Return a single dissolved shape as a shapely Polygon
    """
    counties = gpd.read_file(
        "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_500k.zip"
    )

    nj_counties = counties[
        (counties["STATEFP"] == "34")
        & (counties["NAME"].isin(["Camden", "Burlington", "Mercer", "Gloucester"]))
    ]
    pa_counties = counties[
        (counties["STATEFP"] == "42")
        & (counties["NAME"].isin(["Philadelphia", "Bucks", "Chester", "Delaware", "Montgomery"]))
    ]

    gdf = pd.concat([nj_counties, pa_counties]).dissolve().to_crs(4326)

    return gdf.at[0, "geometry"]
