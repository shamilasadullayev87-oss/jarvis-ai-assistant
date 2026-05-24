"""
Voice Engine - STT, TTS, Wake Word Detection
"""

import logging
import whisper
from pathlib import Path
import os
import time

logger = logging.getLogger(__name__)

class VoiceEngine:
    def __init__(self):
        """Initialize voice engine"""
        logger.info("Initializing voice engine...")
        
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.sr_available = True
        except Exception as e:
            logger.warning(f"SpeechRecognition not available: {e}")
            self.sr_available = False
        
        # Load Whisper model
        model_size = os.getenv("WHISPER_MODEL", "base")
        logger.info(f"Loading Whisper model: {model_size}")
        try:
            self.whisper_model = whisper.load_model(model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper: {e}")
            self.whisper_model = None
        
        # Initialize TTS
        self._init_tts()
        
        logger.info("Voice engine ready")
    
    def _init_tts(self):
        """Initialize text-to-speech"""
        tts_engine = os.getenv("TTS_ENGINE", "pyttsx3")
        
        try:
            if tts_engine == "coqui":
                try:
                    from TTS.api import TTS
                    logger.info("Loading Coqui TTS...")
                    self.tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", gpu=False, verbose=False)
                    self.tts_type = "coqui"
                except:
                    logger.warning("Coqui TTS failed, using pyttsx3")
                    import pyttsx3
                    self.tts = pyttsx3.init()
                    self.tts_type = "pyttsx3"
            else:
                import pyttsx3
                self.tts = pyttsx3.init()
                self.tts_type = "pyttsx3"
            
            logger.info(f"TTS initialized: {self.tts_type}")
        except Exception as e:
            logger.error(f"TTS initialization error: {e}")
            self.tts = None
            self.tts_type = None
    
    def listen(self, timeout=10) -> str:
        """Listen and transcribe user voice"""
        try:
            if not self.sr_available:
                logger.warning("SpeechRecognition not available")
                return ""
            
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            if not self.whisper_model:
                logger.error("Whisper model not loaded")
                return ""
            
            # Convert to WAV for Whisper
            import io
            wav_data = audio.get_wav_data()
            
            # Use Whisper for transcription
            result = self.whisper_model.transcribe(
                io.BytesIO(wav_data),
                language=None,  # Auto-detect
                verbose=False
            )
            
            text = result["text"].strip()
            logger.info(f"Transcribed: {text}")
            return text
        
        except Exception as e:
            logger.error(f"Error in listen: {e}")
            return ""
    
    def listen_for_wakeword(self, timeout=None):
        """Listen for 'Hey Jarvis' wake word"""
        try:
            if not self.sr_available or not self.whisper_model:
                logger.warning("Wake word detection not available")
                return True
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
            
            import io
            text = self.whisper_model.transcribe(
                io.BytesIO(audio.get_wav_data()),
                language="en",
                verbose=False
            )["text"].lower()
            
            if any(phrase in text for phrase in ["hey jarvis", "jarvis", "hey"]):
                logger.info("Wake word detected!")
                return True
        except:
            pass
        
        return False
    
    def detect_language(self, text: str) -> str:
        """Detect language from text"""
        try:
            from langdetect import detect
            lang = detect(text)
            return lang
        except:
            return "en"
    
    def speak(self, text: str, language: str = "en"):
        """Speak text using TTS"""
        try:
            if not self.tts:
                logger.warning("TTS not initialized")
                return
            
            logger.info(f"Speaking: {text[:100]}...")
            
            if self.tts_type == "coqui":
                self._speak_coqui(text, language)
            else:
                self._speak_pyttsx3(text)
        
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def _speak_coqui(self, text: str, language: str):
        """Speak using Coqui TTS"""
        try:
            output_path = Path("temp_output.wav")
            self.tts.tts_to_file(text=text, file_path=str(output_path))
            
            from pydub import AudioSegment
            from pydub.playback import play
            
            sound = AudioSegment.from_wav(str(output_path))
            play(sound)
            
            output_path.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"Coqui TTS error: {e}")
    
    def _speak_pyttsx3(self, text: str):
        """Speak using pyttsx3"""
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            logger.error(f"pyttsx3 error: {e}")
