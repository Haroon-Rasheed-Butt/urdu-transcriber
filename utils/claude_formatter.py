"""
Claude Prompt Generator
Creates formatted prompts for Claude to translate and structure meeting notes.
Supports multiple prompt templates (standard, brief, detailed, technical, client).
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

TEMPLATES = {
    "standard": """\
You are a professional translator and meeting-notes specialist.

Below is a transcript from a meeting conducted in Urdu:

{transcript}

{metadata_block}

Please:
1. Translate this entire transcript to professional English.
2. Structure it as a formal meeting memo with:
   - Executive Summary (2-3 sentences highlighting key points)
   - Key Discussion Points (main topics covered)
   - Decisions Made (concrete decisions and agreements)
   - Action Items (tasks with responsible parties if mentioned)
   - Next Steps (planned follow-ups)

Format it as a professional business document with clear sections.""",

    "brief": """\
Below is an Urdu meeting transcript:

{transcript}

{metadata_block}

Translate to English and provide:
- 3-5 bullet point summary
- Action items list

Keep it concise.""",

    "detailed": """\
You are a professional translator and meeting-notes specialist.

Below is a transcript from a meeting conducted in Urdu:

{transcript}

{metadata_block}

Please produce a comprehensive English meeting memo:
1. Executive Summary (2-3 sentences)
2. Attendees & Roles (if mentioned)
3. Agenda Items Covered
4. Detailed Discussion Points (preserve nuance and context)
5. Decisions Made (with rationale where stated)
6. Action Items (owner, deadline if mentioned, priority)
7. Open Questions / Parking Lot
8. Next Steps & Follow-up Schedule

Preserve all names, numbers, dates, and technical terms accurately.
Format as a professional business document with clear headings.""",

    "technical": """\
You are a technical translator specialising in software engineering meetings.

Below is an Urdu meeting transcript (likely a sprint review, stand-up, or technical design discussion):

{transcript}

{metadata_block}

Translate to English and structure as:
1. Summary (2-3 sentences)
2. Technical Discussion Points (preserve code names, architecture terms, API names)
3. Decisions & Trade-offs
4. Action Items (owner, ticket/issue reference if mentioned)
5. Blockers & Risks
6. Next Steps

Use precise technical language. Keep acronyms and product names as-is.""",

    "client": """\
You are a professional translator preparing client-facing documentation.

Below is an Urdu meeting transcript from a client call:

{transcript}

{metadata_block}

Produce a polished, client-ready English meeting summary:
1. Meeting Overview (date, participants if mentioned, purpose)
2. Key Points Discussed
3. Agreed Deliverables & Timelines
4. Action Items (with owners)
5. Next Meeting / Follow-up

Tone: professional, clear, confident. Avoid internal jargon.""",
}


def _format_metadata_block(metadata):
    """Format metadata dict into a readable block for the prompt."""
    if not metadata:
        return ""
    lines = ["Meeting metadata:"]
    for key, value in metadata.items():
        lines.append(f"  - {key}: {value}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_template(name):
    """
    Return a prompt template string by name.

    Args:
        name: One of 'standard', 'brief', 'detailed', 'technical', 'client'.

    Returns:
        Template string with {transcript} and {metadata_block} placeholders.

    Raises:
        ValueError: If the template name is not recognised.
    """
    if name not in TEMPLATES:
        raise ValueError(
            f"Unknown template '{name}'. "
            f"Available templates: {', '.join(TEMPLATES)}"
        )
    return TEMPLATES[name]


def create_claude_prompt(transcript, template=None, metadata=None):
    """
    Build a complete Claude prompt from a transcript.

    Args:
        transcript: Urdu transcript text.
        template: Template string (from get_template) or None for standard.
        metadata: Optional dict of meeting metadata.

    Returns:
        Formatted prompt string ready to paste into Claude.
    """
    if template is None:
        template = TEMPLATES["standard"]
    metadata_block = _format_metadata_block(metadata)
    return template.format(transcript=transcript, metadata_block=metadata_block)


def save_claude_prompt(prompt, file_path):
    """
    Write a prompt string to a file.

    Args:
        prompt: The formatted prompt text.
        file_path: Path (string or Path) to write to.
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(prompt)


def generate_claude_prompt(urdu_transcript, claude_config=None):
    """
    Generate a Claude-ready prompt from Urdu transcript (legacy helper).

    Args:
        urdu_transcript: Urdu text from Whisper.
        claude_config: Optional configuration dict with 'prompt_template' key.

    Returns:
        Formatted prompt string.
    """
    if claude_config is None:
        claude_config = {}

    custom_template = claude_config.get("prompt_template")
    if custom_template:
        return custom_template.format(transcript=urdu_transcript)

    return create_claude_prompt(urdu_transcript)


def generate_custom_prompt(urdu_transcript, instructions):
    """
    Generate a custom prompt with specific instructions.

    Args:
        urdu_transcript: Urdu text.
        instructions: Custom instructions for Claude.

    Returns:
        Formatted prompt.
    """
    return f"""\
This is a transcript in Urdu:

{urdu_transcript}

{instructions}"""
