import unittest
from unittest.mock import patch

from langchain_core.prompts import ChatPromptTemplate

from safetalk.domain.chat import Message
from safetalk.pipeline.participants import Participant, Patient, Therapist


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

    @patch("safetalk.pipeline.participants.ChatOllama")
    def test_patient(self, mock_llm):
        personality = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "we are testing",
                ),
                ("human", "{input}"),
            ]
        )
        mock_llm.invoke.return_value = "hi"
        p = Patient(personality=personality, name="test patient", llm=mock_llm)
        returned_value = p.responds(
            to_this=Message(role="therapist", content="hi there")
        )

        print(returned_value)
