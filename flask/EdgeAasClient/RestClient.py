from abc import ABC, abstractmethod
from typing import Optional, Dict, Union
import requests

class IRestClient(ABC):
    
    @abstractmethod
    def get(self, url: str, params: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        """
        Send a GET request to the specified URL.
        
        Parameters:
            - url (str): The URL of the request.
            - params (Dict[str, str], optional): The URL parameters to be sent with the request.
            - headers (Dict[str, str], optional): The HTTP headers to send with the request.
            
        Returns:
            Union[Dict[str, Union[str, int]], str]: The response from the server, parsed as a JSON if possible, otherwise as a string.
        """
        pass
    
    @abstractmethod
    def post(self, url: str, data: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        """
        Send a POST request to the specified URL.
        
        Parameters:
            - url (str): The URL of the request.
            - data (Dict[str, str], optional): The data to send in the request's body.
            - headers (Dict[str, str], optional): The HTTP headers to send with the request.
            
        Returns:
            Union[Dict[str, Union[str, int]], str]: The response from the server, parsed as a JSON if possible, otherwise as a string.
        """
        pass
    
    @abstractmethod
    def put(self, url: str, data: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        """
        Send a PUT request to the specified URL.
        
        Parameters:
            - url (str): The URL of the request.
            - data (Dict[str, str], optional): The data to send in the request's body.
            - headers (Dict[str, str], optional): The HTTP headers to send with the request.
        
        Returns:
            Union[Dict[str, Union[str, int]], str]: The response from the server, parsed as a JSON if possible, otherwise as a string.
        """
        pass
    
    @abstractmethod
    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        """
        Send a DELETE request to the specified URL.
        
        Parameters:
            - url (str): The URL of the request.
            - headers (Dict[str, str], optional): The HTTP headers to send with the request.
        
        Returns:
            Union[Dict[str, Union[str, int]], str]: The response from the server, parsed as a JSON if possible, otherwise as a string.
        """
        pass


class RestClient(IRestClient):

    def __init__(self, baseUrl: str = ''):
        self.baseUrl = baseUrl

    def get(self, url: str, params: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        response = requests.get(self.baseUrl + url, params=params, headers=headers)
        return self._parse_response(response)

    def post(self, url: str, data: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        response = requests.post(self.baseUrl + url, json=data, headers=headers)
        return self._parse_response(response)

    def put(self, url: str, data: Optional[Dict[str, str]] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        response = requests.put(self.baseUrl + url, json=data, headers=headers)
        return self._parse_response(response)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> Union[Dict[str, Union[str, int]], str]:
        response = requests.delete(self.baseUrl + url, headers=headers)
        return self._parse_response(response)

    def _parse_response(self, response: requests.Response) -> Union[Dict[str, Union[str, int]], str]:
        try:
            return response.json()
        except ValueError:
            return response.text

