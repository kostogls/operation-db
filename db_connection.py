from pymongo import MongoClient
import certifi

# from credentials import define_credentials

username = 'sofiak'
pwd = 'QEfTRxwcy5X6UcCa'

# def connect_db():
#     ca = certifi.where()
#     # username, pwd = define_credentials()
#     client = MongoClient(
#         "mongodb+srv://{}:{}@cluster0.n4z9isj.mongodb.net/?retryWrites=true&w=majority".format(username, pwd), tlsCAFile=ca)
#     # db = client.aggdata_db
#     db = client.testdb
#     # print(db)
#     return db


def connect_db():
    client = MongoClient("mongodb://root:VNpVXTV2@sdg4.csd.auth.gr:28318")
    db = client.database
    # for coll in db.list_collection_names():
    #     print(coll)
    # print(db)
    try:
        db.command("serverStatus")
        # print('herew')
    except Exception as e:
        print(e)
    else:
        print("You are connected!")
    # client.close()
    return db


connect_db()
# addMongoUser()