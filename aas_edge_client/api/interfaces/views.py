from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Interface
from .serializers import InterfaceSerializer
from submodels_template.parser_submodel import transform_response
from django.conf import settings

#from aas_edge_client.apps import reactor # import the global variable reactor
from django.apps import apps

# call reactor (for future use)
app_config = apps.get_app_config('aas_edge_client')
reactor = app_config.reactor

class InterfaceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Interface instances.
    """
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
    lookup_field = 'interface_id'

    def create(self, request, *args, **kwargs):
        serializer = InterfaceSerializer(data=request.data, context={'request': request, 'view_kwargs': self.kwargs})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InterfaceSerializer(instance)
        responseData = serializer.data
        # Removing 'interface_id', 'id from the response data
        responseData.pop('interface_id', None)
        responseData.pop('id', None)
        return Response(responseData)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InterfaceSerializer(instance, data=request.data, context={'request': request, 'view_kwargs': self.kwargs})
        if serializer.is_valid():
            serializer.save()
            responseData = serializer.data
            # Removing 'interface_id', 'id from the response data
            responseData.pop('interface_id', None)
            responseData.pop('id', None)
            # submodelData = transform_response(responseData, settings.SUBMODEL_TEMPLATE_PATH + '/Submodel_Configuration.json')
            # reactor handle the submodel_data (send to aas repository)
            # reactor.getHadler(event).handle(request)
            # reactor.handleevent(request, 'rest', submodelData=submodelData)
            return Response(responseData, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
