# Urdu Meeting Transcriber

**Automatically transcribe Urdu meetings and convert them to professional English documentation using AI.**

This project uses:
- **Whisper Large-v3** for accurate Urdu speech-to-text transcription
- **faster-whisper** for 2x faster processing with same accuracy
- **Claude AI** for translation and professional structuring

---

## 🎯 What This Does

1. **Records/Uploads** your Urdu meeting audio
2. **Transcribes** to Urdu text using Whisper (overnight processing)
3. **Cleans** audio noise automatically (optional)
4. **Generates** Claude-ready prompt for translation
5. **Outputs** professional English meeting documentation

---

## 💻 System Requirements

### Your System (Confirmed Compatible):
- ✅ Windows 11
- ✅ 32 GB RAM (Perfect for Large-v3 model)
- ✅ RTX 3050 4GB (Will attempt GPU, fallback to CPU)
- ✅ AMD Ryzen CPU

### Software Requirements:
- Python 3.8 - 3.11 (Python 3.12 not yet fully supported)
- pip (Python package manager)
- 10 GB free disk space
- Internet connection (first-time model download)

---

## 📦 Installation

### Step 1: Install Python

Check if you have Python:
```bash
python --version
```

If not installed or version is wrong:
1. Download Python 3.11 from: https://www.python.org/downloads/
2. During installation: ✅ Check "Add Python to PATH"
3. Restart terminal

### Step 2: Download This Project

Extract to: `C:\Users\YourName\urdu-meeting-transcriber`

### Step 3: Install Dependencies

Open Command Prompt in project folder:

```bash
cd C:\Users\YourName\urdu-meeting-transcriber
pip install -r requirements.txt
```

Installation time: 5-10 minutes (~2 GB download)

### Step 4: Test Installation

```bash
python test_installation.py
```

This downloads the Whisper model (~3 GB) and tests your setup.

---

## 🚀 Quick Start

### Basic Usage (3 Steps)

**Step 1: Place audio file**
```
audio/my_meeting.mp3  ← Put your file here
```

**Step 2: Run transcription**
```bash
python transcribe.py audio/my_meeting.mp3
```

**Step 3: Send to Claude**
Open `outputs/claude_prompts/my_meeting_prompt.txt` and paste in Claude!

---

## 📖 Usage Options

### Interactive Mode (Easiest)
```bash
python transcribe_interactive.py
```

### Command Line Options
```bash
# Basic
python transcribe.py audio/meeting.mp3

# With noise cleaning
python transcribe.py audio/meeting.mp3 --clean-noise

# Force CPU
python transcribe.py audio/meeting.mp3 --device cpu

# Batch process multiple files
python batch_transcribe.py audio/
```

---

## 📁 Project Structure

```
urdu-meeting-transcriber/
├── README.md                      ← Setup guide
├── requirements.txt               ← Dependencies
├── config.py                      ← Settings
├── test_installation.py           ← Test setup
├── transcribe.py                  ← Main script
├── transcribe_interactive.py      ← Interactive mode
├── batch_transcribe.py            ← Batch processing
├── utils/                         ← Helper modules
│   ├── audio_cleaner.py
│   ├── whisper_wrapper.py
│   └── claude_formatter.py
├── audio/                         ← Input files
└── outputs/                       ← Results
    ├── urdu_transcripts/
    ├── claude_prompts/
    └── logs/
```

---

## ⚙️ Configuration

Edit `config.py`:

```python
WHISPER_MODEL = "large-v3"  # tiny, base, small, medium, large-v3
DEVICE = "auto"             # auto, cpu, cuda
LANGUAGE = "ur"             # Urdu
NOISE_REDUCTION = True      # Clean audio
```

---

## 📊 Performance (Your System)

| Audio Length | Processing Time (CPU) |
|--------------|-----------------------|
| 15 min       | 30-45 min            |
| 30 min       | 1-1.5 hours          |
| 1 hour       | 2-3 hours            |
| 2 hours      | 4-6 hours            |

Accuracy: ~66-70% for Urdu (you'll review/correct ~30%)

---

## 🔧 Troubleshooting

**"CUDA out of memory"**
→ Script auto-falls back to CPU

**"No module named..."**
→ `pip install -r requirements.txt --upgrade`

**Very slow processing**
→ Close other programs, ensure 32GB RAM available

**Poor transcription**
→ Use `--clean-noise` flag, ensure good audio quality

---

## 🌟 Tips for Best Results

1. ✅ Use external microphone
2. ✅ Record in quiet environment  
3. ✅ Enable noise reduction: `--clean-noise`
4. ✅ Verify Urdu transcript before sending to Claude
5. ✅ Break meetings >2 hours into parts

---

## 🚀 Quick Reference

```bash
# Test setup
python test_installation.py

# Transcribe
python transcribe.py audio/meeting.mp3

# With cleaning
python transcribe.py audio/meeting.mp3 --clean-noise

# Interactive
python transcribe_interactive.py
```

---

**Ready? Run:** `python test_installation.py`

Last Updated: March 2026 | Version: 1.0.0
