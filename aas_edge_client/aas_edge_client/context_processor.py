from django.conf import settings

def vendor_details(request):
    return {
        'VENDOR_NAME': settings.VENDOR_NAME,
        'VENDOR_LINK': settings.VENDOR_LINK,
    }
