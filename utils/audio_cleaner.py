"""
Audio Cleaning Utilities
Reduces noise and normalizes audio
"""

import noisereduce as nr
import soundfile as sf
import librosa
from pathlib import Path

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
