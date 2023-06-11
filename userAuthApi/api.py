from fastapi import FastAPI
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel

class User(BaseModel):
    name: str 
    email: str 
    token: str = None

app = FastAPI()

database = {}

@app.get('/')
def home():
    return {'Data': 'Home'}

@app.get('/data')
def data():
    return database

@app.get('/get-user/{user_id}')
def find_user(user_id: int):
    if database[user_id] not in database.keys():
        return {"Error": "There is no such user in the database."}
    return database[user_id]


@app.post('/auth/{user_id}')
def auth(user_id: int, user_information: User):
    if user_id not in database.keys():
        database[user_id] = user_information
        database[user_id].token = uuid4()
        return {
            "Successful": user_information.email, "Token": user_information.token
        }
    return {"Error": "This user is already exists!"}


@app.delete('/delete-user')
def delete(user_id: int):
    if user_id not in database.keys():
        return{"Error": "There's no such user in the database"}
    else:
        del database[user_id]
        return {"Sucessful": "Deleted this user!"}