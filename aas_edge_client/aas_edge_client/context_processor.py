from django.conf import settings

def vendor_details(request):
    return {
        'VENDOR_NAME': settings.VENDOR_NAME,
        'VENDOR_LINK': settings.VENDOR_LINK,
        'PRIMARY_COLOR': settings.PRIMARY_COLOR,
        'SECONDARY_COLOR': settings.SECONDARY_COLOR,
        'TEXT_COLOR': settings.TEXT_COLOR,
        'BUTTON_COLOR' : settings.BUTTON_COLOR,
    }
