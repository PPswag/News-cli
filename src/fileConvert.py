import csv

def convertToCSV(dict):
    with open('scrapedData.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, dict.keys())
        w.writeheader()
        w.writerow(dict)
