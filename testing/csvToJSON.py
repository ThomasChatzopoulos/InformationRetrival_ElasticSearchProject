import time
import csv, json
import codecs

print("wellcome to my channel *indian accent*")

csvFilePath = "movies.csv"
jsonFile = "myfile.json"

data = {}
with open(csvFilePath,encoding='utf8') as csvFile:
	csvReader = csv.DictReader(csvFile)
	for csvRow in csvReader:
		id = csvRow["movieId"]
		data[id] = csvRow
		
with open(jsonFile,"w",encoding="utf8") as jsonFile:
	jsonFile.write(json.dumps(data,indent=4))