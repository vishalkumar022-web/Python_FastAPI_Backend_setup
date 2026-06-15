from fastapi import APIRouter, Depends, status 
from sqlalchemy.orm import Session 
from src.tasks import controller
from src.tasks.dtos import TaskDTO, Task_OutputDTO 
from src.utils.db import get_db 
from src.utils.helper import is_authenticated # Filter import kiya
from src.user.model import UserModel




task_routes = APIRouter(prefix="/tasks")



# POST CREATE TASK (Protected Route)
@task_routes.post("/create", response_model=Task_OutputDTO, status_code=status.HTTP_201_CREATED) 
def create_task(body: TaskDTO, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)): 
    # Depends(is_authenticated) filter ka kaam karega, token check karega aur sahi user return karega
    return controller.create_task(body, db, user) 




# GET ALL TASKS
@task_routes.get("/get_all_Tasks", response_model=list[Task_OutputDTO], status_code=status.HTTP_200_OK) 
def get_all_tasks(db: Session = Depends(get_db)):
    return controller.get_tasks(db)




# GET ONE TASK
@task_routes.get("/get_task/{id}", response_model=Task_OutputDTO, status_code=status.HTTP_200_OK) 
def get_task(id: int, db: Session = Depends(get_db)):
    return controller.get_one_task(id, db)




# PUT UPDATE TASK (Protected Route)
@task_routes.put("/update_task/{id}", response_model=Task_OutputDTO, status_code=status.HTTP_201_CREATED) 
def update_task(id: int, body: TaskDTO, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    # Yahan check hoga user authorization
    return controller.update_task(id, body, db, user)



# DELETE TASK (Protected Route)
@task_routes.delete("/delete_task/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_task(id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    # Yahan check hoga user authorization
    return controller.delete_task(id, db, user)