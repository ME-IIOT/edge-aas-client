from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import base64 #for encoding and decoding aasIdentifier and submodelId
from threading import Thread, Event
from polling import Polling
import requests
from parser_submodel import *
# from bson.objectid import ObjectId


app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"

mongo = PyMongo(app)

def run_polling(extUrl, intUrl, stopEvent):
    with app.app_context():
        polling = Polling(extUrl, intUrl, stopEvent)
        polling.loop()

has_started = False

SERVER_URL = "http://localhost:51000"
AAS_IDSHORT = "Murrelektronik_V000_CTXQ0_0100001_AAS"
# @app.before_request
# def start_polling_thread():
#     global stop_event, polling_thread, has_started
#     if not has_started:
#         has_started = True
#         stop_event = Event()
#         polling_thread = Thread(target=run_polling, args=('http://repository.aas.dev.iot.murrelektronik.com', 'http://127.0.0.1:5000', stop_event))
#         polling_thread.start()

def collect_data_from_server(serverURL=SERVER_URL, aasIDShort=AAS_IDSHORT):
    # get submodels
    print("Collecting data from server...")

    submodelsURL = f"{serverURL}/aas/{aasIDShort}/submodels"
    response = requests.get(submodelsURL)
    gatewayDB = submodels_transform_data(response.json(), baseURL= "/submodels")
    for submodel in gatewayDB:
        submodelURL = f"{serverURL}/aas/{aasIDShort}/submodels/{submodel['name']}/deep"
        response = requests.get(submodelURL)
        submodel["value"] = submodelElements = aas_SM_element_2_name_value(response.json()["submodelElements"], f"{submodel['link']}/elements")

    # Update the document if it exists, insert if it does not (upsert)
    print("Updating MongoDB...")
    mongo.db.aas.update_one(
        {"id": aasIDShort},  # Query parameter
        {"$set": {"submodels": gatewayDB}},  # Update parameter
        upsert=True  # Insert if not exists
    )

def get_template(submodel: str, elements_list: list, serverURL = SERVER_URL, aasIDShort = AAS_IDSHORT ):
    elements_list = "/".join(elements_list)
    element_URL = f"{serverURL}/aas/{aasIDShort}/submodels/{submodel}/elements/{elements_list}/deep"
    response = requests.get(element_URL).json()["elem"]
    return response

