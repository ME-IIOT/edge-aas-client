# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import InterfaceElements
# from .serializers import InterfaceSerializer
# from submodels_template.parser_submodel import transform_response
# from django.conf import settings

# #from aas_edge_client.apps import reactor # import the global variable reactor
# from django.apps import apps

# # call reactor (for future use)
# app_config = apps.get_app_config('aas_edge_client')
# reactor = app_config.reactor

# class InterfaceViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing Interface instances.
#     """
#     queryset = InterfaceElements.objects.all()
#     serializer_class = InterfaceSerializer
#     # lookup_field = 'interface_id'
#     lookup_field = 'id'

#     def create(self, request, *args, **kwargs):
#         serializer = InterfaceSerializer(data=request.data, context={'request': request, 'view_kwargs': self.kwargs})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = InterfaceSerializer(instance)
#         responseData = serializer.data
#         # Removing 'interface_id', 'id from the response data
#         responseData.pop('interface_id', None)
#         responseData.pop('id', None)
#         return Response(responseData)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = InterfaceSerializer(instance, data=request.data, context={'request': request, 'view_kwargs': self.kwargs})
#         if serializer.is_valid():
#             serializer.save()
#             responseData = serializer.data
#             # Removing 'interface_id', 'id from the response data
#             responseData.pop('interface_id', None)
#             responseData.pop('id', None)
#             # submodelData = transform_response(responseData, settings.SUBMODEL_TEMPLATE_PATH + '/Submodel_Configuration.json')
#             # reactor handle the submodel_data (send to aas repository)
#             # reactor.getHadler(event).handle(request)
#             # reactor.handleevent(request, 'rest', submodelData=submodelData)
#             return Response(responseData, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets, status
from .models import NetworkSetting
from .serializers import NetworkSettingSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, HttpResponseRedirect

class NetworkSettingViewSet(viewsets.ModelViewSet):
    queryset = NetworkSetting.objects.all()
    serializer_class = NetworkSettingSerializer

    def create(self, request, *args, **kwargs):
        if NetworkSetting.objects.exists():
            return Response({"detail": "NetworkSetting already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)

        return super().create(request, *args, **kwargs)


    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if instance:
            # Redirecting to the detail view of the first instance
            return HttpResponseRedirect(redirect_to=f'/api/interfaces/{instance.id}/')
        raise Http404("No NetworkSetting object available. Use POST to create.")


    def update(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No NetworkSetting object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def put(self, request, *args, **kwargs):
        instance = self.queryset.first()
        
        if not instance:
            return Response({"detail": "No NetworkSetting object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
