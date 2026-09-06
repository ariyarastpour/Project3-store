from .models import SiteSetting, LoaderSetting

def site_settings(request):
    """
    تنظیمات عمومی سایت را در تمام قالب‌ها در دسترس قرار می‌دهد.
    """
    try:
        settings = SiteSetting.objects.first()

    except SiteSetting.DoesNotExist:
        settings = None
        
    return {
        'site_settings': settings,
    }

def loader_settings(request):
    """
    Context processor برای دسترسی به تنظیمات لودر در تمام قالب‌ها
    """
    try:
        settings = LoaderSetting.get_settings()
    except:
        settings = None
    
    return {
        'loader_settings': settings
    }