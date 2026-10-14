/**
 * Focus Friend - Formatters Utility
 * Formats distilled signals into clear plain-text summaries for quick export into Slack, Notion, or Todoist.
 */

/**
 * Formats the 3-point distilled signal into an executive summary text.
 * @param {{ vibe: string, deadline: string, action_item: string, engine?: string }} signal
 * @returns {string} Formatted markdown/plain-text summary.
 */
export function formatSignalSummary(signal) {
  if (!signal) return '';

  return `⚡ FOCUS FRIEND SUMMARY
────────────────────────────────
01. THE VIBE:
${signal.vibe || 'Neutral professional tone.'}

02. THE DEADLINE:
${signal.deadline || 'No hard deadline specified.'}

03. THE ACTION ITEM:
➔ ${signal.action_item || 'Review message details.'}
────────────────────────────────
Distilled via Focus Friend (100% Local-First Executive Assistant)`;
}
