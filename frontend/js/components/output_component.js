/**
 * Focus Friend - Output Component
 * Renders the 3 Neo-Brutalist cards and manages copy/completion interactions.
 * Delegates clipboard operations and formatting to modular utilities.
 */

import { store } from '../state/store.js';
import { toast } from './toast_component.js';
import { audioService } from '../services/audio_service.js';
import { copyToClipboard } from '../utils/clipboard.js';
import { formatSignalSummary } from '../utils/formatters.js';

export class OutputComponent {
  constructor() {
    this.section = document.getElementById('output-section');
    this.meta = document.getElementById('output-meta');
    this.textVibe = document.getElementById('text-vibe');
    this.textDeadline = document.getElementById('text-deadline');
    this.textAction = document.getElementById('text-action');
    this.btnCopyAction = document.getElementById('btn-copy-action');
    this.btnCopyAll = document.getElementById('btn-copy-all');
    this.btnMarkDone = document.getElementById('btn-mark-done');
    this.btnReset = document.getElementById('btn-reset');

    this.bindEvents();
    store.subscribe((state, prev) => this.render(state, prev));
    this.render(store.getState());
  }

  bindEvents() {
    if (this.btnCopyAction) {
      this.btnCopyAction.addEventListener('click', () => this.copyAction());
    }

    if (this.btnCopyAll) {
      this.btnCopyAll.addEventListener('click', () => this.copyAll());
    }

    if (this.btnMarkDone) {
      this.btnMarkDone.addEventListener('click', () => {
        store.markTaskDone();
        this.btnMarkDone.textContent = '🎉 TASK OVERCOME!';
        this.btnMarkDone.style.background = 'var(--color-yellow)';
        toast.show('🏆 Paralysis averted! Great job overcoming the cognitive friction.', '🏆');
        setTimeout(() => {
          if (this.btnMarkDone) {
            this.btnMarkDone.textContent = '🎯 PARALYSIS AVERTED!';
            this.btnMarkDone.style.background = '';
          }
        }, 3500);
      });
    }

    if (this.btnReset) {
      this.btnReset.addEventListener('click', () => {
        audioService.play('click');
        store.clearInput();
        const ta = document.getElementById('text-input');
        if (ta) ta.focus();
      });
    }

    // Global copy shortcut: Ctrl+Shift+C (or Cmd+Shift+C)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'c' || e.key === 'C')) {
        if (store.getState().distilledData) {
          e.preventDefault();
          this.copyAction();
        }
      }
    });
  }

  async copyAction() {
    const data = store.getState().distilledData;
    if (!data || !data.action_item) return;

    const ok = await copyToClipboard(data.action_item);
    if (ok) {
      audioService.play('pop');
      toast.show('Action item copied to clipboard!', '📋');
    } else {
      toast.show('Unable to access clipboard.', '⚠️');
    }
  }

  async copyAll() {
    const data = store.getState().distilledData;
    if (!data) return;

    const summary = formatSignalSummary(data);
    const ok = await copyToClipboard(summary);
    if (ok) {
      audioService.play('pop');
      toast.show('Complete 3-card Focus Friend summary copied!', '📋');
    } else {
      toast.show('Unable to access clipboard.', '⚠️');
    }
  }

  render(state, prev) {
    if (!this.section) return;

    if (state.status === 'success' && state.distilledData) {
      const data = state.distilledData;
      if (this.textVibe) this.textVibe.textContent = `"${data.vibe}"`;
      if (this.textDeadline) this.textDeadline.textContent = data.deadline;
      if (this.textAction) this.textAction.textContent = data.action_item;

      const latency = data.latency_seconds || 0.1;
      if (this.meta) {
        this.meta.textContent = `Distilled in ${latency}s • Engine: ${data.engine} • 0 Cloud Data Leaks`;
      }
      this.section.style.display = 'flex';

      if (!prev || prev.status !== 'success') {
        this.section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    } else {
      this.section.style.display = 'none';
    }
  }
}
