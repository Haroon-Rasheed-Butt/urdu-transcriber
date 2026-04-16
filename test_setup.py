#!/usr/bin/env python3
"""
Setup verification script for Urdu Meeting Transcriber.

Checks that all dependencies are installed, detects GPU availability,
and (optionally) downloads the Whisper model on first run.

Usage:
    python test_setup.py
"""

import sys


def check_import(module_name, package_label=None):
    """Try importing a module; return True on success."""
    label = package_label or module_name
    try:
        __import__(module_name)
        print(f"  [OK]  {label}")
        return True
    except ImportError as e:
        print(f"  [FAIL] {label} -- {e}")
        return False


def main():
    print("=" * 60)
    print("URDU MEETING TRANSCRIBER - SETUP CHECK")
    print("=" * 60)
    print()

    all_ok = True

    # ------------------------------------------------------------------
    # 1. Core Python packages
    # ------------------------------------------------------------------
    print("1. Checking Python packages...")
    packages = [
        ("faster_whisper", "faster-whisper"),
        ("torch", "torch (PyTorch)"),
        ("torchaudio", "torchaudio"),
        ("soundfile", "soundfile"),
        ("librosa", "librosa"),
        ("noisereduce", "noisereduce"),
        ("numpy", "numpy"),
        ("scipy", "scipy"),
        ("yaml", "PyYAML"),
    ]

    for module, label in packages:
        if not check_import(module, label):
            all_ok = False
    print()

    # ------------------------------------------------------------------
    # 2. Config loading
    # ------------------------------------------------------------------
    print("2. Checking config.yaml...")
    try:
        import config  # noqa: F811
        print(f"  [OK]  config.yaml loaded")
        print(f"        Model: {config.WHISPER_MODEL}")
        print(f"        Device: {config.DEVICE}")
        print(f"        Compute type: {config.COMPUTE_TYPE}")
        print(f"        Language: {config.LANGUAGE}")
    except Exception as e:
        print(f"  [FAIL] Could not load config -- {e}")
        all_ok = False
    print()

    # ------------------------------------------------------------------
    # 3. GPU detection
    # ------------------------------------------------------------------
    print("3. Checking GPU availability...")
    try:
        import torch

        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"  [OK]  GPU detected: {gpu_name} ({vram:.1f} GB VRAM)")
            if vram <= 4.5:
                print(f"        Note: 4 GB VRAM -- large-v3 will use int8 quantization")
        else:
            print(f"  [INFO] No CUDA GPU detected. Transcription will use CPU (slower).")
    except Exception as e:
        print(f"  [WARN] GPU check failed -- {e}")
    print()

    # ------------------------------------------------------------------
    # 4. Whisper model availability
    # ------------------------------------------------------------------
    print("4. Checking Whisper model...")
    try:
        from faster_whisper.utils import download_model

        model_size = config.WHISPER_MODEL
        print(f"  Downloading / verifying '{model_size}' model...")
        print(f"  (This may take a few minutes on first run -- ~3 GB download)")
        model_path = download_model(model_size)
        print(f"  [OK]  Model ready at: {model_path}")
    except Exception as e:
        print(f"  [WARN] Model check failed -- {e}")
        print(f"        The model will be downloaded automatically on first transcription.")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 60)
    if all_ok:
        print("All checks passed! You're ready to transcribe.")
        print()
        print("Quick start:")
        print("  python transcribe.py <audio_file>")
        print("  python transcribe.py <audio_file> --clean-noise")
    else:
        print("Some checks failed. Please install missing packages:")
        print("  pip install -r requirements.txt")
        print()
        print("For GPU support, install PyTorch with CUDA first:")
        print("  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
