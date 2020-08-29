"""Scripts for insert oportunities from SECOP I."""

# Utilities
import logging
import requests

# Models
from oportunities.models import Oportunidad
from accounts.models import Ciudad

from datetime import datetime

# Log
logging.basicConfig(filename='cities_secopi.log', level=logging.ERROR)


def get_city_by_alias(city):
    """Search for a city by ciudad_alias.
       This method is called only when search by ciudad_lower return None.
    """
    result = Ciudad.objects.filter(ciudad_alias=city).values_list('codigo_ciudad', flat=True)
    if len(result) == 1:
        return result[0]
    else:
        return None


def get_city(city, department=None):
    """This method searchs for a city by ciudad_lower and if is defined by departamento_lower.
    """
    city = city.lower().strip()
    if department:
        department = department.lower().strip()
        result = Ciudad.objects.filter(
            ciudad_lower=city, departamento_lower=department).values_list('codigo_ciudad', flat=True)
    else:
        result = Ciudad.objects.filter(ciudad_lower=city).values_list('codigo_ciudad', flat=True)

    if len(result) == 1:
        return result[0]
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


def search_city_SECOPI(oportunity_data):
    ''' Search the city based on the existing fields of execution place defined in the process
    '''
    try:
        municipio_ejecucion = oportunity_data['municipios_ejecucion'].lower(
    ).strip()
    except:
        municipio_ejecucion = 'no definido'
    try:
        municipio_entrega = oportunity_data['municipio_entrega'].lower().strip()
    except:
        municipio_entrega = 'no definido'
    try:        
        municipio_obtencion = oportunity_data['municipio_obtencion'].lower(
    ).strip()
    except:
        municipio_obtencion = 'no definido'
    municipio_entidad = oportunity_data['municipio_entidad'].lower().strip()
    depto_entidad = oportunity_data['departamento_entidad'].lower().strip()

    if ((municipio_ejecucion == 'no definido') and (municipio_entrega == 'no definido') and (municipio_obtencion == 'no definido')):
        # Validate if municipio_ejecucion and municipio_entrega and municipio_obtencion are not defined, return ubication of entity
        city = get_city(municipio_entidad, department=depto_entidad)
        return True, city
    else:
        if municipio_ejecucion != 'no definido':
            # if municipio_ejecucion exist in a database, check if are more than one
            municipios = municipio_ejecucion.split(';')
            if len(municipios) > 1:
                # Get the first element
                municipio_ejecucion = municipios[0]
            department, city = municipio_ejecucion.split('-')
            city = get_city(city, department=department)
            if city != 90000:
                # If city exist, return city
                return False, city

        if municipio_entrega != 'no definido':
            city = get_city(municipio_entrega)
            if city != 90000:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(municipio_entidad,
                                    department=depto_entidad)
                    # Validate if municipio_entraga is iqual to municipio_entidad, in this case return municipio_entidad
                    if municipio_entrega == municipio_entidad:
                        return False, city
                    else:
                        return True, city
                elif city != 90000:
                    # If city is diferent to undefined, return city
                    return False, city

        if municipio_obtencion != 'no definido':
            city = get_city(municipio_obtencion)
            if city != 90000:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(municipio_entidad,
                                    department=depto_entidad)
                    # Validate if municipio_entraga is iqual to municipio_entidad, in this case return municipio_entidad
                    if municipio_obtencion == municipio_entidad:
                        return False, city
                    else:
                        return True, city
                else:
                    return False, city
            else:
                return True, city
        else:
            # If not exist, return municipio_entidad key
            city = get_city(municipio_entidad, department=depto_entidad)
            return True, city


def validate_codunspsc(data):
    if data['id_objeto_a_contratar'] == '0':
        data['id_objeto_a_contratar'] = '00000000'
    if data['id_familia'] == '0':
        data['id_familia'] = '0000'
    if data['id_clase'] == '0':
        data['id_clase'] = '000000'
    return data


def insert_oportunity_secop_i(data):
    ''' This method insert the data in the 'oportunities_oportunidad' to create
        the new oportunity if this doesn't exists yet. (source: SECOP I)
    '''
    error = False

    num_proceso = Oportunidad.objects.filter(
        num_proceso=data['numero_de_constancia'])
    if len(num_proceso) == 0:
        # The process doesn't exist in the DB
        city_entity = get_city(
            data['municipio_entidad'], department=data['departamento_entidad'])
        undefined, city_process = search_city_SECOPI(data)
        pub_date = datetime.strptime(data['fecha_de_cargue_en_el_secop'], '%m/%d/%Y')
        data = validate_codunspsc(data)
        oportunity = Oportunidad(num_proceso=data['numero_de_constancia'], cod_unspsc_id=data['id_objeto_a_contratar'],
                                 cod_unspsc_familia_id=data['id_familia'] + '0000', cod_unspsc_clase_id=data['id_clase'] + '00',
                                 estado_proceso=data['estado_del_proceso'], fuente=1, entidad=data['nombre_de_la_entidad'],
                                 municipio_entidad_id=city_entity, nit_entidad=data[
                                     'nit_de_la_entidad'], objeto_proceso=data['objeto_a_contratar'],
                                 detalle_objeto_proceso=data['detalle_del_objeto_a_contratar'], valor_proceso=data['cuantia_proceso'],
                                 id_tipo_proceso=int(data['id_tipo_de_proceso']), tipo_proceso=data['tipo_de_proceso'], 
                                 fecha_publicacion=pub_date, plazo_ejecucion_cant=-1, plazo_ejecucion_und='', 
                                 municipio_ejecucion_id=city_process, url_proceso=data['ruta_proceso_en_secop_i']['url'], 
                                 undefined_flag=undefined)

        try:
            # Inserts the new row
            oportunity.save()

        except Exception as e:
            error = True
            logging.error('Cannot commit query to database: ' + str(e))
    else:
        print('El proceso ' + str(num_proceso) + ' ya existe')
    return error


