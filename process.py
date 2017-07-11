import csv

headers = ['name','regionid','city','city_area','state','forecast_pct','forecast_rent_pct',' past_pct','past_rent_pct','rent_final_point','sale_rent_ratio','zestimate','market_health_index']

new_data = []

with open('raw.csv') as inputfile:
  with open('data.csv', 'w') as outputfile:
    reader = csv.DictReader(inputfile, delimiter=',', quotechar='"')
    writer = csv.DictWriter(outputfile, headers, quotechar='"')
    writer.writeheader()
    for row in reader:
      tmp = {}
      for header in headers:
        tmp[header] = row[header]
      new_data.append(tmp)
    writer.writerows(new_data)

