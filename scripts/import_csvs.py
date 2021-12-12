import pandas as pd
from pathlib import Path
from geoalchemy2 import Geometry, WKTElement

from helpers import get_dvrpc_polygon, clip_df_to_region, extract_zipfile, engine, DOWNLOAD_FOLDER


def import_single_zip_file(zipped_filepath: Path) -> None:

    # SHOULD CHECK FIRST TO SEE IF ANY ROWS EXIST WITH THIS DATE IN THE DB!

    # unzip single file
    unzipped_filepath = extract_zipfile(zipped_filepath)

    # read csv as tabular dataframe
    print("\t -> Reading full CSV")
    df = pd.read_csv(unzipped_filepath)

    # spatialize dataframe and clip it
    print("\t -> Clipping spatialized CSV to region")
    dvrpc_polygon = get_dvrpc_polygon()
    clipped_gdf = clip_df_to_region(df, dvrpc_polygon)

    # convert shapely geometry to WKT
    print("\t -> Writing to database")
    clipped_gdf["geom"] = clipped_gdf["geometry"].apply(lambda x: WKTElement(x.wkt, srid=4326))
    clipped_gdf.drop(
        labels="geometry",
        axis=1,
        inplace=True,
    )

    print(clipped_gdf.shape)

    # Make a name for the table in the database: use a single table for each year
    sql_tablename = "ais_" + unzipped_filepath.stem.split("_")[1]

    # Write to databae
    clipped_gdf.to_sql(
        sql_tablename,
        engine,
        schema="raw_data",
        dtype={"geom": Geometry("POINT", srid=4326)},
        index=False,
        if_exists="append",
    )

    # Delete CSV
    print("\t -> Deleting CSV")
    unzipped_filepath.unlink()


if __name__ == "__main__":
    print(DOWNLOAD_FOLDER)

    zipfiles_to_process = sorted(list(DOWNLOAD_FOLDER.rglob("2019/*.zip")))

    for zipfilepath in zipfiles_to_process:
        print(zipfilepath)
        import_single_zip_file(zipfilepath)
