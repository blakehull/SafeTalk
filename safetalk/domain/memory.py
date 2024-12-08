from pydantic import BaseModel, Field

from safetalk.domain.chat import Message


class ShortTermMemory(BaseModel):
    content: list[dict[str, str]] = Field(default_factory=list)

    def update(self, messages: list[Message]) -> None:
        """
        Bootleg short term memory ;)

        Args:
            - messages: Messages to use

        Returns:
            - None
        """
        for message in messages:
            self.content.append(message)
        self.content = self.content[-4:]
