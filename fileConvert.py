import csv
import json

def convertToCSV(dict):
    with open('scrapedData.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, dict.keys())
        w.writeheader()
        w.writerow(dict)

def convertToJSON(dict):
    with open('scrapedData.json', 'w') as f:
        json.dump(dict, f)
