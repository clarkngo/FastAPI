import os
import base64
import json
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()
current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

MONGO_DETAILS = os.getenv("MONGO_DETAILS")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.sample_mflix
print(f"Connecting to MongoDB with details: {MONGO_DETAILS}")

class Movie(BaseModel):
    title: str
    # description: Optional[str] = None
    # price: float
    # is_offer: Optional[bool] = None


@app.get("/test")
async def read_root():
    # Example of using the database to fetch a document from the 'test' collection
    document = await db.movies_react_sample.find_one()
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

# sample
# {"_id":{"$oid":"66637ac09d0106f27c7b8565"},"title":"Star Wars","releaseYear":"1977"}
@app.get("/movies/{movie_id}", response_model=Movie)
async def read_item(movie_id: str):
    movie = await db.movies_react_sample.find_one({"_id": ObjectId(movie_id)})
    if movie:
        movie["_id"] = str(movie["_id"])
        return movie
    raise HTTPException(status_code=404, detail="Movie not found")
