from pydantic import BaseModel

class UserInput(BaseModel):
    '''Base model'''

    task_id: int
    description: str
    done: bool = False