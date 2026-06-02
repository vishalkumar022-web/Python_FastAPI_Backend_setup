# In this Controller file, we will define the functions that will handle the requests from the client and interact with the database to perform the necessary operations. These functions will be called by the routes defined in the routes.py file. We will also handle any errors that may occur during the execution of these functions and return appropriate responses to the client. The functions in this file will be responsible for creating, reading, updating, and deleting task data in the database, as well as any other necessary operations related to tasks. We will use the repository functions defined in the repository.py file to interact with the database and perform the necessary operations on the task data. Additionally, we will use the DTOs defined in the dtos.py file to validate the data received from the client and to structure the data that will be sent back to the client. Overall, this Controller file will serve as the main point of interaction between the client and the database for all task-related operations in our application.  
from src.tasks.dtos import TaskDTO

from sqlalchemy.orm import Session

from src.tasks.model import TaskModel

from fastapi.encoders import jsonable_encoder # yaha ham jsonable_encoder function ko import kar rahe hain, jisse ham apne Pydantic models ko JSON serializable format me convert kar sakte hain. Isse ham apne API responses me Pydantic models ko easily include kar sakte hain aur unhe JSON format me client ko send kar sakte hain. Is function ka use karke ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.

def create_task(body: TaskDTO, db: Session):

    data = body.model_dump() # ye model_dump() method Pydantic model ke data ko dictionary me convert kar deta hai, jisse hum apne repository functions me use kar sakte hain.

    new_task = TaskModel(
        title=data["title"], description=data["description"], status=data["status"]
                         ) # yaha ham TaskModel ke object ko create kar rahe hain, jisme ham apne TaskDTO se data ko pass kar rahe hain. Isse ham apne database me ek naya task record create kar sakte hain.

    db.add(new_task) # yaha ham apne database session me new_task object ko add kar rahe hain, jisse ham apne database me is task record ko save kar sakte hain.
    db.commit() # yaha ham apne database session me changes ko commit kar rahe hain, jisse hamare database me new_task record save ho jayega.
    db.refresh(new_task) # yaha ham apne database session me new_task object ko refresh kar rahe hain, jisse hamare new_task object me database se updated data aa jayega, jaise ki id field jo database me auto-generated hota hai.


    return new_task # yaha ham apne controller function se new_task object ko return kar rahe hain, jisse client ko pata chalega ki task successfully create ho gaya hai aur uska data kya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.
            



def get_tasks(db: Session):
    
    tasks = db.query(TaskModel).all() # yaha ham apne database session me TaskModel ke saare records ko query kar rahe hain aur unhe tasks variable me store kar rahe hain. Isse ham apne database me saare task records ko retrieve kar sakte hain.

    return tasks # yaha ham apne controller function se tasks variable ko return kar rahe hain, jisme ham apne database se saare task records ko include kar rahe hain. Isse client ko pata chalega ki saare tasks successfully retrieve ho gaye hain aur unka data kya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.


def get_one_task(id:int,db: Session):
    
    one_task = db.query(TaskModel).filter(TaskModel.id == id).first() # yaha ham apne database session me TaskModel ke record ko query kar rahe hain jiska id field client se aane wale id parameter ke barabar hai. Isse ham apne database me specific task record ko retrieve kar sakte hain.

    if not one_task: # yaha ham check kar rahe hain ki agar task variable me koi record nahi mila to ham ek error response return karenge, jisme ham status aur message fields ko specify karenge. Isse client ko pata chalega ki unka request unsuccessful tha kyunki specified id ke saath koi task record nahi mila.
        return {"Status": "Error", "message": "Task not found"}

    return one_task # yaha ham apne controller function se one_task variable ko return kar rahe hain, jisme ham apne database se specific task record ko include kar rahe hain. Isse client ko pata chalega ki task successfully retrieve ho gaya hai aur uska data kya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.



