# interfaces/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Interface
from .serializers import InterfaceSerializer

from aas_edge_client.apps import reactor # import the global variable reactor

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
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        
        # Removing 'interface_id' from the response data
        response_data.pop('interface_id', None)
        
        return Response(response_data)

    # If you want to customize other methods (like `list`, `update`, etc.),
    # you can override them here similarly to the `create` method.

    # For example, if you want to add custom logic to the list method:
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     # Add your custom logic here
    #     return Response(serializer.data)
