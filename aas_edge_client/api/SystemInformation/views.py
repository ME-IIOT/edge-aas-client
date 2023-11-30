from rest_framework import viewsets, status
from .models import SystemInformation
from .serializers import SystemInformationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404, HttpResponseRedirect

from django.conf import settings
from EdgeAasMessageHandler.Reactor import AsyncReactor
from EdgeAasMessageHandler.EdgeSubmodelHandler import ( UpdateServerSubmodelSystemInformationHandler,
                                                        EdgeUpdateSubmodelEvent)
from EdgeAasMessageHandler.EdgeHandler import Job
# from EdgeAasMessageHandler.EdgeEventHandler import EdgeEventHandler, EdgeEvent
from datetime import datetime
from django.utils import timezone
import json
import logging
import asyncio


logger = logging.getLogger('django')
class SystemInformationViewSet(viewsets.ModelViewSet):
    queryset = SystemInformation.objects.all()
    serializer_class = SystemInformationSerializer

    reactor = AsyncReactor()

    # reactor.register_handler(EdgeEvent.SYSTEM_INFORMATION_REQUEST, EdgeEventHandler())

    def create(self, request, *args, **kwargs): 
        if SystemInformation.objects.exists():
            existing_configuration = self.queryset.first()
            serializer = SystemInformationSerializer(existing_configuration)
            try:
                asyncio.run(self.reactor.add_job(job=Job(type_=EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION.value, 
                                             request_body=serializer.data)))
                return Response({"detail": "SystemInformation already exists. Use PUT to update."}, status=status.HTTP_409_CONFLICT)
            except Exception as e:
                return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        serializer = SystemInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                asyncio.run(self.reactor.add_job(job=Job(type_=EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION.value, 
                                             request_body=serializer.data)))
                return super().create(request, *args, **kwargs)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

        modified_request_data = request.data.copy()
        modified_request_data['LastUpdate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        serializer = self.get_serializer(instance, data=modified_request_data, partial=True)
        
        # serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                asyncio.run(self.reactor.add_job(job=Job(type_=EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION.value, 
                                             request_body=serializer.data)))
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            logger.info(f"Server SystemInformation is not newer. Server: {request_datetime} Client: {instance_datetime}")
            return Response({'detail': 'Request data is not newer.'}, status=status.HTTP_304_NOT_MODIFIED)

        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                asyncio.run(self.reactor.add_job(job=Job(type_=EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION.value, 
                                             request_body=serializer.data)))
                payload_json = json.dumps(serializer.data)
                # SImqttHandler.publish(topic='ServerSystemInformationChange', payload=payload_json)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'])
    def put(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            return Response({"detail": "No SystemInformation object available. Use POST to create."}, status=status.HTTP_404_NOT_FOUND)

        modified_request_data = request.data.copy()
        modified_request_data['LastUpdate'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        serializer = self.get_serializer(instance, data=modified_request_data, partial=True)
        
        # serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                asyncio.run(self.reactor.add_job(job=Job(type_=EdgeUpdateSubmodelEvent.SYSTEM_INFORMATION.value, 
                                             request_body=serializer.data)))
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)