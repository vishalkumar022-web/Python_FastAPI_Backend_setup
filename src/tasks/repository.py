# In this Repository file, we will define the functions that will interact with the database.
# Ye file hamari "Kitchen" hai. Iska kaam sirf aur sirf database me data dalna (INSERT), 
# nikalna (SELECT), update karna (UPDATE) aur delete karna (DELETE) hai.

from sqlalchemy.orm import Session
from src.tasks.model import TaskModel
from src.tasks.dtos import TaskDTO

def create_task_in_db(body: TaskDTO, db: Session):
    data = body.model_dump() # Pydantic model ko dictionary me convert kiya
    
    new_task = TaskModel(
        title=data["title"], 
        description=data["description"], 
        status=data["status"]
    ) # Model ka object banaya
    
    db.add(new_task) # Database me add kiya
    db.commit() # Changes save kiye
    db.refresh(new_task) # ID generate hone ke baad wapas naya data fetch kiya
    
    return new_task # Controller ko naya task wapas de diya


def get_all_tasks_from_db(db: Session):
    # Database se saare tasks uthaye aur return kar diye
    return db.query(TaskModel).all()


def get_task_by_id_from_db(id: int, db: Session):
    # Database me specific ID wala task dhundha
    # Agar milega toh task ka object return hoga, nahi milega toh 'None' return hoga
    return db.query(TaskModel).filter(TaskModel.id == id).first()


def update_task_in_db(existing_task: TaskModel, body: TaskDTO, db: Session):
    # Yaha dhyan do bhai: Ye function existing_task (jo controller ne dhundh ke diya hai) ko update karega
    update_data = body.model_dump()
    
    for key, value in update_data.items():
        setattr(existing_task, key, value) # setattr se dynamically fields update kiye
        
    db.add(existing_task) # (Fix: Yaha dictionary nahi, balki Model object add karte hain)
    db.commit()
    db.refresh(existing_task)
    
    return existing_task


def delete_task_in_db(task_to_delete: TaskModel, db: Session):
    # Jo task controller ne bheja, usko seedha delete kar diya
    db.delete(task_to_delete)
    db.commit()
    return True