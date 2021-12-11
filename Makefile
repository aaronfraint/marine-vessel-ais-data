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


download:
	cd ${DOWNLOAD_FOLDER} &&  wget -np -r -nH -L --cut-dirs=3 https://coast.noaa.gov/htdata/CMSP/AISDataHandler/$(year)/ 