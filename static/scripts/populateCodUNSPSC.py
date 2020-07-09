import psycopg2
from psycopg2 import sql
import os
import csv


def connectDB():
    try:
        connection = psycopg2.connect(user = os.environ.get('DBUSER', None),
                                      password = os.environ.get('DBPASS', None),
                                      host = os.environ.get('DBHOST', None),
                                      port = os.environ.get('DBPORT', None),
                                      database = os.environ.get('DBNAME', None))        

    except (Exception, psycopg2.Error) as error :        
        return None
    
    else:        
        return connection


def updateDB(connection):
    cursor = connection.cursor()
    with open('codigosUNSPSC.csv', newline='\n') as csvfile:
        read_data = csv.reader(csvfile, delimiter=';')
        for row in read_data:            
            for codigo in row:
                codigo.strip()
                try:
                    int(codigo)
                except:
                    pass
                else:                    
                    query = sql.SQL("SELECT codigo FROM accounts_codunspsc where codigo = '{}'".format(codigo))
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) == 0:
                        print('Inserta codigo ' + codigo)                    
                        query = sql.SQL("INSERT INTO accounts_codunspsc (codigo) VALUES ('{}')".format(codigo))
                        cursor.execute(query)
                        connection.commit()
                    else:
                        print('El codigo ' + codigo + ' ya existe')
    cursor.close()

def populateDB():
    connectionDB = connectDB()
    if connectionDB:
        updateDB(connectionDB)
        connectionDB.close()
    else:
        print('No se pudo establecer conexion a la base de datos')


populateDB()


