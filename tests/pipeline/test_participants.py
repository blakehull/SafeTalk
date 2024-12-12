import unittest

from langchain_core.messages import AIMessage

from safetalk.domain.chat import Message
from safetalk.pipeline.llm import LLM
from safetalk.pipeline.participants import Participant, Patient, Therapist


class MockLLM(LLM):

    def __init__(self):
        super().__init__(None)
        self.response = "test response"

    def invoke(self, *args, **kwargs):
        return AIMessage(content=self.response)


class TestParticipant(unittest.TestCase):

    def test_id(self):
        user_id = "usr123"
        participant = Participant(id=user_id)
        self.assertEqual(participant.id, user_id)


class TestTherapist(unittest.TestCase):

    def test_says(self):
        text = "some text"
        expected_message = Message(role="therapist", content=text)
        therapist = Therapist()
        actual_message = therapist.says(text)
        self.assertEqual(expected_message, actual_message)


class TestPatient(unittest.TestCase):

    def test_patient_responds(self):
        mock_llm = MockLLM()
        patient_name = "test_patient"
        p = Patient(personality=mock_llm, name=patient_name)
        returned_value = p.responds(
            to_this=Message(role="therapist", content="hi there")
        )
        self.assertEqual(returned_value.role, patient_name)
        self.assertEqual(returned_value.content, mock_llm.response)
