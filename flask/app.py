from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import base64 #for encoding and decoding aasIdentifier and submodelId
from threading import Thread, Event
from polling import Polling
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

@app.before_request
def start_polling_thread():
    global stop_event, polling_thread, has_started
    if not has_started:
        has_started = True
        stop_event = Event()
        polling_thread = Thread(target=run_polling, args=('http://repository.aas.dev.iot.murrelektronik.com', 'http://127.0.0.1:5000', stop_event))
        polling_thread.start()


@app.route('/')
def home():
    return "Hello, Flask with MongoDB!"

@app.route('/shells', methods=['GET', 'POST'])
def manage_shells():
    if request.method == 'POST':
        # Fetch data from the POST request payload
        data = request.json
        if not data or not all(key in data for key in ["id", "assetInformation"]): #TODO: add modelType for v3
            return jsonify(message="Missing information"), 400

        # Adding the data to the "shell" collection in MongoDB
        mongo.db.shells.insert_one(data) #table name "shells"
        # send request to the server?
        # TODO

        return jsonify(message="shell added successfully!")
    
    elif request.method == 'GET':
        # Fetching all shells from our MongoDB
        shells = list(mongo.db.shells.find({}))
        
        # Remove the _id key from each shell
        for shell in shells:
            shell.pop("_id", None)
            
        return jsonify(shells=shells)



@app.route('/shells/<aasIdentifier>', methods=['GET']) #TODO: add method PUT
def manage_shell(aasIdentifier):
    # Decode the aasIdentifier using Base64
    decodedAasIdentifier = base64.b64decode(aasIdentifier).decode('utf-8')

    # if request.method == 'PUT':
    #     data = request.json
    #     if not data:
    #         return jsonify(message="No input data provided"), 400

    #     # Replace the entire object with the new data, based on the 'id' field
    #     result = mongo.db.shells.replace_one({"id": decodedAasIdentifier}, data)
        
    #     if result.modified_count == 0:
    #         return jsonify(message="Shell not found or not modified"), 404
    #     # Update server (Your TODO might go here)
    #     # TODO
    #     return jsonify(message="Shell updated successfully!")

    if request.method == 'GET':
        # Fetching the shell data from our MongoDB based on the decodedAasIdentifier
        shell = mongo.db.shells.find_one({"id": decodedAasIdentifier})
        if not shell:
            return jsonify(message="Shell not found"), 404
        
        # Remove the _id key
        shell.pop("_id", None)

        # Return the shell data directly without nesting it under the 'shell' key
        return jsonify(shell)



@app.route('/submodels', methods=['GET', 'POST'])
def manage_submodels():
    if request.method == 'POST':
        # Fetch data from the POST request payload
        data = request.json
        if not data or not all(key in data for key in ["id", "modelType"]): # TODO: check openAPI for required fields
            return jsonify(message="Missing submodel information"), 400
        
        # Adding the submodel data to the "submodel" collection in MongoDB
        mongo.db.submodels.insert_one(data)
        # POST to server
        # TODO

        return jsonify(message="Submodels added successfully!")
    
    elif request.method == 'GET':
        # Fetching all submodels from our MongoDB (can be optimized for larger datasets)
        submodels = list(mongo.db.submodels.find({}))
        
        # Convert the ObjectId to string for serialization
        for submodel in submodels:
            submodel.pop("_id", None)
            
        return jsonify(submodels=submodels)


@app.route('/submodels/<submodelId>', methods=['GET', 'PUT'])
def manage_submodel(submodelId):
    
    # Decode the submodelId using Base64
    decodedSubmodelId = base64.b64decode(submodelId).decode('utf-8')

    if request.method == 'GET':
        submodel = mongo.db.submodels.find_one({"id": decodedSubmodelId})
        if not submodel:
            return jsonify(message="Submodel not found"), 404

        # Remove the _id key
        submodel.pop("_id", None)

        # Return the submodel data directly
        return jsonify(submodel)

    
    elif request.method == 'PUT':
        data = request.json
        if not data:
            print(1)
            return jsonify(message="No input data provided"), 400

        result = mongo.db.submodels.update_one({"id": decodedSubmodelId}, {"$set": data})
        if result.modified_count == 0:
            return jsonify(message="Submodel not found or not modified"), 404
        return jsonify(message="Submodel updated successfully!")

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:  # When you press Ctrl+C
        stop_event.set()       # Signal the thread to stop
        polling_thread.join()  # Wait for the thread to finish
