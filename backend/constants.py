"""
Focus Friend - Centralized Constants and Domain Presets.
Shared across backend services and API endpoints.
"""

from typing import Dict, Any

# Overwhelm Presets designed to test various communication pathologies
OVERWHELM_PRESETS: Dict[str, Dict[str, Any]] = {
    "manager_email": {
        "id": "manager_email",
        "title": "Rambling Boss Email",
        "category": "Email",
        "emoji": "👔",
        "text": (
            "Hey Alex, hope your week is wrapping up nicely! I wanted to touch base regarding the "
            "Q3 product retrospective slide deck we chatted about in passing last Tuesday. Overall the executive "
            "leadership loved the initial high-level vision, but Sarah raised a few concerns about the customer "
            "churn numbers in section 4. No need to rewrite everything—it looks super promising! Could you just "
            "review the updated deck I dropped in Google Drive, fix the slide 7 metric, and send me a 2-sentence "
            "confirmation before end of day Friday so I can sign off on it? Thanks so much for all your hard work on this!"
        )
    },
    "slack_thread": {
        "id": "slack_thread",
        "title": "15-Person Slack Storm",
        "category": "Slack",
        "emoji": "💬",
        "text": (
            "@here hey everyone, quick heads up on the staging deployment. @marcus pushed the auth fix but @dave thinks "
            "the token refresh might still be failing for European timezones. @alex can you jump on staging and verify "
            "whether the user login session persists after 15 minutes? We need to freeze this before tomorrow's 10:00 AM sprint demo. "
            "Also reminder to submit your team lunch preferences in the poll above by noon today. Don't worry about the logging errors "
            "in Datadog, those are unrelated."
        )
    },
    "client_scope": {
        "id": "client_scope",
        "title": "Scope-Creep Client Request",
        "category": "Client",
        "emoji": "📑",
        "text": (
            "Hi team, we were playing around with the latest beta build over the weekend and we really like the new dark mode! "
            "However, our marketing VP was wondering if we could quickly add support for multi-currency invoicing and automatic PDF "
            "generation before we officially go live on November 1st? I know we didn't include this in the original sprint statement "
            "of work, but it should only take a couple of lines of code right? Please let us know if this is doable or if we should "
            "set up a 45-minute sync call tomorrow at 2 PM to negotiate the deliverables."
        )
    },
    "discord_ping": {
        "id": "discord_ping",
        "title": "11:30 PM Panic Discord Ping",
        "category": "Discord",
        "emoji": "🚨",
        "text": (
            "@Alex hey bro sorry for pinging you so late (11:30 PM) but the client demo server just threw a 502 Bad Gateway error "
            "on the checkout endpoint. I tried restarting nginx but it looks like the postgres connection pool is exhausted. "
            "Can you log into the AWS EC2 box whenever you wake up tomorrow morning (ideally before 9 AM EST) and bounce the docker "
            "container? If not let me know so I can ping Jordan."
        )
    }
}

# Default Prompt Template for Local LLM (Phi-3)
PHI3_SYSTEM_PROMPT_TEMPLATE = """You are Focus Friend, a local-first executive function assistant built for individuals with ADHD navigating overwhelming communication.
Extract EXACTLY three fields in strict JSON format:
{{
  "vibe": "A one-sentence plain-English summary of the emotional context and tone (e.g. 'The boss is pleased with your progress and asking for a routine tweak'). Disarms anxiety and rejection sensitivity.",
  "deadline": "The specific calendar dates, timeframes, or deadlines mentioned. If none exist, write 'No hard deadline specified'.",
  "action_item": "A single, clear imperative bullet point starting with an action verb (e.g. 'Review the slide 7 metric and reply with confirmation'). Tells the brain exactly what to do first."
}}

TEXT TO DISTILL:
\"\"\"
{text}
\"\"\"

Return ONLY the raw JSON object with keys "vibe", "deadline", "action_item". Do not wrap with markdown code fences."""
