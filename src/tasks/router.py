# In this router file, we will define the routes that will handle the requests from the client and call the appropriate controller functions to perform the necessary operations on the user data. We will use FastAPI to define these routes and to handle the requests and responses. We will also define any necessary path parameters or query parameters for these routes to ensure that we can properly handle the requests from the client.  


from fastapi import APIRouter , Depends # yaha ye api router ka kaam same to same @RestController IN JAVA  jaisa hi hai, ye hume apne routes ko organize karne me help karega aur hume apne routes ke liye ek common prefix dene ki suvidha bhi dega. Isse hum apne routes ko easily manage kar sakte hain aur unhe logically group kar sakte hain.

from src.tasks import controller

from src.tasks.dtos import TaskDTO # yaha ham TaskDTO paas kr rhe hai kyunki yahi data hamare body me ham paas krenge 

from src.utils.db import get_db # yaha ham get_db function ko import kr rhe hai, jisse ham apne database session ko create kr sake aur usse apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain.


task_routes = APIRouter(prefix="/tasks")


@task_routes.post("/create") # post api method /tasks/create endpoint rhega..

def create_task(body:TaskDTO,db = Depends(get_db)): # yaha ham apne create_task function me body parameter ko TaskDTO type ka define kr rhe hai, jisse ham apne client se aane wale data ko validate kr sake aur ensure kr sake ki wo expected structure ke according hai. Isse ham apne application me data validation ko ensure kr sakte hain aur client se aane wale data ko expected structure ke according validate kar sakte hain. Aur db parameter me ham get_db function ko Depends ke through pass kr rhe hai, jisse ham apne database session ko create kr sake aur usse apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain.
    return controller.create_task(body , db) # yaha ham apne controller ke create_task function ko call kr rhe hai, jisme ham body aur db parameters ko pass kr rhe hai.


@task_routes.get("/get_all_Tasks") # get api method /tasks/get endpoint rhega..
def get_all_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)

