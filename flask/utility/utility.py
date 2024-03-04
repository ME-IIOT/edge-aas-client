import base64
import typing

def encode_base64url(url: str) -> str:
    # Convert the string URL to bytes
    url_bytes = url.encode('utf-8')
    
    # Encode the bytes in base64
    base64_encoded = base64.urlsafe_b64encode(url_bytes)
    
    # Convert the encoded bytes back to string and return
    return base64_encoded.decode('utf-8')

import json

def extract_submodels_id(data: typing.Dict) -> typing.List[str]:
    # Initialize a list to store the filtered values
    filtered_values: typing.List[str] = []
    
    # Iterate through the submodels
    for submodel in data.get("submodels", []):
        if submodel.get("type") == "ModelReference":
            value = submodel.get("keys", [{}])[0].get("value")
            if value:
                filtered_values.append(value)
    
    return filtered_values