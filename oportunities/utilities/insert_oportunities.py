"""Scripts for insert oportunities from SECOP I."""

# Utilities
import logging
import requests

# Models
from oportunities.models import Oportunidad
from accounts.models import Ciudad

# Log
logging.basicConfig(filename='cities_secopi.log', level=logging.ERROR)


def get_city_by_alias(city):
    """Search for a city by ciudad_alias.
       This method is called only when search by ciudad_lower return None.
    """
    result = Ciudad.objects.filter(ciudad_alias=city)
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
            ciudad_lower=city, departamento_lower=department)
    else:
        result = Ciudad.objects.filter(ciudad_lower=city)

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


def search_city_SECOPI(oportunity_data):
    ''' Search the city based on the existing fields of execution place defined in the process
    '''
    municipio_ejecucion = oportunity_data['municipios_ejecucion'].lower(
    ).strip()
    municipio_entrega = oportunity_data['municipio_entrega'].lower().strip()
    municipio_obtencion = oportunity_data['municipio_obtencion'].lower(
    ).strip()
    municipio_entidad = oportunity_data['municipio_entidad'].lower().strip()
    depto_entidad = oportunity_data['departamento_entidad'].lower().strip()

    if ((municipio_ejecucion == 'no definido') and (municipio_entrega == 'no definido') and (municipio_obtencion == 'no definido')):
        # Validate if municipio_ejecucion and municipio_entrega and municipio_obtencion are not defined, return ubication of entity
        city = get_city(municipio_entidad, department=depto_entidad)
        return validate_city(city)
    else:
        if municipio_ejecucion != 'no definido':
            # if municipio_ejecucion exist in a database, check if are more than one
            municipios = municipio_ejecucion.split(';')
            if len(municipios) > 1:
                # Get the first element
                municipio_ejecucion = municipios[0]
            department, city = municipio_ejecucion.split('-')
            city = get_city(city, department=department)
            if city != None:
                # If city exist, return city
                return False, city

        if municipio_entrega != 'no definido':
            city = get_city(municipio_entrega)
            if city != None:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(municipio_entidad,
                                    department=depto_entidad)
                    # Validate if municipio_entraga is iqual to municipio_entidad, in this case return municipio_entidad
                    if municipio_entrega == municipio_entidad:
                        return False, city
                    else:
                        return validate_city(city)
                elif city != 90000:
                    # If city is diferent to undefined, return city
                    return False, city

        if municipio_obtencion != 'no definido':
            city = get_city(municipio_obtencion)
            if city != None:
                # Check if exist more than one city with the same name
                if city == 1:
                    city = get_city(municipio_entidad,
                                    department=depto_entidad)
                    # Validate if municipio_entraga is iqual to municipio_entidad, in this case return municipio_entidad
                    if municipio_obtencion == municipio_entidad:
                        return False, city
                    else:
                        return validate_city(city)
                else:
                    return False, city
        else:
            # If not exist, return municipio_entidad key
            city = get_city(municipio_entidad, department=depto_entidad)
            return validate_city(city)


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
        undefined, city_entity = validate_city(city_entity)
        undefined, city_process = search_city_SECOPI(data)
        data = validate_codunspsc(data)
        oportunity = Oportunidad(num_proceso=data['numero_de_constancia'], cod_unspsc_id=data['id_objeto_a_contratar'],
                                 cod_unspsc_familia_id=data['id_familia'] + '0000', cod_unspsc_clase_id=data['id_clase'] + '00',
                                 estado_proceso=data['estado_del_proceso'], fuente=1, entidad=data['nombre_de_la_entidad'],
                                 municipio_entidad_id=city_entity.codigo_ciudad, nit_entidad=data[
                                     'nit_de_la_entidad'], objeto_proceso=data['objeto_a_contratar'],
                                 detalle_objeto_proceso=data['detalle_del_objeto_a_contratar'], valor_proceso=data['cuantia_proceso'],
                                 id_tipo_proceso=int(data['id_tipo_de_proceso']), tipo_proceso=data['tipo_de_proceso'], 
                                 fecha_publicacion=data['fecha_de_cargue_en_el_secop'], plazo_ejecucion_cant=-1, plazo_ejecucion_und='', 
                                 municipio_ejecucion_id=city_process.codigo_ciudad, fecha_limite='', url_proceso=data['ruta_proceso_en_secop_i']['url'], 
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
    # This method consult the API passing the date as aparameter to the query
    response = requests.get('https://www.datos.gov.co/resource/c82b-7jfi.json?fecha_de_cargue_en_el_secop=' +
                            date + '&estado_del_proceso=Convocado&$limit=3')

    resp = response.json()

    for oportunity in resp:
        insert_oportunity_secop_i(oportunity)
