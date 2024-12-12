from typing import Optional
from uuid import uuid4

from langchain_core.messages import AIMessage
from pydantic import BaseModel, ConfigDict, Field

from safetalk.domain.chat import Message
from safetalk.domain.memory import ShortTermMemory
from safetalk.pipeline.llm import LLM


class Participant(BaseModel):
    """
    A participant is someone who provides input into the session
    """

    id: str = Field(default=str(uuid4()))

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Therapist(Participant):

    @staticmethod
    def says(content: Optional[str]) -> Message:
        return Message(
            role="therapist", content=content if content else input("therapist: ")
        )


class Patient(Participant):
    personality: LLM
    name: str
    memory: ShortTermMemory = Field(default_factory=ShortTermMemory)

    def responds(self, to_this: Message) -> Message:
        """
        Generates a Message for a response to an input from the therapist (usually)

        Args:
            - to_this: Message -> A Message from the therapist

        Returns:
             - The response from the patient
        """
        msg: AIMessage = self.personality.invoke(
            {"input": to_this.content, "history": self.memory.content}
        )
        response: Message = Message(
            role=self.name,
            content=msg.content,
        )
        self.memory.update([to_this, response])
        return response


class Supervisor(Participant):
    evaluator: LLM

    def evaluate(self, transcript: list[dict[str, str]]) -> str:
        """
        Evaluates the therapy session and gives advice on how to be better.

        Args:
            - transcript: a list of therapist -> patient responses

        Returns:
            - the evaluation response
        """
        return self.evaluator.invoke({"session": transcript}).content
