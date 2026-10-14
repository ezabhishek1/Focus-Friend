/**
 * Focus Friend - Text Metrics Utility
 * Business logic for calculating word counts, character counts, and cognitive reading debt.
 */

/**
 * Average adult reading speed (words per minute).
 */
const AVERAGE_WPM = 200;

/**
 * Computes text metrics and estimated focus debt saved.
 * @param {string} text - Raw input message text.
 * @returns {{ words: number, chars: number, timeSavedMinutes: number }}
 */
export function calculateTextMetrics(text) {
  const clean = (text || '').trim();
  const words = clean ? clean.split(/\s+/).length : 0;
  const chars = (text || '').length;
  const rawMinutes = words / AVERAGE_WPM;
  const timeSavedMinutes = words > 15 ? Number(rawMinutes.toFixed(1)) : 0;

  return {
    words,
    chars,
    timeSavedMinutes,
  };
}
