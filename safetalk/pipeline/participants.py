from typing import Optional
from uuid import uuid4

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from safetalk.domain.chat import Message
from safetalk.domain.memory import ShortTermMemory


class Participant(BaseModel):
    """
    A participant is someone who provides input into the session
    """

    id: str = Field(default=str(uuid4()))


class Therapist(Participant):

    @staticmethod
    def says(content: Optional[str]) -> Message:
        return Message(
            role="therapist", content=content if content else input("therapist: ")
        )


class Patient(Participant):
    personality: ChatPromptTemplate
    name: str
    llm: ChatOllama
    memory: ShortTermMemory = Field(default_factory=ShortTermMemory)

    def responds(self, to_this: Message) -> Message:
        """
        Generates a Message for a response to an input from the therapist (usually)

        Args:
            - to_this: Message -> A Message from the therapist

        Returns:
             - The response from the patient
        """
        pipeline: RunnableSequence = self.personality | self.llm
        msg: AIMessage = pipeline.invoke(
            {"input": to_this.content, "history": self.memory.content}
        )
        response: Message = Message(
            role=self.name,
            content=msg.content,
        )
        self.memory.update([to_this, response])
        return response


class Supervisor(Participant):
    criteria: PromptTemplate
    llm: ChatOllama = Field(default=ChatOllama(model="llama3.2"))

    def evaluate(self, transcript: list[dict[str, str]]) -> str:
        """
        Evaluates the therapy session and gives advice on how to be better.

        Args:
            - transcript: a list of therapist -> patient responses

        Returns:
            - the evaluation response
        """
        return (self.criteria | self.llm).invoke({"session": transcript}).content
