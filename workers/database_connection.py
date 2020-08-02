import os
import psycopg2
from psycopg2 import sql
from psycopg2 import errors
import datetime
import logging

logging.basicConfig(filename='cities_secopi.log',level=logging.ERROR)

def connect_database():
    """Connect to database.
    """
    try:
        connection = psycopg2.connect(user=os.environ.get('DBUSER', None),
                                      password=os.environ.get('DBPASS', None),
                                      host=os.environ.get('DBHOST', None),
                                      port=os.environ.get('DBPORT', None),
                                      database=os.environ.get('DBNAME', None))

    except (Exception, psycopg2.Error) as error:
        logging.error('Cannot connect to database: ' + error)
        return None

    else:
        return connection

def get_city_by_alias(city):
    """Search for a city by ciudad_alias.
       This method is called only when search by ciudad_lower return None.
    """
    connection = connect_database()
    cursor = connection.cursor()
    query = sql.SQL(
            "SELECT codigo_ciudad FROM accounts_ciudad WHERE (ciudad_alias = '{}')".format(city))
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(result) == 1:
        return result[0][0]
    else:
        return None

def get_city(cursor, city, department=None):
    """This method searchs for a city by ciudad_lower and if is defined by departamento_lower.
    """
    city = city.lower().strip()
    if department:
        department = department.lower().strip()
        query = sql.SQL(
        "SELECT codigo_ciudad FROM accounts_ciudad WHERE (ciudad_lower = '{}' AND departamento_lower = '{}')".format(city, department))
    else:
        query = sql.SQL(
            "SELECT codigo_ciudad FROM accounts_ciudad WHERE (ciudad_lower = '{}')".format(city))

    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 1:
        return result[0][0]
    if len(result) > 1:
        return 1
    else:
        # Search by ciudad_alias
        city_alias = get_city_by_alias(city)
        if city_alias != None:
            return city_alias
        else:
            # Register log with city not found
            logging.critical('City not found in database: ' + city)
            return 90000


def validate_city(city):
    """This method validate if municipio_entidad exists in a database.
    """
    if city != None:
        return True, city
    else:
        # Validate if city exists in ciudad_alias field
        city_alias = get_city_by_alias(city)
        if city_alias != None:
            return False, city_alias
        else: 
            # If not exist, return foreing key of No existe object
            return True, 90000

def validate_codunspsc(data):
    if data['id_objeto_a_contratar'] == '0':
        data['id_objeto_a_contratar'] = '00000000'
    if data['id_familia'] == '0':
        data['id_familia'] = '0000'
    if data['id_clase'] == '0':
        data['id_clase'] = '000000'   
    return data     

def search_city_SECOPI(cursor, oportunity_data):
    ''' Search the city based on the existing fields of execution place defined in the process
    '''
    municipio_ejecucion = oportunity_data['municipios_ejecucion'].lower().strip()
    municipio_entrega = oportunity_data['municipio_entrega'].lower().strip()
    municipio_obtencion = oportunity_data['municipio_obtencion'].lower().strip()
    municipio_entidad = oportunity_data['municipio_entidad'].lower().strip()
    depto_entidad = oportunity_data['departamento_entidad'].lower().strip()

    if ((municipio_ejecucion == 'no definido') and (municipio_entrega == 'no definido') and (municipio_obtencion == 'no definido')):
        # Validate if municipio_ejecucion and municipio_entrega and municipio_obtencion are not defined, return ubication of entity
        city = get_city(cursor, municipio_entidad, department=depto_entidad)
        return validate_city(city)
    else:
        if municipio_ejecucion != 'no definido':
            # if municipio_ejecucion exist in a database, check if are more than one
            municipios = municipio_ejecucion.split(';')
            if len(municipios) > 1:
                # Get the first element
                municipio_ejecucion = municipios[0]
            department, city = municipio_ejecucion.split('-')
            city = get_city(cursor, city, department=department)
            if city != None:
                # If city exist, return city
                return False, city

        if municipio_entrega != 'no definido':
            city = get_city(cursor, municipio_entrega)
            if city != None:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(cursor, municipio_entidad, department=depto_entidad)
                    # Validate if municipio_entraga is iqual to municipio_entidad, in this case return municipio_entidad
                    if municipio_entrega == municipio_entidad:
                        return False, city
                    else: return validate_city(city)
                elif city != 90000:
                    # If city is diferent to undefined, return city
                    return False, city       

        if municipio_obtencion != 'no definido':
            city = get_city(cursor, municipio_obtencion)
            if city != None:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(cursor, municipio_entidad, department=depto_entidad)
                    # Validate if municipio_entraga is iqual to municipio_entidad, in this case return municipio_entidad
                    if municipio_obtencion == municipio_entidad:
                        return False, city
                    else: return validate_city(city)
                else: return False, city
        else:
            # If not exist, return municipio_entidad key
            city = get_city(cursor, municipio_entidad, department=depto_entidad)
            return validate_city(city)      


