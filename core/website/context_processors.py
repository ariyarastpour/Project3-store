from .models import SiteSetting, LoaderSetting

def site_settings(request):

    try:
        settings = SiteSetting.objects.first()

    except SiteSetting.DoesNotExist:
        settings = None
        
    return {
        'site_settings': settings,
    }

def loader_settings(request):

    try:
        settings = LoaderSetting.get_settings()
    except:
        settings = None
    
    return {
        'loader_settings': settings
    }