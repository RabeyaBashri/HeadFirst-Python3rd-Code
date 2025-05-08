#RUN %pip install pandas lxml --upgrade

import pandas as pd
import json

#URL to scrape
URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"

#table index/serial number on that wiki page
TABLE_INDEX_WIKI=(0,1,3,4)

COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
UPDATED_WIKI_RECORDS_FILE_LOCATION = ""
UPDATED_WIKI_RECORDS_FILE_NAME = "wikiSwimmingRecordspandas.json"
UPDATED_WIKI_RECORDS_FILE_FULL_PATH = f"{UPDATED_WIKI_RECORDS_FILE_LOCATION}{UPDATED_WIKI_RECORDS_FILE_NAME}"

#get only tables (Pandas works with only table and turn each table into dataframe while scraping)
tables = pd.read_html(URL)

#dictionary of dictionary
wiki_records = {}

for tableIndex, course in zip(TABLE_INDEX_WIKI, COURSES):
   #get dataframe by selecting required two column 
   df = tables[tableIndex][["Event","Time"]]

   #skip relay values from the dataframe
   df = df[~df["Event"].str.contains("relay")]

   #reshape dataframe by adding Event column as index 
   df = df.set_index("Event")

   wiki_records[course] = df.to_dict()["Time"]

#SAVE wiki_records dictionary INTO UPDATED_WIKI_RECORDS_FILE_NAME
with open(UPDATED_WIKI_RECORDS_FILE_FULL_PATH,"w") as jsonFile:
    json.dump(wiki_records,jsonFile)




