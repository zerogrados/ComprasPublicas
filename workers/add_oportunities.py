''' This python script send queries to Datos Abiertos API defined and add
    the initial bussiness oportunities to the aplication DB.
'''

import psycopg2
import json
import requests
import datetime
import _thread

import database_connection as db



def get_request(date):
    # This method consult the API passing the date as aparameter to the query
    response = requests.get('https://www.datos.gov.co/resource/c82b-7jfi.json?fecha_de_cargue_en_el_secop=' +
                            date + '&estado_del_proceso=Convocado&$limit=1000')

    resp = response.json()
    
    for i in resp:
        db_connection = db.connect_database()
        # Connect to DB
        if db_connection:
            db.insert_oportunity_secop_i(db_connection, i)
            
        else:
            print('Cannot connect to database')

for day in range(3):
    # Check the API for each day since one month ago
    date = (datetime.datetime.today() -
            datetime.timedelta(days=day)).strftime('%m/%d/%Y')
    
    get_request(date)
    
    
    

    
    
    
