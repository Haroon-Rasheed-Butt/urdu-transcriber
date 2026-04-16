"""
Audio Cleaning Utilities
Reduces noise, normalizes audio, and provides audio file helpers.
"""

import noisereduce as nr
import soundfile as sf
import librosa
from pathlib import Path


def validate_audio_file(audio_path, supported_formats):
    """
    Check that the audio file exists and has a supported extension.

    Args:
        audio_path: Path string to the audio file.
        supported_formats: List of allowed extensions (e.g. [".mp3", ".wav"]).

    Returns:
        True if valid, False otherwise (prints an error message on failure).
    """
    path = Path(audio_path)
    if not path.exists():
        print(f"Error: File not found: {audio_path}")
        return False
    if path.suffix.lower() not in supported_formats:
        print(f"Error: Unsupported format '{path.suffix}'")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return False
    return True


def get_audio_info(audio_path):
    """
    Return basic information about an audio file.

    Args:
        audio_path: Path string to the audio file.

    Returns:
        Dict with keys: duration_seconds, duration_formatted, sample_rate.
    """
    duration = librosa.get_duration(path=audio_path)
    info = sf.info(audio_path)
    minutes, seconds = divmod(int(duration), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        formatted = f"{hours}h {minutes}m {seconds}s"
    else:
        formatted = f"{minutes}m {seconds}s"
    return {
        "duration_seconds": duration,
        "duration_formatted": formatted,
        "sample_rate": info.samplerate,
    }

def clean_audio(audio_path, output_dir=None):
    """
    Clean audio by reducing noise and normalizing
    
    Args:
        audio_path: Path to input audio file
        output_dir: Directory to save cleaned audio (default: same as input)
    
    Returns:
        Path to cleaned audio file
    """
    
    audio_path = Path(audio_path)
    
    if output_dir is None:
        output_dir = audio_path.parent
    else:
        output_dir = Path(output_dir)
    
    # Load audio
    print("   Loading audio...")
    audio, sr = librosa.load(str(audio_path), sr=16000)  # Whisper uses 16kHz
    
    print(f"   Sample rate: {sr} Hz")
    print(f"   Duration: {len(audio)/sr:.1f} seconds")
    
    # Reduce noise
    print("   Reducing noise...")
    reduced_noise = nr.reduce_noise(
        y=audio,
        sr=sr,
        stationary=True,
        prop_decrease=0.8  # Reduce noise by 80%
    )
    
    # Normalize volume
    print("   Normalizing volume...")
    max_val = max(abs(reduced_noise.max()), abs(reduced_noise.min()))
    if max_val > 0:
        normalized = reduced_noise / max_val * 0.95  # Leave some headroom
    else:
        normalized = reduced_noise
    
    # Save cleaned audio
    output_path = output_dir / f"{audio_path.stem}_cleaned.wav"
    sf.write(str(output_path), normalized, sr)
    
    print(f"   Saved to: {output_path.name}")
    
    return str(output_path)