def update_task(id:int, body:TaskDTO, db: Session):

    update_task_ID= db.query(TaskModel).filter(TaskModel.id == id).first() # yaha ham apne database session me TaskModel ke record ko query kar rahe hain jiska id field client se aane wale id parameter ke barabar hai. Isse ham apne database me specific task record ko retrieve kar sakte hain.

    if not update_task_ID: # yaha ham check kar rahe hain ki agar update_task variable me koi record nahi mila to ham ek error response return karenge, jisme ham status aur message fields ko specify karenge. Isse client ko pata chalega ki unka request unsuccessful tha kyunki specified id ke saath koi task record nahi mila.
        return {"Status": "Error", "message": "updated task id is not found"}
    



    # update_task_ID.title = body.title                     # yaha ham update_task variable ke title field ko client se aane wale body parameter ke title field ke barabar set kar rahe hain, jisse ham apne database me specific task record ke title field ko update kar sakte hain.
    # update_task_ID.description = body.description         # yaha ham update_task variable ke description field ko client se aane wale body parameter ke description field ke barabar set kar rahe hain, jisse ham apne database me specific task record ke description field ko update kar sakte hain.
    # update_task_ID.status = body.status                   # yaha ham update_task variable ke status field ko client se aane wale body parameter ke status field ke barabar set kar rahe hain, jisse ham apne database me specific task record ke status field ko update kar sakte hain.


    update_task_data = body.model_dump() # ye model_dump() method Pydantic model ke data ko dictionary me convert kar deta hai, jisse hum apne repository functions me use kar sakte hain.
    for key, value in update_task_data.items(): # yaha ham update_task_data dictionary ke key-value pairs par iterate kar rahe hain, jisse ham apne update_task variable ke corresponding fields ko dynamically update kar sakte hain.
        setattr(update_task_ID, key, value) 
       # es setattr() function ka use karke ham update_task_ID variable ke key field ko value se set kar rahe hain, es se fayda ye hai ki ham apne maan se chahe toh kisi feild ko update kar sakte hain ya nahi bhi kar sakte hain, kyunki ham apne update_task_data dictionary me se jis key ko bhi update karna chahte hain usko ham simply include kar denge aur jis key ko update nahi karna chahte hain usko ham apne update_task_data dictionary me se exclude kar denge. Isse ham apne update_task function ko flexible bana sakte hain aur client ko bhi ye suvidha de sakte hain ki wo apne request body me se sirf un fields ko include kare jo wo update karna chahte hain.



    db.add(update_task_data) # yaha ham apne database session me update_task variable ko add kar rahe hain, jisse ham apne database me is task record ko update kar sakte hain.   
    db.commit() # yaha ham apne database session me changes ko commit kar rahe hain, jisse hamare database me update_task record update ho jayega.
    db.refresh(update_task_data) # yaha ham apne database session me update_task variable ko refresh kar rahe hain, jisse hamare update_task variable me database se updated data aa jayega, jaise ki updated title, description aur status fields.

    return update_task_data # yaha ham apne controller function se update_task variable ko return kar rahe hain, jisme ham apne database se updated task record ko include kar rahe hain. Isse client ko pata chalega ki task successfully update ho gaya hai aur uska updated data kya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.



def delete_task(id:int, db: Session):

    delete_task_ID = db.query(TaskModel).filter(TaskModel.id == id).first() # yaha ham apne database session me TaskModel ke record ko query kar rahe hain jiska id field client se aane wale id parameter ke barabar hai. Isse ham apne database me specific task record ko retrieve kar sakte hain.

    if not delete_task_ID: # yaha ham check kar rahe hain ki agar delete_task variable me koi record nahi mila to ham ek error response return karenge, jisme ham status aur message fields ko specify karenge. Isse client ko pata chalega ki unka request unsuccessful tha kyunki specified id ke saath koi task record nahi mila.
        return {"Status": "Error", "message": "deleted task id is not found"}

    db.delete(delete_task_ID) # yaha ham apne database session me delete_task variable ko delete kar rahe hain, jisse ham apne database me is task record ko delete kar sakte hain.
    db.commit() # yaha ham apne database session me changes ko commit kar rahe hain, jisse hamare database me delete_task record delete ho jayega.

    return None # yaha ham apne controller function se None return kar rahe hain, jisse client ko pata chalega ki task successfully delete ho gaya hai. Is response format se ham apne API responses ko consistent aur informative bana sakte hain, jisse client ko easily samajh me aa sake ki unka request successful tha ya nahi aur agar successful tha to uska result kya hai.



