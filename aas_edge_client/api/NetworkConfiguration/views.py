from rest_framework import viewsets,status
from .models import NetworkConfiguration
from .serializers import NetworkConfigurationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, HttpResponseRedirect

from django.conf import settings
from EdgeAasMessageHandler.Reactor import Reactor
from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent
from datetime import datetime
from django.utils import timezone


class NetworkConfigurationViewSet(viewsets.ModelViewSet):
    queryset = NetworkConfiguration.objects.all()
    serializer_class = NetworkConfigurationSerializer

    reactor = Reactor()

    reactor.register_handler(EdgeEvent.NETWORK_CONFIGURATION_REQUEST, EdgeEventHandler())

    def create(self, request, *args, **kwargs):
        if NetworkConfiguration.objects.exists():
            existing_configuration = self.queryset.first()
            serializer = NetworkConfigurationSerializer(existing_configuration)
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.NETWORK_CONFIGURATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response({"detail": "NetworkConfiguration already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)
        
        serializer = NetworkConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            self.reactor.handle_event( request=request,event_name = EdgeEvent.NETWORK_CONFIGURATION_REQUEST, serializer_data=serializer.data)
            return super().create(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if instance:
            # Redirecting to the detail view of the first instance
            return HttpResponseRedirect(redirect_to=f'/api/NetworkConfiguration/{instance.id}/')
        raise Http404("No NetworkConfiguration object available. Use POST to create.")
    
    def update(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No NetworkConfiguration object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.NETWORK_CONFIGURATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def patch(self, request, *args, **kwargs):
        
        # Fetch the LastUpdate value from the request
        request_last_update = request.data.get('LastUpdate')
        if not request_last_update:
            return Response({'detail': 'LastUpdate is missing in request data'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert the request's LastUpdate value to a datetime object
        request_datetime = datetime.strptime(request_last_update, '%Y-%m-%dT%H:%M:%S')

        instance = self.queryset.first()
        if not instance:
            serializer = NetworkConfigurationSerializer(data=request.data)
            if serializer.is_valid():
                return super().create(request, *args, **kwargs)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # Fetch and convert the instance's LastUpdate value to a datetime object
        instance_datetime = instance.LastUpdate

        
        # Compare the LastUpdate values
        if timezone.make_aware(request_datetime) <= instance_datetime:
            return Response({'detail': 'Request data is not newer.'}, status=status.HTTP_304_NOT_MODIFIED)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.NETWORK_CONFIGURATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    @action(detail=False, methods=['put'])
    def put(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No NetworkConfiguration object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.NETWORK_CONFIGURATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)