"""
Validation: Kiểm tra schema input/output
"""
from pydantic import BaseModel

class ActionInput(BaseModel):
    method: str
    path_params: dict = {}
    query_params: dict = {}
    body_params: dict = {}

def validate_action_input(data: dict):
    return ActionInput(**data)
