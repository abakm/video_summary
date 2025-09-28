from pydantic import BaseModel
from pymongo import MongoClient
from pydantic import BaseModel, constr





class PayloadTemplate(BaseModel):
    youtube_url: str

    # youtube_url: constr(
    #     pattern=r'^(https?://)?(www\.)?((youtube\.com/watch\?v=)|(youtu\.be/))([a-zA-Z0-9_-]{11})(\S+)?$'
    # )

# Database connection
connection = MongoClient("mongodb+srv://shopgenie:shopgenie@cluster0.2zydot4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
database = connection["Summary"]
video_db = database["video"]


