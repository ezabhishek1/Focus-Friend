/**
 * Focus Friend - Input Component
 * Manages raw input buffer, live metrics, and extract triggers.
 */

import { store } from '../state/store.js';
import { toast } from './toast_component.js';
import { audioService } from '../services/audio_service.js';

export class InputComponent {
  constructor() {
    this.textarea = document.getElementById('text-input');
    this.btnExtract = document.getElementById('btn-extract');
    this.btnClear = document.getElementById('btn-clear');
    this.statWords = document.getElementById('stat-words');
    this.statChars = document.getElementById('stat-chars');
    this.statTimeSaved = document.getElementById('stat-time-saved');

    this.bindEvents();
    store.subscribe((state, prev) => this.render(state, prev));
    this.render(store.getState());
  }

  bindEvents() {
    if (this.textarea) {
      this.textarea.addEventListener('input', (e) => {
        store.setInputText(e.target.value);
      });
    }

    if (this.btnClear) {
      this.btnClear.addEventListener('click', () => {
        audioService.play('click');
        store.clearInput();
        if (this.textarea) this.textarea.focus();
      });
    }

    if (this.btnExtract) {
      this.btnExtract.addEventListener('click', () => {
        this.handleExtract();
      });
    }

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl + Enter or Cmd + Enter: Extract Signal
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        this.handleExtract();
      }

      // Escape: Clear input buffer
      if (e.key === 'Escape' && document.activeElement === this.textarea) {
        audioService.play('click');
        store.clearInput();
      }
    });
  }

  async handleExtract() {
    const rawText = store.getState().inputText.trim();
    if (!rawText) {
      toast.show('⚠️ Please paste a message or choose a preset first to extract signal!', '⚠️');
      if (this.textarea) this.textarea.focus();
      return;
    }

    if (rawText.length < 5) {
      toast.show('⚠️ Message must contain at least 5 characters.', '⚠️');
      if (this.textarea) this.textarea.focus();
      return;
    }

    try {
      await store.extractSignal();
    } catch (err) {
      toast.show(`❌ ${err.message}`, '❌');
      if (this.textarea) this.textarea.focus();
    }
  }

  render(state, prev) {
    // Keep textarea synchronized with store (e.g. when preset or clear is dispatched)
    if (this.textarea && state.inputText !== this.textarea.value) {
      this.textarea.value = state.inputText;
    }

    // Metrics & Statistics
    if (!prev || state.stats !== prev.stats) {
      if (this.statWords) this.statWords.textContent = `${state.stats.words} words`;
      if (this.statChars) this.statChars.textContent = `${state.stats.chars} chars`;

      if (this.statTimeSaved) {
        if (state.stats.timeSavedMinutes > 0) {
          this.statTimeSaved.textContent = `~${state.stats.timeSavedMinutes} min focus debt saved`;
          this.statTimeSaved.style.display = 'inline-block';
        } else {
          this.statTimeSaved.textContent = `0 min focus debt`;
        }
      }
    }

    // Button loading state
    if (!prev || state.status !== prev.status) {
      if (this.btnExtract) {
        this.btnExtract.disabled = state.status === 'loading';
      }
    }
  }
}
