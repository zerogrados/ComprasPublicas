import psycopg2
from psycopg2 import sql
from psycopg2 import errors
import os
import json


def connectDB():
    try:
        connection = psycopg2.connect(user=os.environ.get('DBUSER', None),
                                      password=os.environ.get('DBPASS', None),
                                      host=os.environ.get('DBHOST', None),
                                      port=os.environ.get('DBPORT', None),
                                      database=os.environ.get('DBNAME', None))

    except (Exception, psycopg2.Error) as error:
        return None

    else:
        return connection


def updateCities(connection):
    error = None
    cursor = connection.cursor()
    with open('../files/city_alias.json') as jsonfile:
        colombia = json.load(jsonfile)

    for alias in colombia:
        query = sql.SQL(
            "SELECT * FROM accounts_ciudad WHERE (codigo_ciudad = '{}')".format(alias['id']))
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 1:
            query = sql.SQL("UPDATE accounts_ciudad SET ciudad_alias = '{}' WHERE codigo_ciudad = {}".format(
                alias['title'], int(alias['id'])))
            try:
                cursor.execute(query)
                connection.commit()
                print('Se actualizó el alias del Municipio ' + str(alias['title']) + ' con id ' + str(alias['id']))
            except psycopg2.OperationalError as e:
                print(error)
                error = True
                connection.rollback()
                cursor.close()
                connection.close()
                break
        else:
            print('No se encontró el Municipio ' + str(alias['title']) + ' con id ' + str(alias['id']))

    result = not(error)
    return result


def populateCities():
    connection = connectDB()
    if connection:
        result = updateCities(connection)
        if result:
            print('Se actualizó la tabla de ciudades de Colombia')
        else:
            print('No fue posible actualizar la tabla. Ningún cambio fue aplicado')

    else:
        print('No se pudo establecer conexion a la BD')


populateCities()
