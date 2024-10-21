import unittest
from unittest.mock import patch, MagicMock
from src.screen_analysis.vision_analyzer import VisionAnalyzer

class TestVisionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = VisionAnalyzer()

    @patch('google.cloud.vision.ImageAnnotatorClient')
    def test_analyze_image(self, mock_client):
        mock_response = MagicMock()
        mock_response.label_annotations = [
            MagicMock(description='cat'),
            MagicMock(description='animal')
        ]
        mock_client.return_value.label_detection.return_value = mock_response

        result = self.analyzer.analyze_image('fake_path.jpg')
        self.assertEqual(result, ['cat', 'animal'])

    @patch('google.cloud.vision.ImageAnnotatorClient')
    def test_detect_text(self, mock_client):
        mock_response = MagicMock()
        mock_response.text_annotations = [
            MagicMock(description='Hello'),
            MagicMock(description='World')
        ]
        mock_client.return_value.text_detection.return_value = mock_response

        result = self.analyzer.detect_text('fake_path.jpg')
        self.assertEqual(result, ['Hello', 'World'])

    @patch('google.cloud.vision.ImageAnnotatorClient')
    def test_detect_faces(self, mock_client):
        mock_response = MagicMock()
        mock_response.face_annotations = [MagicMock(), MagicMock()]
        mock_client.return_value.face_detection.return_value = mock_response

        result = self.analyzer.detect_faces('fake_path.jpg')
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()
