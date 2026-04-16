"""
Whisper Helper Utilities
Handles model loading and transcription
"""

from faster_whisper import WhisperModel
import torch

def detect_optimal_device():
    """Detect if GPU is available and usable"""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"   GPU detected: {gpu_name}")
        print(f"   VRAM: {vram_gb:.1f} GB")
        return "cuda", vram_gb
    else:
        print("   No GPU detected, using CPU")
        return "cpu", 0

def load_whisper_model(model_size="large-v3", device="auto", compute_type="int8"):
    """
    Load Whisper model with optimal settings
    
    Args:
        model_size: Model size (tiny, base, small, medium, large-v3)
        device: Device to use (auto, cpu, cuda)
        compute_type: Precision (int8, float16, float32)
    
    Returns:
        WhisperModel instance
    """
    
    # Auto-detect device if requested
    if device == "auto":
        detected_device, vram_gb = detect_optimal_device()
        
        # For RTX 3050 (4GB), recommend settings
        if detected_device == "cuda" and vram_gb <= 4.5:
            print(f"   Note: 4GB VRAM detected")
            if model_size == "large-v3":
                print(f"   Trying Large-v3 with int8 quantization...")
                print(f"   If this fails, we'll fallback to CPU")
        
        device = detected_device
    
    try:
        # Try loading model
        model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
            num_workers=4 if device == "cpu" else 1
        )
        
        actual_device = "GPU" if device == "cuda" else "CPU"
        print(f"   Running on: {actual_device}")
        
        return model
        
    except Exception as e:
        # If GPU fails, fallback to CPU
        if device == "cuda":
            print(f"\n⚠️  GPU loading failed: {e}")
            print("   Falling back to CPU mode...\n")
            
            model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8",
                num_workers=4
            )
            
            print("   Running on: CPU")
            return model
        else:
            raise e

def transcribe_audio(model, audio_path, settings):
    """
    Transcribe audio file
    
    Args:
        model: WhisperModel instance
        audio_path: Path to audio file
        settings: Dictionary of transcription settings
    
    Returns:
        tuple: (full_transcript_text, list_of_segments)
    """
    
    # Extract settings
    language = settings.get('language', 'ur')
    task = settings.get('task', 'transcribe')
    beam_size = settings.get('beam_size', 5)
    best_of = settings.get('best_of', 5)
    temperature = settings.get('temperature', 0.0)
    word_timestamps = settings.get('word_timestamps', True)
    vad_filter = settings.get('vad_filter', True)
    
    # Build VAD parameters
    vad_params = None
    if vad_filter:
        vad_params = {
            'threshold': 0.5,
            'min_speech_duration_ms': 250,
            'min_silence_duration_ms': 500
        }
    
    # Transcribe
    segments_generator, info = model.transcribe(
        audio_path,
        language=language,
        task=task,
        beam_size=beam_size,
        best_of=best_of,
        temperature=temperature,
        word_timestamps=word_timestamps,
        vad_filter=vad_filter,
        vad_parameters=vad_params,
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6
    )
    
    # Collect segments
    full_transcript = ""
    segments_list = []
    
    print(f"   Detected language: {info.language} (confidence: {info.language_probability:.1%})")
    print(f"   Duration: {info.duration:.1f} seconds ({info.duration/60:.1f} minutes)")
    print()
    
    segment_count = 0
    for segment in segments_generator:
        segment_count += 1
        
        # Print progress every 10 segments
        if segment_count % 10 == 0:
            print(f"   Processed {segment_count} segments... ({segment.end/60:.1f} min)")
        
        full_transcript += segment.text + " "
        
        segments_list.append({
            'start': segment.start,
            'end': segment.end,
            'text': segment.text
        })
    
    print(f"   Total segments: {segment_count}")
    
    return full_transcript.strip(), segments_list


def estimate_processing_time(duration_seconds, model_size="large-v3", device="cpu"):
    """
    Rough estimate of transcription wall-clock time.

    Based on benchmarks from RTX 3050 4 GB / AMD Ryzen / 32 GB RAM.
    CPU large-v3 runs at roughly 2-3x real-time; GPU is ~4-8x faster.

    Args:
        duration_seconds: Length of the audio in seconds.
        model_size: Whisper model size string.
        device: "cpu" or "cuda".

    Returns:
        Estimated seconds to process.
    """
    # Multipliers: how many seconds of wall-clock per second of audio
    cpu_multipliers = {
        "tiny": 0.3,
        "base": 0.5,
        "small": 1.0,
        "medium": 1.5,
        "large-v3": 2.5,
    }
    gpu_multipliers = {
        "tiny": 0.05,
        "base": 0.1,
        "small": 0.15,
        "medium": 0.25,
        "large-v3": 0.4,
    }
    multipliers = gpu_multipliers if device == "cuda" else cpu_multipliers
    factor = multipliers.get(model_size, 2.5)
    return duration_seconds * factor


def format_time_estimate(seconds):
    """
    Format seconds into a human-readable string like '~12 min' or '~2 h 30 min'.
    """
    minutes = int(seconds / 60)
    if minutes < 1:
        return "< 1 min"
    hours, mins = divmod(minutes, 60)
    if hours:
        return f"~{hours} h {mins} min"
    return f"~{minutes} min"
