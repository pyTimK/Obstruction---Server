import pymongo
from datetime import datetime
import json
from typing import List


class MongoDBHelper:
    def __init__(self, host, port, database):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[database]
        self.cars = self.db["cars"]
        self.violations = self.db["violations"]
        self.readings = self.db["readings"]
        self.coding = self.db["coding"]

    def insert_document(self, collection, document):
        self.db[collection].insert_one(document)

    def read_documents(self, collection, query):
        return self.db[collection].find(query)
    
    def read_documents_page(self, collection, query, page_number, page_size):
        cursor = self.db[collection].find(query).sort('date', pymongo.DESCENDING).skip((page_number - 1) * page_size).limit(page_size + 1)
        
        data = []
        for doc in cursor:
            data.append(json.dumps(doc, default=str))

        is_last_page = len(data) <= page_size
        if not is_last_page:
            data = data[:-1]
        
        return data, is_last_page

    def update_document(self, collection, query, update):
        self.db[collection].update_one(query, update)

    def delete_document(self, collection, query):
        self.db[collection].delete_one(query)

    
    def create_dummy_data(self):
        #! CARS
        car1 = {
                "_id": "ABC123",
                "model": "Toyota",
                "color": "Red",
                "email": "john@example.com",
                "phone": "1234567890",
                "missing": False,
                "is_detected": True,
                "date": datetime.now(),
                "snapshots": [datetime.now(), datetime.now()],
            }
        
        car2 = { 
                "_id": "XYZ789",
                "model": "Honda",
                "color": "Blue",
                "email": "jane@example.com",
                "phone": "9876543210",
                "missing": True,
                "is_detected": False,
                "date": datetime.now(),
                "snapshots": [datetime.now(), datetime.now()],
            }
        
        car3 = {
                "_id": "DEF456",
                "model": "Mitsubishi",
                "color": "Green",
                "email": "afjdksll@gmail.com",
                "phone": "09123456789",
                "missing": False,
                "is_detected": False,
                "date": datetime.now(),
                "snapshots": [datetime.now(), datetime.now()],
            }
        
        car4 = {
                "_id": "GHI789",
                "model": "Ford",
                "color": "Yellow",
                "email": "a@gmail.com",
                "phone": "09123456789",
                "missing": False,
                "is_detected": False,
                "date": datetime.now(),
                "snapshots": [datetime.now(), datetime.now()],
            }
        
        car5 = {
                "_id": "JKL012",
                "model": "Chevrolet",
                "color": "White",
                "email": "fsdfds@email.com",
                "phone": "09123456789",
                "missing": False,
                "is_detected": False,
                "date": datetime.now(),
                "snapshots": [datetime.now(), datetime.now()],
            }
        
        car6 = {
                "_id": "MNO345",
                "model": "Nissan",
                "color": "Black",
                "email": "fdsfds@gmail.com",
                "phone": "09123456789",
                "missing": False,
                "is_detected": False,
                "date": datetime.now(),
                "snapshots": [datetime.now(), datetime.now()],
            }
        
        self.cars.insert_many([car1, car2, car3, car4, car5, car6])
        


        #! VIOLATIONS
        violation1 = {
                "plate_number": car1["_id"],
                "violations": ["Obstruction"],
                "date": datetime.now(),
                "model": car1["model"],
                "color": car1["color"],
            }
        
        violation2 = {
                "plate_number": car2["_id"],
                "violations": ["Missing"],
                "date": datetime.now(),
                "model": car2["model"],
                "color": car2["color"],
            }
        
        violation3 = {
                "plate_number": car3["_id"],
                "violations": ["Obstruction", "Missing"],
                "date": datetime.now(),
                "model": car3["model"],
                "color": car3["color"],
            }
        
        violation4 = {
                "plate_number": car1["_id"],
                "violations": ["Missing"],
                "date": datetime.now(),
                "model": car1["model"],
                "color": car1["color"],
            }
        
        violation5 = {
                "plate_number": car2["_id"],
                "violations": ["Obstruction"],
                "date": datetime.now(),
                "model": car2["model"],
                "color": car2["color"],

            }
        
        violation6 = {
                "plate_number": car4["_id"],
                "violations": ["Missing"],
                "date": datetime.now(),
                "model": car4["model"],
                "color": car4["color"],
            }
        
        violation7 = {
                "plate_number": car5["_id"],
                "violations": ["Obstruction"],
                "date": datetime.now(),
                "model": car5["model"],
                "color": car5["color"],
            }
        
        violation8 = {
                "plate_number": car6["_id"],
                "violations": ["Missing"],
                "date": datetime.now(),
                "model": car6["model"],
                "color": car6["color"],
            }
        
        self.violations.insert_many([violation1, violation2, violation3, violation4, violation5, violation6, violation7, violation8])
        


        #! READINGS
        reading1 = {
                "plate_number": car1["_id"],
                "date": datetime.now(),
                "violations": ["Missing"],
            }

        reading2 = {
                "plate_number": car2["_id"],
                "date": datetime.now(),
                "violations": [],
            }
        
        reading3 = {
                "plate_number": car3["_id"],
                "date": datetime.now(),
                "violations": [],
            }
        
        reading4 = {
                "plate_number": car5["_id"],
                "date": datetime.now(),
                "violations": ["Missing"],
            }
        
        reading5 = {
                "plate_number": car6["_id"],
                "date": datetime.now(),
                "violations": [],
            }
        
        reading6 = {
                "plate_number": car5["_id"],
                "date": datetime.now(),
                "violations": [],
            }
        
        reading7 = {
                "plate_number": car1["_id"],
                "date": datetime.now(),
                "violations": ["Missing"],
            }
        
        reading8 = {
                "plate_number": car4["_id"],
                "date": datetime.now(),
                "violations": [],
            }
        
        self.readings.insert_many([reading1, reading2, reading3, reading4, reading5, reading6, reading7, reading8])
        


    
        
        #! CRUD methods for Car -----------------------------------
    def car_create(self, car):
        result = self.cars.insert_one(car)
        return result.inserted_id
    
    def car_read(self, id):
        print("1111111111111111111")
        data = self.cars.find_one({"_id": id})
        print(data)
        print("22222222222222222222")
        x = json.dumps(data, default=str)
        print(x)
        print("3333333333333333333333333")
        return json.dumps(data, default=str)

    
    def car_read_page(self, query, page_number, page_size):
        return self.read_documents_page("cars", query, page_number, page_size)

    
    def car_update(self, id, data):
        self.cars.update_one({"_id": id}, {"$set": data})
        return id

    def car_delete(self, id):
        self.cars.delete_one({"_id": id})
        return id


    #! CRUD methods for Violation -----------------------------------
    def violation_create(self, violation):
        result = self.violations.insert_one(violation)
        return result.inserted_id
    
    def violation_read(self, id):
        data = self.violations.find_one({"_id": id})
        return json.dumps(data, default=str)
    
    def violation_read_page(self, query, page_number, page_size):
        return self.read_documents_page("violations", query, page_number, page_size)
        
    def violation_update(self,id, data):
        self.violations.update_one({"_id": id}, {"$set": data})
        return id

    def violation_delete(self, id):
        self.violations.delete_one({"_id": id})
        return id


    #! CRUD methods for Reading -----------------------------------
    def reading_create(self, reading):
        result = self.readings.insert_one(reading)
        return result.inserted_id
    
    def reading_read(self, id):
        data = self.readings.find_one({"_id": id})
        return json.dumps(data, default=str)
    
    def reading_read_page(self, query, page_number, page_size):
        return self.read_documents_page("readings", query, page_number, page_size)
    
    def reading_update(self, id, data):
        self.readings.update_one({"_id": id}, {"$set": data})
        return id

    def reading_delete(self, id):
        self.readings.delete_one({"_id": id})
        return id

    #! CRUD methods for Coding -----------------------------------
    def coding_read(self, day: str):
        data = self.coding.find_one({"_id": day})
        return json.dumps(data, default=str)
    
    def coding_read_page(self, query, page_number, page_size):
        return self.read_documents_page("coding", query, page_number, page_size)
    
    def coding_update(self, day: str, data):
        self.coding.update_one({"_id": day}, {"$set": data})
        return day
