import unittest
from unittest.mock import patch, MagicMock
from src.agent_framework.base_agent import BaseAgent, TaskAgent, create_agent

class TestAgentFramework(unittest.TestCase):
    @patch('spade.agent.Agent.start')
    def test_create_base_agent(self, mock_start):
        mock_start.return_value = MagicMock()
        agent = create_agent("test", "password")
        self.assertIsInstance(agent, BaseAgent)
        mock_start.assert_called_once()

    @patch('spade.agent.Agent.start')
    def test_create_task_agent(self, mock_start):
        mock_start.return_value = MagicMock()
        agent = create_agent("test", "password", TaskAgent)
        self.assertIsInstance(agent, TaskAgent)
        mock_start.assert_called_once()

    @patch.object(BaseAgent, 'add_behaviour')
    @patch.object(BaseAgent, 'setup')
    def test_base_agent_setup(self, mock_setup, mock_add_behaviour):
        agent = BaseAgent("test@localhost", "password")
        agent.setup()
        mock_setup.assert_called_once()
        mock_add_behaviour.assert_called_once()

    @patch.object(TaskAgent, 'add_behaviour')
    @patch.object(TaskAgent, 'setup')
    def test_task_agent_setup(self, mock_setup, mock_add_behaviour):
        agent = TaskAgent("test@localhost", "password")
        agent.setup()
        mock_setup.assert_called_once()
        self.assertEqual(mock_add_behaviour.call_count, 2)  # Once for BaseAgent, once for TaskAgent

if __name__ == '__main__':
    unittest.main()
