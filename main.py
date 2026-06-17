# from this main.py file, we will import the app from the app package and run it. This is the entry point of our application, and it will allow us to start the server and listen for incoming requests. By keeping the main.py file simple and focused on running the app, we can ensure that our application is easy to understand and maintain. This also allows us to separate the concerns of running the app from the rest of our application logic, which can be defined in other files and packages.

from fastapi import FastAPI

from src.utils.db import Base, engine
from src.utils.settings import Settings

from src.tasks.model import TaskModel # ye line hamare TaskModel ko import karti hai, jisse ham apne database me "tasks" naam ke table ko create kar sakte hai. Ye line ensure karti hai ki hamare TaskModel ke structure ke according database me ek "tasks" naam ka table create ho jayega.

from src.user.router import user_routes # ye line hamare user_routes ko import karti hai, jisse ham apne application me users ke related routes ko include kar sakte hai. Ye line ensure karti hai ki hamare application me users ke related endpoints properly defined ho jayenge aur ham unhe access kar sakte hai.

Base.metadata.create_all(engine) # es line se ham apne database me tables create karenge jo hamne apne models me define kiye hai. Ye line ensure karti hai ki jab ham apne application ko run karenge, to hamare database me necessary tables create ho jayenge agar wo pehle se exist nahi karte hai.

from src.tasks.router import task_routes

import subprocess

import sys

app = FastAPI(title="Task Management API")

app.include_router(task_routes) # es line se ham apne application me task_routes ko include karenge, jisse hamare application me tasks ke related endpoints properly defined ho jayenge aur ham unhe access kar sakte hai. Ye line ensure karti hai ki hamare application me tasks ke related routes properly registered ho jayenge aur ham unhe use kar sakte hai.

app.include_router(user_routes) # es line se ham apne application me user_routes ko include karenge, jisse hamare application me users ke related endpoints properly defined ho jayenge aur ham unhe access kar sakte hai. Ye line ensure karti hai ki hamare application me users ke related routes properly registered ho jayenge aur ham unhe use kar sakte hai.


@app.on_event("startup")
async def startup_event():
    # Render par har baar startup par migration chal jayegi
    subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"])
 # ye line hamare task_routes ko import karti hai, jisse ham apne application me tasks ke related routes ko include kar sakte hai. Ye line ensure karti hai ki hamare application me tasks ke related endpoints properly defined ho jayenge aur ham unhe access kar sakte hai.