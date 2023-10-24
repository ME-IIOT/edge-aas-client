from rest_framework import viewsets, status
from .models import SystemInformation
from .serializers import SystemInformationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, HttpResponseRedirect

from django.conf import settings
from EdgeAasMessageHandler.Reactor import Reactor
from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent
from datetime import datetime
from django.utils import timezone
from EdgeAasMessageHandler.MqttHandler import MqttHandler
import requests
import json
import atexit

def handle_mqtt_system_information_put(message_topic:str, message_payload: str) -> None:
    try:
        payload_json = json.loads(message_payload)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from message on {message_topic}")
        return
    
    url = f'{settings.CLIENT_URL}/api/SystemInformation/'
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, json=payload_json, headers=headers)

    if response.status_code == 200:
        # print(f'Successfully updated system information')
        pass
    else:
        print(f'Failed to update system information')

# SImqttHandler = MqttHandler(handlerName="System Information MQTT")
# SImqttHandler.connect(host=settings.MQTT_BROKER_HOST, port=settings.MQTT_BROKER_PORT)
# SImqttHandler.loop_start()
# SImqttHandler.subscribe(topic='ClientSystemInformationChange')
# SImqttHandler.set_message_callback(handle_mqtt_system_information_put)
# atexit.register(SImqttHandler.shutdown)
class SystemInformationViewSet(viewsets.ModelViewSet):
    queryset = SystemInformation.objects.all()
    serializer_class = SystemInformationSerializer

    reactor = Reactor()

    reactor.register_handler(EdgeEvent.SYSTEM_INFORMATION_REQUEST, EdgeEventHandler())

    def create(self, request, *args, **kwargs): 
        if SystemInformation.objects.exists():
            existing_configuration = self.queryset.first()
            serializer = SystemInformationSerializer(existing_configuration)
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.SYSTEM_INFORMATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response({"detail": "SystemInformation already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)
        
        serializer = SystemInformationSerializer(data=request.data)
        if serializer.is_valid():
            self.reactor.handle_event( request=request,event_name = EdgeEvent.SYSTEM_INFORMATION_REQUEST, serializer_data=serializer.data)
            return super().create(request, *args, **kwargs)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def list(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if instance:
            # Redirecting to the detail view of the first instance
            return HttpResponseRedirect(redirect_to=f'/api/SystemInformation/{instance.id}/')
        raise Http404("No SystemInformation object available. Use POST to create.")
    
    def update(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No SystemInformation object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.SYSTEM_INFORMATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, *args, **kwargs):

        request_last_update = request.data.get('LastUpdate')
        if not request_last_update:
            return Response({'detail': 'LastUpdate is missing in request data'}, status=status.HTTP_400_BAD_REQUEST)

        request_datetime = datetime.strptime(request_last_update, '%Y-%m-%dT%H:%M:%SZ')

        instance = self.queryset.first()
        if not instance:
            serializer = SystemInformationSerializer(data=request.data)
            if serializer.is_valid():
                return super().create(request, *args, **kwargs)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                event_name=EdgeEvent.SYSTEM_INFORMATION_REQUEST,
                serializer_data=serializer.data
            )
            payload_json = json.dumps(serializer.data)
            # SImqttHandler.publish(topic='ServerSystemInformationChange', payload=payload_json)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def put(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No SystemInformation object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.reactor.handle_event(
                request=request,
                event_name=EdgeEvent.SYSTEM_INFORMATION_REQUEST,
                serializer_data=serializer.data
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)