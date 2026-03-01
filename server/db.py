from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

URI = "mongodb+srv://wokapplicant_db_user:3ps7kYcutHpb58j9@ipis.dare254.mongodb.net/?appName=IPIS" # HARD CODED PASSWORD!!!

def getPotholeCollection():
    """
    Establish connection with the server and fetch the relevant collection.
    """

    # Create a new client and connect to the server
    client = MongoClient(URI, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # fetch database and collection info
    database = client.get_database("PotholeDB")
    potholes = database.get_collection("potholes")

    return potholes

def getOrganizationCollection():
    """
    Establish connection with the server and fetch the relevant collection.
    """

    # Create a new client and connect to the server
    client = MongoClient(URI, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # fetch database and collection info
    database = client.get_database("PotholeDB")
    potholes = database.get_collection("organizations")

    return potholes