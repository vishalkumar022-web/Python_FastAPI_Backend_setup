# In this router file, we will define the routes that will handle the requests from the client and call the appropriate controller functions to perform the necessary operations on the user data. We will use FastAPI to define these routes and to handle the requests and responses. We will also define any necessary path parameters or query parameters for these routes to ensure that we can properly handle the requests from the client.  


from fastapi import APIRouter , Depends , status # yaha ye api router ka kaam same to same @RestController IN JAVA  jaisa hi hai, ye hume apne routes ko organize karne me help karega aur hume apne routes ke liye ek common prefix dene ki suvidha bhi dega. Isse hum apne routes ko easily manage kar sakte hain aur unhe logically group kar sakte hain.

from src.tasks import controller

from src.tasks.dtos import TaskDTO , Task_OutputDTO # yaha ham TaskDTO paas kr rhe hai kyunki yahi data hamare body me ham paas krenge 

from src.utils.db import get_db # yaha ham get_db function ko import kr rhe hai, jisse ham apne database session ko create kr sake aur usse apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain.

from sqlalchemy.orm import Session # yaha ham SQLAlchemy ke Session class ko import kr rhe hai, jisse ham apne database session ko type hint kr sake aur apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain.

task_routes = APIRouter(prefix="/tasks")

#**(db:Session)** ka mtlb hai ki ham apne db parameter ko Session type ka define kr rhe hai, jisse ham apne database session ko type hint kr sake aur apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain. Aur get_db function ko Depends ke through pass kr rhe hai, jisse ham apne database session ko create kr sake aur usse apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain like quering the database, creating new records, updating existing records, and deleting records. Overall, ye db:Session = Depends(get_db) hamare application me database interactions ko manage karne ke liye ek important part hai, jisse ham apne controller functions me database session ka use karke necessary operations perform kar sakte hain aur apne application ke data ko effectively manage kar sakte hain.


@task_routes.post("/create" , response_model=Task_OutputDTO , status_code=status.HTTP_201_CREATED) # post api method /tasks/create endpoint rhega..

def create_task(body:TaskDTO,db:Session = Depends(get_db)): # yaha ham apne create_task function me body parameter ko TaskDTO type ka define kr rhe hai, jisse ham apne client se aane wale data ko validate kr sake aur ensure kr sake ki wo expected structure ke according hai. Isse ham apne application me data validation ko ensure kr sakte hain aur client se aane wale data ko expected structure ke according validate kar sakte hain. Aur db parameter me ham get_db function ko Depends ke through pass kr rhe hai, jisse ham apne database session ko create kr sake aur usse apne controller functions me use kr sake. Isse ham apne application me database interactions ko easily manage kar sakte hain aur apne controller functions me database session ka use karke necessary operations perform kar sakte hain.
    return controller.create_task(body , db) # yaha ham apne controller ke create_task function ko call kr rhe hai, jisme ham body aur db parameters ko pass kr rhe hai.


@task_routes.get("/get_all_Tasks",response_model=list[Task_OutputDTO],  status_code=status.HTTP_200_OK) # get api method /tasks/get endpoint rhega..
def get_all_tasks(db:Session = Depends(get_db)):
    return controller.get_tasks(db)


@task_routes.get("/get_task/{id}", response_model=Task_OutputDTO , status_code=status.HTTP_200_OK) # get api method /tasks/get/{id} endpoint rhega..
def get_task(id:int,db:Session = Depends(get_db)):
    return controller.get_one_task(id,db)


@task_routes.put("/update_task/{id}", response_model=Task_OutputDTO , status_code=status.HTTP_201_CREATED) # put api method /tasks/update/{id} endpoint rhega..
def update_task(id:int, body:TaskDTO, db:Session = Depends(get_db)):
    return controller.update_task(id, body, db)


@task_routes.delete("/delete_task/{id}" , status_code=status.HTTP_204_NO_CONTENT) # delete api method /tasks/delete/{id} endpoint rhega..
def delete_task(id:int, db:Session = Depends(get_db)):
    return controller.delete_task(id, db)



# hr router me hamne body me type TaskDTO diya hai jo ki hamare ko input lene ka kaam krta hai jo ki hamne DTOs file me define kiya hai, aur response_model me Task_OutputDTO diya hai jo ki hamare output ko define krta hai jo ki hamne DTOs file me define kiya hai. Isse ham apne application me data validation aur structuring ko ensure kar sakte hain, jisse client se aane wale data ko expected structure ke according validate kar sakte hain aur hamare API responses ko consistent aur informative bana sakte hain. Overall, ye DTOs hamare application ke liye ek important role play karenge in terms of data validation and structuring for task-related operations.
