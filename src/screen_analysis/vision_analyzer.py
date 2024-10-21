import os
from google.cloud import vision

class VisionAnalyzer:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def analyze_image(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations

        return [label.description for label in labels]

    def detect_text(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        return [text.description for text in texts]

    def detect_faces(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.face_detection(image=image)
        faces = response.face_annotations

        return len(faces)
