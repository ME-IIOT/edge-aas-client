import json

def check_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            json.load(json_file)
        print(f"The JSON file '{file_path}' is valid.")
    except json.JSONDecodeError as e:
        print(f"Error in JSON file '{file_path}':")
        print(f"Line {e.lineno}, column {e.colno}: {e.msg}")
        print(e.doc)
        print("^" * (e.colno - 1))

def restructure_json(file_path):
    # Load JSON data from the file
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    
    # Sort the keys alphabetically
    sorted_data = {key: data[key] for key in sorted(data)}

    # Write the sorted data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(sorted_data, json_file, indent=2)

# Specify the paths to the JSON files
request_file_path = 'request_submodel.json'
response_file_path = 'response_submodel.json'

# Validate the JSON files before proceeding
check_json_file(request_file_path)
check_json_file(response_file_path)

# Restructure the JSON files by sorting keys
restructure_json(request_file_path)
restructure_json(response_file_path)

# Load JSON data from the request_submodel.json and response_submodel.json files
with open(request_file_path, 'r') as request_file:
    request_data = json.load(request_file)

with open(response_file_path, 'r') as response_file:
    response_data = json.load(response_file)

# Compare JSON objects using the == operator
if request_data == response_data:
    print("The JSON objects are the same.")
else:
    print("The JSON objects are different.")
