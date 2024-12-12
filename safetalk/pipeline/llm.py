from abc import ABC

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama


class LLM(ABC):

    def __init__(self, client):
        """
        This is an abstract class for LLMs so that you can swap out LLMs as you develop.

        Args:
             client: an LLM client.
        """
        self.client = client

    def invoke(self, *args, **kwargs): ...


class Ollama(LLM):

    def __init__(self, client: ChatOllama | None, system_prompt: ChatPromptTemplate):
        super().__init__(ChatOllama(model="llama3.2") if not client else client)
        self.pipeline: RunnableSequence = system_prompt | self.client

    def invoke(self, content: dict):
        return self.pipeline.invoke(input=content)
