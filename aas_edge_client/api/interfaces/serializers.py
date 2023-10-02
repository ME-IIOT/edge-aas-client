from rest_framework import serializers
from .models import Interface

class InterfaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interface
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InterfaceSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request', None)
        view_kwargs = self.context.get('view_kwargs', {})

        if request:
            # For POST requests
            if request.method == 'POST':
                if 'interface_id' not in view_kwargs:
                    # This is a POST to /interfaces
                    self.fields['interface_id'].required = True
                    # ... set other field requirements as needed
                else:
                    # This is a POST to /interfaces/{interface_id}
                    self.fields['interface_id'].required = False
                    # ... set other field requirements as needed

            # For GET requests
            elif request.method == 'GET' and 'interface_id' in view_kwargs:
                # For /interfaces/{interface_id} endpoint, exclude 'interface_id'
                self.fields.pop('interface_id', None)
