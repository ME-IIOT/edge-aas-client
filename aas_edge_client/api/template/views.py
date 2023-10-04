import json
import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from .serializers import TemplateSerializer

class TemplateViewSet(viewsets.ViewSet):
    serializer_class = TemplateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            template_name = serializer.validated_data.get('template_name')
            content = serializer.validated_data.get('content')
            
            file_path = os.path.join(settings.SUBMODEL_TEMPLATE_PATH, f'{template_name}.json')
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False, indent=4)
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            files = os.listdir(settings.SUBMODEL_TEMPLATE_PATH)
            templates = [
                {
                    'template_name': os.path.splitext(f)[0],
                    'link': request.build_absolute_uri(f'/api/templates/{os.path.splitext(f)[0]}')
                }
                for f in files if f.endswith('.json')
            ]
            return Response(templates, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            template_path = os.path.join(settings.SUBMODEL_TEMPLATE_PATH, f'{pk}.json')
            with open(template_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
            return Response(content, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({'error': 'Error decoding JSON'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
