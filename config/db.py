from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Herry:Herry%405%405@cluster0.ugnohw5.mongodb.net/"

client = MongoClient(MONGO_URI)

db = client["Student_Management"]

students = db["students"]

teachers = db["teachers"]