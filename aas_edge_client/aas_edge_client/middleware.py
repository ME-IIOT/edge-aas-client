import os
import requests
import json
from django.conf import settings

class StartupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.post_sent = False

    def __call__(self, request):
        # Send POST request only once after the server has started.
        if not self.post_sent:
            self.post_sent = True

            # Get the file path from settings
            file_path = settings.INTERFACES_DEFAULT_FILE_PATH

            # Check if the file exists
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)

                    url = f'{settings.CLIENT_URL}/api/interfaces/'
                    headers = {'Content-Type': 'application/json'}

                    try:
                        response = requests.post(url, headers=headers, json=data)
                        if response.status_code == 200:
                            print("POST request was successful.")
                        else:
                            print(f"Failed to send POST request: {response.status_code}")
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")

                except Exception as e:
                    print(f"Failed to read JSON file: {str(e)}")
            else:
                print(f"JSON file not found at {file_path}")

        response = self.get_response(request)
        return response
