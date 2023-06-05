import azure.cognitiveservices.speech as speechsdk


class AzureSpeechService(object):
    """Azure Speech Service"""

    def __init__(self, config, logger) -> None:
        """
        Initialize Azure Speech Service
        param: config: configuration object
        Return: None
        """
        self.logger = logger
        # Azure Speech Service configuration
        self.speech_config = speechsdk.SpeechConfig(subscription=config.speech_service_key, region=config.speech_service_region)
        # The language of the voice that speaks for TTS
        self.speech_config.speech_synthesis_voice_name=config.speech_synthesis_voice_name
        self.speech_config.speech_recognition_language=config.speech_recognition_language
        # Audio configuration for TTS
        self.audio_config_tts = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        # Audio configuration for STT
        self.audio_config_stt = speechsdk.AudioConfig(use_default_microphone=True)
        # create speech synthesizer for TTS
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config_tts)
        # create speech recognizer for SST
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config_stt)

    
    def recognize_speech_from_mic(self) -> str:
        """
        Recognize speech from microphone
        param: None
        Return: text: str
        """
        self.logger.info("Speak into your microphone.")
        # start speech recognition
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
        # check result 
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            result = speech_recognition_result.text
            self.logger.info(f"Recognized:{result}")
            return result
        # no speech recognized
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            self.logger.error(f"No speech could be recognized: {speech_recognition_result.no_match_details}")
            return 'No speech could be recognized'
        # canceled
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            # check if cancellation is due to an error
            cancellation_details = speech_recognition_result.cancellation_details
            self.logger.error(f"Speech Recognition canceled: {cancellation_details.reason}")
            # check if reason is error
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                self.logger.error(f"Error details: {cancellation_details.error_details}")
            return 'Speech Recognition canceled'
    

    def text_to_speech(self, text: str) -> None:
        """
        Text to speech
        param: text: str
        Return: result: str
        """
        # Synthesizing audio for text
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()
        # Check result
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            self.logger.info(f"Speech synthesized to speaker for text [{text}]")
        # Error
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            self.logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
            # check if reason is error
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    self.logger.error(f"Error details: {cancellation_details.error_details}")
        
        return None
                    

