# Quick Start Guide - 5 Minutes to Your First Transcription

## Step 1: Install Python Dependencies (2 minutes)

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
```

**Wait for installation to complete.** This downloads all necessary packages.

## Step 2: Test Your System (1 minute)

```powershell
python test_setup.py
```

This checks if everything is working and recommends optimal settings for your system.

## Step 3: Transcribe Your First Meeting (2 minutes setup)

### Option A: Quick Test (No Audio File Yet)

The test_setup.py already verified your system works!

### Option B: Transcribe Real Audio

```powershell
# Place your audio file in the project folder
# For example: meeting.mp3

# Run transcription
python transcribe.py meeting.mp3
```

**That's it!** The script will:
1. ✅ Load the AI model (happens once, automatically)
2. ✅ Transcribe your audio (takes 1-2 hours for 1 hour audio)
3. ✅ Generate Urdu transcript
4. ✅ Create Claude prompt

## Step 4: Get English Documentation (30 seconds)

1. Open the file ending with `_claude_prompt.txt`
2. Copy all the text
3. Paste into Claude (Desktop, Web, or Mobile)
4. Claude responds with structured English meeting notes

**Done!** You now have professional English documentation.

---

## Common First-Time Questions

**Q: Where should I put my audio files?**
A: Anywhere! Just provide the path: `python transcribe.py C:\Downloads\meeting.mp3`

**Q: How long does processing take?**
A: About 1-2 hours for 1 hour of audio on CPU (your system)

**Q: Can I run this overnight?**
A: Yes! Perfect for longer meetings

**Q: What if I get an error?**
A: Run `python test_setup.py` again and check the output

**Q: Do I need internet?**
A: Only for the first run (downloads AI model). After that, everything runs offline.

---

## Next Steps

Once you're comfortable with basic usage, check out:

- **README.md** - Complete documentation
- **Advanced options** - `python transcribe.py --help`
- **Batch processing** - Process multiple files: `python batch_transcribe.py`
- **Configuration** - Edit `config.yaml` to customize

---

**Need Help?** 
- Run: `python test_setup.py` to diagnose issues
- Check: README.md troubleshooting section
