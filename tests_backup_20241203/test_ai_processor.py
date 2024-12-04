import unittest
from unittest.mock import patch, MagicMock
from src.ai_processor import process_ai, AIProcessingError

class TestAIProcessor(unittest.TestCase):
    @patch('src.ai_processor.requests.post')
    def test_process_ai_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Test AI response'}}]
        }
        mock_post.return_value = mock_response

        result = process_ai("Test input")
        self.assertEqual(result, "Test AI response")

    @patch('src.ai_processor.requests.post')
    def test_process_ai_request_exception(self, mock_post):
        mock_post.side_effect = Exception("Test error")

        with self.assertRaises(AIProcessingError):
            process_ai("Test input")

    @patch('src.ai_processor.requests.post')
    def test_process_ai_unexpected_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # Empty response
        mock_post.return_value = mock_response

        with self.assertRaises(AIProcessingError):
            process_ai("Test input")

if __name__ == '__main__':
    unittest.main()