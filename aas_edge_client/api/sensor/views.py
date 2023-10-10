from rest_framework import viewsets, status
from .models import Sensors
from .serializers import SensorsSerializer
from rest_framework.response import Response
from django.http import Http404, HttpResponseRedirect
from rest_framework.decorators import action
from EdgeAasMessageHandler.Reactor import Reactor
from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent



class SensorsViewSet(viewsets.ModelViewSet):
    queryset = Sensors.objects.all()
    serializer_class = SensorsSerializer
    
    reactor = Reactor()

    # reactor.register_handler(EdgeEvent.SENSOR_REQUEST, EdgeEventHandler())


    def create(self, request, *args, **kwargs):
        if Sensors.objects.exists():
            return Response({"detail": "Sensors object already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)
        
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if instance:
            return HttpResponseRedirect(redirect_to=f'/api/sensors/{instance.id}/')
        raise Http404("No Sensors object available. Use POST to create.")

    def update(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No Sensors object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(event_name = EdgeEvent.SENSOR_REQUEST, request=request, serializer_data=serializer.data) 
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No Sensors object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put'])
    def put(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No Sensors object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(event_name = EdgeEvent.SENSOR_REQUEST, request=request, serializer_data=serializer.data) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
