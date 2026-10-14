/**
 * Focus Friend - Header Component
 * Handles brand display, status indicators, theme, and sound controls.
 */

import { store } from '../state/store.js';

export class HeaderComponent {
  constructor() {
    this.statusDot = document.getElementById('status-dot');
    this.statusText = document.getElementById('status-text');
    this.statusPill = document.getElementById('ollama-status-pill');
    this.btnRefresh = document.getElementById('btn-refresh-status');
    this.btnSound = document.getElementById('btn-toggle-sound');
    this.soundIcon = document.getElementById('sound-icon');
    this.soundText = document.getElementById('sound-text');
    this.btnTheme = document.getElementById('btn-toggle-theme');
    this.themeIcon = document.getElementById('theme-icon');
    this.themeText = document.getElementById('theme-text');

    this.bindEvents();
    store.subscribe((state, prev) => this.render(state, prev));
    this.render(store.getState());
  }

  bindEvents() {
    if (this.btnRefresh) {
      this.btnRefresh.addEventListener('click', () => {
        if (this.statusDot) this.statusDot.className = 'status-dot pulse-dot';
        if (this.statusText) this.statusText.textContent = 'CHECKING...';
        store.checkSystemHealth();
      });
    }

    if (this.btnSound) {
      this.btnSound.addEventListener('click', () => {
        store.toggleSfx();
      });
    }

    if (this.btnTheme) {
      this.btnTheme.addEventListener('click', () => {
        store.toggleTheme();
      });
    }
  }

  render(state, prev) {
    // Theme Update
    if (!prev || state.theme !== prev.theme) {
      document.body.setAttribute('data-theme', state.theme);
      if (this.themeIcon) this.themeIcon.textContent = state.theme === 'dark' ? '☀️' : '🌙';
      if (this.themeText) this.themeText.textContent = state.theme === 'dark' ? 'LIGHT' : 'DARK';
    }

    // Sound Update
    if (!prev || state.sfxEnabled !== prev.sfxEnabled) {
      if (this.soundIcon) this.soundIcon.textContent = state.sfxEnabled ? '🔊' : '🔇';
      if (this.soundText) this.soundText.textContent = state.sfxEnabled ? 'SFX: ON' : 'SFX: OFF';
    }

    // Ollama Status Update
    if (!prev || state.ollamaStatus !== prev.ollamaStatus) {
      const { connected, activeModel } = state.ollamaStatus;
      if (!this.statusDot || !this.statusText || !this.statusPill) return;

      if (connected && activeModel) {
        this.statusDot.className = 'status-dot status-connected';
        this.statusText.textContent = `OLLAMA ACTIVE (${activeModel})`;
        this.statusPill.title = `Connected to local Ollama inference daemon. Active model: ${activeModel}`;
      } else if (connected) {
        this.statusDot.className = 'status-dot status-fallback';
        this.statusText.textContent = 'OLLAMA READY (FALLBACK ACTIVE)';
        this.statusPill.title = 'Ollama running, model pull pending. Using Zero-Cloud Heuristic Engine.';
      } else {
        this.statusDot.className = 'status-dot status-fallback';
        this.statusText.textContent = 'OFFLINE ENGINE ACTIVE';
        this.statusPill.title = 'Using embedded Zero-Cloud High-Precision Distillation Engine (100% offline & private).';
      }
    }
  }
}
