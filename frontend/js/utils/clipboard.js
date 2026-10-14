/**
 * Focus Friend - Clipboard Utility
 * Modular clipboard helper supporting modern Navigator API with seamless fallback for non-secure contexts.
 */

/**
 * Copies plain text to the user's system clipboard.
 * @param {string} text - The string content to copy.
 * @returns {Promise<boolean>} True if copy succeeded, false otherwise.
 */
export async function copyToClipboard(text) {
  if (!text) return false;

  // 1. Try modern Navigator Clipboard API
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.warn('[Clipboard] Modern API write failed, attempting fallback:', err);
    }
  }

  // 2. Legacy fallback for non-secure context or older webviews
  try {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '-9999px';
    textarea.setAttribute('readonly', '');
    document.body.appendChild(textarea);
    textarea.select();
    const successful = document.execCommand('copy');
    document.body.removeChild(textarea);
    return successful;
  } catch (fallbackErr) {
    console.error('[Clipboard] Fallback execCommand copy failed:', fallbackErr);
    return false;
  }
}
