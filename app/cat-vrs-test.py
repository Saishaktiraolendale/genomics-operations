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




print("\n[txImplication Record for CYP2D6 and Paroxetine]")

query = {
    "gene.display": "CYP2D6",
    "medicationAssessed.display": "Paroxetine"
}

doc = txImplication_db.find_one(query)
if doc:
    print(doc)
else:
    print("No matching txImplication document found.")

# -----------------------------------------------------
# 🧪 MongoDB Queries for txImplication Collection
# -----------------------------------------------------

print("\n[Query 1] Total txImplication documents:")
count = txImplication_db.count_documents({})
print(f"Total documents in txImplication: {count}")

print("\n[Query 2] Records where gene is CYP2D6 and medication is Paroxetine:")
query = {
    "gene.display": "CYP2D6",
    "medicationAssessed.display": "Paroxetine"
}
results = txImplication_db.find(query)

match_count = 0
for doc in results:
    match_count += 1
    print({
        "variationID": doc.get("variationID"),
        "gene": doc.get("gene"),
        "genotype": doc.get("genotype"),
        "predictedImplication": doc.get("predictedImplication"),
        "evidenceLevel": doc.get("evidenceLevel"),
        "medicationAssessed": doc.get("medicationAssessed")
    })

if match_count == 0:
    print("No matching documents found.")
else:
    print(f"✅ Found {match_count} matching documents.")


