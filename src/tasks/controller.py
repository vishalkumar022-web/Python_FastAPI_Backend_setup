# In this Controller file, we will define the functions that will handle the requests from the client and interact with the database to perform the necessary operations. These functions will be called by the routes defined in the routes.py file. We will also handle any errors that may occur during the execution of these functions and return appropriate responses to the client. The functions in this file will be responsible for creating, reading, updating, and deleting task data in the database, as well as any other necessary operations related to tasks. We will use the repository functions defined in the repository.py file to interact with the database and perform the necessary operations on the task data. Additionally, we will use the DTOs defined in the dtos.py file to validate the data received from the client and to structure the data that will be sent back to the client. Overall, this Controller file will serve as the main point of interaction between the client and the database for all task-related operations in our application.  
from src.tasks.dtos import TaskDTO

from sqlalchemy.orm import Session

from src.tasks.model import TaskModel

def create_task(body: TaskDTO, db: Session):

    data = body.model_dump() # ye model_dump() method Pydantic model ke data ko dictionary me convert kar deta hai, jisse hum apne repository functions me use kar sakte hain.

    new_task = TaskModel(
        title=data["title"], description=data["description"], status=data["status"]
                         ) # yaha ham TaskModel ke object ko create kar rahe hain, jisme ham apne TaskDTO se data ko pass kar rahe hain. Isse ham apne database me ek naya task record create kar sakte hain.

    db.add(new_task) # yaha ham apne database session me new_task object ko add kar rahe hain, jisse ham apne database me is task record ko save kar sakte hain.
    db.commit() # yaha ham apne database session me changes ko commit kar rahe hain, jisse hamare database me new_task record save ho jayega.
    db.refresh(new_task) # yaha ham apne database session me new_task object ko refresh kar rahe hain, jisse hamare new_task object me database se updated data aa jayega, jaise ki id field jo database me auto-generated hota hai.


    return {"Status": "Success", "message": "Task created successfully", "data": new_task} # yaha ham apne controller function se ek response return kar rahe hain, jisme ham status, message aur data fields ko specify kar rahe hain. Is response me ham new_task object ko data field me include kar rahe hain, jisse client ko pata chalega ki task successfully create ho gaya hai aur uska data kya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.
            



def get_tasks(db: Session):
    
    tasks = db.query(TaskModel).all() # yaha ham apne database session me TaskModel ke saare records ko query kar rahe hain aur unhe tasks variable me store kar rahe hain. Isse ham apne database me saare task records ko retrieve kar sakte hain.

    return {"Status": "Success", "message": "Tasks retrieved successfully", "data": tasks} # yaha ham apne controller function se ek response return kar rahe hain, jisme ham status, message aur data fields ko specify kar rahe hain. Is response me ham tasks variable ko data field me include kar rahe hain, jisse client ko pata chalega ki tasks successfully retrieve ho gaye hain aur unka data kya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.