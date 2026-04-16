"""
Configuration loader for Urdu Meeting Transcriber
Reads config.yaml and exposes settings as module-level constants.
"""

from pathlib import Path
import yaml

# Load config.yaml from the same directory as this file
_CONFIG_PATH = Path(__file__).parent / "config.yaml"

with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
    _cfg = yaml.safe_load(f)

# Model settings
WHISPER_MODEL = _cfg["model"]["size"]
DEVICE = _cfg["model"]["device"]
COMPUTE_TYPE = _cfg["model"]["compute_type"]

# Audio settings
NOISE_REDUCTION = _cfg["audio"]["noise_reduction"]
SAMPLE_RATE = _cfg["audio"]["sample_rate"]

# Transcription settings
LANGUAGE = _cfg["transcription"]["language"]
TASK = _cfg["transcription"]["task"]
BEAM_SIZE = _cfg["transcription"]["beam_size"]
BEST_OF = _cfg["transcription"]["best_of"]
TEMPERATURE = _cfg["transcription"]["temperature"]
ENABLE_VAD = _cfg["transcription"]["vad_filter"]
VAD_THRESHOLD = _cfg["transcription"]["vad_parameters"]["threshold"]
VAD_MIN_SPEECH_DURATION_MS = _cfg["transcription"]["vad_parameters"]["min_speech_duration_ms"]
VAD_MIN_SILENCE_DURATION_MS = _cfg["transcription"]["vad_parameters"]["min_silence_duration_ms"]
WORD_TIMESTAMPS = _cfg["transcription"]["word_timestamps"]

# Output settings
OUTPUT_DIR = "outputs"
PRINT_SEGMENTS_REALTIME = True

# Supported audio formats
SUPPORTED_FORMATS = [".mp3", ".wav", ".m4a", ".mp4", ".flac", ".ogg", ".webm"]
