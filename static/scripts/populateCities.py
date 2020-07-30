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
    with open('colombia_fix.json') as jsonfile:
        colombia = json.load(jsonfile)

    for department in colombia:
        for city in department['subs']:
            query = sql.SQL(
                "SELECT * FROM accounts_ciudad WHERE (ciudad = '{}' AND departamento = '{}')".format(city['title'], department['title']))
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                query = sql.SQL("INSERT INTO accounts_ciudad (codigo_ciudad, ciudad, departamento, ciudad_lower, departamento_lower) VALUES ('{}', '{}', '{}', '{}', '{}')".format(
                    city['id'], city['title'], department['title'], city['title'].lower(), department['title'].lower()))
                try:
                    cursor.execute(query)
                    connection.commit()
                except psycopg2.OperationalError as e:
                    print(error)
                    error = True
                    connection.rollback()
                    cursor.close()
                    connection.close()
                    break
            else:
                print(city, department['title'], 'ya existe')

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
