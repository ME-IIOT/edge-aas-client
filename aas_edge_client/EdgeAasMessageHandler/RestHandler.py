from abc import ABC, abstractmethod
import requests

class IRestHandler(ABC):

    @abstractmethod
    def get(self, url, params=None, headers=None):
        pass
    
    @abstractmethod
    def post(self, url, data=None, headers=None):
        pass
    
    @abstractmethod
    def put(self, url, data=None, headers=None):
        pass
    
    @abstractmethod
    def delete(self, url, headers=None):
        pass

class RestHandler(IRestHandler):

    def __init__(self, baseUrl=''):
        self.baseUrl = baseUrl

    def get(self, url, params=None, headers=None):
        return self._make_request(requests.get, url, params=params, headers=headers)

    def post(self, url, data=None, headers=None):
        return self._make_request(requests.post, url, json=data, headers=headers)

    def put(self, url, data=None, headers=None):
        return self._make_request(requests.put, url, json=data, headers=headers)

    def delete(self, url, headers=None):
        return self._make_request(requests.delete, url, headers=headers)
    
    def patch(self, url, data=None, headers=None):
        return self._make_request(requests.patch, url, json=data, headers=headers)

    def _make_request(self, method, url, **kwargs):
        response = method(self.baseUrl + url, **kwargs)
        return self._parse_response(response)

    def _parse_response(self, response):
        try:
            content = response.json()
        except ValueError:
            content = response.text

        # Return a dictionary with both the status code and content
        return {
            'status_code': response.status_code,
            'content': content
        }
