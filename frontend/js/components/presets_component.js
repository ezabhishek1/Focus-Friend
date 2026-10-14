/**
 * Focus Friend - Presets Component
 * Renders ADHD overwhelm scenario triggers and dispatches preset load actions.
 */

import { store } from '../state/store.js';
import { toast } from './toast_component.js';

export class PresetsComponent {
  constructor() {
    this.container = document.querySelector('.presets-buttons');
    if (!this.container) return;

    this.bindEvents();
    store.subscribe((state, prev) => this.render(state, prev));
    this.render(store.getState());
  }

  bindEvents() {
    this.container.addEventListener('click', (e) => {
      const btn = e.target.closest('.preset-btn');
      if (!btn) return;

      const presetId = btn.dataset.presetId;
      if (presetId) {
        const loaded = store.loadPreset(presetId);
        if (loaded) {
          toast.show(`Loaded: ${loaded.title}`, loaded.emoji || "⚡");
        }
      }
    });
  }

  render(state, prev) {
    if (!this.container) return;

    // Re-render buttons if presets array changed or on initial load
    const presetsChanged = !prev || state.presets !== prev.presets || this.container.children.length === 0;
    const activeChanged = !prev || state.activePresetId !== prev.activePresetId;

    if (presetsChanged) {
      this.container.innerHTML = state.presets.map(p => {
        const isActive = state.activePresetId === p.id;
        return `
          <button
            type="button"
            class="preset-btn ${isActive ? 'active' : ''}"
            data-preset-id="${p.id}"
            title="${p.title}"
            aria-pressed="${isActive}"
          >
            <span class="preset-emoji">${p.emoji || '⚡'}</span> ${p.title}
          </button>
        `;
      }).join('');
    } else if (activeChanged) {
      this.container.querySelectorAll('.preset-btn').forEach(btn => {
        const isActive = btn.dataset.presetId === state.activePresetId;
        if (isActive) {
          btn.classList.add('active');
          btn.setAttribute('aria-pressed', 'true');
        } else {
          btn.classList.remove('active');
          btn.setAttribute('aria-pressed', 'false');
        }
      });
    }
  }
}
