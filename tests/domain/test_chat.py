import unittest

from safetalk.domain.chat import Message


class TestChat(unittest.TestCase):

    def test_message_init(self):
        content = "Hello, World!"
        role = "test_user"
        message = Message(role=role, content=content)
        self.assertEqual(content, message.content)
        self.assertEqual(role, message.role)
