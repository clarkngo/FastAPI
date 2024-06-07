import os
import base64
import json
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

MONGO_DETAILS = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.test
print(db.list_collection_names())

db = client.sample_mflix.movies_react_sample


class Body(BaseModel):
    length: Union[int, None] = 20

@app.get("/test")
async def read_root():
    # Example of using the database to fetch a document from the 'test' collection
    document = await db.test.find_one()
    return {"Hello": "World", "Document": document}

@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)

@app.get("/api")
async def root():
    print(os.getcwd())
    return {"message": "Hello World"}


# Function to load data from the JSON file
def load_data():
    with open("/workspaces/FastAPI/webapp/data.json", "r") as file:
        return json.load(file)

# API endpoint to get the data
@app.get("/movie/read-file")
async def get_movies():
    data = load_data()
    return data

# API endpoint to get the data
@app.get("/movie/hard-coded")
async def get_movies_hard_coded():
    return {
        "title": "The Basics - Networking",
        "description": "Your app fetched this from a remote endpoint!",
        "movies": [
            {"id": "1", "title": "Star Wars", "releaseYear": "1977"},
            {"id": "2", "title": "Back to the Future", "releaseYear": "1985"},
            {"id": "3", "title": "The Matrix", "releaseYear": "1999"},
            {"id": "4", "title": "Inception", "releaseYear": "2010"},
            {"id": "5", "title": "Interstellar", "releaseYear": "2014"}
        ]
    }

@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    return {'token': string}