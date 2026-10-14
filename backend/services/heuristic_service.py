"""
Focus Friend - Heuristic NLP Extraction Service.
Zero-Cloud, 100% offline rule-based distillation for ADHD executive function support.
Operates completely without external network dependencies.
"""

import re
from typing import Dict, Any, List


class HeuristicExtractionService:
    """Extracts emotional tone, deadlines, and action items using deterministic regex heuristics."""

    DEADLINE_PATTERNS: List[str] = [
        r'\b(?:before\s+end\s+of\s+day\s+\w+|end\s+of\s+day\s+\w+|eod\s+\w+|by\s+\w+\s+eod)\b',
        r'\b(?:before\s+tomorrow\'?s\s+\d+:\d+\s*[ap]m|\d+:\d+\s*[ap]m\s+tomorrow|tomorrow\s+at\s+\d+:\d+\s*[ap]m)\b',
        r'\b(?:before\s+\d+:\d+\s*[ap]m\s+\w+|\d+:\d+\s*[ap]m\s+\w+)\b',
        r'\b(?:by\s+noon\s+today|by\s+noon|by\s+eod|by\s+end\s+of\s+day)\b',
        r'\b(?:before\s+we\s+officially\s+go\s+live\s+on\s+[\w\s\d]+|go\s+live\s+on\s+[\w\s\d]+)\b',
        r'\b(?:by\s+[a-zA-Z]+\s+\d+(?:st|nd|rd|th)?|on\s+[a-zA-Z]+\s+\d+(?:st|nd|rd|th)?)\b',
        r'\b(?:before\s+friday|by\s+friday|end\s+of\s+day\s+friday)\b',
        r'\b(?:tomorrow\s+morning|before\s+9\s*am\s*\w*|tomorrow\s+at\s+2\s*pm)\b',
    ]

    ACTION_TRIGGERS: List[str] = [
        r'could you (?:just )?(?:review|fix|send|check|verify|update|test)',
        r'can you (?:jump|verify|check|test|log|update|take a look|bounce)',
        r'please (?:let us know|review|send|confirm|update)',
        r'can you (?:log into|restart|bounce)',
    ]

    @classmethod
    def extract(cls, text: str) -> Dict[str, Any]:
        """
        Distills raw text into Tone (The Vibe), Timeline (The Deadline), and Task (The Action Item).

        Args:
            text: Raw message content.

        Returns:
            Dict containing 'vibe', 'deadline', 'action_item', 'engine'.
        """
        cleaned_text = text.strip()
        lower = cleaned_text.lower()
        sentences = [s.strip() for s in re.split(r'(?<=[.?!])\s+', cleaned_text) if s.strip()]

        # 1. Distill Tone & Vibe (Emotional Context)
        if any(w in lower for w in ['sorry for pinging', '502', 'error', 'urgent', 'asap', 'late', 'exhausted']):
            vibe = "Mild situational urgency regarding a technical issue; supportive and non-judgmental tone."
        elif any(w in lower for w in ['loved the initial', 'super promising', 'no need to rewrite', 'great work']):
            vibe = "Very positive and reassuring; leadership is pleased with progress and only requests minor polish."
        elif any(w in lower for w in ['scope', 'marketing vp', 'sprint', 'negotiate', 'out of scope']):
            vibe = "Polite exploratory inquiry regarding additional deliverables; open to discussion and pushback."
        elif any(w in lower for w in ['quick heads up', 'poll', 'reminder', 'lunch preferences']):
            vibe = "Routine operational team coordination with casual logistics."
        else:
            vibe = "Collaborative, low-pressure communication requesting standard feedback."

        # 2. Distill Deadline
        deadline = "No hard deadline specified; handle during normal working cadence."
        for pattern in cls.DEADLINE_PATTERNS:
            match = re.search(pattern, cleaned_text, re.IGNORECASE)
            if match:
                raw_match = match.group(0).strip()
                if "friday" in raw_match.lower() and "end of day" in raw_match.lower():
                    deadline = "End of Day Friday"
                else:
                    deadline = raw_match.capitalize()
                break

        # 3. Distill Action Item (Imperative Task)
        action_item = "Review the message details and provide a brief status update."
        found_action = False

        for sentence in sentences:
            for trigger in cls.ACTION_TRIGGERS:
                if re.search(trigger, sentence, re.IGNORECASE):
                    clean = re.sub(
                        r'^(Hey|Hi|Also|So|And)\s+[@\w\s,]+(?:can you|could you|please)\s+',
                        '',
                        sentence,
                        flags=re.IGNORECASE,
                    )
                    clean = re.sub(r'^(can you|could you|please)\s+', '', clean, flags=re.IGNORECASE)
                    clean = clean.rstrip('?').rstrip('.') + '.'
                    clean = clean[0].upper() + clean[1:]
                    action_item = clean
                    found_action = True
                    break
            if found_action:
                break

        if not found_action and sentences:
            for sentence in sentences:
                if re.search(r'\b(review|check|send|update|verify|confirm|fix|test)\b', sentence, re.IGNORECASE):
                    action_item = sentence.rstrip('?').rstrip('.') + '.'
                    break

        # Ensure imperative verb prefix for ADHD clarity
        if not re.match(r'^(Review|Verify|Update|Confirm|Send|Check|Restart|Submit|Fix)\b', action_item):
            action_item = f"Review {action_item[0].lower() + action_item[1:]}"

        return {
            "vibe": vibe,
            "deadline": deadline,
            "action_item": action_item,
            "engine": "Focus Friend Zero-Cloud Heuristic Engine",
        }
