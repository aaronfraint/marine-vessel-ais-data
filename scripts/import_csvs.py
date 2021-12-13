import sys
import pandas as pd
import geopandas as gpd
from pathlib import Path
from sqlalchemy import sql
from tqdm import tqdm
from geoalchemy2 import Geometry, WKTElement

from helpers import (
    get_dvrpc_polygon,
    clip_df_to_region,
    extract_zipfile,
    ENGINE,
    DOWNLOAD_FOLDER,
    days_in_table,
    print_message_and_timer,
)


@print_message_and_timer("Reading raw CSV")
def read_csv(unzipped_filepath: Path) -> pd.DataFrame:
    """
    - Read the raw CSV using a subset of the columns
    - Transform column names to lower case
    """
    df = pd.read_csv(
        unzipped_filepath,
        usecols=[
            "BaseDateTime",
            "LAT",
            "LON",
            "SOG",
            "VesselName",
            "VesselType",
            "Status",
            "Length",
            "Width",
            "Draft",
            "Cargo",
        ],
    )

    df.columns = [x.lower() for x in df.columns]

    return df


@print_message_and_timer("Deleting CSV")
def delete_csv(filepath: Path) -> None:
    """
    Delete the provided filepath
    """
    filepath.unlink()


@print_message_and_timer("Importing to db")
def import_to_db(clipped_gdf: gpd.GeoDataFrame, sql_tablename: str) -> None:
    """
    Import a GeoDataFrame to Postgres by:
        - Create a WKT of shapely geometry in new 'geom' column
        - Drop the shapely 'geometry' column
        - Import to postgres as POINT/4326, appending to table if it already exists
    """
    clipped_gdf["geom"] = clipped_gdf["geometry"].apply(lambda x: WKTElement(x.wkt, srid=4326))
    clipped_gdf.drop(
        labels="geometry",
        axis=1,
        inplace=True,
    )

    # Write to databae
    clipped_gdf.to_sql(
        sql_tablename,
        ENGINE,
        schema="raw_data",
        dtype={"geom": Geometry("POINT", srid=4326)},
        index=False,
        if_exists="append",
    )


def import_single_zip_file(zipped_filepath: Path, sql_tablename: str) -> None:
    """
    All business logic needed to transform a zipped data file into
    rows in a postgres/postgis database table. This will use a tablename
    that uses the year with a prefix of 'ais_'. e.g. 'ais_2019`

    - Unzip file to CSV
    - Clip spatialized CSV to DVRPC region
    - Transform geometries from shapely to WKT
    - Import into database
    - Delete CSV (but not the zip file)
    """

    # unzip single file
    unzipped_filepath = extract_zipfile(zipped_filepath)

    # read csv as tabular dataframe
    df = read_csv(unzipped_filepath)

    # spatialize dataframe and clip it
    dvrpc_polygon = get_dvrpc_polygon()
    clipped_gdf = clip_df_to_region(df, dvrpc_polygon)

    # import to database
    import_to_db(clipped_gdf, sql_tablename)

    # delete unzipped CSV
    delete_csv(unzipped_filepath)


def import_a_year_of_files(year: int) -> None:
    """
    - Find all ZIP files underneath a folder for a specific year
    - Identify the files that haven't been imported yet
    - Import all files that haven't been imported yet
    """
    print(f"IMPORTING ALL ZIP FILES FOR {year}")

    all_zipfiles = sorted(list(DOWNLOAD_FOLDER.rglob(f"{year}/*.zip")))

    sql_tablename = f"raw_data.ais_{year}"
    days_that_were_previously_imported = days_in_table(sql_tablename)

    zipfiles_to_process = [
        x
        for x in all_zipfiles
        if x.stem.replace("_", "-").replace("AIS-", "") not in days_that_were_previously_imported
    ]

    for zipfilepath in tqdm(zipfiles_to_process):
        print(zipfilepath)

        sql_tablename = "ais_" + zipfilepath.stem.split("_")[1]

        import_single_zip_file(zipfilepath, sql_tablename)


if __name__ == "__main__":
    year = sys.argv[1]
    import_a_year_of_files(year)
