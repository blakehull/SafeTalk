from pydantic import BaseModel


class Message(BaseModel):
    """
    This is the basic message model
    """

    role: str
    content: str
