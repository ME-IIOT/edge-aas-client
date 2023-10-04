from rest_framework import serializers

class TemplateSerializer(serializers.Serializer):
    template_name = serializers.CharField(max_length=255)
    content = serializers.JSONField()
