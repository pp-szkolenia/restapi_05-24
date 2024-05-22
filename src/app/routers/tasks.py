from fastapi import status, APIRouter, HTTPException, Response, Depends

from app.models import (TaskBody, TaskResponse, GetAllTasksResponse, GetSingleTaskResponse,
                        PostTaskResponse, PutTaskResponse, SortOrders, PostTaskNoDetailsResponse)
from sqlalchemy.orm import Session
from sqlalchemy import between, asc, desc
from db.orm import get_session
from db.models import TasksTable


router = APIRouter()


@router.get("/tasks", tags=["tasks"], response_model=GetAllTasksResponse)
def get_tasks(session: Session = Depends(get_session), is_complete: bool | None = None,
              min_priority: int = 1, max_priority: int = 5, sort_description: SortOrders = None):
    tasks_query = session.query(TasksTable)

    if is_complete is not None:
        tasks_query = tasks_query.filter_by(is_complete=is_complete)

    tasks_query = tasks_query.filter(between(TasksTable.priority, min_priority, max_priority))

    if sort_description is not None:
        if sort_description == SortOrders.ASC:
            sort_func = asc
        elif sort_description == SortOrders.DESC:
            sort_func = desc

        tasks_query = tasks_query.order_by(sort_func(TasksTable.description))

    tasks_data = tasks_query.all()

    tasks_data = [
            TaskResponse(id_=task.id_number, description=task.description,
                         priority=task.priority, is_complete=task.is_complete)
            for task in tasks_data]

    return {"result": tasks_data}


@router.get("/tasks/{id_}", tags=["tasks"], response_model=GetSingleTaskResponse)
def get_task_by_id(id_: int, session: Session = Depends(get_session)):
    target_task = session.query(TasksTable).filter_by(id_number=id_).first()

    if target_task is None:
        message = {"error": f"Task with id {id_} does not exist!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    target_task = TaskResponse(id_=target_task.id_number, description=target_task.description,
                               priority=target_task.priority, is_complete=target_task.is_complete)

    return {"result": target_task}


@router.post("/tasks", status_code=status.HTTP_201_CREATED, tags=["tasks"],
             response_model=PostTaskResponse | PostTaskNoDetailsResponse)
def create_task(body: TaskBody, session: Session = Depends(get_session), show_task: bool = True):
    task_dict = body.model_dump()
    new_task = TasksTable(**task_dict)

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    new_task = TaskResponse(id_=new_task.id_number, description=new_task.description,
                            priority=new_task.priority, is_complete=new_task.is_complete)

    if show_task:
        return {"message": "New task added", "details": new_task}
    else:
        return {"message": "new task added"}


@router.delete("/tasks/{id_}", tags=["tasks"])
def delete_task_by_id(id_: int, session: Session = Depends(get_session)):
    deleted_task = session.query(TasksTable).filter_by(id_number=id_).first()

    if not deleted_task:
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    session.delete(deleted_task)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/tasks/{id_}", tags=["tasks"], response_model=PutTaskResponse)
def update_task_by_id(id_: int, body: TaskBody, session: Session = Depends(get_session)):
    filter_query = session.query(TasksTable).filter_by(id_number=id_)

    if not filter_query.first():
        message = {"error": f"Task with id {id_} does not exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    filter_query.update(body.model_dump())
    session.commit()

    updated_task = filter_query.first()

    updated_task = TaskResponse(id_=updated_task.id_number, description=updated_task.description,
                                priority=updated_task.priority, is_complete=updated_task.is_complete)

    message = {"message": f"Task with id {id_} updated", "new_value": updated_task}
    return message
