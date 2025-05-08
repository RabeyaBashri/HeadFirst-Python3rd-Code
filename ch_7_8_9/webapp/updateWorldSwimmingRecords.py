#RUN %pip install gazpacho --upgrade

import gazpacho
import json

#URL to scrape
URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"

#table index/serial number on that wiki page
TABLE_INDEX_WIKI=(0,1,3,4)

COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
UPDATED_WIKI_RECORDS_FILE_LOCATION = ""
UPDATED_WIKI_RECORDS_FILE_NAME = "wikiSwimmingRecords.json"
UPDATED_WIKI_RECORDS_FILE_FULL_PATH = f"{UPDATED_WIKI_RECORDS_FILE_LOCATION}{UPDATED_WIKI_RECORDS_FILE_NAME}"

#get entire html page
html = gazpacho.get(URL)

#get each dom element as soup from html
soup = gazpacho.Soup(html)

#get only tables from entire soup list
tables = soup.find("table")

#dictionary of dictionary
wiki_records = {}

for tableIndex, course in zip(TABLE_INDEX_WIKI, COURSES):
    #initialize outer dictionary key (course) with an emtpy inner dictionary as value
    wiki_records[course] = {}

    # nested for loop to iterate through current table's rows (rows started by skipping head column row [1:])
    for row in tables[tableIndex].find("tr")[1:] :
        #find columns for this current row
        columns = row.find("td")
        eventCellValue = columns[0].text
        timeCellValue = columns[1].text

        #skip relay values while storing cell values in inner wiki_records dictionary 
        if "relay" not in eventCellValue:
            wiki_records[course][eventCellValue]=timeCellValue

#SAVE wiki_records dictionary INTO UPDATED_WIKI_RECORDS_FILE_NAME
with open(UPDATED_WIKI_RECORDS_FILE_FULL_PATH,"w") as jsonFile:
    json.dump(wiki_records,jsonFile)




