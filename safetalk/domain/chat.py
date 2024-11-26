import json
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class Message(BaseModel):
    id: int
    role: str
    message: str
    num_responses: int = 0
    responses: Optional[list['Message']] = Field(default_factory=list)

    def model_dump_json(self, **kwargs):
        kwargs.setdefault('exclude_defaults', True)
        return super().model_dump_json(**kwargs)

    def append_response(self, parent_id: int, new_message: 'Message') -> bool:
        if self.id == parent_id:
            self.responses.append(new_message)
            self.num_responses += 1
            return True
        for child in self.responses:
            if child.append_response(parent_id, new_message):
                self.num_responses += 1
                return True
        return False
    
    def get_index(self, id):
        if id < 0:
            return {}
        for response in self.responses:
            if response.id == id:
                return json.loads(response.model_dump_json())
            else:
                response.get_index(id)
        return {}

    class Config:
        from_attributes = True