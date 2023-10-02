from abc import ABC, abstractmethod #Abstract Base Class
from typing import List, Dict, Any, Optional, Callable, Union
from .MqttHandler import  MqttHandler
from .RestHandler import  RestHandler

class IAasClient(ABC):
    def register() -> None:
        pass
    def get_aas() -> None:
        pass
    def set_aas() -> None:
        pass
    def get_submodel() -> None:
        pass
    def set_submodel() -> None:
        pass


class AasRestClient(IAasClient, RestHandler):
    def __init__(self, base_url: str = 'http://repository.aas.dev.iot.murrelektronik.com'): #TODO: Change it later
        # Call the constructor of RestClient
        super().__init__(base_url)

    def register_device(self, payload: Dict[str, Union[str, int]]) -> Union[Dict[str, Union[str, int]], str]:
        # Send a POST request to the base_url/shells with the provided payload
        return self.post('/shells', data=payload)
    
    def register_submodel(self, payload: Dict[str, Union[str, int]]) -> Union[Dict[str, Union[str, int]], str]:
        # Send a POST request to the base_url/submodels with the provided payload
        return self.post('/submodels', data=payload)
    
    def get_all_devices(self) -> Union[List[Dict[str, Union[str, int]]], str]:
        # Send a GET request to the base_url/shells
        return self.get('/shells')

    def get_device(self, aasIdentifier: str) -> Union[Dict[str, Union[str, int]], str]:
        # Send a GET request to the base_url/shells/{aasIdentifier}
        return self.get(f'/shells/{aasIdentifier}')
    
    def get_submodel(self, submodelId: str) -> Union[Dict[str, Union[str, int]], str]:
        # Send a GET request to the base_url/submodels/<{submodelId}
        return self.get(f'/submodels/{submodelId}')
    
    def update_device(self, aasIdentifier: str, payload: Dict[str, Union[str, int]]) -> Union[Dict[str, Union[str, int]], str]:
        # Send a PUT request to the base_url/shells/{aasIdentifier} with the provided payload
        return self.put(f'/shells/{aasIdentifier}', data=payload)
    
    def update_submodel(self, submodelId: str, payload: Dict[str, Union[str, int]]) -> Union[Dict[str, Union[str, int]], str]:
        # Send a PUT request to the base_url/submodels/{submodelId} with the provided payload
        return self.put(f'/submodels/{submodelId}', data=payload)
        
    #TODO: Add more methods
        
    

# class Onboarding:
    
#     def __init__(self, aasClient: IAasClient):
#         self.aasClient = aasClient
    
#     def sendDeviceInfo() -> None:
#         pass

# class RemoteAccess:
#     def method() -> None:
#         pass

# class DeviceManager:
#     onboard: Optional[Onboarding]
#     remoteAccess: Optional[RemoteAccess]



#     def method() -> None:
#         pass
    
    

