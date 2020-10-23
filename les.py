from pymongo import MongoClient
from pprint import pprint
client = MongoClient('127.0.0.1', 27017)
db = client['users_1610']
users = db.users
books = db.books
doc = users.insert_one({"author": "Pir",
                  "age": 30,
                  "text": 'is cool! Wildberry',
                  "date": '20.06.1983'
                  })


# users.insert_one({"author": "Peter",
#                   "age": 78,
#                   "text": 'is cool! Wildberry',
#                   "tags": ['cool', 'hot', 'ice'],
#                   "date": '14.06.1983'
#                   })

# for item in users.find({'author': 'Peter'}, {'author': True, 'date': True, '_id': False}):
#     pprint(item)

# for item in users.find({'age': {'$gt': 100}}):
#     pprint(item)

for item in users.find({}).sort("author", -1).limit(3):
    pprint(item)

print(users.count_documents({}))
for item in users.find({}):
    print(item)
# users.update_one({'author': 'Peter', 'age': 78}, {'$set': {'age': 87}})
# users.replace_one({'author': 'Smith', 'age':16}, doc)
