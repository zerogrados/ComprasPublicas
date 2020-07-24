"""Profile middleware."""

# Models
from accounts.models import Ciudad, CodUNSPSC

def retriveCities(request_cities):
    """
    This method retrive an array of Ciudad objects.
    """
    cities = []
    for city in request_cities.split(','):
        try:
            cities.append(Ciudad.objects.get(codigo_ciudad=city))
        except:
            pass
    
    return cities


def retriveCodes(request_codes):
    """
    This method retrive an array of CodUNSPSC objects.
    """
    codes = []
    for code in request_codes.split(','):        
        try:
            codes.append(CodUNSPSC.objects.get(codigo=code))
        except:            
            pass

    return codes