from accounts.models import Perfil
from .profile_middleware import retriveCities, retriveCodes


def updateProfile(request):
    '''
    This function update the user's profile with the form data
    '''
    perfil = Perfil.objects.get(usuario=request.user)        
    ciudades = retriveCities(request.POST['ciudades'])
    codUNSPSC = retriveCodes(request.POST['unspsc'])
    perfil.nit = request.POST['nit']
    perfil.nom_empresa = request.POST['nom_empresa']
    perfil.telefono = request.POST['telefono']
    perfil.presupuesto_min = request.POST['presupuesto_min']
    perfil.presupuesto_max = request.POST['presupuesto_max']
    perfil.activ_economica.set(codUNSPSC)
    perfil.ciudad.set(ciudades)
    
    try:
        perfil.save()
        return True
    
    except:
        return False