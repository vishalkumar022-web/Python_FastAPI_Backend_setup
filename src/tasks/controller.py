from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.tasks import repository
from src.tasks.dtos import TaskDTO
from src.user.model import UserModel # UserModel import karna padega validation ke liye

# Yahan user pass ho raha hai
def create_task(body: TaskDTO, db: Session, user: UserModel):
    # Repository ko task data ke sath user ki ID bhi de rahe hain
    new_task = repository.create_task_in_db(body, db, user.id)
    return new_task

# Update me bhi user pass karwaya check karne ke liye
def update_task(id: int, body: TaskDTO, db: Session, user: UserModel):
    task_to_update = repository.get_task_by_id_from_db(id, db)

    if not task_to_update:
        raise HTTPException(status_code=404, detail="Given Task Id is not found")
    
    # ---------------------------------------------------------
    # SECURITY CHECK: Kya ye usi user ka task hai?
    # ---------------------------------------------------------
    if task_to_update.user_id != user.id:
        raise HTTPException(status_code=403, detail="Aap dusre ka task update nahi kar sakte bhai!")

    updated_task = repository.update_task_in_db(task_to_update, body, db)
    return updated_task


def delete_task(id: int, db: Session, user: UserModel):
    task_to_delete = repository.get_task_by_id_from_db(id, db)
    
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")

    # ---------------------------------------------------------
    # SECURITY CHECK: Kya ye usi user ka task hai?
    # ---------------------------------------------------------
    if task_to_delete.user_id != user.id:
        raise HTTPException(status_code=403, detail="Aap dusre ka task delete nahi kar sakte bhai!")

    return repository.delete_task_in_db(task_to_delete, db)

# Get functions me usually ownership nahi check karte (taaki sab dekh sakein), par tum chaho toh laga sakte ho.
def get_one_task(id: int, db: Session):
    one_task = repository.get_task_by_id_from_db(id, db)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return one_task

def get_tasks(db: Session):
    return repository.get_all_tasks_from_db(db)