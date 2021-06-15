import unittest

from message_builder import MessageBuilder
from project_manager import ProjectManager


class TestBatteryPm(unittest.TestCase):
    def test_prepare(self):
        for message in MessageBuilder().build_message():
            ProjectManager().send_message(message)

    def test_test(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
