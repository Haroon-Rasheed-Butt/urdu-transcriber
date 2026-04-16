#!/usr/bin/env python3
"""
Main transcription script for Urdu Meeting Transcriber

Usage:
    python transcribe.py audio/meeting.mp3
    python transcribe.py audio/meeting.mp3 --clean-noise
    python transcribe.py audio/meeting.mp3 --device cpu
    python transcribe.py audio/meeting.mp3 --template detailed
"""

import sys
import argparse
import time
from pathlib import Path
import json
from datetime import datetime

import config
from utils.audio_cleaner import clean_audio, get_audio_info, validate_audio_file
from utils.whisper_helper import (
    load_whisper_model,
    transcribe_audio,
    estimate_processing_time,
    format_time_estimate,
)
from utils.claude_formatter import create_claude_prompt, save_claude_prompt, get_template


def main():
    """Main transcription function"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Transcribe Urdu meetings to text and generate Claude prompts"
    )
    parser.add_argument(
        "audio_file",
        help="Path to audio file to transcribe"
    )
    parser.add_argument(
        "--clean-noise",
        action="store_true",
        default=config.NOISE_REDUCTION,
        help="Clean audio noise before transcription"
    )
    parser.add_argument(
        "--no-clean-noise",
        action="store_false",
        dest="clean_noise",
        help="Skip noise reduction"
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "cuda"],
        default=config.DEVICE,
        help="Device to use for processing (default: auto)"
    )
    parser.add_argument(
        "--model",
        default=config.WHISPER_MODEL,
        help=f"Whisper model to use (default: {config.WHISPER_MODEL})"
    )
    parser.add_argument(
        "--output-dir",
        default=config.OUTPUT_DIR,
        help="Output directory for results"
    )
    parser.add_argument(
        "--template",
        choices=["standard", "brief", "detailed", "technical", "client"],
        default="standard",
        help="Claude prompt template to use"
    )

    args = parser.parse_args()

    # Validate audio file
    if not validate_audio_file(args.audio_file, config.SUPPORTED_FORMATS):
        sys.exit(1)

    audio_path = Path(args.audio_file)

    print("=" * 70)
    print("URDU MEETING TRANSCRIBER")
    print("=" * 70)
    print(f"Audio file: {audio_path.name}")
    print(f"Model: {args.model}")
    print(f"Device: {args.device}")
    print(f"Noise reduction: {'Yes' if args.clean_noise else 'No'}")
    print("=" * 70)
    print()

    # Get audio info
    print("Step 1: Analyzing audio file...")
    audio_info = get_audio_info(str(audio_path))
    print(f"  Duration: {audio_info['duration_formatted']}")
    print(f"  Sample rate: {audio_info['sample_rate']} Hz")
    print()

    # Estimate processing time
    estimated_time = estimate_processing_time(
        audio_info["duration_seconds"],
        args.model,
        args.device if args.device != "auto" else "cpu",  # Conservative estimate
    )
    print(f"  Estimated processing time: {format_time_estimate(estimated_time)}")
    print(f"  (This is a conservative estimate. Actual time may be faster.)")
    print()

    # Clean audio if requested
    if args.clean_noise:
        print("Step 2: Cleaning audio (removing noise)...")
        cleaned_audio_path = clean_audio(str(audio_path))
        audio_to_transcribe = cleaned_audio_path
        print()
    else:
        print("Step 2: Skipping noise reduction...")
        audio_to_transcribe = str(audio_path)
        print()

    # Load Whisper model
    print("Step 3: Loading Whisper model...")
    model = load_whisper_model(
        model_size=args.model,
        device=args.device,
        compute_type=config.COMPUTE_TYPE,
    )
    # Determine actual device for logging
    actual_device = args.device
    if actual_device == "auto":
        import torch
        actual_device = "cuda" if torch.cuda.is_available() else "cpu"
    print()

    # Transcribe
    print("Step 4: Transcribing audio...")
    print("(This will take a while. Progress shown below.)")
    print()

    start_time = time.time()

    transcription_settings = {
        "language": config.LANGUAGE,
        "task": config.TASK,
        "beam_size": config.BEAM_SIZE,
        "best_of": config.BEST_OF,
        "temperature": config.TEMPERATURE,
        "word_timestamps": config.WORD_TIMESTAMPS,
        "vad_filter": config.ENABLE_VAD,
    }

    transcript_text, segments = transcribe_audio(
        model, audio_to_transcribe, transcription_settings
    )

    processing_time = time.time() - start_time
    print()

    # Create output directories
    output_dir = Path(args.output_dir)
    urdu_dir = output_dir / "urdu_transcripts"
    claude_dir = output_dir / "claude_prompts"
    log_dir = output_dir / "logs"

    for dir_path in [urdu_dir, claude_dir, log_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Save Urdu transcript
    print("Step 5: Saving results...")

    urdu_file = urdu_dir / f"{audio_path.stem}_urdu.txt"
    with open(urdu_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"  Urdu transcript: {urdu_file}")

    # Create and save Claude prompt
    metadata = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "audio_file": audio_path.name,
        "duration": audio_info["duration_formatted"],
        "language": f"Urdu (auto-detected)",
        "processing_info": f"Model: {args.model}, Device: {actual_device}",
    }

    template = get_template(args.template)
    claude_prompt = create_claude_prompt(
        transcript_text,
        template=template,
        metadata=metadata,
    )

    claude_file = claude_dir / f"{audio_path.stem}_prompt.txt"
    save_claude_prompt(claude_prompt, claude_file)
    print(f"  Claude prompt: {claude_file}")

    # Save processing log
    log_file = log_dir / f"{audio_path.stem}_log.json"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "audio_file": str(audio_path),
        "audio_info": audio_info,
        "model": args.model,
        "device": actual_device,
        "compute_type": config.COMPUTE_TYPE,
        "noise_reduction": args.clean_noise,
        "language": "ur",
        "duration_seconds": audio_info["duration_seconds"],
        "processing_time_seconds": round(processing_time, 1),
        "segments_count": len(segments),
        "template_used": args.template,
    }

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    print(f"  Processing log: {log_file}")

    print()
    print("=" * 70)
    print("TRANSCRIPTION COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print(f"1. Review Urdu transcript: {urdu_file}")
    print(f"2. Copy Claude prompt: {claude_file}")
    print(f"3. Paste prompt into Claude.ai or Claude Desktop app")
    print(f"4. Get your professional English meeting memo!")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTranscription interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
