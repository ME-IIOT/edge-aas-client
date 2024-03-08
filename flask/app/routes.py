from app import app, submodels_collection, AAS_ID_SHORT, AASX_SERVER, AAS_IDENTIFIER
from utility.submodels import (read_content_of_table, 
                               extract_key_value, 
                               aasSM_2_clientJson,
                               clientJson_2_aasSM,
                               read_submodel_element,
                               update_submodel_element,
                               update_submodel)
# from utility.utility import encode_base64url
from flask import request, Flask, jsonify
import json
import requests
from reactor.reactor import AsyncReactor
from reactor.handler import HandlerTypeName, Job
import asyncio
reactor = AsyncReactor()

@app.route('/', methods=['GET'])
def root():
    if request.method == 'GET':
        # asyncio.run(reactor.add_job(job=Job(type_=HandlerTypeName.TestHandler.value, 
        #                         request_body={"message": "Hello, World!"}))
        # )
        # Fetch a document for demonstration
        shell_document = read_content_of_table(collectionName=submodels_collection, 
                                            tableName=f"{AAS_ID_SHORT}:submodels_dictionary")
        baseUrl = request.base_url
        submodelIdShorts, _ = extract_key_value(shell_document)
        return_json = {}
        for submodelIdShort in submodelIdShorts:
            return_json[submodelIdShort] = f"{baseUrl}submodels/{submodelIdShort}"

        return jsonify(return_json), 200

@app.route('/submodels/<submodelIdShort>', methods=['GET', 'PUT'])
def submodel(submodelIdShort):
    if request.method == 'GET':
        # Fetch a document for demonstration
        submodel_template = read_content_of_table(collectionName=submodels_collection,
                                                    tableName=f"{AAS_ID_SHORT}:{submodelIdShort}")
        if submodel_template is None:
            return jsonify({"error": "Submodel not found"}), 404
        else:
            clientJson = aasSM_2_clientJson(submodel_template["submodelElements"])
            return jsonify(clientJson), 200
    elif request.method == 'PUT':
        # updated_data = request.json
        # submodel_template = read_content_of_table(collectionName=submodels_collection,
        #                                             tableName=f"{AAS_ID_SHORT}:{submodelIdShort}")
        # if submodel_template is None:
        #     return jsonify({"error": "Submodel not found"}), 404
        # else:
        #     try:
        #         clientJson_2_aasSM(clientJson=updated_data,
        #                        templateJson= submodel_template["submodelElements"])
        #     except KeyError as e:
        #         return jsonify({"error": str(e)}), 500
        #     insert_result = submodels_collection.update_one(
        #         {"_id": f"{AAS_ID_SHORT}:{submodelIdShort}"},
        #         {"$set": submodel_template},
        #         upsert=True
        #     )
        #     if insert_result.acknowledged:
        #         # TODO: Do we need to result?
        #         submodel_dictionary = read_content_of_table(collectionName=submodels_collection,
        #                                             tableName=f"{AAS_ID_SHORT}:submodels_dictionary")
        #         submodel_uid = submodel_dictionary.get(submodelIdShort)
                
        #         # encode base64
        #         aas_uid = encode_base64url(AAS_IDENTIFIER)
        #         submodel_uid = encode_base64url(submodel_uid)
                
        #         # requests.put(f'{AASX_SERVER}submodels/{submodel_uid}', timeout=0)
        #         aasxUrl = f'{AASX_SERVER}shells/{aas_uid}/submodels/{submodel_uid}'
                
        #         submodel_template_json = json.dumps(submodel_template)

        #         response = requests.put(url=aasxUrl, data=submodel_template_json)
        #         # response = requests.put(url=aasxUrl, data=submodel_template)
                
        #         if response.status_code == 204:
        #             return jsonify({"message": "Submodel updated successfully"}), 204
        #         else:
        #             return jsonify({"error": "Failed to update submodel to server"}), 500
        #         # return jsonify({"message": "Submodel updated successfully"}), 200
        #     else:
        #         return jsonify({"error": "Failed to update submodel"}), 500
        return update_submodel(collectionName=submodels_collection,
                        aas_id_short=AAS_ID_SHORT,
                        submodel_id_short=submodelIdShort,
                        aas_uid=AAS_IDENTIFIER,
                        aasx_server=AASX_SERVER,
                        updated_data=request.json,
                        sync_with_server=True)
    
# TODO: Not sure if i need this endpoint public it
# @app.route('/submodels/<submodelIdShort>/submodel-elements/<submodelElementsPath>', methods=['GET', 'PUT'])
# def submodelElements(submodelIdShort, submodelElementsPath):
#     if request.method == 'GET':
#         content, status_code = read_submodel_element(collectionName=submodels_collection,
#                                                tableName= f"{AAS_ID_SHORT}:{submodelIdShort}", 
#                                                submodelElements = submodelElementsPath)
#         if status_code == 200:
#             if isinstance(content, str):
#                 return content, status_code
#             else:
#                 content = aasSM_2_clientJson(content)
#                 return jsonify(content), status_code
#         else:
#             return jsonify(content), status_code
    
#     elif request.method == 'PUT':
#         # content_type = request.headers.get('Content-Type')
#         # if content_type == "text/plain":
#         #     return jsonify({"error": "Content-Type must be application/json"}), 400
#         updated_data = request.json
#         status_code, message = update_submodel_element(collectionName=submodels_collection,
#                                                tableName= f"{AAS_ID_SHORT}:{submodelIdShort}", 
#                                                submodelElements = submodelElementsPath,
#                                                updated_data = updated_data)
#         return jsonify(message), status_code
        
# Test idea
import os
@app.route('/admin', methods=['GET'])
def admin():
    if request.method == 'GET':
        folder_path = "exposed_script"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # List all files in the folder
            files = os.listdir(folder_path)
            return jsonify(files), 200
        else:
            return "Folder 'exposed_script' does not exist or is not a directory", 404
    else:
        return "Method not allowed", 405
    
@app.route('/admin/<script_name>', methods=['GET', 'PUT'])
def admin_script(script_name):
    if request.method == 'GET':
        folder_path = "exposed_script"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # List all files in the folder
            files = os.listdir(folder_path)
            if script_name in files:
                with open(f"{folder_path}/{script_name}", "r") as file:
                    return file.read(), 200
            else:
                return "Script not found", 404
        else:
            return "Folder 'exposed_script' does not exist or is not a directory", 404
    elif request.method == 'PUT':
        content_type = request.headers.get('Content-Type')
        if content_type == 'text/plain':
            text_data = request.data.decode('utf-8')
        folder_path = "exposed_script"
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # List all files in the folder
            files = os.listdir(folder_path)
            if script_name in files:
                with open(f"{folder_path}/{script_name}", "w") as file:
                    file.write(text_data)
                return "Script updated successfully", 200
            else:
                return "Script not found", 404
        else:
            return "Folder 'exposed_script' does not exist or is not a directory", 404
    else:
        return "Method not allowed", 405
    