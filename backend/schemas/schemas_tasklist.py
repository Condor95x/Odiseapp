from pydantic import BaseModel

class TaskListResponse(BaseModel):
    task_list_id: int
    task_type: str
    task_supclass: str | None = None
    task_class: str | None = None
    task_name: str

    class Config:
        from_attributes = True