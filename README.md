# marine-vessel-ais-data

Scripts to facilitate the download, extraction, and usage of data from https://marinecadastre.gov/ais/

## Requirements

- `make` is used to faciliate running commands. It's not required, but will make your life easier.
- `wget` is required to download the data
- `conda` is needed to run the python scripts
- You also need a `postgres` cluster that you can write to. The database should already exist and have the PostGIS extension enabled.

## Setup

Create the Python environment via:

```
conda env create -f environment.yml
```

Create a `.env` file at the top-level of this codebase, with the following keys defined:

```
DOWNLOAD_FOLDER=/your/path/to/a/folder/with/lots/of/space
LOCAL_DB_URL=postgresql://user:password@your-host/your-database
```

## Usage

Before you can use any of the `make` commands, you need to activate your Python environment with:

```
conda activate marine-vessel-ais-data
```

To download a year's worth of zipped data files, run:

```
make year=2019 download
```

To import these files into Postgres/PostGIS, run:

```
make year=2019 import
```

## To Do

- [ ] Add a `publish` step to push a table to a remote database

- [ ] Add process to check if a file has already been imported before importing it

- [ ] Add a time profiler, and potentially optimize?
