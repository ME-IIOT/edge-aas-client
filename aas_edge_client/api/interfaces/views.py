from rest_framework import viewsets, status
from .models import NetworkSetting
from .serializers import NetworkSettingSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, HttpResponseRedirect

from django.conf import settings
from EdgeAasMessageHandler.Reactor import Reactor
from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent
from django.apps import apps

class NetworkSettingViewSet(viewsets.ModelViewSet):
    queryset = NetworkSetting.objects.all()
    serializer_class = NetworkSettingSerializer

    reactor = Reactor()

    reactor.register_handler(EdgeEvent.INTERFACE_REQUEST, EdgeEventHandler())

    def create(self, request, *args, **kwargs):
        if NetworkSetting.objects.exists():
            return Response({"detail": "NetworkSetting already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)

        self.reactor.handle_event(EdgeEvent.INTERFACE_REQUEST, request)
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
            self.reactor.handle_event(EdgeEvent.INTERFACE_REQUEST, request=request, serializer_data=serializer.data) 
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
            self.reactor.handle_event(EdgeEvent.INTERFACE_REQUEST, request=request, serializer_data=serializer.data) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
