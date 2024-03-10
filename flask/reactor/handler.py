import typing
from abc import ABC, abstractmethod
from utility.utility import encode_base64url
import aiohttp
import json
import enum

async def perform_http_request(method: str, url: str, data=None, headers=None):
    """
    Perform an asynchronous HTTP request and handle exceptions.

    Parameters:
    - method: The HTTP method to use ('GET', 'PUT', 'POST', etc.).
    - url: The URL for the request.
    - data: The request payload, optional.
    - headers: Dictionary of request headers, optional.

    Returns:
    A tuple containing the response data and the HTTP status code.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=data, headers=headers) as response:
                response_data = await response.text()  # Assuming response is text
                if response.status in [200, 201, 204]:
                    return ({"message": response_data}, response.status)
                else:
                    return ({"error": f"HTTP request failed: {response_data}"}, response.status)
    except aiohttp.ClientError as e:
        return ({"error": f"HTTP Client Error occurred: {str(e)}"}, 500)
    except Exception as e:
        return ({"error": f"An unexpected error occurred: {str(e)}"}, 500)

# def perform_http_request(method: str, url: str, data=None, headers=None):
#     """
#     Perform a synchronous HTTP request and handle exceptions.

#     Parameters:
#     - method: The HTTP method to use ('GET', 'PUT', 'POST', etc.).
#     - url: The URL for the request.
#     - data: The request payload, optional.
#     - headers: Dictionary of request headers, optional.

#     Returns:
#     A tuple containing the response data and the HTTP status code.
#     """
#     try:
#         response = requests.request(method, url, data=data, headers=headers)
#         response_data = response.text  # Assuming response is text
#         if response.status_code in [200, 201, 204]:
#             return ({"message": response_data}, response.status_code)
#         else:
#             return ({"error": f"HTTP request failed: {response_data}"}, response.status_code)
#     except requests.RequestException as e:
#         return ({"error": f"HTTP Client Error occurred: {str(e)}"}, 500)
#     except Exception as e:
#         return ({"error": f"An unexpected error occurred: {str(e)}"}, 500)
    
class Job:
    type: str
    requestBody: typing.Dict

    def __init__(self, type_: str, requestBody: typing.Dict):
        self.type = type_
        self.requestBody: typing.Dict = requestBody

class Handler(ABC):
    @abstractmethod
    async def handle(self, job: Job):
        raise NotImplementedError
    
class HandlerTypeName(enum.Enum):
    TestHandler = "TEST_HANDLER"
    UPDATE_AASX_SUBMODEL_SERVER = "UPDATE_AASX_SUBMODEL_SERVER"
    UPDATE_AASX_SUBMODEL_ELEMENT_SERVER = "UPDATE_AASX_SUBMODEL_ELEMENT_SERVER"

class TestHandler(Handler):
    async def handle(self, job: Job):
        print("TestHandler.handle() called")
        print(job.requestBody)

class UpdateAasxSubmodelServerHandler(Handler):
    async def handle(self, job: Job):
        print("UpdateAasxSubmodelServerHandler.handle() called")
        json_data = job.requestBody.get("json_data")
        aas_uid = job.requestBody.get("aas_uid")
        submodel_uid = job.requestBody.get("submodel_uid")
        aasx_server = job.requestBody.get("aasx_server")

        aas_uid = encode_base64url(aas_uid)
        submodel_uid = encode_base64url(submodel_uid)

        aasxUrl = f"{aasx_server}/shells/{aas_uid}/submodels/{submodel_uid}"
        
        json_data = json.dumps(json_data)

        # try:
        #     # Use aiohttp.ClientSession for the asynchronous PUT request
        #     async with aiohttp.ClientSession() as session:
        #         async with session.put(url=aasxUrl, data=json_data) as response:
        #             if response.status == 204:
        #                 # return ({"message": "Submodel to server updated successfully"}, 204)
        #                 print({"message":"Submodel to server updated successfully",
        #                        "status_code": 204})
        #             else:
        #                 # For better error handling, consider reading response text
        #                 error_text = await response.text()
        #                 #return ({"error": f"Failed to update submodel to server: {error_text}"}, response.status)
        #                 print({"error": f"Failed to update submodel to server: {error_text}",
        #                        "status_code": response.status})
        # except aiohttp.ClientError as e:
        #     # Handle client-side errors (e.g., connection problems)
        #     return ({"error": f"HTTP Client Error occurred: {str(e)}"}, 500)
        # except Exception as e:
        #     # Handle other unforeseen errors
        #     return ({"error": f"An unexpected error occurred: {str(e)}"}, 500)
        headers = {"Content-Type": "application/json"}

        # Reuse the perform_http_request function with the required parameters
        response, status = await perform_http_request("PUT", aasxUrl, data=json_data, headers=headers)
        print("Response from Server: ", response, status)

# class UpdateAasxSubmodelServerHandler:
#     def handle(self, job):
#         print("UpdateAasxSubmodelServerHandler.handle() called")
#         json_data = job.requestBody.get("json_data")
#         aas_uid = job.requestBody.get("aas_uid")
#         submodel_uid = job.requestBody.get("submodel_uid")
#         aasx_server = job.requestBody.get("aasx_server")

#         # Your encoding functions here
#         aas_uid = encode_base64url(aas_uid)
#         submodel_uid = encode_base64url(submodel_uid)

#         aasxUrl = f"{aasx_server}/shells/{aas_uid}/submodels/{submodel_uid}"
        
#         json_data = json.dumps(json_data)

#         print("JSON Data: ", json_data)
#         print("AASX URL: ", aasxUrl)

#         headers = {"Content-Type": "application/json"}

#         # Use ThreadPoolExecutor to run the synchronous perform_http_request function
#         with ThreadPoolExecutor(max_workers=5) as executor:
#             future = executor.submit(perform_http_request, "PUT", aasxUrl, data=json_data, headers=headers)
#             response, status = future.result()
#             print("Response from Server: ", response, status)


class UpdateAasxSubmodelElementServerHandler(Handler):
    async def handle(self, job: Job):
        json_data = job.requestBody.get("json_data")
        aas_uid = job.requestBody.get("aas_uid")
        submodel_uid = job.requestBody.get("submodel_uid")
        submodelElements = job.requestBody.get("submodelElements")
        aasx_server = job.requestBody.get("aasx_server")

        aas_uid = encode_base64url(aas_uid)
        submodel_uid = encode_base64url(submodel_uid)

        aasxUrl = f"{aasx_server}/shells/{aas_uid}/submodels/{submodel_uid}/submodel-elements/{submodelElements}"
        
        json_data = json.dumps(json_data)

        headers = {"Content-Type": "application/json"}

        # Reuse the perform_http_request function with the required parameters
        response, status = await perform_http_request("PUT", aasxUrl, data=json_data, headers=headers)
        print(response, status)