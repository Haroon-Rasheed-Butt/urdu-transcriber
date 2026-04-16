# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Urdu Meeting Transcriber: a CLI tool that transcribes Urdu audio using `faster-whisper` (Whisper Large-v3), then generates a Claude-ready prompt for translation into structured English meeting documentation. The workflow is **fully local** — all processing (transcription, noise reduction) happens on-device for privacy; no audio is uploaded to any cloud service. Claude is invoked manually by the user via copy-paste, not via API.

### Why a two-step pipeline (Whisper → Claude), not direct Whisper translation

Whisper's built-in `--task translate` is less accurate for Urdu than transcribing first then translating with Claude, because:
- Claude understands business context, idioms, and Urdu cultural references that Whisper misses
- The user can review and correct the Urdu transcript before passing it to Claude
- Claude translates and structures the output (summary, decisions, action items) in a single pass

### Target output format

When the generated `_prompt.txt` is pasted into Claude, the expected output is a professional English meeting memo with these sections:
- Executive summary (2–3 sentences)
- Key discussion points
- Decisions made
- Action items (with responsible parties where mentioned)
- Next steps

## Setup

```bash
# Install dependencies (PyTorch with CUDA first for GPU support)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

# Verify system (downloads Whisper model ~3 GB on first run)
python test_setup.py
```

On Windows, `setup.bat` automates the above steps.

## Common Commands

```bash
# Single file transcription
python transcribe.py audio/meeting.mp3

# With noise reduction
python transcribe.py audio/meeting.mp3 --clean-noise

# Force CPU (default is auto-detect GPU → CPU fallback)
python transcribe.py audio/meeting.mp3 --device cpu

# Choose prompt template: standard | brief | detailed | technical | client
python transcribe.py audio/meeting.mp3 --template detailed

# Batch process a directory
python batch_transcribe.py audio/
```

## Architecture

```
transcribe.py          ← Entry point: CLI arg parsing, orchestration, output saving
batch_transcribe.py    ← Loops over a directory, shells out to transcribe.py per file
config.py              ← Reads config.yaml → exposes settings as Python constants
config.yaml            ← All runtime defaults (model, device, VAD params, prompt template)
utils/
  whisper_helper.py    ← load_whisper_model(), transcribe_audio(), estimate_processing_time()
  audio_cleaner.py     ← clean_audio(), get_audio_info(), validate_audio_file()
  claude_formatter.py  ← create_claude_prompt(), save_claude_prompt(), get_template(), 5 prompt templates
  __init__.py          ← Re-exports all public functions from the three modules above
```

**Data flow:** audio file → (optional) `clean_audio()` → `load_whisper_model()` + `transcribe_audio()` → `generate_claude_prompt()` → saved files in `outputs/`.

**Outputs** (all under `outputs/`):
- `urdu_transcripts/<stem>_urdu.txt` — raw Urdu transcript
- `claude_prompts/<stem>_prompt.txt` — formatted prompt; user pastes this into Claude manually
- `logs/<stem>_log.json` — processing metadata

## Configuration

Edit `config.yaml` to change defaults. Key settings:

| Setting | Default | Notes |
|---|---|---|
| `model.size` | `large-v3` | `tiny`/`base`/`small`/`medium` available for speed |
| `model.device` | `auto` | Auto-detects GPU; falls back to CPU on OOM |
| `model.compute_type` | `int8` | Quantization; keeps large-v3 within 4 GB VRAM |
| `transcription.language` | `ur` | Urdu |
| `audio.noise_reduction` | `true` | Pre-processing step |

## Performance Reference (RTX 3050 4 GB / AMD Ryzen / 32 GB RAM)

| Audio length | CPU time |
|---|---|
| 15 min | 30–45 min |
| 1 hour | 2–3 hours |
| 2 hours | 4–6 hours |

GPU with int8 quantization significantly improves these figures but may OOM — the loader falls back to CPU automatically.

Expected transcription accuracy is ~75% for clear Urdu audio with the large-v3 model. Noisy recordings benefit significantly from `--clean-noise`. The user reviews the Urdu transcript before sending to Claude, so imperfect transcription is expected and tolerable.
