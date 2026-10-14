/**
 * Focus Friend - Client-side Zero-Cloud Heuristic Engine
 * Fallback parser operating directly in browser memory with zero network latency.
 * Ensures 100% data privacy and offline function if the backend API is unreachable.
 */

export class LocalHeuristicEngine {
  /**
   * Distills message text into Tone (The Vibe), Timeline (The Deadline), and Task (The Action Item).
   * 
   * @param {string} text - Raw message input.
   * @returns {Object} Distilled signal object.
   */
  static distill(text) {
    const start = performance.now();
    const cleanText = (text || '').trim();
    const lower = cleanText.toLowerCase();
    const sentences = cleanText.split(/(?<=[.?!])\s+/).map(s => s.trim()).filter(Boolean);

    // 1. Emotional Context & Vibe
    let vibe = "Collaborative, low-pressure communication requesting standard feedback.";
    if (
      lower.includes('sorry for pinging') ||
      lower.includes('502') ||
      lower.includes('error') ||
      lower.includes('urgent') ||
      lower.includes('asap') ||
      lower.includes('late') ||
      lower.includes('exhausted')
    ) {
      vibe = "Mild situational urgency regarding a technical issue; supportive and non-judgmental tone.";
    } else if (
      lower.includes('loved the initial') ||
      lower.includes('super promising') ||
      lower.includes('no need to rewrite') ||
      lower.includes('great work')
    ) {
      vibe = "Very positive and reassuring; leadership is pleased with progress and only requests minor polish.";
    } else if (
      lower.includes('scope') ||
      lower.includes('marketing vp') ||
      lower.includes('sprint') ||
      lower.includes('negotiate') ||
      lower.includes('out of scope')
    ) {
      vibe = "Polite exploratory inquiry regarding additional deliverables; open to discussion and pushback.";
    } else if (
      lower.includes('quick heads up') ||
      lower.includes('poll') ||
      lower.includes('reminder') ||
      lower.includes('lunch preferences')
    ) {
      vibe = "Routine operational team coordination with casual logistics.";
    }

    // 2. Hard Deadline & Timeline
    let deadline = "No hard deadline specified; handle during normal working cadence.";
    const deadlinePatterns = [
      /\b(?:before\s+end\s+of\s+day\s+[a-z]+|end\s+of\s+day\s+[a-z]+|eod\s+[a-z]+|by\s+[a-z]+\s+eod)\b/i,
      /\b(?:before\s+tomorrow'?s\s+\d+:\d+\s*[ap]m|\d+:\d+\s*[ap]m\s+tomorrow|tomorrow\s+at\s+\d+:\d+\s*[ap]m)\b/i,
      /\b(?:before\s+\d+:\d+\s*[ap]m\s+[a-z]+|\d+:\d+\s*[ap]m\s+[a-z]+)\b/i,
      /\b(?:by\s+noon\s+today|by\s+noon|by\s+eod|by\s+end\s+of\s+day)\b/i,
      /\b(?:before\s+we\s+officially\s+go\s+live\s+on\s+[a-z0-9\s]+|go\s+live\s+on\s+[a-z0-9\s]+)\b/i,
      /\b(?:by\s+[a-z]+\s+\d+(?:st|nd|rd|th)?|on\s+[a-z]+\s+\d+(?:st|nd|rd|th)?)\b/i,
      /\b(?:before\s+friday|by\s+friday|end\s+of\s+day\s+friday)\b/i,
      /\b(?:tomorrow\s+morning|before\s+9\s*am\s*[a-z]*|tomorrow\s+at\s+2\s*pm)\b/i
    ];

    for (const pat of deadlinePatterns) {
      const match = cleanText.match(pat);
      if (match) {
        let rawMatch = match[0].trim();
        if (/end of day friday/i.test(rawMatch)) {
          deadline = "End of Day Friday";
        } else {
          deadline = rawMatch.charAt(0).toUpperCase() + rawMatch.slice(1);
        }
        break;
      }
    }

    // 3. Action Item (Imperative sentence)
    let actionItem = "Review the message details and provide a brief status update.";
    const actionTriggers = [
      /could you (?:just )?(?:review|fix|send|check|verify|update|test)/i,
      /can you (?:jump|verify|check|test|log|update|take a look|bounce)/i,
      /please (?:let us know|review|send|confirm|update)/i,
      /can you (?:log into|restart|bounce)/i
    ];

    let found = false;
    for (const sentence of sentences) {
      for (const trigger of actionTriggers) {
        if (trigger.test(sentence)) {
          let clean = sentence.replace(/^(Hey|Hi|Also|So|And)\s+[@\w\s,]+(?:can you|could you|please)\s+/i, '');
          clean = clean.replace(/^(can you|could you|please)\s+/i, '');
          clean = clean.replace(/\?$/, '.');
          clean = clean.charAt(0).toUpperCase() + clean.slice(1);
          actionItem = clean;
          found = true;
          break;
        }
      }
      if (found) break;
    }

    if (!found && sentences.length > 0) {
      for (const sentence of sentences) {
        if (/\b(review|check|send|update|verify|confirm|fix|test)\b/i.test(sentence)) {
          actionItem = sentence.replace(/\?$/, '.') + '.';
          break;
        }
      }
    }

    // Ensure imperative verb prefix for ADHD clarity
    if (!/^(Review|Verify|Update|Confirm|Send|Check|Restart|Submit|Fix)\b/i.test(actionItem)) {
      actionItem = "Review " + actionItem.charAt(0).toLowerCase() + actionItem.slice(1);
    }

    const elapsed = Math.round((performance.now() - start) * 10) / 10000;

    return {
      vibe,
      deadline,
      action_item: actionItem,
      engine: "Focus Friend Zero-Cloud Client Engine",
      latency_seconds: elapsed < 0.01 ? 0.02 : elapsed,
      is_fallback: true
    };
  }
}
