from MongoDBHelper import MongoDBHelper
db = MongoDBHelper("localhost", 27017, "obstruction")
db.create_dummy_data()