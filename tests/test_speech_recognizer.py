import unittest
from unittest.mock import patch, MagicMock
from src.auditory_input.speech_recognizer import SpeechRecognizer

class TestSpeechRecognizer(unittest.TestCase):
    def setUp(self):
        self.recognizer = SpeechRecognizer()

    @patch('google.cloud.speech.SpeechClient')
    def test_transcribe_audio(self, mock_client):
        mock_response = MagicMock()
        mock_result = MagicMock()
        mock_alternative = MagicMock()
        mock_alternative.transcript = "Hello, world!"
        mock_result.alternatives = [mock_alternative]
        mock_response.results = [mock_result]
        mock_client.return_value.recognize.return_value = mock_response

        result = self.recognizer.transcribe_audio('fake_audio.wav')
        self.assertEqual(result, ["Hello, world!"])

    @patch('google.cloud.speech.SpeechClient')
    def test_streaming_transcribe(self, mock_client):
        mock_response = MagicMock()
        mock_result = MagicMock()
        mock_alternative = MagicMock()
        mock_alternative.transcript = "Streaming audio"
        mock_result.alternatives = [mock_alternative]
        mock_response.results = [mock_result]
        mock_client.return_value.streaming_recognize.return_value = [mock_response]

        result = list(self.recognizer.streaming_transcribe('fake_stream.wav'))
        self.assertEqual(result, ["Streaming audio"])

if __name__ == '__main__':
    unittest.main()
