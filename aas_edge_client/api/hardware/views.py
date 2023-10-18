from rest_framework import viewsets, status
from .models import Hardware
from .serializers import HardwareSerializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from EdgeAasMessageHandler.Reactor import Reactor
from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent
# from django.apps import apps

class HardwareViewSet(viewsets.ModelViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializers

    reactor = Reactor()

    reactor.register_handler(EdgeEvent.HARDWARE_REQUEST, EdgeEventHandler())

    def create(self, request, *args, **kwargs):
        if Hardware.objects.exists():
            existing_setting = self.queryset.first()
            serializer = HardwareSerializers(existing_setting)
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.HARDWARE_REQUEST,
                serializer_data=serializer.data
            )
            return Response({"detail": "Hardware already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)
        
        serializer = HardwareSerializers(data=request.data)
        if serializer.is_valid():
            self.reactor.handle_event( request=request,event_name = EdgeEvent.HARDWARE_REQUEST, serializer_data=serializer.data)
            return super().create(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if instance:
            # Redirecting to the detail view of the first instance
            return HttpResponseRedirect(redirect_to=f'/api/hardware/{instance.id}/')
        raise Http404("No Hardware object available. Use POST to create.")
    
    def update(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No Hardware object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.HARDWARE_REQUEST,
                serializer_data=serializer.data
            )
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No Hardware object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['put'])
    def put(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No Hardware object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)