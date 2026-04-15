#!/usr/bin/env python3
"""
Batch transcription for multiple audio files
Process entire folders overnight
"""

import sys
import subprocess
from pathlib import Path
import argparse


def find_audio_files(directory, supported_formats):
    """Find all audio files in directory"""
    audio_files = []
    
    dir_path = Path(directory)
    
    for format_ext in supported_formats:
        audio_files.extend(dir_path.glob(f"*{format_ext}"))
    
    return sorted(audio_files)


def main():
    """Batch process audio files"""
    
    parser = argparse.ArgumentParser(
        description="Batch transcribe multiple audio files"
    )
    parser.add_argument(
        "directory",
        help="Directory containing audio files"
    )
    parser.add_argument(
        "--clean-noise",
        action="store_true",
        help="Clean audio noise before transcription"
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "cuda"],
        default="auto",
        help="Device to use"
    )
    parser.add_argument(
        "--model",
        default="large-v3",
        help="Whisper model to use"
    )
    
    args = parser.parse_args()
    
    # Find audio files
    supported_formats = [".mp3", ".wav", ".m4a", ".mp4", ".flac", ".ogg", ".webm"]
    audio_files = find_audio_files(args.directory, supported_formats)
    
    if not audio_files:
        print(f"No audio files found in {args.directory}")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return False
    
    print("=" * 70)
    print("BATCH TRANSCRIPTION")
    print("=" * 70)
    print(f"\nFound {len(audio_files)} audio files:")
    
    for i, file in enumerate(audio_files, 1):
        print(f"  {i}. {file.name}")
    
    print(f"\nSettings:")
    print(f"  Model: {args.model}")
    print(f"  Device: {args.device}")
    print(f"  Noise reduction: {'Yes' if args.clean_noise else 'No'}")
    
    response = input(f"\nProcess all {len(audio_files)} files? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Cancelled")
        return False
    
    # Process each file
    print("\n" + "=" * 70)
    print("STARTING BATCH PROCESSING")
    print("=" * 70 + "\n")
    
    successful = []
    failed = []
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n{'='*70}")
        print(f"FILE {i}/{len(audio_files)}: {audio_file.name}")
        print(f"{'='*70}\n")
        
        # Build command
        cmd = [sys.executable, "transcribe.py", str(audio_file)]
        
        if args.clean_noise:
            cmd.append("--clean-noise")
        
        cmd.extend(["--device", args.device])
        cmd.extend(["--model", args.model])
        
        try:
            subprocess.run(cmd, check=True)
            successful.append(audio_file.name)
            print(f"\n✅ {audio_file.name} - SUCCESS")
        
        except subprocess.CalledProcessError:
            failed.append(audio_file.name)
            print(f"\n❌ {audio_file.name} - FAILED")
        
        except KeyboardInterrupt:
            print("\n\nBatch processing interrupted by user")
            break
    
    # Summary
    print("\n" + "=" * 70)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 70)
    
    print(f"\nSuccessful: {len(successful)}/{len(audio_files)}")
    for file in successful:
        print(f"  ✅ {file}")
    
    if failed:
        print(f"\nFailed: {len(failed)}/{len(audio_files)}")
        for file in failed:
            print(f"  ❌ {file}")
    
    print("\nResults saved in outputs/ directory")
    print("=" * 70)
    
    return len(failed) == 0


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
