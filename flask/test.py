from pymongo import MongoClient
import typing
import os

# MongoDB connection URI and database information
MONGO_URI = os.environ.get('MONGO_URI')
DATABASE_NAME = "aas_edge_database"
SHELLS_COLLECTION_NAME = "shells"
SUBMODELS_COLLECTION_NAME = "submodels"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
shells_collection = db[SHELLS_COLLECTION_NAME]
submodels_collection = db[SUBMODELS_COLLECTION_NAME]

# # Delete all documents in the 'shells' collection
# shells_delete_result = shells_collection.delete_many({})
# print(f"Deleted {shells_delete_result.deleted_count} documents from the 'shells' collection.")

# # Delete all documents in the 'submodels' collection
# submodels_delete_result = submodels_collection.delete_many({})
# print(f"Deleted {submodels_delete_result.deleted_count} documents from the 'submodels' collection.")


# # Find all documents in the shells collection
# all_shells_documents = shells_collection.find()

# # Iterate through each document and print
# for document in all_shells_documents:
#     print(document)

# Count documents in the collections
# shells_count = shells_collection.count_documents({})
# submodels_count = submodels_collection.count_documents({})

# print(f"Number of documents in 'shells' collection: {shells_count}")
# print(f"Number of documents in 'submodels' collection: {submodels_count}")

# aasIdShort = os.environ.get('AAS_IDSHORT')
# # dictionary = submodels_collection.find_one(
# #     {"_id": f"{aasIdShort}:submodels_dictionary"},
# #     {"_id": 0}
# # )
# # print(dictionary)

# def read_content_of_table(collectionName, tableName):
#     table_content = collectionName.find_one(
#         {"_id": tableName},
#         {"_id": 0}
#     )
#     return table_content

# aas_table_name =  f"{aasIdShort}:submodels_dictionary"
# print(read_content_of_table(collectionName=submodels_collection, tableName=aas_table_name))

import os

AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
# print(read_submodel_element(submodels_collection, f"{AAS_ID_SHORT}:SystemInformation", "Hardware.Processor"))
# update_submodel_element(submodels_collection, f"{AAS_ID_SHORT}:SystemInformation", "Hardware.Memory.DiskFree", "8GB")
import subprocess
import typing
# # Specify the path to your Bash script
# bash_script_path = '/path/to/your/script.sh'


# # Execute the Bash script and capture the output
# result = subprocess.run(['bash', 'exposed_script/sysInfo.sh'], capture_output=True, text=True)

# if result.returncode == 0:
#     # Print the output of the Bash script
#     print("Output:", result.stdout)
# else:
#     # Print any error message if the command failed
#     print("Error:", result.stderr)
from functools import partial
import concurrent.futures

# folder_path = "exposed_script"
# if os.path.exists(folder_path) and os.path.isdir(folder_path):
#     # List all files in the folder
#     files = os.listdir(folder_path)
#     files.remove("__init__.py")
# print(files)

# def execute_files(files: typing.List[str], folder_path: str) -> None:
#     execute_function = partial(execute_single_file, folder_path=folder_path)
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(execute_function, files)

# def execute_single_file(file: str, folder_path: str) -> None:
#     if file.endswith(".py"):
#         subprocess.run(['python', f'{folder_path}/{file}'])
#     # elif file.endswith(".sh"):
#     #     subprocess.run(['bash', f'{folder_path}/{file}'])
#     else:
#         pass

# execute_files(files, folder_path)
from utility.submodels import read_submodel_element
# overwrite_script(original_script_path="exposed_script/active-hello_world-10.py", 
#                  updated_script_content='print("Hello LNI 4.0 10s!")',
#                  new_script_path="exposed_script/active-hello_world-10.py")#,
# #                 new_script_path="exposed_script/sysInfo.sh")

# content, status_code = overwrite_script(
#     original_script_path="exposed_script/active-hello_world-10.py", 
#     updated_script_content="""print("Hello LNI 4.0!"
# """)
# print(content, status_code)

# Example usage
# bash_script = """
# echo"Hello, World!
# """
# is_valid = check_bash_syntax(bash_script)
# print(f"Is the syntax valid? {is_valid}")

# template, status_code = read_time_series_record_template(collectionName=submodels_collection, 
#                                                          aas_id_short=AAS_ID_SHORT)
# print(template)

template, status_code = read_submodel_element(collectionName=submodels_collection,
                                              aas_id_short=AAS_ID_SHORT,
                                              submodel_id_short="TimeSeries",
                                              submodelElements="Metadata.Record")
print(template, status_code)