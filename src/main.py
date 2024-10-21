import asyncio
from src.screen_analysis.vision_analyzer import VisionAnalyzer
from src.auditory_input.speech_recognizer import SpeechRecognizer
from src.agent_framework.base_agent import create_agent, TaskAgent
from src.communication.websocket_server import app, manager

class TARASSystem:
    def __init__(self):
        self.vision_analyzer = VisionAnalyzer()
        self.speech_recognizer = SpeechRecognizer()
        self.agents = []

    async def setup(self):
        # Create agents
        self.agents.append(create_agent("vision_agent", "password", TaskAgent))
        self.agents.append(create_agent("speech_agent", "password", TaskAgent))

    async def process_image(self, image_path):
        labels = self.vision_analyzer.analyze_image(image_path)
        text = self.vision_analyzer.detect_text(image_path)
        faces = self.vision_analyzer.detect_faces(image_path)
        return f"Labels: {labels}, Text: {text}, Faces: {faces}"

    async def process_audio(self, audio_path):
        transcription = self.speech_recognizer.transcribe_audio(audio_path)
        return f"Transcription: {transcription}"

    async def run(self):
        await self.setup()
        
        # Simulate processing an image
        image_result = await self.process_image("sample_image.jpg")
        await manager.broadcast(f"Image processing result: {image_result}")

        # Simulate processing audio
        audio_result = await self.process_audio("sample_audio.wav")
        await manager.broadcast(f"Audio processing result: {audio_result}")

        # Keep the system running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    taras = TARASSystem()
    
    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(taras.run())

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
