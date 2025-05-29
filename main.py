import pymongo
import getCredentials as cred

username = cred.getUsername()
password = cred.getPassword()
dbName = "firstDB"
colName = "users"
connectionString = f"mongodb+srv://{username}:{password}@practicecluster.nfndhxg.mongodb.net/"

def createDatabase():
    client = pymongo.MongoClient(connectionString)
    mydb = client[dbName]
    dbs = client.list_database_names()
    if dbName in dbs:
        print("db exists")
    else:
        print("db is only created once it gets content")

    # a database stores collections, which are created when they get content (a document)
    collection = mydb[colName]
    collections = mydb.list_collection_names()
    if colName in collections:
        print("collection exists")
    else:
        print("no docs in collection yet")

    #insert one record/ document:
    user = {"name": "abc", "age": 100}
    x = collection.insert_one(user)
    print("auto-assigned unique ID of new item:", x.inserted_id)

    #insert many:
    users = [
        {"name": "def", "age": 50},
        {"name": "ghi", "age": 25}
    ]
    y = collection.insert_many(users)
    print("auto assigned IDs of added items:", y.inserted_ids)

    #insert document(s) with specified id
    #ids must be unique
    try:
        userId = {"_id": 10, "name": "jkl", "age": 200}
        z = collection.insert_one(userId)
        print("user with pre-defined ID:", z.inserted_id)
    except:
        print("user with given _id already exists")

def findDataAndLimitResults():
    client = pymongo.MongoClient(connectionString)
    mydb = client[dbName]
    coll = mydb[colName]

    #find_one() returns first record in collection
    print(coll.find_one())

    #find() returns all records with all (with no params) or specific fields
    records = coll.find()
    for r in records: print(r)

    # use 0 to skip field, 1 to include
    # CANNOT mix 0s and 1s, unless the only 0 is for _id:
    # using 1 to include means unmentioned fields are skipped
    # using 0 means unmentioned fields are included by default
    for r in coll.find({}, {"_id": 0, "name": 1}):
        print(r)

    '''LIMITING'''
    # can limit the number of returned results:
    limit2 = coll.find().limit(2)
    for l in limit2: print(l)

def filterAndSortResults():
    client = pymongo.MongoClient(connectionString)
    mydb = client[dbName]
    coll = mydb[colName]

    '''FILTERING'''
    # first parameter of find is a query (e.g. WHERE in SQL)
    # specific values to search for
    query = {"name": "abc"}
    result = coll.find(query)
    for r in result: print(r)

    # advanced example
    # {%gt: S} = all values whose first letter is S or higher in the alphabet
    advQuery = {"name": {"$gt": "b"}}
    advResult = coll.find(advQuery)
    for ar in advResult: print(ar)

    # regex example
    # {"$regex": "^S"} = all fields starting with S
    # (queries also work with find_one())
    reQuery = {"name": {"$regex": "^a"}}
    reResult = coll.find_one(reQuery)
    for rr in reResult: print(rr)

    '''SORTING'''
    # sort by fieldname, direction (asc/ desc, asc is default):
    sortedAsc = advResult.sort("age")
    sortedAlsoAsc = advResult.sort("age", 1)
    sortedDesc = advResult.sort("age", -1)

    '''NOTE: CAN COMBINE SORTs, LIMITs and FINDs:'''
    # find must come first, sort and limit may change results but order can vary
    advResult = coll.find(advQuery).sort("name").limit(2)
    advResult = coll.find(advQuery).limit(2).sort("name")


def deleteDocs():
    client = pymongo.MongoClient(connectionString)
    mydb = client[dbName]
    coll = mydb[colName]

    # use filter to determine which document to delete
    query = {"name": "def"}
    # delete_one deletes first doc matching the query
    result = coll.delete_one(query)
    deletedDocument = result.raw_result
    print(deletedDocument)

    # can use advanced syntax and delete multiple docs as well
    advQuery = {"name": {"$gt": "b"}}
    result = coll.delete_many(advQuery)
    print("number of deletions:", result.deleted_count)

    # passing an empty query to delete_many deletes ALL docs
    deleteAll = coll.delete_many({})
    print("number of deletions:", deleteAll.deleted_count)

def updateDocs():
    client = pymongo.MongoClient(connectionString)
    mydb = client[dbName]
    coll = mydb[colName]

    # write a query to find a record, then new data to insert in it
    query = {"name": "def"}
    changes = {"age": 1000}
    result = coll.update_one(query, changes)
    print("was update successful:", result.did_upsert)

    # can update many the same way
    advQuery = {"name": {"$gt": "b"}}
    result = coll.update_many(advQuery, changes)
    print("number of changes:", result.modified_count)

def dropCollection():
    client = pymongo.MongoClient(connectionString)
    mydb = client[dbName]
    coll = mydb[colName]

    # can drop a collection with .drop()
    # returns true if successful, false if not (collection doesn't exist)
    coll.drop()