def get_request(date):
    # This method consult the SECOPI API passing the date as aparameter to the query

    response = requests.get('https://www.datos.gov.co/resource/c82b-7jfi.json?fecha_de_cargue_en_el_secop=' +
                            date.strftime('%m/%d/%Y') + '&estado_del_proceso=Convocado&$limit=1000')

    resp = response.json()

    for oportunity in resp:
        insert_oportunity_secop_i(oportunity)

    # This method consult the SECOPII API passing the date as aparameter to the query

    response = requests.get('https://www.datos.gov.co/resource/p6dx-8zbt.json?fecha_de_publicacion_del=' + 
                            date.strftime("%Y-%m-%d") + 'T00:00:00.000&id_estado_del_procedimiento=50&$limit=1000')
                               
    resp = response.json()

    for oportunity in resp:
        insert_oportunity_secop_ii(oportunity)


def search_city_entity_secop_ii(city, department):
    city = city.lower().strip()
    department = department.lower().strip()
    if department == 'distrito capital de bogotá':
        city_entity = get_city(city)
        return city_entity
    if (city != 'no definido') and (department != 'no definido'):
        city_entity = get_city(
            city, department=department)
        return city_entity
    else:
        return 90000
    if department != 'no definido':
        city_entity = get_city(city)
        return city_entity
    
def search_city_process_secop_ii(data):
    city = data['ciudad_de_la_unidad_de'].lower().strip()
    city_process = get_city(city)
    if city != 'no definida':
        if city_process != 90000:
            if city_process == 1:
                # Validate if ciudad_de_la_unidad_de is iqual to ciudad_entidad, in this case return ciudad_entidad key
                if data['ciudad_de_la_unidad_de'] == data['ciudad_entidad']:
                    return False, data['city_entity']
                else:
                    return True, 90000                    
            else:
                # Return ciudad_de_la_unidad_de key
                return False, city_process
        else:
            # City not found
            return True, city_process
    else:
        # If ciudad_de_la_unidad_de is not defined, return city_entity key
        return True, data['city_entity']


def insert_oportunity_secop_ii(data):
    ''' This method insert the data in the 'oportunities_oportunidad' to create
        the new oportunity if this doesn't exists yet. (source: SECOP II)
    '''
    error = False

    num_proceso = Oportunidad.objects.filter(
        num_proceso=data['id_del_proceso'])
    if len(num_proceso) == 0:
        # The process doesn't exist in the DB
        city_entity = search_city_entity_secop_ii(
            data['ciudad_entidad'], data['departamento_entidad'])
        data['city_entity']= city_entity
        undefined, city_process = search_city_process_secop_ii(data)
        pub_date = data['fecha_de_publicacion_del'].split('T')[0]
        codigo_unspsc = data['codigo_principal_de_categoria'].split('.')[1]
        try:
            if data['descripci_n_del_procedimiento']:
                pass
        except:
            data['descripci_n_del_procedimiento'] = None

        oportunity = Oportunidad(num_proceso=data['id_del_proceso'], cod_unspsc_id=codigo_unspsc,
                                 estado_proceso='Convocado', fuente=2, entidad=data['entidad'],
                                 municipio_entidad_id=city_entity, nit_entidad=data[
                                     'nit_entidad'], objeto_proceso=data['nombre_del_procedimiento'],
                                 detalle_objeto_proceso=data['descripci_n_del_procedimiento'], valor_proceso=data['precio_base'],
                                 tipo_proceso=data['modalidad_de_contratacion'], fecha_publicacion=pub_date, 
                                 plazo_ejecucion_cant=data['duracion'], plazo_ejecucion_und=data['unidad_de_duracion'],
                                 municipio_ejecucion_id=city_process, url_proceso=data['urlproceso']['url'], 
                                 undefined_flag=undefined)

        try:
            # Inserts the new row
            oportunity.save()

        except Exception as e:
            error = True
            logging.error('Cannot commit query to database: ' + str(e))
    else:
        print('El proceso ' + str(num_proceso) + ' ya existe')
    return error