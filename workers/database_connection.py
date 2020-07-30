import os
import psycopg2
from psycopg2 import sql
from psycopg2 import errors
import datetime


def connect_database():
    try:
        connection = psycopg2.connect(user=os.environ.get('DBUSER', None),
                                      password=os.environ.get('DBPASS', None),
                                      host=os.environ.get('DBHOST', None),
                                      port=os.environ.get('DBPORT', None),
                                      database=os.environ.get('DBNAME', None))

    except (Exception, psycopg2.Error) as error:
        print(error)
        return None

    else:
        return connection


def get_city(cursor, city, department=None):
    city = city.lower()
    if department:
        department = department.lower()
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
        return None


def validate_city(city):
    if city != None:
        return True, city
    else:
        return True, ''


def search_city_SECOPI(cursor, oportunity_data):
    ''' Search the city based on the existing fields of execution place defined in the process
    '''
    municipio_ejecucion = oportunity_data['municipios_ejecucion'].lower()
    municipio_entrega = oportunity_data['municipio_entrega'].lower()
    municipio_obtencion = oportunity_data['municipio_obtencion'].lower()
    municipio_entidad = oportunity_data['municipio_entidad'].lower()
    depto_entidad = oportunity_data['departamento_entidad'].lower()

    if ((municipio_ejecucion == 'no definido') and (municipio_entrega == 'no definido') and (municipio_obtencion == 'no definido')):
        city = get_city(cursor, municipio_entidad, department=depto_entidad)
        return validate_city(city)
    else:
        if municipio_ejecucion != 'no definido':            
            department, city = municipio_ejecucion.split('-')
            city = get_city(cursor, city, department=department)
            if city != None:
                return False, city
            else:
                return True, ''

        elif municipio_entrega != 'no definido':
            city = get_city(cursor, municipio_entrega)
            if city != None:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(cursor, municipio_entidad, department=depto_entidad)
                    return validate_city(city)
                else: return False, city
            else: return True, ''

        elif municipio_obtencion != 'no definido':
            city = get_city(cursor, municipio_obtencion)
            if city != None:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(cursor, municipio_entidad, department=depto_entidad)
                    return validate_city(city)
                else: return False, city
            else: return True, ''


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
            datetime.datetime.now(), datetime.datetime.now(), data['numero_de_constancia'], data['id_objeto_a_contratar'], int(data['id_familia'] + '0000'),
            int(data['id_clase'] + '00'), data['estado_del_proceso'], 1, data['nombre_de_la_entidad'], 
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
            print(error)
            error = True
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
    else:
        print('El proceso ' + num_proceso + ' ya existe')
    

    return error
            


