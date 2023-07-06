from pymongo import MongoClient
import certifi

# from credentials import define_credentials


def connect_db():
    ca = certifi.where()
    # username, pwd = define_credentials()
    client = MongoClient(
        "mongodb+srv://{}:{}@cluster0.n4z9isj.mongodb.net/?retryWrites=true&w=majority".format(username, pwd), tlsCAFile=ca)
    # db = client.aggdata_db
    db = client.testdb
    # print(db)
    return db


connect_db()
# addMongoUser()
