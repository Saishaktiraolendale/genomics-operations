import os
import pymongo
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
# Load secrets from secrets.env file if available
load_dotenv(Path(__file__).parent.parent / "secrets.env")

# MongoDB Client URIs
FHIR_genomics_data_client_uri = f"mongodb+srv://readonly:{os.getenv('MONGODB_READONLY_PASSWORD')}@cluster0.8ianr.mongodb.net/FHIRGenomicsData"

# MongoDB Clients
client = pymongo.MongoClient(FHIR_genomics_data_client_uri)

# Databases
db = client.FHIRGenomicsData

# Collections
patients_db = db.Patients
variants_db = db.Variants
tests_db = db.Tests
genotypes_db = db.Genotypes
dxImplication_db = db.dxImplication
txImplication_db = db.txImplication

subject = "L2345"
ranges = ["NC_000007.14:55019016-55211628", "NC_000008.11:127735433-127742951"]
experimental = True

# If experimental, query mongoDb for txImplication records that have regions that intersect our ranges

# print(patients_db.find_one({"patientID": subject}))
# {"region":{"$exists":true}}
# print(txImplication_db.find_one({"evidenceLevel": "CPIC Level A"}))
# resultSet = (txImplication_db.find({"region": {"$exists":True}}))
# for result in resultSet:
#     print(result)

query = {
    '$or': [
        {
            'region': {
                '$elemMatch': {
                    'refseq': 'NC_000007.14',
                    'start': {'$lt': 55211628},
                    'end': {'$gte': 55019016}
                }
            }
        },
        {
            'region': {
                '$elemMatch': {
                    'refseq': 'NC_000008.11',
                    'start': {'$lt': 127742951},
                    'end': {'$gte': 127735433}
                }
            }
        }
    ]
}

resultSet = (txImplication_db.find(query))
for result in resultSet:
    print(result)


new_subject = "PH800"

print(f"\n[Patient Info for {new_subject}]")
new_patient_data = patients_db.find_one({"patientID": new_subject})
if new_patient_data:
    print(new_patient_data)
else:
    print(f"No patient found with ID: {new_subject}")




print("\n[All txImplication Records]")
for doc in txImplication_db.find():
    print(doc)


