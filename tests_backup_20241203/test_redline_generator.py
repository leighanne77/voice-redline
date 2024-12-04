import unittest
from src.redline_generator import generate_redline, RedlineGenerationError

class TestRedlineGenerator(unittest.TestCase):
    def test_generate_redline_success(self):
        ai_response = "This is a normal sentence. This sentence contains discrimination. Another normal sentence."
        expected_output = "Redline Analysis:\n\nThis is a normal sentence. REDLINE: This sentence contains discrimination. Another normal sentence.\n\nNote: Sentences preceded by 'REDLINE:' indicate potential discriminatory language or practices that should be reviewed and addressed."
        
        result = generate_redline(ai_response)
        self.assertEqual(result, expected_output)

    def test_generate_redline_no_issues(self):
        ai_response = "This is a normal sentence. Another normal sentence."
        expected_output = "Redline Analysis:\n\nThis is a normal sentence. Another normal sentence.\n\nNote: Sentences preceded by 'REDLINE:' indicate potential discriminatory language or practices that should be reviewed and addressed."
        
        result = generate_redline(ai_response)
        self.assertEqual(result, expected_output)

    def test_generate_redline_error(self):
        with self.assertRaises(RedlineGenerationError):
            generate_redline(None)  # Passing None should raise an error

if __name__ == '__main__':
    unittest.main()