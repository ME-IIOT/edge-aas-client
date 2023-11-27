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

    def __init__(self, baseUrl='', timeout=None):
        self.baseUrl = baseUrl
        self.timeout = timeout  # Set a default timeout for all requests

    def get(self, url, params=None, headers=None, timeout=None):
        return self._make_request(requests.get, url, params=params, headers=headers, timeout=timeout)

    def post(self, url, data=None, headers=None, timeout=None):
        return self._make_request(requests.post, url, json=data, headers=headers, timeout=timeout)

    def put(self, url, data=None, headers=None, timeout=None):
        return self._make_request(requests.put, url, json=data, headers=headers, timeout=timeout)

    def delete(self, url, headers=None, timeout=None):
        return self._make_request(requests.delete, url, headers=headers, timeout=timeout)
    
    def patch(self, url, data=None, headers=None, timeout=None):
        return self._make_request(requests.patch, url, json=data, headers=headers, timeout=timeout)

    def _make_request(self, method, url, **kwargs):
        # Use the timeout value from the method argument or fall back to the instance's default
        timeout = kwargs.pop('timeout', self.timeout)
        response = method(self.baseUrl + url, timeout=timeout, **kwargs)
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
