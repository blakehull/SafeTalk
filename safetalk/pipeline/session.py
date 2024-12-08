from abc import ABC, abstractmethod

from pydantic import BaseModel

from safetalk.domain.chat import Message
from safetalk.pipeline.participants import Patient, Supervisor, Therapist


class Session(BaseModel, ABC):
    therapist: Therapist
    history: list[dict[str, str]]

    @abstractmethod
    def start(self) -> None:
        """
        The process that runs the session
        """
        ...


class SupervisorSession(Session):
    supervisor: Supervisor

    def start(self):
        print(self.supervisor.evaluate(self.history))


class TherapySession(Session):
    patient: Patient

    def start(self):
        """
        CLI interface currently
        TODO: Allow this to integrate into an app (like a react app, etc)
        """
        print("type 'exit' to stop the session")
        therapist_says: Message = self.therapist.says(content=None)
        while therapist_says.content != "exit":
            patient_says: Message = self.patient.responds(therapist_says)
            print(patient_says.content)
            self.history.append(therapist_says.model_dump())
            self.history.append(patient_says.model_dump())
            therapist_says: Message = self.therapist.says(content=None)