def delete_element(submodel, elements_list):
    elements_path = "/".join(elements_list)
    element_URL = f"{SERVER_URL}/aas/{AAS_IDSHORT}/submodels/{submodel}/elements/{elements_path}"
    
    try:
        response = requests.delete(element_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        return response.json()  # Assuming the server responds with JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error deleting element: {e}")
        return None

def add_element(submodel, elements_list, request_data):
    elements_path = "/".join(elements_list)
    element_URL = f"{SERVER_URL}/aas/{AAS_IDSHORT}/submodels/{submodel}/elements/{elements_path}"
    
    try:
        response = requests.put(element_URL, json=request_data)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        return response.json()  # Assuming the server responds with JSON data
    except requests.exceptions.RequestException as e:
        print(f"Error adding element: {e}")
        return None

def update_element(submodel: str, elements_list: list, request_data, serverURL = SERVER_URL, aasIDShort = AAS_IDSHORT,  ):
    delete_elements_path = "/".join(elements_list)
    delete_element_URL = f"{serverURL}/aas/{aasIDShort}/submodels/{submodel}/elements/{delete_elements_path}"
    add_elements_path = "/".join(elements_list.pop(-1))
    add_element_URL = f"{serverURL}/aas/{aasIDShort}/submodels/{submodel}/elements/{add_elements_path}"
    # delete_element(submodel=submodel, elements_list=elements_list)
    # add_element(submodel=submodel, elements_list=elements_list, request_data=request_data)
    response = requests.delete(delete_element_URL)
    response = requests.put(add_element_URL, data=request_data)
    return None

def update_database(submodel, path_list, data):
    try:
        # Fetch the entire document
        query = {"id": AAS_IDSHORT}
        aas_data = mongo.db.aas.find_one(query)

        if not aas_data:
            return {"error": "AAS Data not found", "status_code": 404}

        # Navigate to the submodel and path
        submodel_data = None
        for sm in aas_data.get("submodels", []):
            if sm["name"] == submodel:
                submodel_data = sm
                break
        
        if not submodel_data:
            return {"error": "Submodel not found", "status_code": 404}

        elements = submodel_data["value"]
        for path in path_list:
            found = False
            for element in elements:
                if element["name"] == path:
                    if path != path_list[-1]:
                        elements = element['value']
                    # else:
                    #     elements = element
                    found = True
                    break
            if not found:
                return {"error": f"Path {path} not found", "status_code": 404}

        # Now 'elements' should be the part of the data we want to update
        # Replace the element has name == path_list[-1] with the new data
        for i,element in enumerate(elements):
            if element["name"] == path_list[-1]:
                elements[i] = data[0]
                break


        # Update the entire document in the database
        result = mongo.db.aas.replace_one({"_id": aas_data["_id"]}, aas_data)

        if result.modified_count == 0:
            return {"message": "Data was not updated, likely because it is the same as existing data", "status_code": 200}

        return {"message": "Data updated successfully", "status_code": 200}

    except Exception as e:
        # Log the error and return a 500 error to the client
        print(str(e))  # or use logging if set up
        return {"error": "An error occurred while updating the data", "status_code": 500}


    
    

@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    # Query the MongoDB collection for the desired document
    data = mongo.db.aas.find_one({"id": AAS_IDSHORT})
    
    # Check if data was found
    if data:
        # Remove MongoDB's internal _id before returning data as it is not JSON serializable
        data.pop('_id', None)
        return jsonify(data)
    else:
        return jsonify(error="Data not found"), 404
    
@app.route('/submodels/<submodel>', methods=['GET', 'POST'], strict_slashes=False)
def get_submodels(submodel):
    # For GET request method
    if request.method == 'GET':
        # Query MongoDB for the submodel
        data = mongo.db.aas.find_one({"id": AAS_IDSHORT, "submodels.name": submodel}, {"_id": 0, "submodels.$": 1})
        
        # Check if data was found
        if data and 'submodels' in data and len(data['submodels']) > 0:
            return jsonify(data['submodels'][0])
        else:
            return jsonify(error="Submodel not found"), 404
    # For POST request method
    elif request.method == 'POST':
        pass

@app.route('/submodels/<submodel>/elements/<path:elements_path>', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
def get_submodel_elements(submodel, elements_path):
    # Split the path into parts
    # path_list = elements_path.split("/")
    
    path_list = [element for element in elements_path.split("/") if element]
    if request.method == 'GET':
        
        # Construct a MongoDB query using path_parts
        query = {"id": AAS_IDSHORT, "submodels.name": submodel}
        
        # Find the document
        data = mongo.db.aas.find_one(query, {"_id": 0, "submodels.$": 1})
        
        # Check if data was found
        if data and 'submodels' in data and len(data['submodels']) > 0:
            submodel_data = data['submodels'][0]
            
            # Navigate through the element_path to find the specific element
            elements = submodel_data['value']
            try:
                for path in path_list:
                    for element in elements:
                        if element['name'] == path:
                            if path != path_list[-1]:
                                elements = element['value']
                            else:
                                elements = [element]
                            break
                    else:
                        raise KeyError(f"Element path {elements_path} not found")
                    # submodel_data = submodel_data['value'][path]  # Example navigation; adjust per schema
            except (KeyError, TypeError):
                # Return a 404 error if the path is not found
                return jsonify(error=f"Element path {elements_path} not found"), 404
            
            return jsonify(elements)  # Return found data
        else:
            return jsonify(error="Data not found"), 404
        
    elif request.method == 'POST':
        # Implement logic for POST method here
        pass
    elif request.method == 'PUT':
        try:
            data = request.json
            if not data:
                return jsonify(message="No input data provided"), 400

            # Update Database
            update_result = update_database(submodel, path_list, data)

            if 'error' in update_result:
                return jsonify(
                    message=update_result.get('message', None),
                    error=update_result.get('error', None),
                    server_response=None
                ), update_result.get('status_code', 500)

            # Update Server
            # 1. Get template
            template = [get_template(submodel=submodel, elements_list=path_list)]

            # 2. Translate data to template
            data = name_value_2_django_response(data)
            django_response_2_aas_SM_element(data, template)
            templateData = template[0]

            # 3. Send request to server
            response = delete_element(submodel=submodel, elements_list=path_list)
            path_list.pop(-1)
            response = add_element(submodel=submodel, elements_list=path_list, request_data=templateData)

            return jsonify(
                message=update_result.get('message', None),
                error=update_result.get('error', None),
                server_response=response
            ), update_result.get('status_code', 500)

        except Exception as e:
            # Handle other exceptions
            return jsonify(message="An error occurred", error=str(e)), 500
    elif request.method == 'DELETE':
        # Implement logic for DELETE method here
        pass



if __name__ == '__main__':
    # try:
    #     collect_database_from_server()
    #     app.run(debug=True)
    # except KeyboardInterrupt:  # When you press Ctrl+C
    #     stop_event.set()       # Signal the thread to stop
    #     polling_thread.join()  # Wait for the thread to finish
    collect_data_from_server()
    app.run(debug=True)
