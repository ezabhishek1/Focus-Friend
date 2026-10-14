/**
 * Focus Friend - Toast Notification Component
 * Reusable notification display for clipboard confirmation, feedback, and error alerts.
 */

export class ToastComponent {
  constructor() {
    this.toastEl = document.getElementById('toast');
    this.toastMsgEl = document.getElementById('toast-message');
    this.toastIconEl = document.querySelector('.toast-icon');
    this.timer = null;
  }

  /**
   * Displays a toast notification message.
   * @param {string} message - User-facing text to display.
   * @param {string} [icon="📋"] - Emoji or icon symbol.
   * @param {number} [durationMs=2800] - Visibility window in milliseconds.
   */
  show(message, icon = "📋", durationMs = 2800) {
    if (!this.toastEl || !this.toastMsgEl) return;

    this.toastMsgEl.textContent = message;
    if (this.toastIconEl && icon) {
      this.toastIconEl.textContent = icon;
    }

    this.toastEl.classList.add('show');
    clearTimeout(this.timer);
    this.timer = setTimeout(() => {
      if (this.toastEl) {
        this.toastEl.classList.remove('show');
      }
    }, durationMs);
  }
}

export const toast = new ToastComponent();
