"""
Claude Prompt Generator
Creates formatted prompts for Claude to translate and structure meeting notes
"""

def generate_claude_prompt(urdu_transcript, claude_config=None):
    """
    Generate a Claude-ready prompt from Urdu transcript
    
    Args:
        urdu_transcript: Urdu text from Whisper
        claude_config: Optional configuration dict
    
    Returns:
        Formatted prompt string
    """
    
    if claude_config is None:
        claude_config = {}
    
    # Get custom template or use default
    template = claude_config.get('prompt_template')
    
    if template:
        # Use custom template
        prompt = template.format(transcript=urdu_transcript)
    else:
        # Use default template
        prompt = f"""This is a transcript from a meeting conducted in Urdu:

{urdu_transcript}

Please:
1. Translate this entire transcript to professional English
2. Structure it as a formal meeting memo with:
   - Meeting Summary (2-3 sentences highlighting key points)
   - Key Discussion Points (main topics covered)
   - Decisions Made (concrete decisions and agreements)
   - Action Items (tasks with responsible parties if mentioned)
   - Next Steps (planned follow-ups)

Format it as a professional business document with clear sections."""
    
    return prompt

def generate_custom_prompt(urdu_transcript, instructions):
    """
    Generate a custom prompt with specific instructions
    
    Args:
        urdu_transcript: Urdu text
        instructions: Custom instructions for Claude
    
    Returns:
        Formatted prompt
    """
    
    prompt = f"""This is a transcript in Urdu:

{urdu_transcript}

{instructions}"""
    
    return prompt
