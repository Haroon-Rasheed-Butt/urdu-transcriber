# Installation & Setup Guide

Complete step-by-step installation guide for Windows 11.

## Prerequisites

### 1. Python 3.9 or Higher

**Check if you have Python:**
```powershell
python --version
```

If you see `Python 3.9.x` or higher, you're good! Skip to step 2.

**If not installed:**
1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Restart PowerShell/Command Prompt

### 2. Verify pip (Python Package Manager)

```powershell
pip --version
```

Should show something like: `pip 24.0 from ...`

If not, run:
```powershell
python -m ensurepip --upgrade
```

### 3. (Optional) CUDA for GPU Acceleration

**You have RTX 3050, so this is recommended but not required.**

Check if CUDA is installed:
```powershell
nvidia-smi
```

You already have CUDA 13.0 installed (confirmed from your system info), so you're all set!

## Automated Installation (Recommended)

### Option 1: Using setup.bat (Easiest)

1. **Download/Extract the project folder** to your computer
   - Example: `C:\Users\haroonrasheed\urdu-meeting-transcriber`

2. **Open the folder** in File Explorer

3. **Double-click `setup.bat`**
   - This runs the automated setup script

4. **Wait for installation** (5-10 minutes)
   - Downloads all required packages
   - Creates necessary folders
   - Runs system test

5. **Done!** If you see "Setup Complete!", you're ready.

## Manual Installation

If automated setup fails, follow these steps:

### Step 1: Open PowerShell in Project Folder

1. Navigate to project folder in File Explorer
2. Hold **Shift** + **Right-click** in empty space
3. Select "Open PowerShell window here"

### Step 2: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 3: Install PyTorch with CUDA Support

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**This step is important for GPU acceleration!**

Wait 2-5 minutes for download and installation.

### Step 4: Install Other Requirements

```powershell
pip install -r requirements.txt
```

Wait 3-5 minutes for installation.

### Step 5: Create Folders

```powershell
mkdir audio
mkdir output
```

### Step 6: Test Installation

```powershell
python test_setup.py
```

If you see ✅ marks and "Test completed!", you're ready!

## Troubleshooting Installation

### Error: "Python is not recognized"

**Problem:** Python not in PATH

**Solution:**
1. Reinstall Python
2. Make sure to check "Add Python to PATH"
3. Restart computer

### Error: "pip install failed"

**Problem:** Network issues or pip version

**Solution:**
```powershell
# Update pip
python -m pip install --upgrade pip

# Try install again with verbose output
pip install -r requirements.txt --verbose
```

### Error: "CUDA out of memory" during test

**Problem:** GPU memory insufficient

**Solution:** This is fine! The script will automatically use CPU mode.

### Error: "Microsoft Visual C++ 14.0 required"

**Problem:** Missing C++ build tools (rare on Windows 11)

**Solution:**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Restart
4. Try installation again

### Slow Installation

**This is normal!** First-time installation can take 10-15 minutes because:
- PyTorch is ~2 GB
- Other packages are ~500 MB
- Whisper models download on first use (~3 GB)

## Verifying Installation

Run the test script:
```powershell
python test_setup.py
```

You should see:
```
✅ Python version is compatible (3.9+)
✅ CUDA is available
✅ Sufficient RAM for Large-v3 model
✅ Model loading works!
```

## First Run Notes

### The First Transcription Will Take Longer

When you run your first transcription:
```powershell
python transcribe.py meeting.mp3
```

The script will:
1. Download Whisper model (~3 GB) - **one-time only**
2. Cache model locally
3. Start transcription

**First run:** Model download + transcription (15-20 min extra)
**Subsequent runs:** Just transcription (normal speed)

The model is saved to:
- Windows: `C:\Users\YourName\.cache\huggingface\hub\`

### Storage Requirements

Make sure you have:
- **10 GB free** for models and processing
- More if you process many large files

## Updating the Software

To update packages to latest versions:

```powershell
pip install --upgrade faster-whisper noisereduce soundfile librosa torch
```

## Uninstalling

To remove everything:

1. Delete the project folder
2. (Optional) Clear model cache:
   ```powershell
   rmdir /s %USERPROFILE%\.cache\huggingface\hub
   ```

## Network/Firewall Issues

If downloads fail:

1. **Check internet connection**
2. **Disable VPN temporarily** (if using)
3. **Check corporate firewall** (if on work network)
4. **Try manual download:**
   - PyTorch: https://pytorch.org/get-started/locally/
   - Whisper models: Download manually from HuggingFace

## Next Steps After Installation

Once installation is complete:

1. **Read QUICKSTART.md** - 5-minute guide to first transcription
2. **Place audio file** in project folder
3. **Run transcription** - `python transcribe.py your_audio.mp3`
4. **Get English notes** - Paste Claude prompt into Claude

## Getting Help

If you're stuck:

1. Run `python test_setup.py` and save the output
2. Check README.md troubleshooting section
3. Verify all prerequisites are met
4. Make sure you have 10+ GB free disk space

## System Requirements Summary

**Minimum:**
- Windows 10/11 (64-bit)
- Python 3.9+
- 8 GB RAM
- 10 GB free disk space
- Internet (first-time setup only)

**Recommended (Your System):**
- ✅ Windows 11
- ✅ Python 3.9+
- ✅ 32 GB RAM
- ✅ NVIDIA RTX 3050
- ✅ 10+ GB free disk

You're all set for optimal performance!
