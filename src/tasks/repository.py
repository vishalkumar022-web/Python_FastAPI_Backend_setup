from sqlalchemy.orm import Session
from src.tasks.model import TaskModel
from src.tasks.dtos import TaskDTO



# 1. Create Task me 'current_user_id' parameter add kiya
def create_task_in_db(body: TaskDTO, db: Session, current_user_id: int):
    data = body.model_dump() 
    
    new_task = TaskModel(
        title=data["title"], 
        description=data["description"], 
        status=data["status"],
        user_id=current_user_id # Yahan humne task ko uske maalik (user) se link kar diya!
    ) 
    
    db.add(new_task) 
    db.commit() 
    db.refresh(new_task) 
    return new_task 



def get_all_tasks_from_db(db: Session):
    return db.query(TaskModel).all()



def get_task_by_id_from_db(id: int, db: Session):
    return db.query(TaskModel).filter(TaskModel.id == id).first()



def update_task_in_db(existing_task: TaskModel, body: TaskDTO, db: Session):
    update_data = body.model_dump()
    for key, value in update_data.items():
        setattr(existing_task, key, value) 
        
    db.add(existing_task) 
    db.commit()
    db.refresh(existing_task)
    return existing_task



def delete_task_in_db(task_to_delete: TaskModel, db: Session):
    db.delete(task_to_delete)
    db.commit()
    return True