import os
import json

with open('colombia.json') as jsonfile:
    colombia = json.load(jsonfile)
    id_department = 1000
    cities = []
    zones = []
    for deparment in colombia:
        id_city = id_department + 1
        for city in deparment['ciudades']:
            cities.append({"id": str(id_city), "title": city})
            id_city += 1
        departamento = {
            "id": str(id_department), "title": deparment['departamento'], "subs": cities}
        zones.append(departamento)
        cities = []        
        id_department += 1000

        #deparment['id'] = str(id_department)
        #id_city = id_department + 1
        # for city in deparment['ciudades']:
        #    ciudad = dict()
        #    ciudad['title'] = city
        #    ciudad['id'] = str(id_city)
        #    id_city += 1
        #
        #id_department += 1000

    print(zones)
