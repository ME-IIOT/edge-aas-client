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

from utility.submodels import read_submodel_element, update_submodel_element
import os

AAS_ID_SHORT = os.environ.get('AAS_IDSHORT')
# print(read_submodel_element(submodels_collection, f"{AAS_ID_SHORT}:SystemInformation", "Hardware.Processor"))
update_submodel_element(submodels_collection, f"{AAS_ID_SHORT}:SystemInformation", "Hardware.Memory.DiskFree", "8GB")
