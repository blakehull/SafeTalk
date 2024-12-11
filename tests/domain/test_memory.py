import unittest

from safetalk.domain.chat import Message
from safetalk.domain.memory import ShortTermMemory


class TestMemory(unittest.TestCase):

    def test_short_term_memory_update(self):
        stm = ShortTermMemory()
        content = [Message(role="test_user", content="Hello, World!")]
        self.assertEqual(stm.content, [])
        stm.update(content)
        self.assertEqual(stm.content, [c.model_dump() for c in content])

    def test_short_term_memory_recall(self):
        content = [Message(role="test_user", content=f"message {n}") for n in range(50)]
        expected_content = [c.model_dump() for c in content[-4:]]
        stm = ShortTermMemory()
        stm.update(content)
        self.assertListEqual(stm.content, expected_content)
