/**
 * Focus Friend - Centralized Reactive State Store
 * Implements an observable Pub/Sub pattern with dedicated Action Dispatchers and Selector-based subscriptions.
 */

import { CONFIG } from '../config.js';
import { ApiService } from '../services/api_service.js';
import { audioService } from '../services/audio_service.js';
import { calculateTextMetrics } from '../utils/text_metrics.js';

class Store {
  constructor() {
    const savedTheme = localStorage.getItem(CONFIG.STORAGE_KEYS.THEME) || 'light';
    const savedSfx = localStorage.getItem(CONFIG.STORAGE_KEYS.SFX) !== 'false';

    this.state = {
      inputText: '',
      status: 'idle', // 'idle' | 'loading' | 'success' | 'error'
      distilledData: null,
      theme: savedTheme,
      sfxEnabled: savedSfx,
      ollamaStatus: {
        connected: false,
        activeModel: null,
        models: [],
      },
      presets: CONFIG.DEFAULT_PRESETS,
      activePresetId: null,
      errorMessage: null,
      stats: {
        words: 0,
        chars: 0,
        timeSavedMinutes: 0,
      },
    };

    /** @type {Set<{ listener: Function, selector: Function|null }>} */
    this.subscribers = new Set();
  }

  /**
   * Returns a snapshot copy of current state.
   * @returns {typeof this.state}
   */
  getState() {
    return { ...this.state };
  }

  /**
   * Internal state mutator that persists user options and notifies subscribers.
   * @param {Partial<typeof this.state>} partialState
   */
  setState(partialState) {
    const prevState = { ...this.state };
    this.state = { ...this.state, ...partialState };

    // Persist user preferences
    if ('theme' in partialState) {
      try {
        localStorage.setItem(CONFIG.STORAGE_KEYS.THEME, this.state.theme);
      } catch (e) {
        console.debug('[Store] LocalStorage unavailable for theme persistence');
      }
    }
    if ('sfxEnabled' in partialState) {
      try {
        localStorage.setItem(CONFIG.STORAGE_KEYS.SFX, String(this.state.sfxEnabled));
      } catch (e) {
        console.debug('[Store] LocalStorage unavailable for SFX persistence');
      }
    }

    this.notify(prevState);
  }

  /**
   * Subscribe to state mutations.
   * Optionally provide a selector function to only be called when selected slice changes.
   * 
   * @param {Function} listener - Callback receiving (newState, prevState)
   * @param {Function} [selector=null] - (state) => selectedSlice
   * @returns {Function} Unsubscribe handle
   */
  subscribe(listener, selector = null) {
    const record = { listener, selector };
    this.subscribers.add(record);
    return () => this.subscribers.delete(record);
  }

  /**
   * Notify all registered subscribers safely.
   * @param {typeof this.state} prevState
   */
  notify(prevState) {
    for (const { listener, selector } of this.subscribers) {
      try {
        if (selector) {
          const currentSlice = selector(this.state);
          const prevSlice = selector(prevState);
          if (currentSlice !== prevSlice) {
            listener(this.state, prevState);
          }
        } else {
          listener(this.state, prevState);
        }
      } catch (err) {
        console.error('[Store] Subscriber callback exception:', err);
      }
    }
  }

  // =========================================================================
  // ACTION DISPATCHERS (Business & State Flow Management)
  // =========================================================================

  /**
   * Sets input buffer text and recalculates text metrics using text_metrics utility.
   * @param {string} text
   */
  setInputText(text) {
    const stats = calculateTextMetrics(text);
    this.setState({
      inputText: text,
      stats,
    });
  }

  /**
   * Clears the input buffer and resets extraction card view.
   */
  clearInput() {
    this.setInputText('');
    this.setState({
      status: 'idle',
      distilledData: null,
      errorMessage: null,
      activePresetId: null,
    });
  }

  /**
   * Loads an overwhelm scenario preset by ID.
   * @param {string} presetId
   * @returns {Object|null}
   */
  loadPreset(presetId) {
    const found = this.state.presets.find(p => p.id === presetId);
    if (!found) return null;

    audioService.play('click');
    this.setInputText(found.text);
    this.setState({
      activePresetId: presetId,
      status: 'idle',
      distilledData: null,
      errorMessage: null,
    });
    return found;
  }

  /**
   * Updates presets list (e.g. after fetching from backend).
   * @param {Array} presets
   */
  setPresets(presets) {
    if (Array.isArray(presets) && presets.length > 0) {
      this.setState({ presets });
    }
  }

  /**
   * Triggers Signal extraction orchestration.
   * @returns {Promise<Object>} Distilled signal result.
   */
  async extractSignal() {
    const rawText = this.state.inputText.trim();
    if (!rawText) {
      throw new Error("Please enter or paste a message first to extract signal.");
    }

    if (this.state.status === 'loading') return;

    audioService.play('click');
    this.setState({ status: 'loading', errorMessage: null });

    try {
      const result = await ApiService.extract(rawText);
      this.setState({
        status: 'success',
        distilledData: result,
        errorMessage: null,
      });
      audioService.play('success');
      return result;
    } catch (err) {
      audioService.play('error');
      this.setState({
        status: 'error',
        errorMessage: err.message || 'Distillation failed.',
      });
      throw err;
    }
  }

  /**
   * Toggles theme between 'light' and 'dark'.
   */
  toggleTheme() {
    audioService.play('click');
    const next = this.state.theme === 'dark' ? 'light' : 'dark';
    this.setState({ theme: next });
  }

  /**
   * Toggles sound synthesis on/off.
   */
  toggleSfx() {
    audioService.play('click');
    this.setState({ sfxEnabled: !this.state.sfxEnabled });
  }

  /**
   * Refreshes backend health and Ollama daemon connectivity.
   * @returns {Promise<Object>}
   */
  async checkSystemHealth() {
    const info = await ApiService.checkHealth();
    this.setState({
      ollamaStatus: {
        connected: Boolean(info.ollama_connected),
        activeModel: info.active_model || null,
        models: info.active_model ? [info.active_model] : [],
      },
    });
    return info;
  }

  /**
   * Celebrates completion of the extracted action item.
   */
  markTaskDone() {
    audioService.play('celebrate');
  }

  /**
   * Resets all transient state back to idle.
   */
  reset() {
    this.clearInput();
  }
}

export const store = new Store();
