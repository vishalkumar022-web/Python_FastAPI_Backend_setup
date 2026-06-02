# from this main.py file, we will import the app from the app package and run it. This is the entry point of our application, and it will allow us to start the server and listen for incoming requests. By keeping the main.py file simple and focused on running the app, we can ensure that our application is easy to understand and maintain. This also allows us to separate the concerns of running the app from the rest of our application logic, which can be defined in other files and packages.

from fastapi import FastAPI

from src.utils.db import Base, engine

Base.metadata.create_all(engine) # es line se ham apne database me tables create karenge jo hamne apne models me define kiye hai. Ye line ensure karti hai ki jab ham apne application ko run karenge, to hamare database me necessary tables create ho jayenge agar wo pehle se exist nahi karte hai.


app = FastAPI(title="Task Management API")


