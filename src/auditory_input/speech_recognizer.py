from google.cloud import speech

class SpeechRecognizer:
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe_audio(self, audio_file_path, language_code="en-US"):
        with open(audio_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
        )

        response = self.client.recognize(config=config, audio=audio)

        transcriptions = []
        for result in response.results:
            transcriptions.append(result.alternatives[0].transcript)

        return transcriptions

    def streaming_transcribe(self, stream_file):
        client = speech.SpeechClient()

        with open(stream_file, "rb") as audio_file:
            content = audio_file.read()

        # In practice, stream should be a generator yielding chunks of audio data
        stream = [content]
        requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                    for chunk in stream)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )

        streaming_config = speech.StreamingRecognitionConfig(config=config)

        responses = client.streaming_recognize(
            config=streaming_config,
            requests=requests,
        )

        for response in responses:
            for result in response.results:
                yield result.alternatives[0].transcript
