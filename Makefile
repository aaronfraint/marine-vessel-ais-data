# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

all:
	@echo Makefile for marine-vessel-ais-data
	@echo -----------------------------------
	@echo Commands include:
	@echo "\t >" make year=2021 download
	@echo "\t >" make year=2021 import


download:
	cd ${DOWNLOAD_FOLDER} &&  wget -np -r -nH -L --cut-dirs=3 https://coast.noaa.gov/htdata/CMSP/AISDataHandler/$(year)/ 

import:
	python ./scripts/import_csvs.py ${year}