def insert_oportunity_secop_i(connection, data):
    ''' This method insert the data in the 'oportunities_oportunidad' to create
        the new oportunity if this doesn't exists yet. (source: SECOP I)
    '''
    error = False
    num_proceso = data['numero_de_constancia']    
    cursor = connection.cursor()
    query = sql.SQL(
        "SELECT num_proceso FROM oportunities_oportunidad WHERE (num_proceso = '{}')".format(num_proceso))
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        # The process doesn't exist in the DB                        
        city_entity = get_city(cursor, data['municipio_entidad'], department=data['departamento_entidad'])
        undefined, city_entity = validate_city(city_entity)
        undefined, city_process = search_city_SECOPI(cursor, data)
        data = validate_codunspsc(data)
        query = sql.SQL("""INSERT INTO oportunities_oportunidad (
                                                                created_at,
                                                                updated_at,
                                                                num_proceso,
                                                                cod_unspsc_id,
                                                                cod_unspsc_familia_id,
                                                                cod_unspsc_clase_id,
                                                                estado_proceso,
                                                                fuente,
                                                                entidad,
                                                                municipio_entidad_id,
                                                                nit_entidad,
                                                                objeto_proceso,
                                                                detalle_objeto_proceso,
                                                                valor_proceso,
                                                                id_tipo_proceso,
                                                                tipo_proceso,
                                                                fecha_publicacion,
                                                                plazo_ejecucion_cant,
                                                                plazo_ejecucion_und,
                                                                municipio_ejecucion_id,
                                                                fecha_limite,
                                                                url_proceso,
                                                                undefined_flag
                                                                ) VALUES ('{}', '{}', '{}', '{}', '{}',
                                                                          '{}', '{}', '{}', '{}', '{}',
                                                                          '{}', '{}', '{}', '{}',
                                                                          '{}', '{}', '{}', '{}',
                                                                          '{}', '{}', '{}', '{}', '{}')""".format(
            datetime.datetime.now(), datetime.datetime.now(), data['numero_de_constancia'], data['id_objeto_a_contratar'], data['id_familia'] + '0000',
            data['id_clase'] + '00', data['estado_del_proceso'], 1, data['nombre_de_la_entidad'], 
            city_entity, data['nit_de_la_entidad'], data['objeto_a_contratar'],
            data['detalle_del_objeto_a_contratar'], data['cuantia_proceso'], int(data['id_tipo_de_proceso']), 
            data['tipo_de_proceso'], data['fecha_de_cargue_en_el_secop'], -1, '', city_process, '', 
            data['ruta_proceso_en_secop_i']['url'], undefined)
        )

        try:
            # Inserts the new row
            cursor.execute(query)
            connection.commit()
            
        except psycopg2.OperationalError as e:
            logging.error('Cannot commit query to database: ' + error)
            error = True
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    else:
        print('El proceso ' + num_proceso + ' ya existe')
    

    return error
            


